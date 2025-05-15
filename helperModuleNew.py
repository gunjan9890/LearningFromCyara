#!/usr/bin/env python3
import os
import json
import socket
import time
import sys
import hashlib
import threading
import boto3
import pymysql
import logging

from typing import Set

try:
    file_name = '/home/scripts/NewOutboundCallGenScripts/config.json'
    with open(file_name,'r') as configFile:
        file_data = configFile.read()
        config = json.loads(file_data)

    file_name = '/etc/spearline/db.json'
    with open(file_name,'r') as configFile:
        file_data = configFile.read()
        db_config = json.loads(file_data)
except Exception as e:
        logging.error(f"Error in {file_name}:{e}")
        sys.exit (0)

BOTO_REGION='eu-west-1'
BOTO_SNS_ENDPOINT='arn:aws:sns:eu-west-1:203698524759:'
SOURCE_IP=config["SOURCE_IP"]
SECRET_KEY="8e74Ebn8572Rtjdyr8aVX3816bBt204"
MD5_HASH=hashlib.md5(f"{SOURCE_IP}{SECRET_KEY}".encode()).hexdigest()
#CHECKOUT_IP='172.30.0.211'
CHECKOUT_IP=config["CHECKOUT_IP"]
DEVEL=True if config["__DEV__"] == 1 else False
CHECKOUT_PORT=12347 if not DEVEL else 12348
CALL_SCRIPT_SERVER=config["CALL_SCRIPT_SERVER"]
JP_TABLE = "job_processing_outbound_conf"

if CALL_SCRIPT_SERVER == "0":
    providerType = "p.provider_type_id = 6"
else:
    providerType = "p.provider_type_id != 6"


if config.get('__DEV__',1) == 1:
    db_key = 'spearlinedb_devel'
else:
    db_key = 'spearlinedb_write'



def sql_query (query: str, return_dict: bool = False, is_select: bool = True,fetch_all: bool = True) -> Set:
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

def get_route(companyId,testTypeId,routeId,countryCodeId,numberTypeId,serverId,ddiproviderTypeId=-1):
    try:
        providerTypeId = ddiproviderTypeId if ddiproviderTypeId != -1 else providerType
        if routeId is not None:
            getRouteDetails="SELECT r.id as rid,r.route,p.id,pc.cli,r.strip_digits as rp FROM route r LEFT JOIN provider p ON r.provider_id=p.id LEFT JOIN provider_cli pc ON r.cli_id=pc.id WHERE r.id={0} AND {1} limit 1".format(routeId,providerTypeId)
        else:
            getRouteDetails="SELECT r.id as rid,r.route,p.id,pc.cli,r.strip_digits as rp FROM route r LEFT JOIN provider p ON r.provider_id=p.id LEFT JOIN provider_cli pc ON r.cli_id=pc.id WHERE r.country_code_id={0} AND r.number_type_id={1} AND p.server_id={2} AND r.status=1 AND p.provider_type_id NOT IN (7,8,9) AND {3} order by r.priority limit 1".format(countryCodeId,numberTypeId,serverId,providerTypeId)

        logging.info("getRouteDetails=%s" % getRouteDetails)
        route = sql_query(getRouteDetails,fetch_all=False)
        return route if route else None
    except Exception as e:
        logging.exception(f"Got error in get route: {e}")
        return None

def generateVideo(callID):
    command = "ffmpeg -pattern_type glob -framerate 1 -i '/home/screenshot/zoom_outbound/*{0}*.png' -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -pix_fmt yuv420p /home/video_ready/{0}.mp4".format(callID)
    logging.info("{0} - FFMPEG Command  ({1})".format(callID,command))
    response = os.popen(command)
    response.read()
    response.close()
    logging.info("{0} - Video File Created moving to upload folder...".format(callID))
    os.system("mv -f /home/screenshot/zoom_outbound/*{0}*.png /home/screenshot_uploaded/".format(callID))


def alert_send_sns(topic,subject,message):
    try:
        client = boto3.client('sns',region_name=BOTO_REGION)
        endpoint = BOTO_SNS_ENDPOINT
        details = "hostname = " + socket.gethostname()
        message = message + "\n---------------------------\n" + details
        logging.critical("SNS sent. sns message: {0}".format(message))
        if topic:
            response = client.publish(
                TargetArn="{0}{1}".format(endpoint,topic),
                Message=message,
                Subject=subject
            )
            logging.info("SNS sent. Response: {0}".format(response))
    except Exception as e:
        logging.exception("ERROR in SNS : {0} ".format(e))

