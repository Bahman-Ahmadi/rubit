import selenium.webdriver, options, datetime

# VARIABLES
configs = list(map(lambda x:x.split("="),open("config.txt").read().strip().split("\n")))
configKeys,configValues = [i[0] for i in configs],[i[1] for i in configs]
name = f"logcat_{str(datetime.datetime.now()).split(' ')[0]}-{'-'.join(str(datetime.datetime.now()).split(' ')[1].split(':'))[:8]}.txt"
try:
	open(name,"x")
	logcat = open(name,"a+")
except:
	logcat = open(name,"a+")

def log(mode,line,data):
	logcat.write(f"#{mode} - {str(datetime.datetime.now())} - in line{str(line)}: {data}\n")

logcat.write(f"		this robot logcat maked at {str(datetime.datetime.now())}		\n\n")
browser = selenium.webdriver.Chrome(configValues[configKeys.index("driver")])
opt = options.run(browser)
log("OK", 20, "browser opened successful.")

# LOGIN
browser.get("https://web.rubika.ir")
while 1:
	try:
		opt.login(configValues[configKeys.index("phone")])
		break
	except:
		continue

log("OK",31,"successfully logged in")

# FIND & GO TO CHAT
chats = browser.find_elements_by_xpath(opt.xpather(["span","verified","true"]))
log("OK",35,"chats was defind. i’m searching for ChatRoom.")


for chatRoom in chats:
	if chatRoom.text == configValues[configKeys.index("chat")]:
		chats[chats.index(chatRoom)].click()
		break

log("OK",43,"Good!! ChatRoom was defind :)")

# FIND & EXEC COMMANDS
messages = opt.getElementsData(opt.xpather(["div","dir","ltr"]))
conditions, codes = [j.split("->")[0] for j in open("callback.txt").read().strip().split("\n")], [m.split("->")[1] for m in open("callback.txt").read().strip().split("\n")]
for message in messages: print(message)
log("OK",48,"ChatRoom’s messages was saved. let's executing thats!")
while 1:
	print("i’m in the while loop")
	for message in messages:
		print("i’m in the message foreach loop")
		if message in conditions and message != "else": exec(codes[conditions.index(message)])
		else: exec(codes[conditions.index("else")])
	print("message loop ended")
	log("OK",57,"ChatRoom’s messages executed!")

	# getting updates
	opt.send("get updates...",bool(int(configValues[configKeys.index("send_by_enter")])))
	oldMessages = messages
	messages = opt.getElementsData(opt.xpather(["div","dir","ltr"]))

	# don’t reaction to old messages
	retries = 0
	while 1:
		print(f"\rretry for {retries} time(s) for getting new messages.",end="")
		retries += 1

		messages = opt.getElementsData(opt.xpather(["div","dir","ltr"]))
		if len(messages) != len(oldMessages): break

	print("\nnew messages was sent, i’m going to executing that")
