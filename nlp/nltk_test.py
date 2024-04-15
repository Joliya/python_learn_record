"""
@file: nltk_test.py
@time: 2024/4/15 17:33
@desc: 
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

text = "NLP is a powerful tool for natural language processing."
tokens = word_tokenize(text)
tags = pos_tag(tokens)

print(tags)
