# -*- coding: utf-8 -*-

"""
Created on Thu May 17 17:11:33 2018

@author: Administrator
"""

from lxml import etree

import requests

import threading

from queue import Queue

import os

import time

import json

class ThreadCraw(threading.Thread):
    def __init__(self, pageQueue, dataQueue, nameQueue):
        super(ThreadCraw,self).__init__()
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.nameQueue= nameQueue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        # print(self.nameQueue)

    def run(self):
        # while not CRAWL_EXIT:
        while not self.pageQueue.empty():
            try:
                # print('ABC')
                page = self.pageQueue.get(False)
            except:
                # print('abc')
                pass
            else:
                # time.sleep(2)
                print(page, os.getpid(), self.nameQueue)
                url = 'https://www.qiushibaike.com/8hr/page/' + str(page)
                content = requests.get(url, headers=self.headers)
                self.dataQueue.put(content.text)


class ThreadParse(threading.Thread):
    '''
    处理数据线程
    '''
    def __init__(self, pageQueue, dataQueue, threadparsename, filename, lock):
        super(ThreadParse,self).__init__()
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.threadparsename = threadparsename
        self.filename = filename
        self.lock = lock
        # print(self.threadparsename)

    def run(self):
        time.sleep(2)

        while (not self.dataQueue.empty())|(not self.pageQueue.empty()) :

            try:

                html = self.dataQueue.get(False)
            except:
                print('结束了%s'%self.threadparsename)
                pass
            else:
                self.parse((html))
                print('q'*30)
                print(self.threadparsename)



    def parse(self, html):
        text = etree.HTML(html)
        node_list = text.xpath('//div[contains(@id, "qiushi_tag")]')
        items = {}
        for node in node_list:
            username = node.xpath('.//div/a/@title')[0]
            image = node.xpath('.//div[@class="thumb"]/scr')
            context = node.xpath('.//div[@class="content"]/span')[0].text.strip()
            zan = node.xpath('.//i')[0].text
            comments = node.xpath('.//i')[1].text
            # print(username,image,context,zan,comments)
            items = {
                'username' : username,
                'image' : image,
                'context' : context,
                'zan' : zan,
                'comments' : comments

            }
            self.lock.acquire()
            self.filename.write(json.dumps(items, ensure_ascii = False)+'\n')
            self.lock.release()
            # with self.lock:
            #     self.filename.write(json.dumps(items, ensure_ascii = False)+'\n')




# CRAWL_EXIT = False
PARSE_EXIT = False
def main():
    '''
    爬虫函数，定义初始数据
    :return:
    '''
    pageQueue = Queue(10)
    for i in range(1, 11):
        pageQueue.put(i)
    dataQueue = Queue()
    threadcrawl = []
    nameQueue = ['A','B','C']
    for i in range(0,3):
        thread = ThreadCraw(pageQueue, dataQueue, nameQueue[i])
        thread.start()
        threadcrawl.append(thread)

    filename = open('duanzi.json','a')
    lock = threading.Lock()
    threadparse = []
    threadparsename = ['解析A','解析B', '解析C',]
    for name in threadparsename:
        thread = ThreadParse(pageQueue, dataQueue, name, filename , lock)
        thread.start()
        threadparse.append(thread)


    print('线程数：%s'%threading.enumerate())
    # while not pageQueue.empty():
    #     pass
    for thread in threadcrawl:
        thread.join()
    print('_'*30)

    # while not dataQueue.empty():
    #     pass
    #
    # print('*'*30)
    # global PARSE_EXIT
    # PARSE_EXIT = True

    for threadp in threadparse:
        threadp.join()
    print('+'*30)
    # with lock:
    filename.close()
    print('结束了')
if __name__ == '__main__':

    main()