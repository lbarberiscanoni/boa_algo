from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import subprocess
import time
from datetime import datetime
import order
import sys

from os.path import expanduser
home = expanduser("~")

market = str(sys.argv[1])
side = str(sys.argv[2])
task = str(sys.argv[3])

class Trade():

    def __init__(self, market, side):
        self.market = market
        self.side = side
        self.url_options = {
                "nyse": {
                    "long": "http://online.wsj.com/mdc/public/page/2_3021-gainnyse-gainer.html", 
                    "short": "http://online.wsj.com/mdc/public/page/2_3021-losenyse-loser.html",
                }, "nasdaq": {
                    "long": "http://online.wsj.com/mdc/public/page/2_3021-gainnnm-gainer.html", 
                    "short": "http://online.wsj.com/mdc/public/page/2_3021-losennm-loser.html"
                }
        }
        self.parameter_options = {
                "nyse": 
                    {"long": 
                        {"ceiling": 3.5, "floor": -0.5, "position": 2}, 
                    "short": 
                        {"ceiling": 3.5, "floor": -0.5, "position": 2}
                    }, 
                "nasdaq": 
                    {"long": 
                        {"ceiling": 8, "floor": -0.5, "position": 1}
                    , "short": 
                        {"ceiling": 6.5, "floor": -0.5, "position": 1}
                    } 
        }


        if sys.platform == "darwin":
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.PhantomJS()

    def statusUpdate(self, message):
        orderUpdate = "python gmailText.py -u hllbck7@gmail.com -p l0ll02013 -t 8642436724@text.att.net -b '" + str(message) + "'"
        subprocess.call(orderUpdate, shell=True)

    def checkRanks(self):
        self.browser.get(self.url_options[self.market][self.side])
        rows = self.browser.find_elements_by_css_selector(".mdcTable tbody tr")
        #removing extra rows that don't contain data
        for i in range(0, len(rows) - 100):
            rows.pop(i)

        row = rows[int(self.parameter_options[self.market][self.side]["position"]) - 1]
        rowData = row.text.split(" ")
        ticker = str(rowData[len(rowData) - 5]).replace("(", "").replace(")", "")

        return ticker

    def checkAssets(self):
        aum = self.browser.find_element_by_id("SpnNvCOBPctTOTAL")
        aum = str(aum.text).replace("%", "")
        return float(aum)

    def run(self):
        i = 0
        status = 0
        errors = 0
        closures = 0
        instance = order.Order("eths1982", "Lorenzo#1", self.browser)
        instance.login()
        time.sleep(3)
        while status == 0:
            try:
                print "loop #" + str(i)
                today = str(datetime.now()).split(" ")[1]
                today = today.split(".")[0]
                today = int(today.replace(":", ""))
                print today
                if 125000 < today <= 131000:
                    ticker = self.checkRanks()
                    if errors < 5:
                        try:
                            #instance.buyOrder(ticker)
                            self.statusUpdate("time to invest")
                            time.sleep(3)
                            status = 1
                        except Exception as e:
                            print e
                            errors += 1
                    else:
                        status = 1

                else:
                    self.browser.refresh()
                    aum = self.checkAssets()
                    print aum
                    if aum >= self.parameter_options[self.market][self.side]["ceiling"]:
                        self.statusUpdate("ceiling was hit")

                time.sleep(1)
                i += 1
            except Exception as e:
                self.statusUpdate(str(e))

        self.statusUpdate("done for the day")
        self.browser.close()

if task == "trade":
    Trade(market, side).run()
elif task == "test":
    print Trade(market, side).checkRanks()
