from selenium.webdriver import Chrome as _Chrome, ChromeOptions as _ChromeOptions
from selenium.common.exceptions import InvalidArgumentException as _InvalidArgumentException
import options as _options
from datetime import datetime as _datetime
from os import path as _path
from bs4 import BeautifulSoup as _BeautifulSoup


class Bot:
	def _accessFile(self,filename):
		_here = _path.dirname(_path.dirname(_path.abspath(__file__)))
		return _path.join(_here,filename)

	configs = list(map(lambda x:x.split("="),open(_accessFile(0,"config.txt")).read().strip().split("\n")))
	configKeys = [m[0] for m in configs]
	configValues = [n[1] for n in configs]
	conditions = [j.split("->")[0] for j in open(_accessFile(0,"callback.txt")).read().strip().split("\n")]
	codes = [k.split("->")[1] for k in open(_accessFile(0,"callback.txt")).read().strip().split("\n")]
	browser = _Chrome(configValues[configKeys.index("driver")])
	opt = _options.run(browser)

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
		options = _ChromeOptions()
		options.add_argument('user-data-dir=selenium')
		try: Bot.browser = _Chrome(options=options, **settings)
		except _InvalidArgumentException: raise Exception("another window(s) is running, you should first close that(s).")
		else:
			Bot.browser.get("https://web.rubika.ir")
			Bot.browser.implicitly_wait(1)

		while True:
			try:
				Bot.opt.login(Bot.configValues[Bot.configKeys.index("phone")])
				break
			except:
				continue

	@staticmethod
	def runCommands():
		messages = Bot.opt.getElementsData(Bot.opt.xpather(["div","dir","rtl"]))

		while True:
			for message in messages:
				if message in Bot.conditions and message != "else":
					exec(Bot.codes(Bot.conditions.index(message)))
					Bot.opt.send("test is vaild!",Bot.configValues[Bot.configKeys.index("send_by_enter")])
				elif not message in Bot.conditions:
						exec(Bot.codes(Bot.conditions.index("else")))

			# getting updates
			#  Bot.opt.send("get updates...",bool(int(Bot.configValues[Bot.configKeys.index("send_by_enter")])))
			oldMessages = messages
			messages = Bot.opt.getElementsData(Bot.opt.xpather(["div","dir","rtl"]))

			# don’t reaction to old messages
			while True:
				Bot.browser.refresh()
				messages = Bot.opt.getElementsData(Bot.opt.xpather(["div","dir","rtl"]))
				if len(messages) != len(oldMessages):
					break

	@staticmethod
	def API():
		def find(element, dataList):
			return _BeautifulSoup(element,"html.parser").find(dataList[0], {dataList[1], dataList[2]}).text
		
		messages = Bot.browser.find_elements_by_xpath(Bot.opt.xpather(["div","class","clearfix"]))
		for message in messages:
			date = find(message,["span","class","im_message_date_text"])
			author = find(message,["a","class","im_message_author"])
			text = find(message,["div","dir","rtl"])
			
		

if __name__ == '__main__':
	print("Rubit Library 1.0.0\nfor help follow http://ru-bit.ir/last")
	bot = Bot()
	bot.login()
	bot.opt.goto(Bot.configValues[Bot.configKeys.index("chat")])
	bot.runCommands()

else:
	print("Rubit Library 1.0.0\nfor help follow http://ru-bit.ir/last")