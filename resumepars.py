import re
import nltk
# Download this two packages if you are running this for the first time, otherwise comment it out
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

EXTRA = ["dsa", "c", "python", "java", "github", "testing", "debugging", "problem", "version"]


class Resumepars:
    def __init__(self, **kwargs):
        text = kwargs['text']
        dfd = kwargs['dfd']
        self.personal_info = {}
        self.jobs_scores = {}
        # Cleaning and extracting the main text
        cleaned = re.sub('\W+', ' ', text.lower())
        tokenized = word_tokenize(cleaned)

        # Getting basic_info
        self.personal_info = {
            'name': ' '.join(tokenized[:2]),
            'phone_no': ''.join(re.findall('\+\d{2}\-\d{10}', text[:100])),
            'email': ''.join(re.findall('\w+@\w+.\w+', text[:100]))
        }
        # Lemmatizing each of the tokenized word
        lemmatizer = WordNetLemmatizer()
        lemmatized = [lemmatizer.lemmatize(token) for token in tokenized]

        self.job_check(lemmatized, dfd)

    #This function gives variable growth for different ratios of common elements
    #It grows rapidly for first 1/3 elements then grows linearly upto 0.75 ratio and then has decreased growth
    def score(self, n):
        if n <= 1 / 3:
            return 3 * n / 2
        if n <= 0.75:
            return ((24 * n) + 4.5) / 25
        return ((2 * n) / 5) + 0.6

    def final_score(self, s, m, e):
        sure = self.score(s) * 50
        maybe = self.score(m) * 20
        extra = self.score(e) * 30
        return sure + maybe + extra

    def job_check(self, lemmatized, dfd):
        # Formatting the dictionary object for further use
        jobs = {dfd['Job'][i]: {key: dfd[key][i].replace(',', '').split() for key in dfd if key != 'Job'} for i in
                range(len(dfd['Job']))}

        for job in jobs:
            sure_keys = jobs[job]['Sure']
            maybe_keys = jobs[job]['Maybe']
            sure_score = len(set(lemmatized) & set(sure_keys)) / len(sure_keys)
            maybe_score = len(set(lemmatized) & set(maybe_keys)) / len(maybe_keys)
            extra_score = len(set(lemmatized) & set(EXTRA)) / len(EXTRA)
            self.jobs_scores[job] = self.final_score(sure_score, maybe_score, extra_score)

        scores = sorted(self.jobs_scores)
        self.top_job_scores = scores[-1:-4:-1]

    def name(self):
        return self.personal_info['name']

    def phone(self):
        return self.personal_info['phone_no']

    def email(self):
        return self.personal_info['email']

    def final_job_scores(self):
        return self.top_job_scores
