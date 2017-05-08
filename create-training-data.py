import os
import xml.etree.ElementTree as ET
import requests
import urllib
import simplejson as json
import spacy
from fuzzywuzzy import fuzz


from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree


nlp = spacy.load('en')


def main():
    for idx, article in enumerate(os.listdir('../ousd-articles')):
        print(str(idx) + " " + article)
        root = ET.parse('../ousd-articles/'+article)
        for elem in root.findall('.//text'):
            try:
                chunk_nouns(elem.text)
            except Exception as e:
                print(e)



def enrich_core_nlp(text):
    pass
    # print(elem.text.encode('utf-8'))
    # querystring = urllib.parse.urlencode({"annotators": "tokenize,ssplit,pos,depparse","openie.resolve_coref": "false"})
    # print('http://localhost:9000/?'+querystring)
    # r = requests.get('http://localhost:9000/?properties={"annotators":"tokenize,ssplit,pos","outputFormat":"json","openie.resolve_coref": "false"}', data=elem.text.encode('utf-8'))


def enrich_core_nlp(text):
    pass
    # tagged_text = "[ The/DT cat/NN ] sat/VBD on/IN [ the/DT mat/NN ] [ the/DT dog/NN ] chewed/VBD ./."
    # gold_chunked_text = tagstr2tree(tagged_text)
    # unchunked_text = gold_chunked_text.flatten()

    # sentences = json.loads(r.content, strict=False)

def chunk_nouns(text):
    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    count = 1
    sent_count = 0
    for np in doc.noun_chunks:
        if(np.root.is_stop==False and (len(np.text.split(' '))>1 or np.root.ent_type!=0)):
            # if sentence has changed, add 1 to sentence count
            try:
                if (fuzz.ratio(np.sent.text, sentences[sent_count]) < 95):
                    sent_count += 1
            except:
                sent_count -= 1

            if(np.start_char==np.sent.start_char):
                question = np.doc.text[np.end_char:np.sent.end_char]
            else:
                question = np.doc.text[np.sent.start_char:np.start_char]

            if(sent_count == len(sentences)):
                incorrect_sentence = sentences[sent_count-1]
            else:
                try:
                    incorrect_sentence = sentences[sent_count+1]
                except Exception as e:
                    #print(e)
                    incorrect_sentence = sentences[sent_count - 1]

            count, string = create_train_sentence(np.sent.text, incorrect_sentence,
                                                  question, np.text, count)
            append_text(string)


def create_train_sentence(sent1, sent2, question, answer, count):
    string = str(count) + ' ' + sent1 + '\n'
    count += 1
    string += str(count) + ' ' + sent2 + '\n'
    count += 1
    string+= str(count)+ ' ' + question + '?\t' + answer + ' ' + str(count-2) + '\n'
    count += 1
    return count, string

def append_text(text):
    with open('training_data_1_supported_fact.txt','a') as train_file:
        train_file.write(text)

if __name__ == '__main__':
    main()