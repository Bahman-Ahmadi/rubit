import selenium.webdriver
from time import sleep


class run:
	def __init__(self,driver):
		self.driver = driver


	def login(self,phone):
		try:
			self.driver.find_element_by_name("phone_number").clear()
			self.driver.find_element_by_name("phone_number").send_keys(phone)
			self.driver.find_element_by_xpath(run.xpather(["span","msgid","modal_next"])).click()
			self.driver.find_element_by_xpath(run.xpather(["span","rb-localize","modal_ok"])).click()
			for i in range(31):
				print(f"\rplease wait {str(30-i)}” for verifcation code!",end="")
				sleep(1)
			print("\n\n")
			self.driver.find_element_by_name('phone_code').send_keys(input("enter code number: "))
			print()
			for j in range(4):
				print(f"\rplease wait {str(3-j)}” for loading rubika!",end="")
				sleep(1)
		except Exception:
			print("please login your account")


	def goto(self, title):
		chats = self.driver.find_elements_by_xpath(run.xpather(["span","verified","true"]))
		if title in chats: chats[chats.index(title)].click()
		else: raise IndexError(f"Bot not found any chatRoom by title: {title}")


	def send(self, text):
		field = self.driver.find_element_by_xpath(run.xpather(["div","class","composer_rich_textarea"]))
		field.send_keys(text+selenium.webdriver.common.keys.Keys.ENTER)

	def reply(self, message):
		message.click()
		self.driver.find_element_by_xpath(run.xpather(["a","rb-localize","im_reply"])).click()


	def delete(self, message):
		message.click()
		self.driver.find_element_by_xpath(run.xpather(["a","rb-localize","im_delete"])).click()
		self.driver.find_element_by_xpath(run.xpather(["i","class","icon-checkbox-inner"])).click()
		self.driver.find_element_by_xpath(run.xpather(["span","rb-localize","confirm_modal_messages_delete_submit"])).click()


	def forward(self, message, to):
		message.click()
		self.driver.find_element_by_xpath(run.xpather(["a","rb-localize","im_forward"])).click()
		self.driver.find_element_by_xpath(run.xpather(["button","class","im_submit"])).click()
		chats = self.driver.find_elements_by_xpath(run.xpather(["span","verified","true"]))
		if to in chats: chats[chats.index(to)].click()
		else: raise IndexError(f"Bot not found any chatRoom by title: {to}")
		self.driver.find_element_by_xpath(run.xpather(["div","class","composer_rich_textarea"])).send_keys(selenium.webdriver.common.keys.Keys.ENTER)


	def search(self, query):
		self.driver.find_element_by_class_name("navbar-search-wrap").click()
		self.driver.find_element_by_class_name("im_dialogs_search_field").send_keys(query)
		sleep(3)
		return zip([i.text for i in self.driver.find_elements_by_class_name("im_dialog_user")],[j.text for j in self.driver.find_elements_by_class_name("im_dialog_message_text")])


	def cancelSearch(self):
		self.driver.find_element_by_class_name("icon-search-clear").click()


	@staticmethod
	def xpather(tagInfo):
		info = {"tag": tagInfo[0], "attr": tagInfo[1], "value": tagInfo[2]}
		return f'//{info.get("tag")}[@{info.get("attr")}="{info.get("value")}"]'

	def getElementsData(self,elementsXpath):
		listWebElements = self.driver.find_elements_by_xpath(elementsXpath)
		result = []
		for webElement in listWebElements:
			result.append(webElement.text)
		return result


class new(run):
	def __init__(self):
		self.driver.find_element_by_class_name("dropdown-toggle").click()

	def group(self, contact, name):
		self.driver.find_element_by_xpath(self.xpather(["a","rb-localize","head_new_group"]))
		contacts = self.driver.find_element_by_class_name("contacts_modal_contact_name")
		contacts[contacts.index(contact)].click()
		self.driver.find_element_by_xpath(self.xpather(["a","rb-localize","modal_next"]))
		self.driver.find_element_by_class_name("md-input").send_keys(name)
		self.driver.find_element_by_class_name("btn").click()
		sleep(3)
		self.driver.get("https://web.rubika.ir")

	def channel(self, name):
		self.driver.find_element_by_xpath(self.xpather(["a","rb-localize","im_new_channel"]))
		self.driver.find_element_by_xpath(self.xpather(["a","rb-localize","modal_next"]))
		self.driver.find_element_by_class_name("md-input").send_keys(name)
		self.driver.find_element_by_class_name("btn").click()
		sleep(3)
		try:
			self.driver.find_element_by_class_name("md_simple_modal_footer")
			raise Exception("unable to make channel. please enable two-steps verification and then try again.")
		except selenium.common.exceptions.NoSuchElementException: ...
		self.driver.get("https://web.rubika.ir")

	def contact(self, phone, firstName, lastName):
		self.driver.find_element_by_xpath(self.xpather(["a","rb-localize","head_new_contact"]))
		if type(phone) == str and phone.startswith("09") and len(phone) == 11:
			self.driver.find_element_by_name("phone").send_keys(phone)
			self.driver.find_element_by_name("first_name").send_keys(firstName)
			self.driver.find_element_by_name("last_name").send_keys(lastName)
			self.driver.find_element_by_class_name("btn").click()
			sleep(3)
			self.driver.get("https://web.rubika.ir")
		else:
			raise TypeError("phone number is not true! enter that like: 09XXXXXXXXX in a string")


