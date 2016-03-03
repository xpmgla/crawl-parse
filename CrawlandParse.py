#SUMMARY: With this algorithm, we will navigate to two predetermined
#websites and download its entire source code. In the second part, we will
#extract the elements that we are actually interested in and discard
#the rest. Also, just to make it more complicated and provide a
#framework for future studies, we will create a nice output-file.


##########################################################################
#####               A. Preliminary Steps: The Set-up                ######
##########################################################################

####
### A.1 Import a bunch of add-ins.
#       Some need to be installed for the algorithm to work! You may use the pip-installer.

#[EXPLAINER]: Some of the functions we use need special modules.
#Some of those come with the Python-standard package and we simply need
#to import them. Other don't and we have to install them before we
#can import them.

import time
import os
import io
import requests
from bs4 import BeautifulSoup
import re

#[EXPLAINER]: Just for the prettiness of output!
print "This script was started " + time.ctime()

####
### A.2 Define miscellaneous variables.
#       They are merely tools- we are not really interested in them.

ProgressCounter = 1

####
### A.3 Define names and paths of In- and Output-Data,
#       so python can find the relevant directories and files

#[EXPLAINER]: The correct specification here depends on the folder
#structure you choose. I will give you an example of what I found
#to be helpful.

dir = "C:\Users\gaetsche\Desktop\CrawlandParse"
dir_input = dir + "\Input"
dir_output = dir + "\Output"
InputDataName = 'InputData.txt'
OutputDataName = "OutputResults.txt"

####
### A.4 Open and Read Input-Data!
#

#[EXPLAINER]: This command tells python which directory we want to work in.
os.chdir(dir_input)

#[EXPLAINER]: Reads in our Input-Data and splits it up in lines. Store
#everything in the list called RawInputs.
RawInputs = io.open(InputDataName, 'r', encoding='utf-8').read().splitlines()

#[EXPLAINER]: For later prettiness.
TotalCount = len(RawInputs)

####
### A.5 Prepare Output-Data.
#

#[EXPLAINER]: As we are done with our Input, we can switch to the
#Output-Directory now.
os.chdir(dir_output)

#[BIG EXPLAINER]: Under the prespecified name, we open our output-file.
#The option 'w' means that a new file will be created. If another file
#with the same name exists in the targeted directed directory, it will
#be deleted. Hence, the first time we write into or output, that's
#exactly what we want. In all subsequent times we will use the option 'a',
#which means we will append to an existing file.
#Now we can write as we please. The string \t stands for tabstopp and
#\n stands for new line. I normally try to create a nice header, such that
#later we can open the data nicely in Excel.
with open(OutputDataName, 'w') as TargetData:
    TargetData.write("ID\tURL\tWikipediaHeaders\n")

##########################################################################
#####   B. Create the ingredients we will later use                 ######
##########################################################################
#Start a loop over all units of observation that lasts for the whole script!

for RawInput in RawInputs:
    #[EXPLAINER]: Again, just for prettiness and keep the process tractable.
    print "We are at number " + str(ProgressCounter) + " of " + str(TotalCount) + "!"
    
    ####
    ### B.1 Define Variables that we will work with and write them into Output
    #       Each entry in the list RawInputs is a unit of observation
    #       and contains all relevant information associated with it.
    
    
    ## B.1.i Start by picking those apart and defining all its elements as variables

    #[EXPLAINER]: Here split all attributes of each observation into its elements
    TotalInfoperEntry = RawInput.split('#')
    #[EXPLAINER]: Here we tell python manually what is what. From then on, we
    #can call it by its name!
    ID, URL = TotalInfoperEntry[0:2]
    
    ## B.1.ii Write all info back into Result-File
    with open(OutputDataName, 'a') as TargetData:
        TargetData.write(ID.encode('utf-8') + '\t')
        TargetData.write(URL.encode('utf-8') + '\t')

    ##########################################################################
    #####   C. Get the SourceCode!                                      ######
    ##########################################################################

    ####
    ### C.1 Navigate to webpage, get source code, make sure it's encoded
    #       correctly and turn it into parseable form.

    #[EXPLAINER]: One of THE quintessential blocks! Here you get the
    #source code.
    r = requests.get(URL)
    #[EXPLAINER]: Encode it as you want.
    r.encode = "utf-8"
    #[EXPLAINER]: And turn it into parseable material via the module
    #BeautifulSoup
    html_raw = r.text
    SourceCode = BeautifulSoup(html_raw)
    
    #[EXPLAINER]: This piece will not be used in the final version,
    #is extremely helpful on the way.
    #    print SourceCode.prettify()

    ##########################################################################
    #####   D. Second Part: Parse your SourceCode!                      ######
    ##########################################################################

    #[EXPLAINER]: This part is more craft than art and has to be tailored
    #to each specific websit you are working with.
    #Our mission for today is to parse Headlines out of Wikipedia-pages.

    #[EXPLAINER]: This is convoluted! In words it says:
    #Check my SourceCode for all tags named "h1" that have an id
    #called "firstHeading" and call those tags entry in the loop
    #that follows. This is the basic search structure for all your parsing!
    for entry in SourceCode.find_all('h1', {'id':'firstHeading'}):
        #[EXPLAINER]: Write to your Output-File.
        with open(OutputDataName, 'a') as TargetData:
            #[EXPLAINER]: What do we write? The text in the tag specified
            #beforehand.
            TargetData.write(entry.getText().encode('utf-8'))

    #HERE FOLLOW SOME EXAMPLES THAT WE WILL NOT EXECUTE IN THIS ALGORITHM
    #AND THAT ARE NOT FROM WIKIPEDIA, BUT THAT YOU MIGHT FIND HELPFUL
    #IN YOUR FUTURE WORK.
            
    #[EXPLAINER]: This extracts not the text of a tag, but one of its
    #constituents. Here, we take what is noted under "content".
    #for entry2 in SourceCode.find_all('meta', {'name':'KLAUSI'}):
    #    SomeContainer = entry4.get('content').encode('utf-8')

    #[EXPLAINER]: Maybe it is hard to unambiguously navigate to a tag
    #via tag names or names of its elements. But there might be something unique
    #in some of its textual elements. Then you can use the "re" module.
    #Basically, below we say: Search in the SourceCode for tags named a
    #and search among these for a tag that has "Peterchen" written in its
    #element href. Then get me the href!
    #for entry3 in SourceCode.find_all('a', {'href':re.compile("Peterchen")}):
    #    entry3.get('href')

    ##########################################################################
    #####   E. Finalize your loop!                                      ######
    ##########################################################################
    #Click ProgressCounter a notch, so we always know where we are
    #when the code runs
    ProgressCounter = int(ProgressCounter) + 1
    #Add a new line to the Main-Output-File
    with open(OutputDataName, 'a') as TargetData:
        TargetData.write('\n')
            
