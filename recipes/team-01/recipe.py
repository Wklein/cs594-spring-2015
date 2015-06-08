# '''
# Created on June 6, 2015
# 
# @author: Alex N., Laura M., and Will K.
# '''
import oauth2 as oauth
import json
import pymongo
import datetime
import sys
# 

#Variables that contains the user credentials to access Twitter API 

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

print sys.argv[1]
print sys.argv[2]
print sys.argv[3]
print sys.argv[4]

print sys.argv[5]
print sys.argv[6:]

#Access codes are retrieved from the command line.  This was useful for creating a shell script to create and run trackers
#for several keyword sets.
access_token = sys.argv[1]
access_token_secret = sys.argv[2]
consumer_key = sys.argv[3]
consumer_secret = sys.argv[4]
 
client = pymongo.MongoClient()
db = client.tweetcounts
storyName = sys.argv[5]
trackWord = sys.argv[6:]


 #This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
 
	def on_data(self, data):
	
		#"data" is a fairly large JSON string with too many fields to list here.
		#Take the console output from this print statement to find the fields you're interested in.
		print data
		
		#Individual fields can be retrieved by the following line.  json.loads(data) returns a dict created from the JSON string.
		print json.loads(data)["id"]
		
		#Inserting into mongo is simple one-liner.  
		#db.collectionName.insert({ *** Mongo document *** })
		return True
 
	def on_error(self, status):
		#The error codes can give some insight into why twitter rejected your request.
		#420 is a common error and it typically means that you're overloading your access keys.
		#It can also appear occasionally when initiating several instances of this program.  It often resolves itself in a couple of minutes.
		print "Error code : " + str(status)	
 
if __name__ == '__main__':
 
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#This line filters Twitter Streams to capture data by the keywords given on the command line.
	stream.filter(track=trackWord)








