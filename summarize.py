import nltk
from nltk.corpus import stopwords
import operator
import math
import sys

# importing stopwords that should be ignored during summary computation 
stop_words = str(stopwords.words('english'))

# lowerbound to avoid dissimilar sentences
LOWER_BOUND = .20   
# upperbound to exclude duplicate sentences
UPPER_BOUND = .90   			

# Checks if a word is either a punctuator or a stopword
def is_unimportant(word):
	return word in ['.', '!', ',',] or '\'' in word or word in stop_words   
	
# Function to filter out unimportant token
def only_important(sent):
    return filter(lambda w: not is_unimportant(w), sent)                  
    
# Computes the similarity between two sentences
def compare_sents(sent1, sent2):
    if not len(sent1) or not len(sent2):
        return 0
    else:
		return len(set(only_important(sent1)) & set(only_important(sent2))) \
		      / ((len(only_important(sent1)) + len(only_important(sent2)))/ 2.0) 
		
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
		return sum(compare_sents_bounded(sent, sent1) for sent1 in sents) / float(len(sents))


# Computes and prints the summary of the document
def summarize_block(block):      
    if not block:
        return None
    
    # Extracts token from the document
    i = 1
    sents = []
    summary_list = []
    S = (nltk.sent_tokenize(block))
    word_sents = list(map(nltk.word_tokenize, S))
    for item in S:
    	sents=sents + [(item,i)]
    	i = i + 1
    	
    blocksize= i - 1
    
    # Summary is 10% of original document
    summary_size=math.ceil(0.1*blocksize) 			
    d = dict((compute_score(word_sent, word_sents), sent)  \
                      for sent, word_sent in zip(sents, word_sents))
    
    # creating a summary list with sentences in cronological form                      
    sorted_d = sorted(d.items(), key = operator.itemgetter(0), reverse = True)
    i=1
    for item in sorted_d:
    	if(i>summary_size):
    		break;
    	else:
    		summary_list=summary_list+[item]
    		i=i+1;
    summary_list_sorted = sorted(summary_list, key=lambda x: x[1])
    
    # printing the computed summary 
    for item in summary_list_sorted:
    	print item[1][0]
    	
    	
def main():													
    data = []
    filename = '' 
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print 'Specify the file name'
        exit(0)      
 	
    fp = open(filename)
    file_contents = fp.read()
    summarize_block(file_contents)


if __name__ == '__main__':
    main()
