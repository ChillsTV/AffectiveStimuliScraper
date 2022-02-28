
import os
import sys
import time
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import numpy as np
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import deque
from tkinter import *

window=Tk()
sourcevar = StringVar()
writevar = StringVar()
devKey = StringVar()
seedKey = StringVar()
keywordsString = StringVar()
levelSet = IntVar()
scrapeThresholdSet = StringVar()

# DEVELOPER_KEY = "AIzaSyCfvuQuwTtkNszQ60xO7lI2PbLXp2XDU5M"
DEVELOPER_KEY = "xxxx"
wordlist_english = ["frisson", "chill", "gooseflesh", "goosebump"]
writeToFile = False
seed_vid = "J7GY1Xg6X20" #Charlie Chaplin video
level = 0
stimulationFactor = 10

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secrets.json"


s_result= {"positive":0,"negative":0,"neutral":0,"count":0} 


global writer,ofile

commentbot = SentimentIntensityAnalyzer()

def guiLabels(win):
	mainLBL = Label(win, text='Affective Stimuli Scraper')
	mainLBL.place(x=400,y=20,anchor = 'center')
	mainLBL.config(font=("Calibri", 24))

	sourceLBL = Label(win, text='Select Source for Scraping')
	sourceLBL.place(x=250,y=60,anchor = 'center')	

	developerKeyLBL = Label(win, text='Enter Developer Key')
	developerKeyLBL.place(x=300,y=120,anchor = 'center')	

	fileWriteLBL = Label(win, text='Write to a CSV File?')
	fileWriteLBL.place(x=300,y=180,anchor = 'center')	

	parameterLBL = Label(win, text='Parameters')
	parameterLBL.config(font=("Calibri", 20))
	parameterLBL.place(x=400,y=250,anchor = 'center')

	seedLBL = Label(win, text='Enter Seed Key')
	seedLBL.place(x=100,y=300,anchor = 'center')

	levelLBL = Label(win, text='Select Depth of Search')
	levelLBL.place(x=500,y=300,anchor = 'center')

	keywordsLBL = Label(win, text='KeyWords')
	keywordsLBL.config(font=("Calibri", 20))
	keywordsLBL.place(x=400,y=370,anchor = 'center')

	keysLBL = Label(win, text='Enter keywords to search for, separated by commas:')
	keysLBL.place(x=250,y=420,anchor = 'center')

	scrapeLBL = Label(win, text='Enter threshold of hit count for reporting (number>0):')
	scrapeLBL.place(x=250,y=460,anchor = 'center')
	# filtersLBL = Label(win, text='Filters')
	# filtersLBL.config(font=("Calibri", 20))
	# filtersLBL.place(x=400,y=470,anchor = 'center')


def radioButtons(win):
	s1 = Radiobutton(win, text='Youtube', variable=sourcevar, value='youtube')
	s1.place(x=450,y=60,anchor = 'center')
	s2 = Radiobutton(win, text='Reddit', variable=sourcevar, value='reddit')
	s2.place(x=550,y=60,anchor = 'center')

	w1 = Radiobutton(win, text='Yes', variable=writevar, value='yes')
	w1.place(x=450,y=180,anchor = 'center')
	w2 = Radiobutton(win, text='No', variable=writevar, value='no')
	w2.place(x=550,y=180,anchor = 'center')


def entryFields(win):
	dev = Entry(win,width=20,textvariable = devKey)
	dev.place(x=500,y=120,anchor = 'center')

	seed = Entry(win,width=20,textvariable = seedKey)
	seed.place(x=260,y=301,anchor = 'center')

	keywords = Entry(win,width=30,textvariable = keywordsString)
	keywords.place(x=560,y=420,anchor = 'center')

	scrapeFactor = Entry(win,width=30,textvariable = scrapeThresholdSet)
	scrapeFactor.place(x=560,y=460,anchor = 'center')

def dropdownMenus(win):
	levelSet.set(0) # default value
	level_options = [0,1,2,3,4,5,6]
	levelMenu = OptionMenu(win, levelSet, *(level_options))
	levelMenu.place(x=620,y=300,anchor = 'center')




def get_authenticated_service():
	if os.path.exists("CREDENTIALS_PICKLE_FILE"):
		with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
			credentials = pickle.load(f)
	else:
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
		credentials = flow.run_console()
		with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
			pickle.dump(credentials, f)
	return googleapiclient.discovery.build(
		api_service_name, api_version, credentials=credentials)

def get_related_videos(vid_id):
	youtube = get_authenticated_service()
	request = youtube.search().list(
		part="snippet",
		relatedToVideoId=vid_id,
		type="video"
	)
	response = request.execute()
	return response


def sentiment_analysis(sentence):
	vs = commentbot.polarity_scores(sentence)
	s_result["count"] += 1
	if vs['compound'] >= 0.05:
		s_result["positive"] += 1
	elif vs['compound'] <= -0.05:
		s_result["negative"] += 1
	else:
		s_result["neutral"] += 1
	return

