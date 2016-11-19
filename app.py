## Import Slack Python API
from slacker import Slacker
import credential

## Open the database
file = open(credential.csvFile, 'r')

## Your Slack authentication code
slack = Slacker(credential.code)
memberList = slack.users.list()

# Declare lists for later
addList = []
kickList = []

## Goes through each line of the database
for line in file:
	
	## Since my database has information in the form id, first_name last_name, senator_status, etc.
	## I split it to get the name and senator status data
	dataPartition = line.split(',',3)
	namePartition = dataPartition[1].split(' ', 1)

	## Our emails are in the form of the first initial of the first name concatenated onto
	## the entire last name. This will help us identify the Slack users. This should work for most names. 
	emailCode = namePartition[0][0].lower() + namePartition[1].lower()

	# Saves the names of all people wh should be in the group
	if (dataPartition[2] == 'Y'):
		addList.append(emailCode)
		
	# Saves the names of all the people who shouldn't be in the group
	else:
		kickList.append(emailCode)		

memberList = slack.channels.info(credential.generalChannelID)
userCodesFirstSlice = memberList.raw.split("members\":[", 1)
userCodesSecondSlice = userCodesFirstSlice[1].split("]", 1)
userCodes = userCodesSecondSlice[0].split(',')

## Fetches slack userID codes and places them in a list
idList = []
for senatorID in userCodes:
	idList.append(senatorID.replace("\"",""))


for senatorID in idList:
	
	## This is horrendous and I will fix it
	userInfo = slack.users.info(senatorID)
	userInfoFirstSlice = userInfo.raw.split("\"email\":\"",1)
	userInfoSecondSlice = userInfoFirstSlice[1].split("@",1)
	userID1 = userInfoSecondSlice[0].replace("1","")
	userID2 = userID1.replace("2","")
	userID3 = userID2.replace("0","")
	userID4 = userID3.replace("9","")
	userID5 = userID4.replace("8", "")
	userID6 = userID5.replace("7","")

	## if the email is in addList, then they are added to the group
	## if the email is in kickList, then they are kicked from the group
	## We pass over errors here to avoid the program crashing if someone 
	## is already not in the group when the program tries to kick them.
	try: 
		if userID6 in addList:
			print userID6 + ' added!'
			slack.groups.invite(credential.senatorChannelID, senatorID)
		if userID6 in kickList:
			print userID6 + ' removed!'
			slack.groups.kick(credential.senatorChannelID, senatorID)
	except:
		pass

file.close()
