#pylint:disable=W0702
import selenium.webdriver, options as Opt, datetime

# VARIABLES
name = f"logcat_{str(datetime.datetime.now()).split(' ')[0]}-{'-'.join(str(datetime.datetime.now()).split(' ')[1].split(':'))[:8]}.txt"
try:
	open(name,"x")
	logcat = open(name,"a+")
except:
	logcat = open(name,"a+")

def log(mode,line,data):
	logcat.write(f"#{mode} - {str(datetime.datetime.now())} - in line{str(line)}: {data}\n")

logcat.write(f"		this robot logcat maked at {str(datetime.datetime.now())}		\n\n")
browser = selenium.webdriver.Chrome()
opt = Opt.run(browser)
log("OK", 18, "browser opened successful.")

# LOGIN
browser.get("https://web.rubika.ir")
while 1:
	try:
		opt.login("9944331890")
		break
	except:
		continue

log("OK",29,"successfully logged in")

# FIND & GO TO CHAT
chats = browser.find_elements_by_xpath(opt.xpather(["span","verified","true"]))
log("OK",33,"chats was defind. i’m searching for discord group.")


for chatRoom in chats:
	if chatRoom.text == "Discord":
		chats[chats.index(chatRoom)].click()
		break

log("OK",41,"Good!! discord was defind :)")

# FIND & EXEC COMMANDS
messages = opt.getElementsData(opt.xpather(["div","dir","rtl"]))
for message in messages: print(message)
log("OK",46,"discord’s messages was saved. let's executing thats!")
while 1:
	print("i’m in the while loop")
	for message in messages:
		print("i’m in the message foreach loop")
		if message == "sayHello":
			print("message is (sayHello)")
			opt.send("hello",True)
		else:
			print(f"message is: ({message})")
			opt.send(f"'{message}' is not an executable command!",True)
	print("message loop ended")
	log("OK",58,"discord’s messages executed!")

	# getting updates
	opt.send("get updates...",True)
	oldMessages = messages
	messages = opt.getElementsData(opt.xpather(["div","dir","ltr"]))

	# don’t reaction to old messages
	retrys = 0
	while 1:
		print(f"\rretry for {retrys} time(s) for getting new messages.",end="")
		retrys += 1

		messages = opt.getElementsData(opt.xpather(["div","dir","ltr"]))
		if len(messages) != len(oldMessages): break

	print("\nnew messages was sent, i’m going to executing that")
