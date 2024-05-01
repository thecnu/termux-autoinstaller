import os
import time
import logging
import datetime
import requests

#adb shell nohup am instrument -w io.appium.uiautomator2.server.test/androidx.test.runner.AndroidJUnitRunner

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

config = {
    "baseApi": "http://127.0.0.1:6790/wd/hub",
    "appPackage": "com.android.chrome",
    "appActivity": "com.google.android.apps.chrome.IntentDispatcher"
}

isAndroid = 'ANDROID_STORAGE' in os.environ or 'ANDROID_ROOT' in os.environ

try:
    # launch apps
    if isAndroid:
        os.system("am start -W -n {0}/{1} -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000".format(
            config["appPackage"], config["appActivity"]))
    else:
        os.system("adb shell am start -W -n {0}/{1} -S -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -f 0x10200000".format(
            config["appPackage"], config["appActivity"]))

    def command(type, *args, **kwargs):
        requestData = kwargs.get('data', None)
        sessionId = kwargs.get('sessionId', None)
        elementId = kwargs.get('elementId', None)

        #if status == 200:


        if type == "status":
            requestMethod = "get"
            requestUrl = "{0}/status".format(config['baseApi'])
        elif type == "createSession":
            requestMethod = "post"
            requestUrl = "{0}/session".format(config['baseApi'])
        elif type == "findElement":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/element".format(
                config['baseApi'], sessionId)
        elif type == "clickElement":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/element/{2}/click".format(
                config['baseApi'], sessionId, elementId)
        elif type == "inputElement":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/element/{2}/value".format(
                config['baseApi'], sessionId, elementId)
        elif type == "goBack":
            requestMethod = "post"
            requestUrl = "{0}/session/{1}/back".format(
                config['baseApi'], sessionId)

        if requestMethod == 'post':
            r = requests.post(requestUrl, json=requestData)
        else:
            r = requests.get(requestUrl, json=requestData)

        if r.ok:
            return r.json()
        else:
            raise Exception(r.json()["value"]["error"])

    logging.info("checking is uiautomator server running")
    if not command('status'):
        raise Exception("UIAutomator server not running.")

    logging.info("create new session")
    sessionId = command("createSession", data={
        "capabilities": {
        }
    })["sessionId"]


    #command("clickElement", sessionId=sessionId, elementId=elementId2)
    #logging.info("ilk arama click ok")

    def permission():
        try:

            time.sleep(1)
            logging.info("izin bekleme click")
        
            # XPath ifadesiyle eşleşen öğeleri bul
            elements = command("findElement", sessionId=sessionId, data={
                    "strategy": "xpath",
                    "selector": "//android.widget.Button[@text='Allow']"
            })["value"]["ELEMENT"] 
        
            command("clickElement", sessionId=sessionId, elementId=elements)
            logging.info("izin verildi")
            return True
        except:
            return False   


    
#------------------------------------------------------------------------------------------------------------------------------------------------------------

    while True:
        if permission == True:
            time.sleep(2)
            logging.info("true")
            permission()
        else:
            logging.info("false")
            time.sleep(5)
            permission()


#------------------------------------------------------------------------------------------------------------------------------------------------------------


except Exception as e:
        logging.error(str(e))
exit()