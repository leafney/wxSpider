# coding:utf-8

"""
Python爬虫获取微信公众号文章列表
author:xue
time:2016-7-23

Ubuntu + Python2.7.x

需要安装：

$ sudo pip install selenium
$ sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev (lxml的依赖包)
$ sudo pip install lxml
PhantomJS  (从phantomjs官网下载安装包)
"""

from urllib import quote
from selenium import webdriver
import time
from lxml import etree
import re

class weixinSpider(object):
	"""docstring for weixinSpider"""
	def __init__(self):
		# 设置selenium参数
		cap=webdriver.DesiredCapabilities.PHANTOMJS
		cap["phantomjs.page.settings.loadImages"]=False
		self.driver=webdriver.PhantomJS(desired_capabilities=cap)


	# 通过搜狗微信搜索公众号信息页面修改url参数搜索
	def getProfile(self,keyWord):
		"""
		测试发现不能通过直接请求 “http://weixin.sogou.com/weixin?type=1&query=dotNET%E8%B7%A8%E5%B9%B3%E5%8F%B0&ie=utf8” 该网页得到
		当前窗口句柄的方式，来得到
		"""

		# 通过直接网址输入参数获取
		url_kw=quote(keyWord) # 对中文unicode操作
		wx_url="http://weixin.sogou.com/weixin?type=1&query="+url_kw+"&ie=utf8"
		# print(wx_url)
		self.driver.get(wx_url)
		# 测试是否获取内容
		# html=self.driver.execute_script("return document.documentElement.outerHTML")
		# print(html.encode('utf-8'))

		now_handle=self.driver.current_window_handle
		# print(now_handle)
		# 得到第一个公众号
		self.driver.find_element_by_xpath('//*[@id="sogou_vr_11002301_box_0"]').click()
		time.sleep(5)
		# 获取所有窗口句柄
		all_handle=self.driver.window_handles

		for handle in all_handle:
			# print(handle)
			if handle != now_handle:
				# 定位到弹出的窗口句柄
				self.driver.switch_to_window(handle)		
				# 在弹出的窗口中进行操作
				print(self.driver.title)
				html=self.driver.execute_script("return document.documentElement.outerHTML")
				# print(html.encode('utf-8'))

				# 解析文章列表
				page=etree.HTML(html)
				for sel in page.xpath('//*[@id="history"]/div/div/div/div'):
					hrefs=sel.xpath('h4/@hrefs')[0]
					title=sel.xpath('h4[@class="weui_media_title"]')[0].xpath('string(.)').strip()
					desc=sel.xpath('*[@class="weui_media_desc"]/text()')[0]
					pubtime=sel.xpath('*[@class="weui_media_extra_info"]/text()')[0]
					# 将文章的临时链接转换成真实文章链接
					temp_link='http://mp.weixin.qq.com'+str(hrefs)

					print(temp_link.encode('utf-8'))
					print('真实链接如下')
					real_link=self.getRealLink(temp_link)
					print(real_link)
					print('真实链接如上')
					# print(title.encode('utf-8'))
					# print(desc.encode('utf-8'))
					# print(pubtime.encode('utf-8'))
					# print('----------------')
					break # 为了便于观察只显示第一个文章的信息


	# 获取微信文章列表数据
	# 从搜狗微信搜索首页模拟输入关键词点击按钮方式获取
	def getProfileByQuery(self,keyWord):
		# 从首页进行搜索获取
		self.driver.get('http://weixin.sogou.com/')
		# self.driver.find_element_by_id("upquery").send_keys(u"中文") # 这里要是unicode类型
		self.driver.find_element_by_id("upquery").send_keys(keyWord.decode('utf-8'))
		self.driver.find_element_by_class_name("swz2").click()
		# 输出当前页获取的内容
		# html=self.driver.execute_script("return document.documentElement.outerHTML")
		# print(html.encode('utf-8'))

		# 获取当前窗口句柄
		now_handle=self.driver.current_window_handle
		print(now_handle)
		# 点击得到结果的第一个公众号信息
		self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div/div[2]/div/div[1]').click()
		# 等待所有窗口完全打开
		time.sleep(5)
		# 获取所有窗口句柄
		all_handle=self.driver.window_handles

		for handle in all_handle:
			print(handle)
			if handle != now_handle:
				# 定位到弹出的窗口句柄
				self.driver.switch_to_window(handle)		
				# 在弹出的窗口中进行操作
				print(self.driver.title)
				# 内容
				html=self.driver.execute_script("return document.documentElement.outerHTML")
				# print(html.encode('utf-8'))

	# 通过临时链接获取文章真实链接
	def getRealLink(self,tmpLink):
		# 获取网页内容
		self.driver.get(tmpLink)
		html=self.driver.page_source
		# print(html.encode('utf-8'))
		# with open('123.html','w') as f:
		# 	f.write(html.encode('utf-8'))

		# 使用正则获取 msg_link 的值
		msg_link=re.compile(r'var msg_link = "(.+?)";')
		# http://mp.weixin.qq.com/s?__biz=MzAwNTMxMzg1MA==&amp;mid=2654067783&amp;idx=1&amp;sn=a0778a114e18f9468b5745d4f8401cda#rd
		m_link=msg_link.search(html)
		real_link=''
		if m_link:
			msgcover=m_link.group(1)
			real_link=msgcover.replace('&amp;','&')

		# print(real_link)
		return real_link


	def __del__(self):
		print('quit out')
		self.driver.quit()




if __name__ == '__main__':
	
	spider=weixinSpider()

	spider.getProfile("dotnet跨平台")

	# spider.getProfileByQuery("dotnet跨平台")