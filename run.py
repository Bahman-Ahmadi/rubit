versions = open("versions.txt").read().strip().split("\n")
numricalLastVersion, lastVersion = 0,""
for v in versions:
    numricalThisVersion = int(v.replace("_",""))

    if numricalLastVersion - numricalThisVersion < 0:
        numricalLastVersion,lastVersion = numricalThisVersion,v

from os import system
system(f"python {lastVersion}/bot.py")
