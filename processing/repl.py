import query

while True:
  var = raw_input("\033[92mDear Introducemeto, introduce me to... \033[0m")
  try:
    print ">", [x[0] for x in query.ranked_query(str("@IntroduceMeTo " + var))]
    print ""
  except:
    print "> NO HUMANS FOUND"
    print ""