def checkInPort(uId,providerId):
    requestString="ci;%s;%s;%s" % (MD5_HASH,uId,providerId)
    logging.debug("\t\tCheckin Request=%s" % requestString)
    try:
        checkInSocket=socket.socket()
        checkInSocket.settimeout(3)
        checkInSocket.connect((CHECKOUT_IP,CHECKOUT_PORT))
        checkInSocket.send(requestString.encode())
        responseString=checkInSocket.recv(1024)
        checkInSocket.close()
        logging.debug("\t\tCheckIn Response %s",responseString)
    except socket.timeout:
        logging.error("\t\tCheckout. Socket Timeout.")
    except socket.error as e:
        logging.error("\t\tCheckout. Socket Error (%d:%s)." % (e.args[0],e.args[1]))
    return

def checkOutPort(companyId,testTypeId,providerId):
    requestString="pco;%s;%s;%s;%s" % (MD5_HASH,companyId,providerId,testTypeId)
    logging.debug("\t\tCheckout Request=%s" % requestString)
    try:
        checkOutSocket=socket.socket()
        checkOutSocket.settimeout(3)
        #checkOutSocket.connect(("79.125.21.138",12347))
        checkOutSocket.connect((CHECKOUT_IP,CHECKOUT_PORT))
        checkOutSocket.send(requestString.encode())
        responseString=checkOutSocket.recv(1024)
        checkOutSocket.close
        logging.debug("\t\tCheckout Response %s",responseString)
        if (responseString == ''):
            return ('na','No Response from Checkout')
        responseString=responseString.decode().split(";")
        return (responseString[0],responseString[1])
    except socket.timeout:
        logging.error("\t\tCheckout. Socket Timeout.")
        return ('na','Socket Timeout')
    except socket.error as e:
        logging.error("\t\tCheckout. Socket Error (%d:%s)." % (e.args[0],e.args[1]))
        return ('na','Socket Error')


############## UTILITY CLASSES ADDED BY RAVINDRA D. BHATT ########
class AMIAction():
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.logout_action = "Action: Logoff\r\n\r\n"
        self.login_action="Action: Login\r\nUsername: admin\r\nSecret: mvemj6u9p\r\nEvents: off\r\n\r\n"

    def get_response(self,action,buff_size: int =1024):
        try:
            self.sock.send(action.encode())
            data = bytearray()
            while True:
                response = self.sock.recv(buff_size)
                data.extend(response)
                #if b'Error' in response or b'Success' in response:
                if b'Response' in response:
                    break
            return data.decode()
        except OSError as e:
            logging.error(f"Socket Error:{e}")
            return None


    def login(self,addr,port:int = 5038,timeout: int= 3):
        try:
            self.sock = socket.socket()
            self.sock.settimeout(timeout)
            self.sock.connect((addr,port))
            res = self.get_response(self.login_action,84)
            logging.info(f"\t\tAMI Login Response:\n {res}")
            res_list = res.split('\n')
            if 'Message: Authentication accepted\r' in res_list or 'Success' in res_list:
                return True
            else:
                return False
        except OSError as e:
            logging.error("Socket Error: %s : %s",addr,e)
            return False


    def logout(self):
        try:
            res = self.get_response(self.logout_action,84)
            logging.info(f"\t\tAMI Logout Response:\n {res}")
            self.sock.close()
            return True
        except OSError as e:
            logging.exception("Error in AMI logout %s" % e.args)
            return False
    # generic method for all socket operations
    def exec_action(self,ami_command):
        pass

def time_since(from_time: time):
    return int(time.time() - int(from_time))
def get_jp_table(tt_id):
    return f"{JP_TABLE}_long" if tt_id == 81 else JP_TABLE

class cliUpdateThread(threading.Thread):
    def __init__(self,jpID, test_type_id, test_counter):
        super().__init__()
        self.jpId = jpID
        self.testTypeId = test_type_id
        self.testCounter = test_counter
        self.threadTime = int(time.time())
        self.db = pymysql.connect(**db_config[db_key],connect_timeout=120,autocommit = True)
        self.jp_table = get_jp_table(self.testTypeId)
        self.cur = self.db.cursor()

    def run(self):
        logging.info("Running cliUpdate thread for JobId: {0}".format(self.jpId))
        while time_since(self.threadTime) < 35:
            try:
                query = "SELECT sic.cli FROM spearline_incoming_call sic left join server s on sic.server_id=s.id left join provider p on p.server_id=s.id left join provider_did pd on pd.provider_id=p.id left join {2} jp on jp.provider_did_id=pd.id WHERE sic.call_time > jp.ddi_call_start_time and call_time <= (jp.ddi_call_connect_time + INTERVAL 30 SECOND) AND RIGHT(sic.did,3) = RIGHT(pd.did,3) and jp.id={0} and jp.test_counter={1}".format(self.jpId,self.testCounter,self.jp_table)
                logging.debug(query)
                rowcount = self.cur.execute(query)
                if rowcount > 0:
                    result = self.cur.fetchone()
                    logging.info(f"For {self.jpId}_{self.testCounter} found  cli:{result[0]}")
                    query = "UPDATE {4} set received_cli = '{0}'  WHERE id = {1} AND test_type_id = {2} AND test_counter = {3}".format(result[0],self.jpId,self.testTypeId,self.testCounter,self.jp_table)
                    logging.debug(query)
                    rowcount = self.cur.execute(query)
                    logging.debug("Update rewcount",rowcount)
                    if rowcount > 0:
                        break
            except pymysql.OperationalError as e:
                logging.exception(f"We got error in sql_query {e} query: {query}")
            except pymysql.Error as e:
                logging.exception(f"We got error in sql_query: {e.args} query: {query}")
            time.sleep(1)
        self.cur.close()
        self.db.close()

