import fitz
import re
import pandas as pd
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.corpus import wordnet
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
def get_part_of_speech(word):
  probable_part_of_speech = wordnet.synsets(word)
  pos_counts = Counter()
  pos_counts["n"] = len(  [ item for item in probable_part_of_speech if item.pos()=="n"]  )
  pos_counts["v"] = len(  [ item for item in probable_part_of_speech if item.pos()=="v"]  )
  pos_counts["a"] = len(  [ item for item in probable_part_of_speech if item.pos()=="a"]  )
  pos_counts["r"] = len(  [ item for item in probable_part_of_speech if item.pos()=="r"]  )

  most_likely_part_of_speech = pos_counts.most_common(1)[0][0]
  return most_likely_part_of_speech



doc = fitz.open(r'Devansh_Kapri_Resume.pdf')
text = ""
for page in doc:
  text+=page.get_text()
print(text)
# print(cleaned)
cleaned = re.sub('\W+', ' ', text.lower())
tokenized = word_tokenize(cleaned)
print(tokenized)

Name = None
Phone_no = None
Email = None

def contact_check(var):
  flag = True
  try:
    int(var)
  except ValueError:
    flag = False
  finally:
    return flag


def basic_info(text_list):
  global Name,Phone_no,Email
  var = text_list[:50]
  # Name = text_list[:2].join(' ')
  Name = text_list[0] + ' ' + text_list[1]
  for i in range(len(var)):
    if (len(var[i]) == 10):
      if contact_check(var[i]):
        Phone_no = var[i]

    elif var[i] == '@':
      Email = var[i - 1] + var[i] + var[i + 1]

basic_info(tokenized)
print(Name)
print(Email)
print(Phone_no)
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(token,get_part_of_speech(token)) for token in tokenized]
print(lemmatized)
software = ["c","java","python","javascript","sql","mysql","github","software","algorithm","web","html","css","php"]
print(len(set(lemmatized)&set(software)))
df = pd.read_csv('resume_parser.csv')
# print(df)
dfd = df.to_dict()

jobs = {dfd['Job'][i]: {key: dfd[key][i].replace(',', '').split() for key in dfd if key != 'Job'}for i in range(len(dfd['Job']))}
print(jobs)


def score(n):
  if n <= 1 / 3:
    return 3 * n / 2
  if n <= 0.75:
    return ((24 * n) + 4.5) / 25
  return ((2 * n) / 5) + 0.6


def final_score(s, m, e):
  sure = score(s) * 50
  maybe = score(m) * 20
  extra = score(e) * 30
  return sure + maybe + extra

EXTRA =["dsa", "c", "python", "java",  "github", "testing", "debugging", "problem","version"]

Final_scores = {}

for job in jobs:
    sure_keys = jobs[job]['Sure']
    maybe_keys = jobs[job]['Maybe']
    sure_score = len(set(lemmatized) & set(sure_keys))/len(sure_keys)
    maybe_score = len(set(lemmatized) & set(maybe_keys))/len(maybe_keys)
    extra_score = len(set(lemmatized) & set(EXTRA))/len(EXTRA)
    Final_scores[job] = final_score(sure_score, maybe_score,extra_score)

print(Final_scores)