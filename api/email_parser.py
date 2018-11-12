import pandas as pd
import random
from apiApp.models import Player, TargetRel

def makeUsers():
	emails = pd.read_csv("emails.csv")
	cleanedEmails = []
	for ex in emails["email"]:
		string = ex
		cleanedEmails.append(string[string.find("<")+1:string.find(">")])
	cleanedEmails = cleanedEmails
	for email in cleanedEmails:
		email = email.lower()
	users = list(cleanedEmails)
	random.shuffle(users)

	notPlaying = [["barron", "alexandra"],
	["bussgang", "jonah"],
	["carlson", "amelia"],
	["chung", "malia"],
	["cole", "matis"],
	["delano", "cori"],
	["heyburn", "caroline"],
	["lachenauer", "sophia"],
	["marshall", "daisy"],
	["perry-friedman", "henry"],
	["sams", "nyla"],
	["solter", "theodore"],
	["tarraza", "deanna"],
	["moremen", "charlotte"],
	["michael", "george"],
	["chung", "asia"]]
	total = len(notPlaying)
	oldLen = len(users)
	complete = 0
	badIndexs = []
	for user in users:
		for na in notPlaying:
			if na[0] in user:
				if na[1] in user:
					badIndexs.append(users.index(user))
					complete+=1
				

	users = [i for j, i in enumerate(users) if j not in badIndexs]

	print "Eval:",
	print total
	print complete
	print oldLen-len(users)

	print users

	for user in users:
		newUser = Player(email=user)
		newUser.initPull()
		newUser.save()
		if users.index(user) == 0 or users.index(user) == len(users)-1:
			if users.index(user) == len(users)-1:

				userBefore = Player.objects.get(email=users[users.index(user)-1])
				tarRel = TargetRel(tagger=userBefore,target=newUser)
				tarRel.save()

				print "on the last"
				userBefore = Player.objects.get(email=users[0])
				tarRel = TargetRel(tagger=newUser,target=userBefore)
				tarRel.save()

		else:
			userBefore = Player.objects.get(email=users[users.index(user)-1])
			tarRel = TargetRel(tagger=userBefore,target=newUser)
			tarRel.save()
[]
