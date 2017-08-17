# coding=utf-8
from __future__ import absolute_import
import datetime
from selenium.webdriver.common.by import By

from .stock import int_to_date
from .base_page import BasePage


class TG(BasePage):
    def __init__(self,driver):
        super(TG, self).__init__(driver)
        self.driver.switch_to.default_content()
        ifrs = self.driver.find_elements(By.CSS_SELECTOR, 'iframe.dialogBodyIfr')
        for ifr in ifrs:
            if ifr.size['width'] != 0:
                self.driver.switch_to.frame(ifr)
                break


    def adslot(self, ads):
        actual = self.driver.find_element(By.CSS_SELECTOR,'td.col-adslot').text
        if actual!= ads:
            assert False, "Expect: {0}. Actual: {1}".format(ads, actual)

    def platform(self, platform):
        actual = self.driver.find_element(By.CSS_SELECTOR, 'td.col-platform').text
        if actual != platform:
            assert False, "Expect: {0}. Actual: {1}".format(platform, actual)


    def region(self, regions):
        regions = regions.split(';')
        tds = self.driver.find_elements(By.CSS_SELECTOR, 'td.col-region')
        for (region, td) in zip(regions, tds):
            actual = td.text
            if actual != region:
                assert False, "Expect: {0}. Actual: {1}".format(region, actual)


    def price(self, prices):
        prices = prices.split(';')
        tds = self.driver.find_elements(By.CSS_SELECTOR, 'td.col-price')
        for (price, td) in zip(prices, tds):
            actual = td.text
            if actual != price:
                assert False, "Expect: {0}. Actual: {1}".format(price, actual)

    def date(self, d):
        dates= list()
        start = int(d.split(';')[0])
        end = int(d.split(';')[1])
        index = d.split(';')[2].split('.')
        for i in range(end-start):
            dates.append(int_to_date(start+i))

        date = map(lambda i: dates[i], index)
        months_tds = self.driver.find_elements(By.XPATH,'/td[@data-col="month"]')
        days_tds = self.driver.find_elements(By.XPATH,'/td[@data-col="date"]')
        for m in months_tds:
            width = int(m.get_attribute('colspan')) if m.get_attribute('colspan') else 1
            date_ = date[0:width]
            day_ths = days_tds[0:width]
            for d, td in zip(date_, day_ths):
                if d[0:7]!=m.text:
                    assert False, "Expect: {0}. Actual: {1}".format(d[0:7], m.text)
                if d[7:] != td.text:
                    assert False, "Expect: {0}. Actual: {1}".format(d[7:], td.text)

    def delivery(self, sum):
        divs = self.driver.find_elements(By.CSS_SELECTOR,'div.val_cpm')
        actual = sum(map(lambda ele: int(ele.text), divs))
        if sum != actual:
            assert False, "Expect: {0}. Actual: {1}".format(sum, actual)

    def verify(self, **kwargs):
        dic = {
            '广告位':self.adslot,
            '端口':self.platform,
            '地域':self.region,
            '价格':self.price,
            '排期':self.date,
            '下单量':self.delivery
        }

        for key, value in kwargs.items():
            if key in dic.keys():
                dic[key](value)