def sendToManager(call_string,server):
    try:
        ami = AMIAction()
        ami.login(server)
        ami.get_response(call_string)
        ami.logout()
    except Exception as e:
        logging.info(f"Error in send to manager: {e}")

def checkRecordingLegReady(jpId,testCounter,testTypeId):
    result = 0
    try:
        query="SELECT recording_ready FROM {2}_status WHERE {2}_id={0} AND test_counter={1}".format(jpId,testCounter,get_jp_table(testTypeId))
        logging.info("checkRecordingLegReady Query={}".format(query))
        qry_res = sql_query(query,fetch_all=False)
        if qry_res is not None and qry_res[0] != "0000-00-00 00:00:00":
            logging.info("recordingLegStarted={}".format(qry_res[0]))
            result = 1
    except Exception as e:
        logging.info(f"Error in checkRecordingLegReady: {e}")
    return result

def checkRecordingLegStatus(jpId,testCounter,testTypeId):
    result = 0
    try:
        query="SELECT IF(call_connect_time = '0000-00-00 00:00:00' or call_end_time!='0000-00-00 00:00:00',0,1) as connected FROM {3} WHERE id={0} AND test_counter={1} AND test_type_id={2}".format(jpId,testCounter,testTypeId,get_jp_table(testTypeId))
        logging.info("checkRecordingLegStatus Query={}".format(query))
        qry_res = sql_query(query,fetch_all=False)

        if qry_res[0] :
            logging.info("recordingLegStarted={}".format(qry_res[0]))
            result = 1
    except Exception as e:
        logging.info(f"Error in checkRecordingLegStatus: {e}")
    return result

def updateOutboundStatus(jpId,columnName,testCounter,testTypeId):
    try:
        jp_table = get_jp_table(testTypeId)
        if 'call_description_id' in columnName:
            query="UPDATE {4} SET ddi_call_end_time=NOW(),updated_on=NOW(),{0} WHERE id = {1}  and test_counter = {2} AND test_type_id={3}".format(columnName,jpId,testCounter,testTypeId,jp_table)
        else:
            query="UPDATE {4} SET {0}=NOW() WHERE id = {1}  and test_counter = {2} AND test_type_id={3}".format(columnName,jpId,testCounter,testTypeId,jp_table)
        logging.info("updateOutboundStatus Query={}".format(query))
        sql_query(query,is_select=False)
        if columnName == "ddi_call_connect_time":
            playing_ready ="UPDATE {2}_status SET playing_ready=NOW() WHERE {2}_id={0} and test_counter={1}".format(jpId,testCounter,jp_table)
            sql_query(playing_ready)
    except Exception as e:
        logging.info(f"Error in updateOutboundStatus: {e}")

def hangupChannel(callServer,jpId,testCounter,testTypeId):

    try:
        query="SELECT recording_channel FROM {2}_status WHERE {2}_id={0} and test_counter={1} and recording_ready != '0000-00-00 00:00:00';".format(jpId,testCounter,get_jp_table(testTypeId))
        logging.info("[{0}_{1}_{2}] HangupChannel Query={3}".format(jpId,testCounter,testTypeId,query))
        recording_channel = sql_query(query,fetch_all=False)
        if recording_channel is not None and recording_channel[0]:
            logging.info("recording_channel={}".format(recording_channel[0]))
            hangupCommand = "Action: Hangup\r\nChannel: {}\r\n\r\n".format(recording_channel[0])
            logging.info("{0} - {1}  - {2}".format(callServer,hangupCommand,jpId))
            sendToManager(hangupCommand,callServer)
    except Exception as e:
            logging.exception("Exception in hangupChannel. ({}).".format(e))


