import sys
import time
import json
import hashlib
import socket
import threading
import logging
import logging.handlers
from helperModuleNew import *
from selenium_testbase import SeleniumTestBase
from zoom_bridge import ZoomOutbound

formatter = logging.Formatter('%(asctime)s %(levelname)s:%(thread)d:%(threadName)s:%(lineno)d:\t%(message)s')
handler = logging.handlers.TimedRotatingFileHandler('/var/log/spearline/zoom_workspace_meet.log', when="H",
                                                    interval=1, backupCount=30)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.info("#"*50)
logging.info("-"*20 + " ZOOM CALL SCRIPT " + "-"*20)
logging.info("#"*50)

try:
    # Import socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Create an abstract socket, by prefixing it with null.
    s.bind('\0conf_zoom_workspace_meet_lock')
except socket.error as e:
    logging.warning("Process already running (%d:%s). Exiting" % (e.args[0], e.args[1]))
    sys.exit(0)

try:
    file_name = '/home/scripts/NewOutboundCallGenScripts/config.json'
    with open(file_name, 'r') as configFile:
        file_data = configFile.read()
        config = json.loads(file_data)

    file_name = '/etc/spearline/db.json'
    with open(file_name, 'r') as configFile:
        file_data = configFile.read()
        db_config = json.loads(file_data)
except Exception as e:
    logging.error(f"Error in {file_name}:{e}")
    sys.exit(0)

CALL_SCRIPT_SERVER = config["CALL_SCRIPT_SERVER"]
SECRET_KEY = "8e74Ebn8572Rtjdyr8aVX3816bBt204"
REFRESH_INTERVAL = config.get('refresh_interval', 15)
CONF_RECORD = {}


def release_bridge(lock, bridgeKey):
    try:
        lock.acquire()
        if CONF_RECORD:
            if bridgeKey in CONF_RECORD:
                logging.info(f"Removing key {bridgeKey}")
                if 'duId' in CONF_RECORD[bridgeKey] and CONF_RECORD[bridgeKey]["duId"] != None:
                    checkInPort(CONF_RECORD[bridgeKey]["duId"], CONF_RECORD[bridgeKey]["dpID"])
                del CONF_RECORD[bridgeKey]
    except Exception as e:
        logging.exception("Exception in releaseBridge - {0}".format(e))
    finally:
        lock.release()