class settings(run):
	def __init__(self):
		self.driver.find_element_by_class_name("dropdown-toggle").click()
		self.driver.find_element_by_xpath(run.xpather(["a","rb-localize","head_settings"])).click()

	def getMe(self):
		from bs4 import BeautifulSoup
		from requests import get
		page = BeautifulSoup(get("https://rubika.ir/"+self.driver.find_element_by_class_name("settings_modal_username_link").text[1:]).text,"html.parser")
		def find(tag,attr): return page.find(tag,{"class":attr})
		name = find("div","rlp-content-caption-wrap").text.strip()
		bio = find("span","rlp-content-info").text
		fallowers = find("span","rlp-content-peer number-persian").text
		avatar = page.find("img",attrs={"class":"profile-img"})["src"]
		return {"name":name,"bio":bio,"fallowers":fallowers,"avatar":avatar}
		
	def setName(self,firstName,lastName):
		if firstName != "":
			self.driver.find_element_by_class_name("icon-bar").click()
			self.driver.find_element_by_xpath(run.xpather(["a","rb-localize","settings_modal_edit_profile"]))
			self.driver.find_element_by_name("first_name").clear()
			self.driver.find_element_by_name("first_name").send_keys(firstName)
			self.driver.find_element_by_name("last_name").clear()
			self.driver.find_element_by_name("last_name").send_keys(lastName)
			self.driver.find_element_by_xpath(run.xpather(["a","ng-disabled","updating"])).click()
			self.driver.find_element_by_class_name("icon-back").click()
			self.driver.find_element_by_class_name("icon-back").click()
		else:
			self.driver.find_element_by_class_name("icon-back").click()
			raise AttributeError("firstName argument can't be an empty string")

	def setBio(self,phone,text):
		self.driver.get("https://m.rubika.ir")
		self.driver.find_element_by_id("mobile").send_keys(phone)
		self.driver.find_element_by_xpath(run.xpather(["button","type","submit"])).click()
		self.driver.find_element_by_id("code").send_keys(input(">>> code: "))
		sleep(3)
		self.driver.find_element_by_id("Capa_1").click()
		self.driver.find_element_by_xpath(run.xpather(["svg","xmlns","http://www.w3.org/2000/svg"])).click()
		self.driver.find_element_by_class_name("al-center").click()
		self.driver.find_element_by_id("bio").clear()
		self.driver.find_element_by_id("bio").send_keys(text)
		self.driver.find_element_by_id("Capa_1").click()
		self.driver.get("https://web.rubika.ir")


	def setUsername(self,username):
		if not "@" in username and username.endswith("_bot"):
			self.driver.find_element_by_xpath(run.xpather(["a","rb-localize","settings_modal_edit_username"])).click()
			self.driver.find_element_by_name("username").clear()
			self.driver.find_element_by_name("username").send_keys(username)
			self.driver.find_element_by_class_name("icon-back").click()
			self.driver.find_element_by_class_name("icon-back").click()
		else:
			self.driver.find_element_by_class_name("icon-back").click()
			raise AttributeError("'@' can't be in username argument and username should be endswith '_bot' and len of that should be more of 7 characters")


class user(run):
	def __init__(self, ID):
		self.ID = ID

	def getInfo(self):
		from bs4 import BeautifulSoup
		from requests import get
		page = BeautifulSoup(get("https://rubika.ir/"+self.ID).text,"html.parser")
		def find(tag,attr): return page.find(tag,{"class":attr})
		name = find("div","rlp-content-caption-wrap").text.strip()
		bio = find("span","rlp-content-info").text
		fallowers = find("span","rlp-content-peer number-persian").text
		avatar = page.find("img",attrs={"class":"profile-img"})["src"]
		return {"name":name,"bio":bio,"fallowers":fallowers,"avatar":avatar}

	def downloadAvatar(self, path):
		from bs4 import BeautifulSoup
		from requests import get
		page = BeautifulSoup(get("https://rubika.ir/"+self.ID).text,"html.parser")
		avatar = page.find("img",attrs={"class":"profile-img"})["src"]
		with open(f"{path}/{self.ID}.jpg","wb") as file:
			file.write(get(avatar).content)