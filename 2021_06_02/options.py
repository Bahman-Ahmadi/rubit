import selenium.webdriver
from time import sleep

class run:
	def __init__(self,driver):
		self.driver = driver


	def login(self,phone):
		self.driver.find_element_by_name("phone_number").send_keys(phone)
		self.driver.find_element_by_xpath("//span[@msgid=\"modal_next\"]").click()
		self.driver.find_element_by_xpath("//span[@rb-localize=\"modal_ok\"]").click()

		for i in range(31):
			print(f"\rplease wait {str(30-i)}” for verifcation code!",end="")
			sleep(1)
		print("\n\n")

		self.driver.find_element_by_name('phone_code').send_keys( input("enter code number: ") )
		print()

		for j in range(4):
			print(f"\rplease wait {str(3-j)}” for loading rubika!",end="")
			sleep(1)

		print("\nlogged in!")


	def send(self,msg,shouldSendWithEnter):
		field = self.driver.find_element_by_xpath('//div[@class="composer_rich_textarea"]')
		if shouldSendWithEnter:
			field.send_keys(msg+selenium.webdriver.common.keys.Keys.ENTER)
		else:
			field.send_keys(msg)
			self.driver.find_element_by_xpath('//button[@class="im_submit"]').click()


	def reply(self,message_id):
		self.driver.find_elements_by_xpath("//span[contains(@dir, 'rtl')]")[message_id].click()
		self.driver.find_element_by_xpath("//button[@rb-localize=\"message_action_reply\"]").click()


	def delete(self,message_id):
		self.driver.find_elements_by_xpath("//span[contains(@dir, 'rtl')]")[message_id].click()
		self.driver.find_element_by_xpath("//button[@rb-localize=\"message_action_delete\"]").click()
		self.driver.find_element_by_xpath("//i[@class=\"icon-checkbox-inner\"]").click()
		self.driver.find_element_by_xpath("//span[rb-localize=\"confirm_modal_messages_delete_submit\"]").click()


	def forward(self,message):
		self.driver.find_element_by_xpath("//button[@rb-localize=\"message_action_forward\"]").click()
		message.click()
		self.driver.find_element_by_xpath('//button[@class="im_submit"]').click()


	@staticmethod
	def xpather(tagInfo):
		info = {"tag": tagInfo[0], "attr": tagInfo[1], "value": tagInfo[2]}
		return f'//{info.get("tag")}[@{info.get("attr")}="{info.get("value")}"]'

	def getElementsData(self,elements_xpath):
		listWebElements = self.driver.find_elements_by_xpath(elements_xpath)
		result = []
		for webElement in listWebElements:
			result.append(webElement.text)

		return result
