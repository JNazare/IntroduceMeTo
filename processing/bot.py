import twitter, time
import query

#enter your consumer key,secret and access token secret,key in below function as parameters 

api=twitter.Api(consumer_key='YwQu5ABQ6awwclxwCPuA',
  consumer_secret='4fMIT8iUMrG6kcs7DtDM2Pg7ZtjpBSqZxnQWcOxVl8',
  access_token_key='1262285642-BsrFsVDxy3p4qMKUKM2TEtdiYE0HOgrtwzpmcBp',
  access_token_secret='ObALKXcoWloiW1qnMqWDsEE4vn3bLY68Y18fzAOZls') 

#now using PostUpdate method of the api we can use to post an update on twitter account 

#status = api.PostUpdate('Hello world.') 
#print status.text 

api._calculate_status_length = lambda x, y: 0

print 'Starting bot...', time.time()
last = time.time() - (1*60*5)
while True:
  print 'Checking since', last
  mentions = api.GetMentions()
  next_last = time.time()
  for t in mentions:
    if last < t.created_at_in_seconds:
      text = t.text
      user = t.user.screen_name
      print 'Found: @', user, ':', text
      rank = query.ranked_query(text)
      print ""
      print 'Top three:', rank[0:3]
      if len(rank):
        twtw = ('@' + user + ' Meet ' + ", ".join([(x[0] + ' ()') for x in rank[0:3]]))[0:74]
        for x in rank:
          twtw = twtw.replace('()', '(' + x[2].url + ')' if x[2].url else '', 1)
        status = api.PostUpdate(twtw, in_reply_to_status_id=t.id)
        print status.text
      else:
        status = api.PostUpdate('@' + user + ' There is no one for you to meet :(', in_reply_to_status_id=t.id)
      # try:
      #   if from_tweet.compare_twitter_lkdin(text, 'twitter_processing/linkedin_raw.txt') > 0.5:
      #     status = api.PostUpdate('@' + user + ' meet @timcameronryan! ' + str(time.time()))
      #   else:
      #     status = api.PostUpdate('@' + user + ' there is no one for you to meet. ' + str(time.time()))
      #   print status.text
      # except Error, e:
      #   print e
      #   print 'Error posting, continuing...'

  last = next_last
  time.sleep(60)