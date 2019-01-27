import nltk
from textblob import TextBlob
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import json


# read dairy file into the system as a list, every item will be a string

def get_dairy():
    file_name = "text"
    with open( file_name, "r") as f:
        dairy = f.readlines()
        dairy = [x.strip() for x in dairy] 
    return dairy

# get ghe tone for each dairy
# input: string
# output: json file contain the tone for each sentence, maybe return the main mood
def get_main_tone(dairy):
    outfile = open('data.json', 'a')
    outfile.write('[')
    counter = 0
    for element in dairy:
        # analysis of tone for each sentence
        tone_analyzer = ToneAnalyzerV3(
                        version='2017-09-21',
                        iam_apikey = 'EWXcYvK8jEhxlasD-ptCuuVRGJq3xcSUeqWYYRaZYQ2G',
                        url='https://gateway.watsonplatform.net/tone-analyzer/api')

        tone_analysis = tone_analyzer.tone({'text': element}, 'application/json').get_result() 
        

        if counter == 0:
            # do not add ,
            json.dump(tone_analysis, outfile)
            counter += 1
            
        else:
            # add ,
            outfile.write(',')
            outfile.write('\n')
            json.dump(tone_analysis, outfile)
           
    
    outfile.write(']')
    outfile.close()
        #print(json.dumps(tone_analysis, indent=2))

    with open('data.json', 'r') as f:
        tone_dict = json.load(f)


    # get list of mood
    tone_list = []
    for tone in tone_dict['sentences_tone']:
        for index in range(0,len(tone['tones'])):
            mood = tone['tones'][index]['tone_id']
            print(mood)
            tone_list.append(mood)
    return tone_list

print(get_main_tone(get_dairy()))  

# get the score of your mood
# make a threshold, send message or not, give sources
# input: string
# output: score
# def get_score(text):



# # fitbit
# def fitbit_score():


# # if you are "negative" and the score in high, send a message
# # topolio?
# def send_message(mood, score):



# def main():

"""


blob1 = TextBlob("i hate monday but i love california")
print (format(blob1.sentiment))
"""