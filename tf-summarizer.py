import nltk
from nltk.corpus import stopwords
import math
import string
import sys


delimiters =[".", ",", ";", ":", "?", "/", "!", "'s", "'ll", "'d", "'nt", ")", "("]
stop_words = str(stopwords.words('english'))


def read_doc(name):
    rawtext = open(name, 'r')
    blocks = rawtext.readlines()
    
    return blocks

def main():
    data = []
    
    filename = ''
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print 'Specify the file name'
        exit(0)
        
    paras = read_doc(filename)
    
    
    # using each block
    count = 1;
    for i in range(len(paras)):
        para = paras[i]
        sentences = nltk.sent_tokenize(para)
        
        for sentence in sentences:
            words =  nltk.word_tokenize(sentence.lower())
            # remove stop words and punctuations
            
            fil_words = filter(lambda word:\
                        word not in delimiters and word not in stop_words, words)
            
            data.append({'orig': sentence, 'tokens': fil_words, 'index': count})
            
            count += 1
        
    
    # Calculating Term frequency
    term_freq = {}
    for sentence in data:
        for term in sentence['tokens']:
            if term not in term_freq.keys():
                term_freq[term] = 1;
            else:
                term_freq[term] += 1;
                    
    #Setting a score with the term frequencies per sentence
    for i in range(len(data)):
        sentence = data[i]
        
        score = 0
        for term in sentence['tokens']:
            score += term_freq[term]
                
        data[i]['score'] = float(score)/(len(sentence['tokens']))
    
    summary = []
    
    # Sorting according the score
    newlist = sorted(data, key=lambda k: k['score'], reverse=True) 
    
    #Extracting only a fraction of the sorted ranked list
    for j in range(int(math.ceil(float(len(newlist))/10))):
        line = newlist[j]
        summary.append(line)
    
    # Printing according to actual order
    ordered_summary = sorted(summary, key=lambda k: k['index'])
    summary = [sentence['orig'] for sentence in ordered_summary]
    
    print string.join(summary)
    
    
if __name__ == '__main__':
    main()

