from urllib.request import urlopen
from urllib.error import HTTPError
import json
import logging
from config import TargetConfig
import ssl
from datetime import datetime, time
from time import sleep
import pymysql
import argparse

# python3 main.py --tg WEATHER_CRAWLING

def main(args, logger):

    for target in args.tg:
        if target == 'WEATHER_CRAWLING':
            try:
                loop = True
                while loop == True:

                    #DB
                    conn = pymysql.connect(host=TargetConfig.DB_HOST, user=TargetConfig.DB_USER, password=TargetConfig.DB_PW, db=TargetConfig.DB_NAME, charset='utf8')
                    curs = conn.cursor()

                    print("-- 크롤링 시작 " + datetime.now().strftime('%Y%m%d %H:%M:%S'))

                    url = TargetConfig.WEATHER
                    try:
                        context = ssl._create_unverified_context()
                        html = urlopen(url, context=context)
                        source = html.read()
                        html.close()
                    except HTTPError as e:
                        err = e.read()
                        errCode = e.getcode()
                        print("HTTP ERROR >>>> " + errCode)

                    response = json.loads(source)

                    weaters = response.get("wetrMap")
                    w_time = weaters[0][1]

                    for i in range(1,len(weaters)):

                        code = weaters[i][0]
                        region = weaters[i][1].get("rgnNm")
                        temperature = int(weaters[i][1].get("tmpr"))
                        txt = weaters[i][1].get("wetrTxt")

                        # -- test -- 
                        print(w_time)
                        print("지역코드: ", code)
                        print("지역이름: ", region)
                        print("기온: ", temperature)
                        print("날씨: ", txt)
                        print("~~~~~")

                        sql = 'INSERT INTO WEATHER (CODE, REGION, TEMPERATURE, W_TXT, W_TIME, C_TIME) VALUES (%s, %s, %s, %s, %s, now()) ON DUPLICATE KEY UPDATE TEMPERATURE = %s, W_TIME = %s, C_TIME = now(), W_TXT = %s'
                        data = (code, region, temperature, txt, w_time, temperature, w_time, txt)
                        curs.execute(sql, data)
                        conn.commit()
                        print("@@ 데이터 입력 @@")
                        
                    print("-- S L E E P !")
                    sleep(10)
                
            except Exception as ex:
                logger.error("main error(2) " + str(ex))

if __name__ == '__main__':

    logging.basicConfig(format='[%(lineno)d]%(asctime)s||%(message)s')
    logger = logging.getLogger(name="myLogger")

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--tg', nargs='+', help='start crawling')
    args = parser.parse_args()

    try:
        main(args, logger)
    except:
        logger.error("main error(1)")
        raise