def sentiment_display():

	gen = ' ********************* YOUTUBE COMMENT ANALYZER *********************'
	for i in gen:
		print (i, end='')
		sys.stdout.flush()
		time.sleep(0.01)
	print("\n")

	gen= ' ********************************************************************'
	for i in gen:
		print(i, end='')
		sys.stdout.flush()
		time.sleep(0.01)
	print("\n")

	positive_percentage = s_result["positive"] / s_result["count"] * 100
	negative_percentage = s_result["negative"] / s_result["count"] * 100
	neutral_percentage = s_result["neutral"] / s_result["count"] * 100

	time.sleep(1)
	print(" ==> PERCENTAGE OF COMMENTS THAT ARE POSITIVE : ",positive_percentage,"%\n")
	time.sleep(1)
	print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEGATIVE : ",negative_percentage,"%\n")
	time.sleep(1)
	print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEUTRAL  : ",neutral_percentage,"%\n")
	return

def recursive_find(seed_vid,level):
	if level > 0 :	
		results = get_related_videos(seed_vid)
		for item in results['items']:
			rel_vid_id = item['id']['videoId']
			report = get_video_comments(part='snippet,replies', videoId=rel_vid_id,textFormat='plainText')
			if report["Scrape Count"] > stimulationFactor :
				recursive_find(rel_vid_id,level-1)
	else :
		return


def get_video_comments(**kwargs):
	word_appear = np.zeros(len(wordlist_english))
	comments_with_word = ""
	youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
	results = youtube.videos().list(part="snippet,statistics",id=kwargs['videoId']).execute()
	for item in results['items']:
		title = item['snippet']['title']
		tc = item['statistics']['commentCount']
		likes = item['statistics']['likeCount']
		dislikes = 0 #Deprecated feature from YT
		#dislikes = item['statistics']['dislikeCount']
	try:
		print(title)
	except:
		report = {"Scrape Count":0}
		return report
	print("Total Comments:" + str(tc))
	results = youtube.commentThreads().list(**kwargs).execute()
	commentNumber = 0
	while results:
		for item in results['items']:
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			word_in_comment = check_words(comment)
			word_appear = word_appear + word_in_comment
			if(np.sum(word_in_comment)):
				comments_with_word = comments_with_word + " , " + comment
			sentiment_analysis(comment)
			print(commentNumber, end="\r")
			commentNumber = commentNumber + 1
			sys.stdout.flush()
		if 'nextPageToken' in results:
			kwargs['pageToken'] = results['nextPageToken']
			results = youtube.commentThreads().list(**kwargs).execute()
		else:
			break

	report = {"ID":kwargs['videoId'] , "Title":title , "Total Comments":tc , 
				"Likes": likes, "Dislikes": dislikes, "Scrape Count":np.sum(word_appear) , 
				  "positive":s_result["positive"] , "negative":s_result["negative"] , 
				  "neutral":s_result["neutral"] , "comments":comments_with_word
					}
					
	report.update(dict(zip(wordlist_english, word_appear)))

	#print(report)
	if(report["Scrape Count"] > stimulationFactor):
		if(writeToFile):
			global writer
			writer.writerow(report)
	return report

def check_words(sentence):
	temp = np.zeros(len(wordlist_english))
	sentence = sentence.lower()
	i = 0 
	for word in wordlist_english:
		if word in sentence:
			temp[i] = temp[i] + 1
		i += 1
	return temp

def gui():
	guiLabels(window)
	radioButtons(window)
	entryFields(window)
	dropdownMenus(window)
	searchButton = Button(window, text = "Start Search", command = searchCallback)
	searchButton.place(x=400,y=500,anchor = 'center')
	window.title('Affective Stimulus Scraper')
	window.geometry("800x600")
	window.mainloop()

def setParameters():
	# print(sourcevar.get())

	global writeToFile,DEVELOPER_KEY,seed_vid,wordlist_english,level,stimulationFactor

	# print(writevar.get())
	if(writevar.get() == 'yes'):
		writeToFile = True
	else:
		writeToFile = False

	# print(devKey.get())
	if devKey.get():
		DEVELOPER_KEY = devKey.get()

	# print(seedKey.get())
	if seedKey.get():
		seed_vid = seedKey.get()

	# print(keywordsString.get())
	if keywordsString.get():
		wordlist_english = keywordsString.get().split(",")


	# print(levelSet.get())
	level=levelSet.get()

	if scrapeThresholdSet.get():
		try:
		    stimulationFactor = int(scrapeThresholdSet.get())
		except ValueError:
		    print("Threshold is not a number. setting default to 10")
		    stimulationFactor = 10

def searchCallback():
	setParameters()
	initializeFile()
	print(wordlist_english)

	report = get_video_comments(part='snippet,replies', videoId=seed_vid,textFormat='plainText')
	if report["Scrape Count"] > stimulationFactor :
		recursive_find(seed_vid,level)


def initializeFile():
	global writeToFile,seed_vid
	if(writeToFile):
		global writer,ofile
		filename = 'Scraped_stimulus_' + seed_vid + '.csv'
		ofile  = open(filename, "w")

		csv_columns = ["ID", "Title" , "Total Comments" , 
				"Likes", "Dislikes", "Scrape Count" , "positive",
					"negative", "neutral", "comments"]

		for items in wordlist_english:
			csv_columns.append(items)

		writer = csv.DictWriter(ofile,fieldnames=csv_columns)
		writer.writeheader()



def main():
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

	gui()

	if(writeToFile):
		ofile.close()



if __name__ == "__main__":
	main()



