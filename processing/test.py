import newquery

# Testing

rank = newquery.ranked_query("@IntroduceMeTo JavaScript developers in the Boston area that studied at Olin College")
# rank = query.ranked_query("")

print ""
print 'Top three:', rank[0:3]
twtw = ('@timcameronryan Seek out ' + ", ".join([(x[0] + ' ()') for x in rank[0:3]]))[0:140-60+6]
for x in rank:
  twtw = twtw.replace('()', '(' + x[2].url + ')', 1)
print twtw, len(twtw)