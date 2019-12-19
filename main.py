from urllib.request import urlopen
from urllib.error import HTTPError
import json
import logging
from config import TargetConfig
import ssl



def main():

    try:
        print("-- 크롤링 시작 --")
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

        for i in range(1,len(weaters)+1):
            print(weaters[i][1].get("rgnNm"))
            print(int(weaters[i][1].get("tmpr")))
    
    except Exception as ex:
        logging.info("main error(2)" + str(ex))
    




if __name__ == '__main__':

    try:
        main()
    except:
        logging.info("main error(1)")