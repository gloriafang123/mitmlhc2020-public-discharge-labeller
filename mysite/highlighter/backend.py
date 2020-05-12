import tensorflow as tf
import numpy as np
import re
import pickle
import h5py
from mysite.settings import BASE_DIR
import os

########## scispacy imports #############
# make sure you have pip installed scispacy

import spacy
import scispacy
import en_core_sci_sm   #The model we are going to use
from spacy import displacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.umls_linking import UmlsEntityLinker
import urllib

from highlighter.definition_function import get_definitions

#### get_summary(): used if using ML model #######

####load model and vectors ####
# make sure you have word_embeddings (e.g. glove or other) 
# pickled at the correct location.

model = tf.keras.models.load_model(
	os.path.join(BASE_DIR, 'highlighter/load/models/model1')
	) 
	#model is called model1. Must be relative to BaseDir (mysite/, the root not the app)
	#not sure if the other assets, variables, protobuf is needed;
		#if it is needed, the way to get them on colab is to
		#save load and save again, into a folder.

with open(os.path.join(BASE_DIR,'highlighter/load/word_embeddings.pickle'), 'rb') as handle:
	word_embeddings = pickle.load(handle)

max_length = 206 #current shape model is trained on, needs changing later

#labels in vec_label func may need to change later, depend on model

################################

def get_summary(original_string_cleaned_data, labels):
	"""
	returns an html_string of the highlighted summary
	"""

	#get the body text only
	original_summary = original_string_cleaned_data["original"]
	output_labels = get_label_list(original_summary)

	original_summary_separated = re.sub("[^a-zA-Z0-9.]", " ", original_summary)
	original_summary_separated = original_summary_separated.split()

	#sometimes the original and the labels aren't the same length, but not sure why.
	# assert (len(original_summary_separated) == len(output_labels))

	html_string = "" 
	#zip takes shorter list.

	# NOTE for now all labels are in the class 'label'.
	# ideally, we need several cases to deal with each of the 10 HPI labels
	# and also add 10 classes to the styles.css file.
	for word,label in zip(original_summary_separated, output_labels):
		if label != "Other":
			html_string += "<div class='label'>" + word + "</div> "
		else:
			html_string += word + " "

	return  html_string
	# "Example Trained <div class='label'> String </div> Here "


def vec_label(vec):
	"""
	finds the corresponding label for a vector
	"""
	idx = np.argmax(vec)
	labels = ["Other","Movement","Meds_Treatments","Procedures_Results",
		"Vitals_Labs","Symptoms_Signs", "ProcedureHistory","MedicationHistory",
		"DiagnosisHistory","Demographics"]
	return labels[idx]


def get_words_from_text(text, max_length=206):
	"""
	get vectorized word embeddings based on input string text
	"""
  # max length: pad or cut off
	text = re.sub("[^a-zA-Z0-9.]", " ", text)
	tokens = text.lower().strip().split()

  	#also replace lowercase...
	words = np.concatenate([tokens[0:max_length],
		[' ']*(max_length - len(tokens))
		], axis=0) # note, ' ' will get np zeros, not in word_embeddings.
  
	words_vec = [word_embeddings.get(i, np.zeros(100)) for i in words]

	words_vec2 = np.array(words_vec).reshape(1, len(words_vec), len(words_vec[0]))

	return words_vec2


def get_label_list(input_summary, max_length=max_length):
	"""
	get list of labels based on summary string
	"""
	wv = get_words_from_text(input_summary, max_length)

	new_preds = model.predict(np.reshape(wv, list(wv.shape)),
		batch_size=1) 

	predicted_labels = np.array([vec_label(i) for i in new_preds[0]])

	return predicted_labels



######## Code below is used if using get_summary_scispacy() #########
# nlp_reader takes forever to load. unfortunately cannot be pickled.

nlp_reader = en_core_sci_sm.load()
cui_linker = UmlsEntityLinker(resolve_abbreviations=True)
nlp_reader.add_pipe(cui_linker)


def get_summary_scispacy(input_summary, *args):
	tagged_sent = nlp_reader(input_summary["original"])
	sentence_html = displacy.render(tagged_sent, style="ent")
	sentence_ents = tagged_sent.ents
	output_html = fix_html(sentence_html, sentence_ents)

	definitions = get_definitions(input_summary["original"])
	definitions_html = dict_to_html(definitions)
	return output_html, definitions_html

def dict_to_html(d):
	output = ""
	for word in d:
		defs = "<br>".join(d[word])
		output += "<br> <b>" + word + ":</b> <br> " + defs
	print(output)
	return output


def fix_html(sentence_html, sentence_ents):
	"""
	updates the html text:
	instead of ENTITY, use a CUI that is a (google) search link 
	(could update link later)

	input: sentence_html that is already tagged; sentence_ents is list of entities.
	"""
	words = sentence_html.split("<mark")
	print (len(words))
	output = [words[0]] #first term doesn't have "mark" on it
	for i in range(1, len(words)):

		try:
			cui = sentence_ents[i-1]._.umls_ents[0][0] #if no cui, this will be out of range
		except:
			cui = "SEARCH"
		replaced = words[i].replace('class="entity"', 'class="entity tooltipped" data-position="top" data-tooltip="' +  str(cui) +
                     '"')

		#note: currently tooltips don't work.
		replaced = replaced.replace('<span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: uppercase; vertical-align: middle; margin-left: 0.5rem">ENTITY</span>',
                                '<a href="http://www.google.com/search?q=' +urllib.parse.quote_plus(str(sentence_ents[i-1])) + '">'+ str(cui)+' </a>')
		output.append(replaced)
	return '<mark'.join(output)
