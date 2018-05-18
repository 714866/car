# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 17:11:33 2018

@author: Administrator
"""
import urllib

import requests
from lxml import etree

class spy():
   def __init__(self):
       self.page = 1
       self.url = 'https://www.qiushibaike.com/8hr/page/'+str(self.page)
       self.urlheaders={
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
       'Accept-Language': 'zh-CN,zh;q=0.8'
           }

   def Req(self):
       response = requests.get(self.url,headers=self.urlheaders).text
       html = etree.HTML(response)
       result = html.xpath('//div[contains(@class,"article block untagged mb15")]')

       for sit in result:
           content=sit.xpath('.//div[@class="content"]/span/text()')[0].strip()
           Urlimg=sit.xpath('./div[2]/a/img/@src')
           print(content,Urlimg)

if __name__=='__main__':
   neihhan=spy()
   neihhan.Req()