class GetJobs(threading.Thread):
    def __init__(self):
        super().__init__()
        self.allowed_keys = 8
        self.ami = AMIAction()
        self.last_server = None
        self.last_connection = True
        self.last_server_time = None
        self.lock = threading.Lock()

    def run(self):
        logging.info("-"*20 + " Getting Jobs " + "-"*20)
        logging.info("-"*50)
        sql = """
                SELECT jp.id AS jpID,jp.test_type_id,jp.route_id,jp.test_counter,
                jp.provider_did_id,jp.ddi_cli,
                n.number,n.company_id,n.country_code_id,n.number_type_id,
                s.id AS sID,s.ip,
                it.ivr_traversal,
                pr.did,pr.provider_id AS dpID,
                b.bridge,b.id AS bID,
                obdg.url,obdg.username,obdg.password,
                bp.conference_id,bp.passcode,
                c.country_prefix,c.country_name
                FROM  job_processing_outbound_conf jp
                LEFT JOIN number n ON jp.number_id=n.id
                LEFT JOIN server s ON jp.server_id=s.id
                LEFT JOIN ivr_traversal it ON jp.ivr_traversal_id=it.id
                LEFT JOIN provider_did pr ON jp.provider_did_id=pr.id
                LEFT JOIN outbound_bridge_ddi obd ON jp.outbound_bridge_ddi_id=obd.id
                LEFT JOIN bridge b ON obd.bridge_id=b.id
                LEFT JOIN outbound_bridge_ddi_gartner obdg ON jp.outbound_bridge_ddi_id=obdg.outbound_bridge_ddi_id
                LEFT JOIN bridge_passcode bp ON b.id=bp.bridge_id
                LEFT JOIN country_code c ON pr.country_code_id=c.id
                WHERE
                jp.call_start_time='0000-00-00 00:00:00'
                AND jp.ddi_call_start_time='0000-00-00 00:00:00'
                AND jp.processing_complete=0
                AND jp.test_type_id IN (66)
                AND n.company_id IN (93)
                AND s.call_script_on IN ({0})
                AND obdg.url like "https://app.zoom.us/wc/%"
                AND NOW() >= jp.created_on
                ORDER BY s.id desc,jp.id
                """.format(CALL_SCRIPT_SERVER)
        logging.info("Job Processing Query : \n\t[ {0} ]\n\t".format(sql))
        logging.info("Conference Dictionary = \n\t[ {0} ]\n\t ".format(CONF_RECORD))
        while True:

            db_data = sql_query(sql, return_dict=True)
            if db_data is None:
                logging.info(f"No job processing data found going to sleep - {REFRESH_INTERVAL} seconds")
                time.sleep(REFRESH_INTERVAL)
                continue
            try:
                for test in db_data:
                    logging.info(f"Job processing data :  \n\t##{test}##\n\t")
                    server = test['ip']
                    bridge_key = "{0}-{1}".format(test['conference_id'], test['passcode'])
                    # process already existing keys
                    if bridge_key in CONF_RECORD:
                        logging.info(("Bridge [{0}] Conference [{1}] passcode [{2}]"
                                      " allready in progress since [{3}].").format(
                            test['bridge'], test['conference_id'], test['passcode'],
                            time_since(CONF_RECORD[bridge_key]["conf_initiated"])))
                        # remove keys older than 180 seconds.
                        if time_since(CONF_RECORD[bridge_key]["conf_initiated"]) > 180:
                            del CONF_RECORD[bridge_key]
                        continue

                    if len(CONF_RECORD) >= self.allowed_keys:
                        logging.info(f'Call count:{len(CONF_RECORD)} exceeds {self.allowed_keys}')
                        continue

                    # if key does not exist in CONF_RECORD
                    logging.info("New Call Will be Generated - Adding Bridge Key to Dictionary")
                    CONF_RECORD[bridge_key] = test
                    CONF_RECORD[bridge_key]['conf_initiated'] = time.time()
                    logging.info("Updated Conference Dictionary = \n\t[ {0} ]\n\t ".format(CONF_RECORD))

                    # if last server time is more than 5 minutes set last server to None
                    if self.last_server_time is not None and int(time.time() - self.last_server_time) > 300:
                        self.last_server, self.last_server_time = None, None

                    if server != self.last_server:
                        # if last server is not same as current server value, close socket to last_server.
                        if self.last_server is not None and self.last_connection == True:
                            if self.ami.logout() == False:
                                logging.error(
                                    f"\t\tAMI LOGOUT ISSUE :Server {self.last_server}.Continuing with next Server")
                                release_bridge(self.lock, bridge_key)
                                continue
                        logging.info(f"Going to\t\t Connect on Server {server}")
                        if self.ami.login(server):
                            serverMD5 = hashlib.md5("{0}{1}".format(server, SECRET_KEY).encode()).hexdigest()
                            self.last_connection = True
                        else:
                            release_bridge(self.lock, bridge_key)
                            self.last_connection = False
                    # if connected to last server
                    if self.last_connection == True:

                        routeDetails = get_route(test['company_id'], test['test_type_id'], test['route_id'],
                                                 test['country_code_id'], test['number_type_id'], test['sID'])
                        if routeDetails is None:
                            logging.error(
                                "\t\tNo recording route details available for Job Processing ID {} We release conference for other server to use".format(
                                    test['jpID']))
                            self.last_server, self.last_server_time = server, time.time()
                            release_bridge(self.lock, bridge_key)
                            continue
                        self.last_server, self.last_server_time = server, None
                        routeId, route, providerId, cli, stripDigits = routeDetails
                        logging.info(
                            "route={0}\tproviderId={1}\tcli={2}\tstripDigits={3}".format(route, providerId, cli,
                                                                                             stripDigits))
                        checkOutDetails = checkOutPort(test['company_id'], test['test_type_id'], providerId)
                        if (checkOutDetails[0] == 'na'):
                            logging.error("\t\tNo Port from Checkout System. Reason:{}".format(checkOutDetails[1]))
                            self.last_server, self.last_server_time = server, time.time()
                            release_bridge(self.lock, bridge_key)
                            continue
                        didCheckOutDetails = checkOutPort(test['company_id'], test['test_type_id'], test['dpID'])
                        if (didCheckOutDetails[0] == 'na'):
                            logging.error("\t\tNo Port from Checkout System. Reason:{}".format(didCheckOutDetails[1]))
                            self.last_server, self.last_server_time = server, time.time()
                            checkInPort(checkOutDetails[0], providerId)
                            release_bridge(self.lock, bridge_key)
                            continue
                        CONF_RECORD[bridge_key]["duId"] = didCheckOutDetails[0]
                        dialString = "{0}{1}".format(route, test['number'][stripDigits:])
                        if cli is None:
                            cli = 'Spearline'
                        amiString = "Action: Originate\r\nChannel: local/s@testType17Proxy\r\nContext: testType17\r\nExten: s\r\nPriority: 1\r\nAsync: yes\r\nTimeout: 100000\r\nVariable: _jpId={0}\r\nVariable: _testTypeId={1}\r\nVariable: _routeId={2}\r\nVariable: _serverMD5={3}\r\nVariable: ivrTraversal={4}\r\nVariable: _testCounter={5}\r\nVariable: _dialString={6}\r\nVariable: _providerId={7}\r\nVariable: _cli={8}\r\nVariable: _uId={9}\r\nVariable: _mPasscode={10}\r\nVariable: _pPasscode={11}\r\nVariable: _duId={12}\r\n\r\n".format(
                            test['jpID'], test['test_type_id'], test['route_id'], serverMD5,
                            test['ivr_traversal'].replace(',', '\,'), test['test_counter'], dialString, providerId, cli,
                            checkOutDetails[0], test['conference_id'], test['passcode'], didCheckOutDetails[0])
                        logging.info(
                            "\t\tAMI String:\n {0} ".format(amiString))
                        if self.ami.get_response(amiString) is not None:
                            self.last_connection = True
                            logging.info("callID : [{0}_{1}_{2}] Recording Leg Initiated".format(test['jpID'],
                                                                                                 test['test_counter'],
                                                                                                 test['test_type_id']))
                            timestamp = int(time.time())
                            test.update({'timestamp': timestamp, 'bridge_key': bridge_key})
                            time.sleep(1)
                            thread = OutboundProcessThread(kwargs=test)
                            thread.setName(
                                "{0}_{1}_{2}".format(test['jpID'], test['test_counter'], test['test_type_id']))
                            thread.start()
                            threads.append(thread)
                        else:
                            self.last_connection = False
                            checkInPort(checkOutDetails[0], providerId)
                            release_bridge(self.lock, bridge_key)
                    else:
                        logging.error("\t\tServer {}. Connection issue so continue with next record".format(server))
                        release_bridge(self.lock, bridge_key)
                        self.last_server = server
                        if self.last_server_time is None:
                            self.last_server_time = time.time()

                    if self.last_server is not None and self.last_connection is True:
                        logging.info("\tClosing last connection to a Server {0}".format(server))
                        self.last_server, self.last_server_time = None, None
                        self.ami.logout()

            except Exception as e:
                logging.exception(f"Got Error in getJobs: {e}")
            time.sleep(REFRESH_INTERVAL)


