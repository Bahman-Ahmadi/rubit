from subprocess import getoutput

versions = [i for i in getoutput("ls").split("\n") if "_" in i]
numricalLastVersion, lastVersion = 0,""
for v in versions:
    numricalThisVersion = int(v.replace("_",""))

    if numricalLastVersion - numricalThisVersion < 0:
        numricalLastVersion,lastVersion = numricalThisVersion,v

from os import system
system(f"python {lastVersion}/bot.py")
