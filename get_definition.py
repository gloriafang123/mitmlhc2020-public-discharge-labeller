
## Author: Xiaoyi Wang ##

from glob import glob
import csv
import re 
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize



def simple_get(url):
	try:
		with closing(get(url, stream=True, timeout=10)) as resp:
			if is_good_response(resp):
				return resp.content
			else:
				return None

	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None


def is_good_response(resp):
	content_type = resp.headers['Content-Type'].lower() if "Content-Type" in resp.headers else None
	return (resp.status_code == 200 
			and content_type is not None 
			and content_type.find('html') > -1)


def log_error(e):
	print(e)



####### returns a dictionary that maps the word to a definition#####
####### the text being parsed is in the inp variable, so this can be modified######
def get_definitions(inp):
	map_sites = {}
	map_sites['a'] = "a-through-c#"
	map_sites['b'] = "a-through-c#"
	map_sites['c'] = "a-through-c#"
	map_sites['d'] ="d-through-i#"
	map_sites['e']= "d-through-i#"
	map_sites['f'] = "d-through-i#"
	map_sites['g'] = "d-through-i#"
	map_sites['h'] ="d-through-i#"
	map_sites['i'] ="d-through-i#"
	map_sites['j'] ="j-through-p#"
	map_sites['k'] ="j-through-p#"
	map_sites['l'] ="j-through-p#"
	map_sites['m'] ="j-through-p#"
	map_sites['n'] ="j-through-p#"
	map_sites['o'] ="j-through-p#"
	map_sites['p'] ="j-through-p#"
	map_sites['q'] ="q-through-z#"
	map_sites['r'] ="q-through-z#"
	map_sites['s'] ="q-through-z#"
	map_sites['t'] ="q-through-z#"
	map_sites['u'] ="q-through-z#"
	map_sites['v'] ="q-through-z#"
	map_sites['w'] ="q-through-z#"
	map_sites['x'] ="q-through-z#"
	map_sites['y'] ="q-through-z#"
	map_sites['z'] ="q-through-z#"
	ret = {}
#	inp = "He has diabetes. They recorded high levels of adrenaline."

	#use nltk to tokenize the words and remove any stop words from the vocabulary
	
	text_tokens = word_tokenize(inp)
	text_tokens = [word.lower() for word in text_tokens if not word in stopwords.words() and word not in ".,/:;'{}&*"]

	for word in text_tokens:
		first_letter = word[0]
		try:
			url1 = map_sites[first_letter]
		except:
			continue
		url2 = first_letter.upper()+"-terms"
		url = "https://www.health.harvard.edu/medical-dictionary-of-health-terms/"+url1+url2
		resp = simple_get(url)
		if resp is not None:
			html = BeautifulSoup(resp, 'html.parser')

			for a in html.find_all('p'):
				for s in a.find_all("strong"):
					term = s.text.lower()[:-2]
					term_words = term.split()
					if word in term_words:
						if word in ret:
							ret[word].add(a.text[0].upper() + a.text[1:])
						else:
							ret[word] = set([a.text[0].upper() + a.text[1:]])
						break
	return ret


if __name__ == "__main__":
	inp = "He has diabetes. They recorded high levels of adrenaline."
	key_definitions = get_definitions(inp)
	print(key_definitions)