class ScreenShotThread(threading.Thread):
    def __init__(self, callId, browserObj, bridgeKey):
        super().__init__()
        self.call_id = callId
        self.key = bridgeKey
        self.browser = browserObj
        self.start_time = int(time.time())
        self.start_num = 1

    def run(self):
        logging.info(f"Screenshot thread started for {self.call_id}")
        try:
            # Take screenshot every second till key is in CONF_RECORD
            while self.key in CONF_RECORD:
                self.browser.save_screenshot(f"/home/screenshot/{self.call_id}-{str(self.start_num).zfill(3)}.png")
                time.sleep(1)
                self.start_num += 1
            generateVideo(self.call_id)
        except WebDriverException as WDE:
            logging.exception(f"Issue with web broswer:{WDE} ")
            generateVideo(self.call_id)
        except MaxRetryError as MCE:
            logging.exception(f"WEB BROWSER COULDNOT BE CONNECTED :{MCE}")
            generateVideo(self.call_id)
        except Exception as e:
            logging.exception(f"Error Occured in screenshot: {e}")
            generateVideo(self.call_id)


class OutboundProcessThread(threading.Thread):
    def __init__(self, **conditions):
        super().__init__()
        self.zoomOutbound = None
        self.data = conditions['kwargs']
        self.jpId = self.data['jpID']
        self.testTypeId = self.data['test_type_id']
        self.testCounter = self.data['test_counter']
        self.countryPrefix = self.data['country_prefix']
        self.countryName = self.data['country_name']
        self.ddiNumber = self.data['did']
        self.bridgeName = self.data['bridge']
        self.bridgeUrl = self.data['url']
        self.bridgeUsername = self.data['username']     # consider this as Your Name while joining meeting
        self.bridgePassword = self.data['password']     # consider this as Meeting Passcode
        self.lastUpdated = self.data['timestamp']
        self.callServer = self.data['ip']
        self.bridgeKey = self.data['bridge_key']
        self.state = "DDI_INIT"
        self.running = None
        self.sessionID = None
        self.outboundConnectedTimestamp = 0
        self.outbundThreadStart = int(time.time())
        self.dialOutError = "updated_on"
        self.lastException = "NULL"
        self.callID = "{0}_{1}_{2}".format(self.jpId, self.testCounter, self.testTypeId)
        self.lock = threading.Lock()

    def run(self):
        logging.info(f"{self.callID} in Outbound Process.")
        self.running = True
        while self.running:
            logging.info(f"Current State of Outbound Thread - {self.callID} : {self.state}")
            try:
                if time_since(self.outbundThreadStart) > 260 and self.state != "OUTBOUND_ERROR":
                    logging.info(
                        "{} - Thread is running since last 4 minutes something wrong.... Terminate the thread".format(
                            self.callID))
                    self.lastException = "Call OK - Dial out taking too long to connect to number possible of having an issue with CPU"
                    self.state = "OUTBOUND_ERROR"

                if time_since(self.lastUpdated) > 120 and self.state != "OUTBOUND_ERROR":
                    logging.info(
                        "[{0}] Recording channel call failed terminating - [{1}]".format(self.callID, self.state))
                    self.lastException = "Recording channel call failed terminating"
                    self.state = "RECORDING_DISCONNECTED"

                if self.state == 'DDI_INIT':
                    try:
                        self.zoomOutbound = ZoomOutbound({})
                        SeleniumTestBase.set_screenshot_reference(self.callID)
                        time.sleep(0.5)
                        logging.info("[{0}] - Browser Initialized".format(self.callID))
                        self.state = 'DDI_LOGIN'
                    except Exception as e:
                        logging.exception(f"Exception {e} in {self.callID} when initializing chrome.")
                        self.state = 'OUTBOUND_ERROR'
                        time.sleep(10)

                if self.state == 'DDI_LOGIN':
                    try:
                        self.zoomOutbound.start_browser_HAR_capture()
                        self.zoomOutbound.open_bridge_url(self.bridgeUrl)
                        recordingStatus = checkRecordingLegStatus(self.jpId, self.testCounter, self.testTypeId)
                        if recordingStatus is None or str(recordingStatus) == "0":
                            logging.info(
                                "callID [{0}] Recording Leg is not connected Wait some more time".format(self.callID))
                            self.state = "DDI_WAIT"
                            self.lastUpdated = int(time.time())
                            continue
                        else:
                            self.state = "DDI_RR_WAIT"
                    except Exception as e:
                        logging.exception(f"Exception {e} in {self.callID} when tried to Open Bridge.")
                        self.lastException = e
                        self.state = "OUTBOUND_ERROR"

                if self.state == "DDI_WAIT":
                    recordingStatus = checkRecordingLegStatus(self.jpId, self.testCounter, self.testTypeId)
                    if recordingStatus is None or str(recordingStatus) == "0":
                        logging.info(
                            "callID [{0}] Recording Leg is not connected Wait some more time".format(self.callID))
                        time.sleep(5)
                        continue
                    else:
                        self.state = "DDI_RR_WAIT"
                        self.lastUpdated = int(time.time())

                if self.state == "DDI_RR_WAIT":
                    recordingStatus = checkRecordingLegReady(self.jpId, self.testCounter, self.testTypeId)
                    if recordingStatus is None or str(recordingStatus) == "0":
                        logging.info("callID [{0}] Recording Leg is not ready Wait some more time".format(self.callID))
                        time.sleep(5)
                        continue
                    else:
                        self.state = "DDI_START_MEETING"
                        self.lastUpdated = int(time.time())

                if self.state == "DDI_START_MEETING":
                    try:
                        self.zoomOutbound.start_meeting(self.bridgePassword, self.bridgeUsername)
                        self.lastUpdated = int(time.time())
                        self.state = "DDI_START_CALL"
                    except Exception as e:
                        logging.exception(f"[{self.callID}] Error in joining meeting")
                        self.lastException = e
                        self.state = "OUTBOUND_ERROR"

                if self.state == "DDI_START_CALL":
                    try:
                        updateOutboundStatus(self.jpId, "ddi_call_start_time", self.testCounter, self.testTypeId)
                        call_status = self.zoomOutbound.connect_call(self.countryName,self.ddiNumber, "", "", timeout_seconds=300)
                        logging.info("callID [{0}] .Call Started. Country - {1}, Prefix - {2}, Number - {3}".
                                     format(self.callID, self.countryName, self.countryPrefix, self.ddiNumber))

                        if call_status is True:
                            updateOutboundStatus(self.jpId, "ddi_call_connect_time", self.testCounter, self.testTypeId)
                            # Updatinf Cli details
                            thread = cliUpdateThread(self.jpId, self.testTypeId, self.testCounter)
                            thread.setName("cliUpdate_{0}_{1}_{2}".format(self.jpId, self.testCounter, self.testTypeId))
                            thread.setDaemon(True)
                            thread.start()
                            self.outboundConnectedTimestamp = int(time.time())
                            self.state = "DDI_CALL_CONNECTED"
                        else:
                            self.state = "OUTBOUND_ERROR"
                    except Exception as e:
                        logging.exception("[{0}] - Exception Call Starting- {1}".format(self.callID, e))
                        self.lastException = e
                        self.state = "OUTBOUND_ERROR"

                if self.state == "DDI_CALL_CONNECTED" or self.state == "DDI_CALL_GENERATED":
                    logging.info(
                        f"{self.callID} - Call generated/connected since [{time_since(self.outboundConnectedTimestamp)}] seconds")
                    if time_since(self.outboundConnectedTimestamp) > 80:
                        self.state = "DDI_CALL_COMPLETED"
                    else:
                        time.sleep(5)

                if self.state == "DDI_CALL_COMPLETED":
                    try:
                        hangupChannel(self.callServer, self.jpId, self.testCounter, self.testTypeId)
                        updateOutboundStatus(self.jpId, "ddi_call_end_time", self.testCounter, self.testTypeId)
                        logging.info("callID [{0}] Meeting Completed".format(self.callID))
                        self.zoomOutbound.close_bridge()
                        self.state = "OUTBOUND_COMPLETED"
                    except Exception as e:
                        logging.exception("[{0}] - Exception Call Ending- {1}".format(self.callID, e))
                        self.state = "OUTBOUND_ERROR"

                if self.state == "OUTBOUND_ERROR":

                    try:
                        logging.info(
                            "callID [{0}] Disconnected Going to Terminate calls. Thread count={1}".format(self.callID,
                                                                                                          threading.active_count()))
                        alert_send_sns("Outbound-Test-Failed",
                                       "ERROR : Issue detected in script - zoom_workspace_meet.py",
                                       "callId-{0}\nLastException[{1}]".format(self.callID, self.lastException))
                        hangupChannel(self.callServer, self.jpId, self.testCounter, self.testTypeId)
                        updateOutboundStatus(self.jpId, self.dialOutError, self.testCounter, self.testTypeId)
                        SeleniumTestBase.capture_screen()
                        SeleniumTestBase.dump_page_source()
                        self.state = "OUTBOUND_COMPLETED"
                    except Exception as e:
                        logging.exception("[{0}] - Exception Handling Outbound Error steps- {1}".format(self.callID, e))
                        self.state = "OUTBOUND_COMPLETED"

                if self.state == "RECORDING_DISCONNECTED":
                    logging.info(
                        "callID [{0}] Recording Channel Disconnected Going to Terminate calls. Thread count={1}".format(
                            self.callID, threading.active_count()))
                    self.state = "OUTBOUND_ERROR"

                if self.state == "OUTBOUND_COMPLETED":
                    generateVideo(self.callID)
                    release_bridge(self.lock, self.bridgeKey)
                    try:
                        SeleniumTestBase.get_driver().quit()
                        logging.info("closed browser session and released bridge")
                        self.zoomOutbound.stop_proxy_server()
                        self.zoomOutbound.dump_HAR_file_contents()
                    except Exception as e:
                        logging.exception(f"Exception in closing browser session and releasing bridge : {e}")
                    finally:
                        self.running = False

            except Exception as e:
                logging.exception("An Error Detected in Outbound Thread - {}".format(e))
                self.lastException = e
                self.state = "OUTBOUND_ERROR"


#####################################################################################
# main process
threads = []
start_time = time.time()

t1 = GetJobs()
t1.name = 'GetJobs'
t1.daemon = True
t1.start()
time.sleep(1)
threads.append(t1)

while True:
    try:
        if (time_since(start_time) > 630) and len(CONF_RECORD) == 0:
            logging.info("Exiting script after 10 minutes 30 seconds.")
            sys.exit(0)

        for t in threads:
            if not t.is_alive():
                if t.name == 'GetJobs':
                    logging.info(f"{t.name} died/not running. killing main thread")
                    sys.exit(0)

        time.sleep(30)
    except Exception as e:
        logging.exception(f"Exception in main ({e})")

