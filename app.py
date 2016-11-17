## Import Slack Python API
from slacker import Slacker
import credential

## Open the database
file = open(credential.csvFile, 'r')

## Your Slack authentication code
slack = Slacker(credential.code)
memberList = slack.users.list()

print memberList.body	


## Goes through each line of the database
for line in file:
	
	## Since my database has information in the form id, first_name last_name, senator_status, etc.
	## I split it to get the name and senator status data
	dataPartition = line.split(',',3)
	namePartition = dataPartition[1].split(' ', 1)

	## Our emails are in the form of the first initial of the first name concatenated onto
	## the entire last name. This will help us identify the Slack users. This should work for most names. 
	emailCode = namePartition[0][0].lower() + namePartition[1].lower()



	#if (dataPartition[2] == 'Y'):
		#memberList = slack.channels.info(credential.generalChannelID)
		#Slack API Code (Add to group) 
	#else:
		#senatorList = slack.groups.info(credential.senatorChannelID)
		#Slack API Code (Remove from group)

file.close()


#https://api.slack.com/methods/groups.list/test