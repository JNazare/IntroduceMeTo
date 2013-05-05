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

def search_field(lemmalist, keywords):
	found_words = []
	keywords = lemmatize_list(keywords)
	for keyword in keywords:
		if keyword.lower() in lemmalist:
			found_words.append(keyword.lower())
	# if len(found_words) > 0:
		# print found_words
	return found_words

# Model a FLESHY HUMAN

class Person(object):
	def __init__(self, json):
		self.url = json.get('url', '') or ''
		self.name = json.get('name', '') or ''
		self.name_lemma = lemmatize_list(remove_filler_words(remove_punctuation(json.get('name', ''))).lower().split())
		self.location = lemmatize_list(remove_filler_words(remove_punctuation(json.get('location', ''))).lower().split())
		self.headline = lemmatize_list(remove_filler_words(remove_punctuation(json.get('headline', ''))).lower().split())
		self.interests = lemmatize_list(remove_filler_words(remove_punctuation(json.get('interests', ''))).lower().split())
		self.skills = lemmatize_list(remove_filler_words(remove_punctuation(json.get('skills', ''))).lower().split())
		self.educations = lemmatize_list(remove_filler_words(remove_punctuation(json.get('educations', ''))).lower().split())
		self.positions = lemmatize_list(remove_filler_words(remove_punctuation(json.get('positions', ''))).lower().split())
		
	def __str__(self):
		return "Name: " + self.name + "\n" + "Locations: " + self.location + "\n" + "Interests: " + self.interests + "\n" + "Skills: " + self.skills + "\n" + "Educations: " + self.educations + "\n" + "Positons: " + self.positions

	def search_name(self, keywords):
		return search_field(self.name_lemma, keywords);

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

	def search_all(self, keywords):
		return self.search_location(keywords) + \
			self.search_headline(keywords) + \
			self.search_interests(keywords) + \
			self.search_skills(keywords) + \
			self.search_educations(keywords) + \
			self.search_positions(keywords)