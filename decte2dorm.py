import uidodorm as ud
from bs4 import BeautifulSoup
import lxml
import numpy as np
import pandas as pd
import sys, string, re

text1 = open(r"pd_inputs/tlsg06.xml", "r")
text1 = text1.read()

def tagclean(text):
    #replace self-closed 'pause' and 'unclear word' tags with something handleable:
    pausepattern = re.compile("(<)(pause)(/>)")
    text1 = pausepattern.sub(r"[\2] ", text)
    unclearpattern = re.compile("(<)(unclear)(/>)")
    text1 = unclearpattern.sub(r"[\2] ", text1)
    #get rid of all the other self-closing tags:
    pattern = re.compile("(<)([^>]+)(/>)")
    subbed_text = pattern.sub(r"", text1)
    return subbed_text

def decteints(text):
    utterances = open(r"pd_outputs/dectedormsutts.txt", "w")
    soup = BeautifulSoup(tagclean(text), "xml")
    #pull out only the transcribed interviews (leaving out POS-tagged, phonetic data, processed 'interviewee only' entries):
    intpattern = re.compile(".*necteortho.*")
    intsonly = soup.find_all(name="text", attrs={"id" : intpattern})
    utterances.write(str(intsonly))
    utterances.close()
    return intsonly

def multidorm(text, dormuido=False):
    #opens output file for writing to:
    output2 = open(r"pd_outputs/dectedorms.txt", "w")
    intsonly = decteints(text)
    #dictionary for storing data:
    data = {"Speaker":[], "Line No.":[], "Utterance":[], "Dorm":[], "Dorm-Uido":[]}
    #this will need to be changed to a loop when I have more than one interview; it's the list of utterances in the interview.
    lst = intsonly[0].find_all(name="u")
    print(lst)
    count = 0
    #line number of text as analysed, either poem line or sentence number:
    line = 1
    #dormuido parameter determines whether dorm-uido is included, default is just dorms:
    if dormuido == True:
        #while loop stops one from the end of list entries:
        while count < len(lst)-1:
            #for each string in the list of strings generated above:
            for i in range(len(lst)-1):
                #gets dorm & rounds to 2d.p., gets uido, finds dorm-uido and round to 2.dp:
                #intrview = lst[i].find(attrs={"id"})
                speakr = lst[i].attrs["who"]
                uttrance = lst[i].find(string=True)
                dorm1 = ud.getDORM(uttrance)
                dormf = "{:.2f}".format(dorm1)
                uido1 = ud.dorm(ud.uido(uttrance))
                du1 = float(dorm1) - float(uido1)
                duf = "{:.2f}".format(du1)
                #appends line number, dorm, & dorm-uido to the data dictionary:
                #data["Interview"].append(intrview)
                data["Speaker"].append(speakr)
                data["Line No."].append(line)
                data["Utterance"].append(uttrance)
                data["Dorm"].append(dorm1)
                data["Dorm-Uido"].append(du1)
                #writes those, along with the string analysed, to output file:
                output2.write(str(line)+" "+str(speakr)+": "+str(uttrance)+" DORM: "+str(dormf)+", DORM-UIDO:"+str(duf)+",\n")
                count += 1
                line += 1
        #final run of the loop ensures output text file is formatted without trailing comma:
        #intrview = lst[len(lst)-1].find(attrs={"id"})
        speakr = lst[len(lst)-1].attrs["who"]
        uttrance = lst[len(lst)-1].find(string=True)
        dorm1 = ud.getDORM(uttrance)
        dormf = "{:.2f}".format(dorm1)
        uido1 = ud.dorm(ud.uido(uttrance))
        du1 = float(dorm1) - float(uido1)
        duf = "{:.2f}".format(du1)
        #data["Interview"].append(intrview)
        data["Speaker"].append(speakr)
        data["Line No."].append(line)
        data["Utterance"].append(uttrance)
        data["Dorm"].append(dorm1)
        data["Dorm-Uido"].append(du1)
        #converts the data dictionary into pandas dataframe to be returned:
        #the conversion to dataframe isnt working because arrays arent the same length, returning data dictionary for now:
        #multidormdata = pd.DataFrame.from_dict(data)
        output2.write(str(line)+" "+str(speakr)+": "+str(uttrance)+" DORM: "+str(dormf)+", DORM-UIDO: "+str(duf))
        #closes output file when all is done:
        output2.close()
        return data
    else:
        data = {"Interview":[], "Speaker":[], "Line No.":[], "Utterance":[], "Line/Sentence":[], "Dorm":[]}
        while count < len(lst)-1:
            for i in range(len(lst)-1):
                #intrview = lst[i].find(attrs={"id"})
                speakr = lst[i].attrs["who"]
                uttrance = lst[i].find(string=True)
                dorm1 = ud.getDORM(uttrance)
                dormf = "{:.2f}".format(dorm1)
                #data["Interview"].append(intrview)
                data["Speaker"].append(speakr)
                data["Line No."].append(line)
                data["Utterance"].append(uttrance)
                data["Dorm"].append(dorm1)
                output2.write(str(line)+" "+str(speakr)+": "+str(uttrance)+" SENTENCE DORM:"+str(dormf)+",\n")
                count += 1
                line += 1
        #intrview = lst[len(lst)-1].find(attrs={"id"})
        speakr = lst[len(lst)-1].attrs["who"]
        uttrance = lst[len(lst)-1].find(string=True)
        dorm1 = ud.getDORM(uttrance)
        dormf = "{:.2f}".format(dorm1)
        #data["Interview"].append(intrview)
        data["Speaker"].append(speakr)
        data["Line No."].append(line)
        data["Utterance"].append(uttrance)
        data["Dorm"].append(dorm1)
        #the conversion to dataframe isnt working because arrays arent the same length, returning data dictionary for now:
        #multidormdata = pd.DataFrame.from_dict(data)
        output2.write(str(line)+" "+str(speakr)+": "+str(uttrance)+" SENTENCE DORM:"+str(dormf))
        output2.close()
        return data

        
        
dormy = multidorm(text1, dormuido=True)
print(dormy)
