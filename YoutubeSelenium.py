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
import urllib3, requests


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
	IP_SERVEUR = ""

	
	def __init__(self):
		self.HOSTNAME = socket.gethostname()
		self.YOUTUBE_VIDEO_URL = str(sys.argv[2])
		duree = str(sys.argv[3])
#		self.IP_SERVEUR = str(sys.argv[4])
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
		elif sys.argv[1] == 'quic':
			self.testChromeQUIC()
		else:
			print('Paramètres incorrectes')
			exit() 
#		self.sendData()


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


		

		#test speed
		video = driver.find_element_by_tag_name("video")
		js = "return arguments[0].playbackRate = 1;"	#set playbackrate
		driver.execute_script(js,video)		# to execute javascript


		driver.find_element_by_xpath("//*[text()[contains(.,'Stats for')]]").click()
		while actualDuration < self.DURATION:

			js = "return arguments[0].duration;"	#set playbackrate
			videoDuration = driver.execute_script(js,video)		# duration of the video
			if actualDuration >= videoDuration:
				break


			ts = time.time()
			timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
			idVideo = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(1) > span:nth-child(2)").text  
			droppedFrames = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(19) > span:nth-child(2)").text		
			buffer = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(16) > span:nth-child(2) > span:nth-child(2)").text
			speed = driver.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(15) > span:nth-child(2) > span:nth-child(2)").text
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


	def testChromeQUIC(self):
			options = webdriver.ChromeOptions()
#			options.add_argument('headless')
#			options.add_argument('disable-gpu')
			options.add_argument('ignore-certificate-errors')
			options.add_argument('--proxy-server='+self.ADDRESS_PROXY_MITM+':'+self.PORT_PROXY_MITM)
			options.add_argument('--no-sandbox')
			options.add_argument('--enable-quic')
#			options.add_argument('window-size=1200x600')
#			options.add_argument('--dump-dom')
			driver = webdriver.Chrome(chrome_options=options)
			driver.get(self.YOUTUBE_VIDEO_URL)
			actionChains = ActionChains(driver)
			elementToRightClick = driver.find_element_by_id("movie_player")
			actionChains.context_click(elementToRightClick).perform()
			self.getYoutubeStats(driver)
			driver.quit()


#	def sendData(self):
#			http = urllib3.PoolManager()
#			request = http.request('POST',self.IP_SERVEUR)
#			request.add_header('Content-Type','application/json')
#			rep = http.urlopen(request, json.dumps(self.JSONARRAY))
#			print(rep)
#			response = requests.get(self.IP_SERVEUR, self.JSONARRAY)
#			print('ok')
#			print(response)

youtubeSel = YoutubeSelenium()
youtubeSel.launchTest()
