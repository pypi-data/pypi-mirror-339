import argparse
import json
import logging
import os
import threading
import time
from datetime import datetime, timedelta

import websocket

from prophecy_lineage_extractor import messages
from prophecy_lineage_extractor.constants import (
    SEND_EMAIL, PROPHECY_PAT, LONG_SLEEP_TIME,
    BRANCH, OUTPUT_DIR, RECURSIVE_EXTRACT, RUN_FOR_ALL_PIPELINES,
)
from prophecy_lineage_extractor.graphql import checkout_branch
from prophecy_lineage_extractor.utils import (
    delete_file, safe_env_variable, send_excel_email, get_ws_url,
    get_output_path, convert_csv_to_excel, get_monitor_time, KEEP_RUNNING, get_prophecy_name,
    get_temp_csv_path
)
from prophecy_lineage_extractor.ws_handler import WorkflowMessageHandler

class PipelineProcessor:
    def __init__(self, project_id, branch, output_dir, send_email, recursive_extract, pipeline_id_str=None):
        self.project_id = project_id
        self.pipeline_id_list = pipeline_id_str.split(",")
        self.branch = branch
        if output_dir is not None:
            self.output_dir = output_dir
            os.environ[OUTPUT_DIR] = output_dir
        self.send_email = send_email
        self.recursive_extract = recursive_extract
        self.last_meaningful_message_time = datetime.now()
        self.workflow_msg_handler = None
        self.ws = None

    def update_monitoring_time(self):
        self.last_meaningful_message_time = datetime.now()
        logging.warning(
            f"[MONITORING]: Updating idle time, current idle time"
            f"= {datetime.now() - self.last_meaningful_message_time}"
        )

    def on_error(self, ws, error):
        logging.error("Error: " + str(error))
        ws.close()
        exit(1)

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("### WebSocket closed ###")

    def on_message(self, ws, message):
        logging.info(f"\n\n### RECEIVED a message### ")
        try:
            json_msg = json.loads(message)
            if "method" in json_msg:
                method = json_msg["method"]
                logging.warning(f"method: {method}")
                if method == "properties/didOpen":
                    self.update_monitoring_time()
                    self.workflow_msg_handler.handle_did_open(ws, json_msg)
                elif method == "properties/didUpdate":
                    self.update_monitoring_time()
                    self.workflow_msg_handler.handle_did_update(ws, json_msg)
                elif method == "error":
                    logging.error(f"Error occurred:\n {json_msg['params']['msg']}")
                    raise Exception(f"Error occurred and we got method='Error'\n {json_msg}")
            else:
                raise Exception("method is not found in message", json_msg)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON message: {e}")
            raise e

    def on_open(self, ws):
        delete_file(get_temp_csv_path(), recursive=True)
        logging.info(f"\n\n### SENDING INIT PIPELINE for {self.project_id} ### ")
        ws.send(messages.init_pipeline(self.project_id, self.pipeline_id_list[0]))
        time.sleep(LONG_SLEEP_TIME)
        self.workflow_msg_handler = WorkflowMessageHandler(self.project_id, self.pipeline_id_list)

    def end_ws(self):
        logging.info(f"Started Generating excel report")
        output_excel_file = convert_csv_to_excel(project_id=self.project_id,
                             pipeline_dataset_map = self.workflow_msg_handler.pipeline_dataset_map)
        logging.info(f"Finishing Generating excel report {output_excel_file}")
        try:
            if self.send_email:
                logging.info("sending mail as --send-email passed")
                send_excel_email(self.project_id, output_excel_file)
            else:
                logging.info("Not sending mail not --send-email was not passed")
        except Exception as e:
            logging.error(e)
            raise e
        finally:
            self.ws.close()

    def monitor_ws(self):
        logging.info("Monitor thread started.")
        time.sleep(10)
        monitor_time = get_monitor_time()
        logging.info(f"[MONITORING] Monitor Time: {monitor_time} seconds")
        while self.ws.keep_running:
            global KEEP_RUNNING
            if set(self.workflow_msg_handler.datasets_processed) == set(self.workflow_msg_handler.datasets_to_process):
                KEEP_RUNNING = False
            if datetime.now() - self.last_meaningful_message_time > timedelta(seconds=monitor_time):
                logging.warning(f"[MONITORING]: No meaningful messages received in the last {monitor_time} seconds, closing websocket")
                self.end_ws()
            else:
                logging.warning(
                    f"[MONITORING]: KEEP_RUNNING={KEEP_RUNNING}, Idle time"
                    f"""{datetime.now() - self.last_meaningful_message_time} seconds / {get_monitor_time()} seconds;\n
                         datasets_processed = {len(self.workflow_msg_handler.datasets_processed)} OUT OF {self.workflow_msg_handler.total_index}
                    """,
                )
                if not KEEP_RUNNING:
                    logging.warning("COMPLETED REQUIRED TASK: Please end")
                    self.end_ws()
            time.sleep(10)
        logging.info("Monitor thread ended.")

    def run_websocket(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            get_ws_url(),
            header={"X-Auth-Token": safe_env_variable(PROPHECY_PAT)},
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        monitor_thread = threading.Thread(target=self.monitor_ws, daemon=True)
        monitor_thread.start()

        self.ws.run_forever()

    def process(self):
        checkout_branch(self.project_id, self.branch)
        logging.info("Starting WebSocket thread..")
        ws_thread = threading.Thread(target=self.run_websocket, daemon=True)
        ws_thread.start()
        ws_thread.join()

def main():
    parser = argparse.ArgumentParser(description="Prophecy Lineage Extractor")
    parser.add_argument("--project-id", type=str, required=True, help="Prophecy Project ID")
    parser.add_argument("--pipeline-id", type=str, required=True, nargs='+', help="Prophecy Pipeline ID(s)")
    parser.add_argument("--send-email", action="store_true", help="Enable verbose output")
    parser.add_argument("--branch", type=str, default="default", help="Branch to run lineage extractor on")
    parser.add_argument("--recursive_extract", type=str, default="true", help="Whether to Recursively include Upstream Source Transformations")
    parser.add_argument("--run_for_all", type=str, default="false", help="Whether to Create Project Level Sheet")
    parser.add_argument("--output-dir", type=str, required=True, help="Output directory inside the project")

    args = parser.parse_args()
    # Access arguments
    # os.environ[PROJECT_ID] = args.project_id
    os.environ[SEND_EMAIL] = str(args.send_email)
    os.environ[BRANCH] = args.branch
    os.environ[OUTPUT_DIR] = args.output_dir
    os.environ[RECURSIVE_EXTRACT] = args.recursive_extract
    os.environ[RUN_FOR_ALL_PIPELINES] = args.run_for_all

    args = parser.parse_args()

    for pipeline_id_str in args.pipeline_id:
        # for pipeline_id in pipeline_id_str.split(","):
        pipeline_output_dir = os.path.join(args.output_dir)
        os.makedirs(pipeline_output_dir, exist_ok=True)
        print(f"pipeline_id={pipeline_id_str}")
        processor = PipelineProcessor(
            project_id=args.project_id,
            pipeline_id_str=pipeline_id_str,
            branch=args.branch,
            output_dir=pipeline_output_dir,
            send_email=args.send_email,
            recursive_extract=args.recursive_extract
        )
        processor.process()

if __name__ == "__main__":
    main()
