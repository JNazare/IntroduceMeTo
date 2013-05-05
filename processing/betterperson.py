"""
A class describing a person.
"""
import nltk
wnl = nltk.WordNetLemmatizer()

def lemmatize_list(lst):
		lemma_words = []
		for l in lst:
			lemma_words.append(wnl.lemmatize(l))
		return lemma_words

def list_to_lower(lst):
	new_list = []
	for l in lst:
		l = l.lower()
		new_list.append(l)
	return new_list

def remove_punctuation(s):
	puncts = ['.', ',', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '|']
	for c in s:
		if c in puncts:
			s = s.replace(c, "")
	return s

def find_filler_words():
	"""Helper function to find_key_words: grab all of the common words"""
	fin = open('words/common_words.txt', 'r')
	commons = [line.strip() for line in fin]
	commons = list_to_lower(commons)
	fin.close()
	return commons

def remove_filler_words(s):
	"""Helper function to find_key_words: remove all common words from tweet"""
	commons = find_filler_words()
	stripped_words = ""
	s = s.split()
	ct = 0
	for word in s:
		if ct == 0:
			if word not in commons:
				stripped_words = stripped_words + word
		elif word not in commons:
			stripped_words = stripped_words + " " + word
		ct = ct + 1
	return stripped_words

# Given a list of keywords, see if a field matches.

def search_field(field, keywords):
	found_words = []
	for keyword in keywords:
		if keyword in lemmatize_list(field.lower().split()):
			found_words.append(keyword)
			keywords.remove(keyword)
	found_words = lemmatize_list(found_words)
	if len(found_words) > 0:
		pass
		#print found_words
	return ' '.join(found_words)

# Model a FLESHY HUMAN

class Person(object):
	def __init__(self, json):
		self.url = json.get('url', '')
		self.name = remove_filler_words(remove_punctuation(json.get('name', '')))
		self.location = remove_filler_words(remove_punctuation(json.get('location', '')))
		self.headline = remove_filler_words(remove_punctuation(json.get('headline', '')))
		self.interests = remove_filler_words(remove_punctuation(json.get('interests', '')))
		self.skills = remove_filler_words(remove_punctuation(json.get('skills', '')))
		self.educations = remove_filler_words(remove_punctuation(json.get('educations', '')))
		self.positions = remove_filler_words(remove_punctuation(json.get('positions', '')))
		
	def __str__(self):
		return "Name: " + self.name #+ "\n" + "Locations: " + self.location + "\n" + "Interests: " + self.interests + "\n" + "Skills: " + self.skills + "\n" + "Educations: " + self.educations + "\n" + "Positons: " + self.positions

	def search_name(self, keywords):
		return search_field(self.name, keywords);

	def search_location(self, keywords):
		return search_field(self.location, keywords);

	def search_headline(self, keywords):
		return search_field(self.headline, keywords);

	def search_interests(self, keywords):
		return search_field(self.interests, keywords);

	def search_skills(self, keywords):
		return search_field(self.skills, keywords);

	def search_educations(self, keywords):
		return search_field(self.educations, keywords);

	def search_positions(self, keywords):
		return search_field(self.positions, keywords);