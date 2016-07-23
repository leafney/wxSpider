#coding:utf-8

"""
测试获取公众号文章列表
参考自知乎：https://www.zhihu.com/question/31285583/answer/100263061
"""

from selenium import webdriver
import time

driver = webdriver.PhantomJS()
# 请求微信首页，输入关键词，点击“搜公众号” 
driver.get('http://weixin.sogou.com/')
driver.find_element_by_id("upquery").send_keys(u"浙江旅游")
driver.find_element_by_class_name("swz2").click()
# 在这里得到当前窗口句柄
now_handle = driver.current_window_handle
print(now_handle)
driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div/div[2]/div/div[1]').click()
time.sleep(10) #等待所有窗口完全打开,10秒够用了， 不好用就判断新窗口是否完全打开 
# 获取所有窗口句柄
all_handle = driver.window_handles
for handle in all_handle:
	# print(handle)
	if handle != now_handle:
		# 在弹出的窗口中进行操作
		driver.switch_to_window(handle)

		print(u"当前网页title" + driver.title)
		# 内容
		# html=driver.execute_script("return document.documentElement.outerHTML")
		# print(html.encode('utf-8'))

# print(driver.page_content)
driver.quit()


# 关于窗口句柄实例参考：http://www.cnblogs.com/jane0912/p/4177779.html
 # https://segmentfault.com/q/1010000004846074/a-1020000005101364

 # 亲测该代码可行