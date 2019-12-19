from urllib.request import urlopen
from urllib.error import HTTPError
import json
import logging
from config import TargetConfig
import ssl
from datetime import datetime, time
from time import sleep

def main():

    try:
        loop = True
        while loop == True:

            print("-- 크롤링 시작 " + datetime.now().strftime('%Y%m%d %H:%M:%S'))

            url = TargetConfig.WEATHER
            try:
                context = ssl._create_unverified_context()
                html = urlopen(url, context=context)
                source = html.read()
                html.close()
            except HTTPError as e:
                err = e.read()
                code = e.getcode()
                print("HTTP ERROR >>>> " + code)

            response = json.loads(source)

            weaters = response.get("wetrMap")
            time = weaters[0][1]
            print(time)

            for i in range(1,len(weaters)):
                print(weaters[i][1].get("rgnNm"))
                print(int(weaters[i][1].get("tmpr")))
            
            print("S L E E P !")
            sleep(10)
        
    except Exception as ex:
        logging.error("main error(2)" + str(ex))

if __name__ == '__main__':

    try:
        main()
    except:
        logging.error("main error(1)")