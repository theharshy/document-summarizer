import os
import sys
import summarizecluster as SC

def main():
    inputdir = ''
    outputdir = '' 
    if len(sys.argv) > 2:
        inputdir = sys.argv[1]
        outputdir = sys.argv[2]  
    else:
        print 'Specify the input and output directories'
        exit(0)  
    
    #Checking if the input directory exist
    if not os.path.isdir(inputdir):
        print ('The input directory does not exist\n')
        exit(0)
        
    # Creating output directory if doesn't exist
    if not os.path.isdir(outputdir):
        print ('Creating the new output directory\n')
        os.makedirs(outputdir) 
        
    # Start running program
    for filename in filter(lambda x: x.endswith('.txt'), os.listdir(inputdir)):
        SC.compute_summary(os.path.join(inputdir, filename), \
                        os.path.join(outputdir, filename))
                        
    print("Summary Generation Completed!\n")
  
    
if __name__ == '__main__':
    main()
