import json
import logging
import msvcrt
import os.path
import platform
import socket
import sys
import threading
import time
from typing import Set

import pymysql, pymysql.cursors

config = {}
db_config = {}
db_key = "spearlinedb_devel"


def setup_logging(log_file: str, log_level:str):
    import logging.handlers

    logger = logging.getLogger()
    log_type = None
    if log_level.lower() == "debug":
        log_type = logging.DEBUG
    elif log_level.lower() == "info":
        log_type = logging.INFO
    elif log_level.lower() == "warning":
        log_type = logging.WARNING
    elif log_level.lower() == "error":
        log_type = logging.ERROR
    else:
        log_type = logging.INFO

    # set logging level for the root logger
    logger.setLevel(log_type)

    # file handler
    file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=52428800, backupCount=30)
    file_handler.setLevel(log_type)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_type)

    formatter = logging.Formatter('%(asctime)s: %(module)s :%(levelname)s: %(threadName)s :%(lineno)d:\t%(message)s')

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def ensure_single_instance(lock_name: str):
    """
    Ensures that only one instance of the script can run at a time.
    Handles both Windows and Linux platforms.
    """
    os_name = platform.system()
    if os_name == "Windows":
        # Use msvcrt to lock a file for Windows
        lock_file = f"{lock_name}.lock"
        try:
            lock = open(lock_file, "w")
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            logging.debug("No other instance is running. Lock acquired.")
            return lock
        except OSError:
            logging.error("Another instance is already running. Exiting.")
            sys.exit(1)
    elif os_name == "Linux":
        # Use an abstract socket for Linux
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.bind('\0' + lock_name)
            logging.debug("No other instance is running. Lock acquired.")
            return s
        except socket.error as e:
            logging.error("Another instance is already running. Exiting.")
            sys.exit(1)
    else:
        logging.error(f"Unsupported operating system: {os_name}. Exiting.")
        sys.exit(1)


def get_configuration() -> dict:
    """
    Reads the configuration from a JSON file.
    :return: dict
    """
    config_file_name = 'config.json'
    if os.path.isfile(config_file_name):
        with open(config_file_name, 'r') as config_file:
            try:
                file_config = json.load(config_file)
                return file_config
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON from {config_file_name}: {e}")
                sys.exit(1)
    else:
        logging.error(f"Configuration file {config_file_name} not found.")
        sys.exit(1)


def get_db_configuration() -> dict:
    """
    Reads DB Configuration
    :return: dict
    """
    db_config_file_name = config["db_config_file_path"]
    logging.debug(f"DB Configuration file path : {db_config_file_name}")
    if os.path.isfile(db_config_file_name):
        with open(db_config_file_name, 'r') as db_config_file:
            try:
                file_config = json.load(db_config_file)
                logging.debug("DB Configuration file loaded successfully")
                logging.debug(json.dumps(file_config, indent=4, sort_keys=True, default=str))
                return file_config
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON from {db_config_file_name}: {e}")
                sys.exit(1)
    else:
        logging.error(f"Database Configuration file {db_config_file_name} not found.")
        sys.exit(1)


def sql_query (query: str, return_dict: bool = False, is_select: bool = True,fetch_all: bool = True) -> Set | None:
    '''Common function to execute sql query'''
    affected_rows = 0
    result = None
    try:
        db = pymysql.connect(**db_config[db_key],connect_timeout=120,autocommit = True)

        with db:
            cur = db.cursor(pymysql.cursors.DictCursor) if return_dict else db.cursor()
            with cur:
                affected_rows = cur.execute(query)
                if is_select and affected_rows > 0:
                    result = cur.fetchall() if fetch_all else cur.fetchone()
    except pymysql.OperationalError as e:
        logging.error(f"We got error in sql_query {e} query: {query}")
    except pymysql.Error as e:
        logging.error(f"We got error in sql_query: {e.args} query: {query}")

    return result if is_select else affected_rows


