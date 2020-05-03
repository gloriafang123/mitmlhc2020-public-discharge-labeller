import random 

import tensorflow as tf
import numpy as np
import re
import pickle
import h5py
from mysite.settings import BASE_DIR
import os

####load model and vectors ####

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
	for word,label in zip(original_summary_separated, output_labels):
		if label != "Other":
			html_string += "<div class='label'>" + word + "</div> "
		else:
			html_string += word + " "

	return  html_string + str(random.randint(0,10))
	# "Example Trained <div class='label'> String </div> Here "


def vec_label(vec):
	idx = np.argmax(vec)
	labels = ["Other","Movement","Meds_Treatments","Procedures_Results",
		"Vitals_Labs","Symptoms_Signs", "ProcedureHistory","MedicationHistory",
		"DiagnosisHistory","Demographics"]
	return labels[idx]


def get_words_from_text(text, max_length=206):
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
