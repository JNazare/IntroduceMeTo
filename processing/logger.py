import query

def log(tweet):
	f = open('log.txt', 'a')
	three = query.ranked_query(tweet)[0:3]
	f.write("TWEET: " + tweet + "\n")
	for e in three:
		f.write(str(e)+"\n")
	f.write('--------------\n\n')
	f.close()

tweet = "@IntroduceMeTo students at Northeastern"
log(tweet)