class GetJobs(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.lock = threading.Lock()
        self.CALL_SCRIPT_SERVER = config["CALL_SCRIPT_SERVER"]
        self.CONF_RECORD = {}
        self.SECRET_KEY = "8e74Ebn8572Rtjdyr8aVX3816bBt204"
        self.REFRESH_INTERVAL = config.get('refresh_interval', 15)
        self.kill_received = False

    def run(self):
        while self.kill_received is False:
            logging.info("Checking for jobs to process")
            # Keep on checking Jobs
            logging.debug("-" * 20 + " Getting Jobs " + "-" * 20)
            logging.debug("-" * 50)
            sql = """
                SELECT jp.id AS jpID,jp.test_type_id,jp.route_id,jp.test_counter,
                jp.provider_did_id,jp.ddi_cli,jp.min_expected_call_length,
                n.number,n.company_id,n.country_code_id,n.number_type_id,
                s.id AS sID,s.ip,
                it.ivr_traversal,
                pr.did,pr.provider_id AS dpID,
                b.bridge,b.id AS bID,
                obdg.url,obdg.username,obdg.password,
                bp.conference_id,bp.passcode,
                c.country_prefix,c.country_name,
                did_s.ip as did_server
                FROM  job_processing_outbound_conf_long jp
                LEFT JOIN number n ON jp.number_id=n.id
                LEFT JOIN server s ON jp.server_id=s.id
                LEFT JOIN ivr_traversal it ON jp.ivr_traversal_id=it.id
                LEFT JOIN provider_did pr ON jp.provider_did_id=pr.id
                LEFT JOIN  provider p on pr.provider_id = p.id
                LEFT JOIN server did_s on p.server_id = did_s.id
                LEFT JOIN outbound_bridge_ddi obd ON jp.outbound_bridge_ddi_id=obd.id
                LEFT JOIN bridge b ON obd.bridge_id=b.id
                LEFT JOIN outbound_bridge_ddi_gartner obdg ON jp.outbound_bridge_ddi_id=obdg.outbound_bridge_ddi_id
                LEFT JOIN bridge_passcode bp ON b.id=bp.bridge_id
                LEFT JOIN country_code c ON pr.country_code_id=c.id
                WHERE
                jp.call_start_time='0000-00-00 00:00:00'
                AND jp.ddi_call_start_time='0000-00-00 00:00:00'
                AND jp.processing_complete=0
                AND jp.test_type_id IN (81)
                AND n.company_id IN (93)
                AND s.call_script_on IN ({0})
                AND obdg.url like "https://app.zoom.us/wc/%"
                AND NOW() >= jp.created_on
                ORDER BY s.id desc,jp.id
                """.format(self.CALL_SCRIPT_SERVER)
            logging.debug("Job Processing Query : \n\t[ {0} ]\n\t".format(sql))
            logging.debug("Conference Dictionary = \n\t[ {0} ]\n\t ".format(self.CONF_RECORD))

            db_data = sql_query(sql, return_dict=True)
            if db_data is None:
                logging.info(f"No job processing data found going to sleep - {self.REFRESH_INTERVAL} seconds")
                time.sleep(self.REFRESH_INTERVAL)
                continue
            else:
                logging.info(f"Job Processing data found - {len(db_data)} records")
                for row in db_data:
                    logging.info("-" * 50)
                    logging.info(row)
                    logging.info("-"*50)
                    # # Check if the job is already processed
                    # if row["jpID"] in self.CONF_RECORD:
                    #     logging.debug(f"Job ID {row['jpID']} already processed. Skipping.")
                    #     continue
                    # # Process the job
                    # logging.debug(f"Processing Job ID {row['jpID']}")
                    # self.process_job(row)
                    # # Add the job to the processed list
                    # self.CONF_RECORD[row["jpID"]] = row
            logging.info(f"Going to sleep for {self.REFRESH_INTERVAL} seconds")
            time.sleep(self.REFRESH_INTERVAL)


if __name__ == "__main__":
    # Set up the configuration
    config = get_configuration()
    # set up logging
    setup_logging(config["log_file_path"], 'info')
    logging.debug("Setup for Logging information is completed")
    logging.debug("Configuration file loaded successfully")
    logging.debug(json.dumps(config, indent=4, sort_keys=True, default=str))
    # set lock to make sure only 1 instance of the script is running
    lock = ensure_single_instance("zoom_long_call")
    # get db configuration
    db_config = get_db_configuration()
    try:
        logging.info("Starting the script")
        # Start the job processing thread
        job_processor = GetJobs()
        job_processor.start()
        time.sleep(120)
        job_processor.kill_received = True
        logging.info("Max time reached, stopping the script.")


    finally:
        lock.close()
        logging.info("Lock released. Exiting script.")
