#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
from selenium.webdriver import ActionChains
from selenium import webdriver
from configobj import ConfigObj
from psutil import virtual_memory
import time, datetime
import pyautogui, sys
import json
import os
import socket


class YoutubeSelenium:

	FIREFOX_PATH_PROFILE = "/home/mohammed/.mozilla/firefox/yvo73q2n.default"
	ADDRESS_PROXY_MITM = "proxy.rd.francetelecom.fr"
	YOUTUBE_API_KEY = ""
	PORT_PROXY_MITM = 8080
	DURATION = 0
	YOUTUBE_VIDEO_URL = ""
	YOUTUBE_URL = "https://www.youtube.com/watch?v="
	HOSTNAME = None
	JSONARRAY = []

	
	def __init__(self):
		self.HOSTNAME = socket.gethostname()
		self.YOUTUBE_VIDEO_URL = str(sys.argv[2])
		duree = str(sys.argv[3])
		try:
			self.DURATION = float(duree)
		except Exception as e:
			print("La durée de la vidéo est incorrecte")
		self.readConfigFile()



	def launchTest(self):
		if len(sys.argv) != 4:
			print('Nombre de parametres insuffisant')
			exit()

		if sys.argv[1] == 'firefox':
			self.testFirefox()
		elif sys.argv[1] == 'chrome':
			self.testChrome()
		else:
			print('Paramètres incorrectes')
			exit() 


	def readConfigFile(self):
		config = ConfigObj('config.properties')
		if config['ADDRESS_PROXY_MITM'] != "":
			self.ADDRESS_PROXY_MITM = config['ADDRESS_PROXY_MITM']
		if config['PORT_PROXY_MITM'] != "":
			self.PORT_PROXY_MITM = config['PORT_PROXY_MITM']
		if config['FIREFOX_PATH_PROFILE'] != "":
			self.FIREFOX_PATH_PROFILE = config['FIREFOX_PATH_PROFILE']
		if config['YOUTUBE_API_KEY'] != "":
			self.YOUTUBE_API_KEY = config['YOUTUBE_API_KEY']


	def getYoutubeStats(self,driver):
		actualDuration = 0

		driver.find_element_by_xpath("//*[text()[contains(.,'Stats for')]]").click()
		while actualDuration < self.DURATION:
			ts = time.time()
			timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
			idVideo = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(1) > span:nth-child(2)").text  
			droppedFrames = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(18) > span:nth-child(2)").text		
			buffer = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(15) > span:nth-child(2) > span:nth-child(2)").text
			speed = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(14) > span:nth-child(2) > span:nth-child(2)").text
			mem = virtual_memory()
			memFree = mem.free			#get free memory

			video = driver.find_element_by_tag_name("video")

			js = "return arguments[0].currentTime;"
			actualDuration = driver.execute_script(js,video)		# to execute javascript
			if self.YOUTUBE_VIDEO_URL == self.YOUTUBE_URL+idVideo:
				data = json.dumps({'time':timestamp,
									'hostname':self.HOSTNAME,
									'idVideo' : idVideo,
									'speed' : speed,
									'buff' : buffer,
									'droppedF': droppedFrames,
									'freeMem' : memFree})
				self.JSONARRAY.append(data)
			else:
				if driver.find_element_by_xpath("//*[text()[contains(.,'Skip Ad')]]").size() != 0 :
					driver.find_element_by_xpath("//*[text()[contains(.,'Skip Ad')]]").click()

		print(self.JSONARRAY)		


	def testFirefox(self):
			#add an ssl exception to Firefox
			profile = webdriver.FirefoxProfile()
			profile.default_preferences["webdriver_assume_untrusted_issuer"] = 'false'
			
			#set proxy
			profile.set_preference("network.proxy.type", 1)
			profile.set_preference("network.proxy.http", self.ADDRESS_PROXY_MITM)
			profile.set_preference("network.proxy.http_port", int(self.PORT_PROXY_MITM))
			profile.set_preference("network.proxy.ssl", self.ADDRESS_PROXY_MITM)
			profile.set_preference("network.proxy.ssl_port", int(self.PORT_PROXY_MITM))

			profile.update_preferences()
			driver = webdriver.Firefox(profile)
			driver.get(self.YOUTUBE_VIDEO_URL)

			elementToRightClick = driver.find_element_by_css_selector(".ytp-fullscreen-button");
		
			x = elementToRightClick.location['x']
			y = elementToRightClick.location['y']
			pyautogui.moveTo(x,y)
			pyautogui.dragTo(x, y, button='right')

			self.getYoutubeStats(driver)
			driver.quit()


	def testChrome(self):
			options = webdriver.ChromeOptions()
#			options.add_argument('headless')
#			options.add_argument('disable-gpu')
			options.add_argument('ignore-certificate-errors')
			options.add_argument('--proxy-server='+self.ADDRESS_PROXY_MITM+':'+self.PORT_PROXY_MITM)
			options.add_argument('--no-sandbox')
#			options.add_argument('window-size=1200x600')
#			options.add_argument('--dump-dom')
			driver = webdriver.Chrome(chrome_options=options)
			driver.get(self.YOUTUBE_VIDEO_URL)
			actionChains = ActionChains(driver)
			elementToRightClick = driver.find_element_by_id("movie_player")
			actionChains.context_click(elementToRightClick).perform()
			self.getYoutubeStats(driver)
			driver.quit()



youtubeSel = YoutubeSelenium()
youtubeSel.launchTest()