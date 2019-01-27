import nltk
from textblob import TextBlob
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import json
import numpy as np 


# read dairy file into the system as a list, every item will be a string

def get_diary():
    file_name = "negative"
    with open( file_name, "r") as f:
        diary = f.readlines()
        diary = [x.strip() for x in diary] 
    return diary

# get ghe tone for each dairy
# input: string
# output: json file contain the tone for each sentence, maybe return the main mood
def get_main_tone(diary):
    open('data.json', "w").close()
    outfile = open('data.json', 'a')
    outfile.write('[')
    counter = 0
    for element in diary:
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
    for each_json in tone_dict:
        for tone in each_json['sentences_tone']:
            for index in range(0,len(tone['tones'])):
                mood = tone['tones'][index]['tone_id']
                tone_list.append(mood)
    return tone_list

print(get_main_tone(get_diary()))  

# get the score of your mood
# make a threshold, send message or not, give sources
# input: list of strtings from get_dairy()
# output: score, threshold = -0.6
def get_score(input_diary):
    score = []
    subjectivity = []
    red_flag = ["kill","hurt","cut","hate","worst","horrible","awful","repulsive",
                "loathsome","obnoxious","disgusting","pesky","sad","crying","depressed",
                "anxious","scared","afraid","lethal","die","harm","pointless","fatal","injure",
                "violent","toxic","murder","suicidal"]

    red = 0
    for sentence in input_diary:
        blob = TextBlob(sentence)
        score.append(blob.sentiment[0])
        subjectivity.append(blob.sentiment[1])
        for word in sentence:
            if word in red_flag:
                red = red + 1
    # get average score in range [-1.0, 1.0]
    score = np.array(score)
    subjectivity = np.array(subjectivity)
    mean_score = np.mean(score) + red*(-0.2)
    mean_subjectivity = np.mean(subjectivity) 
    return mean_score

print(get_score(get_diary()))


# if you are "negative" and the score in high, send a message

#def send_message(mood, score):



def main():

if __name__ == "__main__":

"""


blob1 = TextBlob("i hate monday but i love california")
print (format(blob1.sentiment))
"""