import nltk
from nltk.corpus import stopwords
import math
import string
import sys
import numpy as np
from scipy.cluster.vq import kmeans2
import operator																		

delimiters =[".", ",", ";", ":", "?", "/", "!", "'s", "'ll", "'d", "'nt", ")", "("]

# importing stopwords that should be ignored during summary computation 
stop_words = str(stopwords.words('english'))                                   

# lowerbound to avoid dissimilar sentences
LOWER_BOUND = .20   
# upperbound to exclude duplicate sentences
UPPER_BOUND = .90   			

# Checks if a word is either a punctuator or a stopword
def is_unimportant(word):
    return word in delimiters or '\'' in word or word in stop_words   


# Function to filter out unimportant token
def only_important(sent):
    return filter(lambda w: not is_unimportant(w), sent)                  


# Computes the similarity between two sentences
def compare_sents(sent1, sent2):
    if not len(only_important(sent1)) or not len(only_important(sent2)):
        return 0
    else:
        return len(set(only_important(sent1)) & set(only_important(sent2))) / \
        ((len(set(only_important(sent1))) + len(set(only_important(sent2))))/ \
          2.0) 


# Test whether the similarity score of two sentences are within bounds
def compare_sents_bounded(sent1, sent2):
    cmpd = compare_sents(sent1, sent2)
    if LOWER_BOUND < cmpd < UPPER_BOUND:
        return cmpd
    else:
        return 0


# Used to compute similarity score for a sentence against all other sentences
def compute_score(sent, sents):										
    if not len(sent):
        return 0
    else:
        return sum(compare_sents_bounded(sent, sent1) for sent1 in sents) /  \
               float(len(sents))


# Computes the sentences that best summarizes the block
def summarize_block(block): 
    if not block:
        return []
    else:
        sents=[]
        summary_list=[]
        
        word_sents = [block[i]['orig'] for i in range(0,len(block))]
        
        for i in range(0,len(block)):
            sents = sents + [(block[i]['orig'], block[i]['index'])]
        
        # variable to select number of sentences from each cluster
        summary_size = 3
         
        if(len (block) < summary_size):
            summary_size=len(block)
         
        # Sort summarized sentences in chronological order    
        d = dict((compute_score(word_sent, word_sents), sent)
                for sent, word_sent in zip(sents, word_sents))
        sorted_d = sorted(d.items(), key=operator.itemgetter(0),reverse=True)     
        
        # Selecting best sentences that describe a block
        i = 0
        for item in sorted_d:
            if(i>summary_size):                                     
                break;
            else:
                summary_list = summary_list + [item[1]]     
                            
            i= i + 1
                
        return summary_list;


# Reads from file
def read_doc(name):                                                
    rawtext = open(name, 'r')
    data = rawtext.readlines()
    return data


def compute_summary(inputfile, outputfile):
    # Reading the Input File
    data = []
    paras = read_doc(inputfile)
    count = 1;
    
    # Tokenizing the sentences from input
    for i in range(len(paras)):
        para = paras[i]
        sentences = nltk.sent_tokenize(para)
        
        for sentence in sentences:
            words =  nltk.word_tokenize(sentence.lower())
            
            # remove stop words and punctuations
            fil_words = filter(lambda word:  word not in delimiters or  \
                               '\'' in word and word not in stop_words, words) 

            data.append({'orig': sentence, 'tokens': fil_words, 'index': count})
            count += 1
            
    # Calculating Term frequency
    term_freq = {}                                   
    i=0
    finalsummary=[]
    for sentence in data:
        for term in sentence['tokens']:
            if term not in term_freq.keys():
                term_freq[term] = 1;
            else:
                term_freq[term] += 1
                
    Vectors = np.zeros(shape=(len(data),len(term_freq.keys())))
    
    # Creating a Term Vector for each sentence
    for sentence in data: 
        j=0
        for unique_words in term_freq.keys():
            if unique_words in sentence['tokens'] :
                Vectors[i][j]=term_freq[unique_words]     
            j=j+1
        i=i+1
        
    k = int(math.ceil(0.04 * len(data)))
    
    # Performing K means clustering
    centroid,label = kmeans2(Vectors, k, minit='points')
    
    # Clustering Vectors according to their Simmilarity
    cluster=[[] for _ in range(0,k)]
    for i in range(0,len(data)):
        cluster[label[i]].append(data[i])
        
    for i in range(0,k):
    	if(len(cluster[i])!=0):
        	ret= summarize_block(cluster[i])
        	
        	# We choose sentences from each cluster
        	finalsummary = finalsummary + ret
    
    #Sorting the sentences cronologically
    summary_list_sorted=sorted(finalsummary, key=lambda x: x[1])
    
    #Writing the final output file
    output = open(outputfile, 'w')
    for item in summary_list_sorted:
        output.write(item[0])
        output.write('\n')
        

def main():													
    inputfile = ''
    outputfile = '' 
    if len(sys.argv) > 2:
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
        
        compute_summary(inputfile, outputfile)
    else:
        print 'Specify the input and output file'
        
    
if __name__ == '__main__':
    main()

