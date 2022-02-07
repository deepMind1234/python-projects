from ast import keyword
from ctypes.wintypes import WORD
import nltk
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from numpy import RankWarning
from pkg_resources import WorkingSet
from collections import Counter
import math
import os
import re


ps = PorterStemmer()


class summarizer:


    def __init__(self, filepath, filecount):
        self.filepath = filepath
        self.filecount= filecount
        self.tokenizedfile = self.tokenizer()
        self.processed_words = self.word_processor()
        self.idf,self.tfdict =  self.tf_idf()
        
    
    
    global filter_stopwords
    def filter_stopwords(word):
        stopword = set(stopwords.words('english'))
        if word not in stopword:
            return True
        else:
            return False
    

    def word_processor(self):
        processedwords = {}
        regex = r'[^a-zA-Z0-9\s]'
        for k,v in self.tokenizedfile.items():
            tokenized_doc = []
            for sent in v:
                re.sub(regex,'', sent)
                words = word_tokenize(sent)
                tokenized_words = [word for word in words if len(word) > 1] # remove words sub length 1
                word_list= list(filter(filter_stopwords,tokenized_words)) # filter stopwords
                tokenized_words = [word.lower() for word in word_list] # lower case all words
                for word in tokenized_words:
                    word.replace("'", "")
                tokenized_doc.append(tokenized_words)
            processedwords.update({k:tokenized_doc})
        return processedwords
        

    def tokenizer(self):
        num_files = 0
        tokenized_files = {}
        for filename in os.scandir(self.filepath):
            if filename.is_file():
                source_file = str(filename.path)
                with open(source_file, "r", encoding='utf-8') as file:
                    text = file.read()
                    sentences = sent_tokenize(text)
                    tokenized_files.update({source_file:sentences})
                    num_files += 1
                    if num_files >= self.filecount:
                        break
        return tokenized_files

    def sentence_position(self):
        sentence_position = {}
        for k,v in self.tokenizedfile.items():
            rankings = []
            denominator = len(v)
            for count,value in enumerate(v):
                rankings.append((denominator-count)/denominator)
            sentence_position.update({k:rankings})
        return sentence_position 
        pass
    
    def keyword(self):
        important_pos = ["NN","NNS","NNP","VB","VBG","VBP"]
        keywords = {}
        for k,v in self.processed_words.items():
            sent_pos_list = []
            for wordlist in v:
                important_pos_words = []
                pos_tagged = nltk.pos_tag(wordlist)
                for pair in pos_tagged:
                    if pair[1] in important_pos:
                        important_pos_words.append(pair[0])
                sent_pos_list.append(important_pos_words)
            keywords.update({k:sent_pos_list})
        return keywords

    def important_entity_inclusion(self):
        pass

    def sentence_length(self, threshold):
        sentence_length = {}
        for k,v in self.tokenizedfile.items():
            allowed_sent = []
            for sent in v:
                words= word_tokenize(sent)
                if len(words) >= threshold:
                    allowed_sent.append(1)
                else:
                    allowed_sent.append(0)
            sentence_length.update({k:allowed_sent}) 
        return sentence_length
        pass

    def tf_idf(self):
        idf_dict = Counter()
        dictTF_dict = {}
        for k,v in self.processed_words.items():
            tf_dict = Counter()
            sent_term_frequency = []
            for sent in v:
                tf_sent = Counter(sent)
                #sent_term_frequency.append(tf_sent)
                tf_dict += tf_sent
            idf_dict += tf_dict
            dictTF_dict.update({k:tf_dict})
        return idf_dict,dictTF_dict

    def generate_idf_score(self,word):
        num_docs_withword = 0
        num_docs = 0
        for k,v in self.tfdict.items():
            num_docs += 1
            if word in v.keys():
                num_docs_withword += 1

        idf_score = math.log(num_docs/(1+num_docs_withword))
        return idf_score
    
    def generate_tf_score(self,filename,word):
        terms_in_doc = self.tfdict[filename]
        num_term = terms_in_doc[word]
        total_word = sum(terms_in_doc.values())
        tf_score = math.log(num_term/1+total_word)
        return tf_score

    def tf_idf_score(self):
        sentence_scores_per_doc= {}
        for k,v in self.tokenizedfile.items():
            sentence_score_list= []
            for sent in v:
                sentence_score = 0
                for word in sent:
                    sentence_score +=  self.generate_idf_score(word = word) * self.generate_tf_score(filename = k, word = word)
                sentence_score_list.append(sentence_score)      
            sentence_scores_per_doc.update({k:sentence_score_list})
        return sentence_scores_per_doc

    def TextRank(self):
        pass



val = summarizer(".\\TextCorpus",10)
#print(val.sentence_length(threshold = 10))
print(val.keyword())


