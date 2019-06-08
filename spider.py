#coding:utf-8
import datetime
import json
import re
import threading
import time
import requests
import csv
import mysql
from queue import Queue
from lxml import etree
#from com.grg.spider.zhaobiao.mysql import MySQL
class ZhenfucaigouSpider():
    def __init__(self):
        self.url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1'
        self.keyword = ''
        self.start_time = '2018:06:01'
        self.end_time = '2018:12:29'

        self.params = {
            'searchtype': '1',
            'page_index':'',
            'bidSort': '0',
            'pinMu': '0',
            'bidType': '0',
            'displayZone':'',
            'zoneId':'',
            'kw':self.keyword,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'timeType': '6'
        }
        self.headers = {
            'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
            'Host': 'search.ccgp.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36',
            'keep-alive':'False'
        }
    #    mysql = MySQL()

    def get_page(self,page_index):
        try:
            self.params['page_index'] = page_index
            response = requests.get(url=self.url,headers=self.headers,params=self.params)
            if response.status_code == 200:
                html = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                #print(html)
                return html
            else:
                print(response.status_code)
        except requests.ConnectionError:
            return None

    def get_detail_page(self,url):
        try:
            response = requests.get(url=url,timeout=5)
            if response.status_code == 200:
                html = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                #print(html)
                return html
        except requests.ConnectionError:
            return None


    def get_all_url(self,html):
        pattern1 = '<.*?(href=".*?htm").*?'
        href_url = re.findall(pattern1, html, re.I)
        # print(href_url)
        url_list = []
        for url in href_url:
            url1 = url.replace('href=','').replace('"','')
            url_list.append(url1)
        return url_list

    def parse_datail_page(self,html,url):
        table_list = html.xpath('//div[@class="table"]//tr')
        # print(table_list)
        # time.sleep(20)
        all_info = {
            'url':None,
            '采购项目名称':None,
            '爬取时间':None,
            '品目':None,
            '采购单位':None,
            '行政区域':None,
            '公告时间':None,
            '获取招标文件时间':None,
            '招标文件售价':None,
            '获取招标文件地点':None,
            '开标时间':None,
            '开标地点':None,
            '预算金额':None,
            '项目联系人':None,
            '项目联系电话':None,
            '采购单位地址':None,
            '采购单位联系方式':None,
            '代理机构名称':None,
            '代理机构地址': None,
            '代理机构联系方式':None
        }
        all_info['url']=url
        try:
            for table in table_list:
                if len(table.xpath('td[@class="title"]/text()'))>0:
                    #print(''.join(table.xpath('td[@class="title"]/text()'))+":"+''.join(table.xpath('td[@colspan="3"]/text()')))
                    title = ''.join(table.xpath('td[@class="title"]/text()'))
                    value = ''.join(table.xpath('td[@colspan="3"]/text()'))
                    if (title.find('附件')==0):
                        value = 'http://www.ccgp.gov.cn/oss/download?uuid='+''.join(table.xpath('td[@colspan="3"]/a/@id'))
                        #print(title+value)
                    if ('公告时间' in title):
                        title = '公告时间'
                        value = table.xpath('td[@width="168"]/text()')[1]
                        district_key = '行政区域'
                        district_value = (table.xpath('td[@width="168"]/text()'))[0]
                        all_info[district_key]=district_value
                    if '首次公告日期' in title :
                        title = '首次公告日期'
                        value = table.xpath('td[@width="168"]/text()')[0]
                        key='更正日期'
                        zhongbiaoriqi_value = table.xpath('td[@width="168"]/text()')[1]
                        all_info[key]=zhongbiaoriqi_value

                    if '本项目招标公告日期中标日期' in title :
                        title = '本项目招标公告日期'
                        value = table.xpath('td[@width="168"]/text()')[0]
                        zhongbiaoriqi_key = '中标日期'
                        zhongbiaoriqi_value = table.xpath('td[@width="168"]/text()')[1]
                        all_info[zhongbiaoriqi_key]=zhongbiaoriqi_value
                        #print('中标日期'+zhongbiaoriqi_value)
                    if '本项目招标公告日期成交日期' in title:
                        title = '本项目招标公告日期'
                        value = table.xpath('td[@width="168"]/text()')[0]
                        zhongbiaoriqi_key = '中标日期'
                        zhongbiaoriqi_value = ''.join(table.xpath('td[@width="168"]/text()'))[11:]
                        #print('zhongbiaoriqi_value:'+zhongbiaoriqi_value)
                        all_info[zhongbiaoriqi_key] = zhongbiaoriqi_value
                    all_info[title] = value
                    all_info['爬取时间']= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(e.args)
            return False
        else:
            return all_info


    def start_getInfo(self,url):
        html = self.get_detail_page(url)
        html = etree.HTML(html)
        print(threading.active_count())
        #print(threading.enumerate())
        all_info = self.parse_datail_page(html,url)
        if all_info!=False:
            info_list.put(all_info)
        if flag.isSet():        #当写文件线程阻塞等待时激活
            print(000)
            flag.clear()
            # cond.acquire()
            # cond.notifyAll()
            # cond.release()


        #writeCsv(text=tuple(all_info.values()))
#写入csv文件类
class SaveInfoToCsv():
    def __init__(self,queue,fileName):
        self.queue=queue
        self.fileName=fileName
        self.count=0        #记录写入个数
    def getSingleRecord(self):          #从队列中拿记录
        # if self.queue.empty() or self.queue.full():
        #     print('队列为空,写线程暂停等待')
        #     return False
        temp=self.queue.get()
        return tuple(temp.values())
    def writeCsv(self):
        count = 0
        with open(self.fileName, 'a', encoding='utf-8', newline='') as csvFile:
            writer = csv.writer(csvFile,delimiter='\t')
            while True:
                try:
                    if self.queue.empty():       #当队列为空时将写文件线程阻塞等待
                        print(555)
                        flag.set()
                        flag.wait()
                        # cond.acquire()
                        # cond.wait()
                        # cond.release()

                    writer.writerow(self.getSingleRecord())
                    count+=1
                    if count==20:
                        self.count=self.count+count
                        print('成功写入{}个'.format(self.count))
                        count=0
                except Exception as e:
                    print(e)
                    pass

if __name__ == '__main__':
    zhenfucaigouSpider = ZhenfucaigouSpider()
    cond=threading.Condition()      #设立线程条件变量
    flag=threading.Event()                      #线程阻塞标志
    info_list=Queue(0)            #设置队列大小(无穷大)
    # db = mysql.SaveToMysql(info_list)
    saveInfo = SaveInfoToCsv(queue=info_list, fileName='data.csv')
    save_thread = threading.Thread(target=saveInfo.writeCsv)
    save_thread.start()
    for i in range(1,200):
        print('正在爬取第{}页'.format(str(i)))
        html = zhenfucaigouSpider.get_page(page_index=i)
        url_list =zhenfucaigouSpider.get_all_url(html)

        '''上面已经获取到了url_list，即单个分页中的所有招标信息的url,在这里需要创建多线程对url分别进行请求解析，
            同时，每个线程将信息解析完后加入到存数据库队列之中，然后由专门的线程进行存入'''
        print(url_list)
        threads=[]
        for url in url_list:
           threads.append(threading.Thread(target=zhenfucaigouSpider.start_getInfo,args=(url,)))
        for i in range(len(url_list)):
            threads[i].start()
        for i in range(len(url_list)):
            threads[i].join()

        time.sleep(5)
        # print(666)
        # time.sleep(30)







