from selenium.webdriver import Chrome as _Chrome, ChromeOptions as _ChromeOptions
from selenium.common.exceptions import InvalidArgumentException as _InvalidArgumentException
import options, selenium
from datetime import datetime as _datetime
from os import path as _path
from bs4 import BeautifulSoup as _BeautifulSoup
from re import search as _search
from configparser import ConfigParser as _configuration

class Bot:
	def __init__(self): ...

	def _accessFile(self,filename):
		here = _path.dirname(_path.dirname(_path.abspath(__file__)))
		return _path.join(here,filename)

	settings = _configuration()
	settings.read(_accessFile(0,"settings.ini"))
	c_options = _ChromeOptions()
	options.binary_location = settings["configs"]["browser"]
	browser = _Chrome(settings["configs"]["driver"],options=c_options)
	opt = options.run(browser)

	@staticmethod
	def log(mode,line,data):
		date = str(_datetime.datetime.now()).split(' ')[0]
		time = '-'.join(str(_datetime.datetime.now()).split(' ')[1].split(':'))[:8]
		name = f"logcat_{date}-{time}.txt"
		try:
			open(Bot._accessFile(0,name),"x")
			logcat = open(name,"a+")
			logcat.write(f"		this robot logcat maked at {str(_datetime.datetime.now())}		\n\n")
		except:
			logcat = open(name,"a+")

		logcat.write(f"#{mode} - {str(_datetime.datetime.now())} - in line{str(line)}: {data}\n")

	@staticmethod
	def login(**settings):
		c_options.add_argument('user-data-dir=selenium')
		try:
			Bot.browser = _Chrome(options=c_options, **settings)
		except _InvalidArgumentException:
			raise Exception("another window(s) is running, you should first close that(s).")
		else:
			Bot.browser.get("https://web.rubika.ir")
			Bot.browser.implicitly_wait(1)

		while True:
			try:
				Bot.opt.login(Bot.settings["configs"]["phone"])
				break
			except:
				continue

	@staticmethod
	def runCommands():
		def findCommands():
			messages = []
			try:
				messages = Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["div","dir","rtl"])) + Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["div","dir","ltr"]))
			except Exception as e:
				if type(e) == selenium.common.exceptions.StaleElementReferenceException or type(e) == selenium.common.exceptions.NoSuchElementException:
					try:
						messages = Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["div","dir","rtl"]))
					except Exception as ee:
						if type(ee) == selenium.common.exceptions.StaleElementReferenceException or type(ee) == selenium.common.exceptions.NoSuchElementException:
							try:
								messages = Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["div","dir","ltr"]))
							except Exception as eee :
								if type(eee) == selenium.common.exceptions.StaleElementReferenceException or type(eee) == selenium.common.exceptions.NoSuchElementException :
									messages = []
			return messages

		Messages = findCommands()
		conditions, commands = list(Bot.settings["callbacks"].keys()), list(Bot.settings["callbacks"].values())

		while True:
			for message in Messages:
				if str(message.text) in conditions and str(message) != "else":
					exec(commands[conditions.index(str(message))])
				elif not str(message) in conditions:
					exec(commands[conditions.index("else")])

			# getting updates
			oldMessages = Messages
			Messages = findCommands()

			# don’t reaction to old messages
			while True:
				Bot.browser.refresh()
				Messages = findCommands()
				if len(Messages) != len(oldMessages):
					break

	@staticmethod
	def messages(messagesElements=None):
		def _find(element, dataList):
			return str(_BeautifulSoup(element,"html.parser").find(dataList[0], {dataList[1], dataList[2]}).text)

		if messagesElements == None:
			messages = Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["div","class","clearfix"]))
		else:
			messages = messagesElements

		for message in messages:
			result = {"from":{},"reply":{}}
			result["element"] = message
			result["time"] = _find(message.text,["span","class","im_message_date_text"])
			result["from"]["name"] = _find(message.text,["a","class","im_message_author"])
			try: result["text"] = _find(message.text,["div","dir","rtl"])
			except: result["text"] = _find(message.text,["div","dir","ltr"])
			try:
				result["reply"]["to"] = _search("<span>.+</span>", Bot.browser.find_elements_by_class_name("im_message_reply")[messages.index(message)].text).group()[6:-7]
				try: result["reply"]["text"] = _search("dir=\"rtl\">.+</span>", Bot.browser.find_elements_by_class_name("im_message_reply_body")[messages.index(message)].text).group()[10:-21]
				except: result["reply"]["text"] = _search("dir=\"ltr\">.+</span>", Bot.browser.find_elements_by_class_name("im_message_reply_body")[messages.index(message)].text).group()[10:-21]
			except AttributeError: ...
				
			#find sender inforamtions
			source = Bot.browser.page_source()
			Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["a","class","im_message_author"]))[messages.index(message)].click()
			result["from"]["status"]= _find(source,["p","class","mobile_user_modal_status"])		
			try:
				result["from"]["username"] = _find(_BeautifulSoup(source,"html.parser").find_all("div", {"class","mobile_modal_section_value"})[0],["div","class","mobile_modal_section_value"])
				result["from"]["biography"] = _find(_BeautifulSoup(source,"html.parser").find_all("div", {"class","mobile_modal_section_value"})[1],["div","class","mobile_modal_section_value"])
			except:
				result["from"]["username"] = None
				result["from"]["biography"] = None

			Bot.browser.find_element_by_class_name("icon-back").click()
			
	@staticmethod
	def screenshot():
		path = _path.dirname(_path.dirname(_path.abspath(__file__)))
		Bot.browser.get_screenshot_as_png()
		print(f"screen shot saved in {path}")

	@staticmethod
	def back(): Bot.browser.find_element_by_class_name("icon-back").click()


if __name__ == '__main__':
	print("Rubika Library 1.0.0\nfor help follow http://rubit.ir/1.0.0")
	bot = Bot()
	bot.login()
	bot.opt.goto(Bot.settings["configs"]["chat"])
	bot.runCommands()

else:
	print("Rubika Library 1.0.0\nfor help follow http://rubit.ir/1.0.0")
