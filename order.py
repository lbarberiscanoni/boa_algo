from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time


class Order():

    def __init__(self, username, password, browser):
        self.username = username
        self.password = password
        self.browser = browser

    def login(self):
        self.browser.get("https://olui2.fs.ml.com/login/login.aspx?sgt=3")
        userInpt = self.browser.find_element_by_id("txtUserid")
        userInpt.send_keys(self.username)
        passInpt = self.browser.find_element_by_id("txtPassword")
        passInpt.send_keys(self.password)
        submitBtn = self.browser.find_element_by_id("btnValidate")
        submitBtn.click()

    def checkAssets(self):
        myAccount = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphRight2_View3_TCPE1pnlHeader")
        myAccount.click()
        time.sleep(1)
        try:
            currentBalance = self.browser.find_elements_by_css_selector("#tblDetailbTCPE_Balances .txtRight")[1]
            assets = float(str(currentBalance.text).replace("$", ""))
        except:
            myAccount.click()
            time.sleep(1)
            currentBalance = self.browser.find_elements_by_css_selector("#tblDetailbTCPE_Balances .txtRight")[1]
            assets = float(str(currentBalance.text).replace("$", ""))
        return assets

    def exitPosition(self, ticker):
        actionInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_ddlOrderType")
        actionInpt.send_keys("Sell")
        tickerInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_txtSymbol")
        tickerInpt.send_keys(ticker)
        tickerInpt.send_keys(Keys.RETURN)
        time.sleep(1)
        qtyInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_cbSellAll")
        qtyInpt.click()

    def getCurrentPrice(self):
        currentPrice = self.browser.find_element_by_css_selector(".wgt-trade-qte-table .noborder .floatRight")
        currentPrice = float(str(currentPrice.text).replace("$", ""))
        return currentPrice

    def confirmTrade(self):
        durationInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_ddlExpiration")
        durationInpt.send_keys("Good Until Canceled (30 days)")
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        submitBtn = self.browser.find_element_by_css_selector(".actionlinks a #ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_resxlblOrderPreviewText")
        submitBtn.click()
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        confirmBtn = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_EquitiesResourceLabel2")
        #confirmBtn.click()

    def safePass(self):
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_SafePassControl_ecmsEntryHeader")))
        self.browser.execute_script("LaunchGetSafePassCodeModal()")
        time.sleep(1)
        self.browser.switch_to_frame("pucSendAuthCodeModal")
        emailInpt = self.browser.find_element_by_id("ctl00_ctl00_cphNestedUtility_cphStage_trEmail")
        print emailInpt.text

    def stopLossOrder(self, ticker):
        self.browser.get("https://olui2.fs.ml.com/Equities/OrderEntry.aspx")
        self.exitPosition(ticker)
        currentPrice = self.getCurrentPrice()

        orderTypeInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_ddPriceType")
        orderTypeInpt.send_keys("Stop Quote Limit")
        stopPriceInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_txtStopPrice")
        stopPriceInpt.send_keys(str(format((currentPrice * 0.995), ".2f")))
        limitPriceInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_txtLimitPrice")
        limitPriceInpt.send_keys(str(format((currentPrice * 0.990), ".2f")))

        self.confirmTrade()

    def ceiling(self, ticker):
        self.browser.get("https://olui2.fs.ml.com/Equities/OrderEntry.aspx")
        self.exitPosition(ticker)
        currentPrice = self.getCurrentPrice()

        orderTypeInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_ddPriceType")
        orderTypeInpt.send_keys("Limit")
        time.sleep(0.5)
        limitPriceInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_txtPrice")
        limitPriceInpt.send_keys(str(format((currentPrice * 1.35), ".2f")))

        self.confirmTrade()

    def buyOrder(self, ticker):
        self.browser.get("https://olui2.fs.ml.com/Equities/OrderEntry.aspx")
        aum = self.checkAssets()
        actionInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_ddlOrderType")
        actionInpt.send_keys("Buy")
        tickerInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_txtSymbol")
        tickerInpt.send_keys(ticker)
        tickerInpt.send_keys(Keys.RETURN)
        time.sleep(1)
        currentPrice = self.browser.find_element_by_css_selector(".wgt-trade-qte-table .noborder .floatRight")
        currentPrice = float(str(currentPrice.text).replace("$", ""))
        tradeSize = int(aum // currentPrice)
        qtyInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_txtQuantity")
        qtyInpt.send_keys(str(tradeSize))
        orderTypeInpt = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_ddPriceType")
        orderTypeInpt.send_keys("Market")
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        submitBtn = self.browser.find_element_by_css_selector(".actionlinks a #ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_resxlblOrderPreviewText")
        submitBtn.click()
        time.sleep(1)
        self.safePass()
        #self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        #confirmBtn = self.browser.find_element_by_id("ctl00_ctl00_ctl00_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_EquitiesResourceLabel2")
        #confirmBtn.click()

    def test(self):
        self.login()
        time.sleep(5)
        #self.buyOrder("VRX")
        time.sleep(2)
        self.buyOrder("ISSC")
        time.sleep(5)

if __name__ == "__main__":
    username = str(sys.argv[1])
    password = str(sys.argv[2])
    x = Order(username, password, webdriver.Chrome()).test()
