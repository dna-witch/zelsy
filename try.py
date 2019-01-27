import nltk
from textblob import TextBlob
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import json
from nltk.tokenize import TweetTokenizer
import numpy as np 
from twilio.rest import Client


# read dairy file into the system as a list, every item will be a string
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

def get_diary():
    #file_name = "negative"
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

# most frequent mood
# input: list 
# output: list of only one element 
def mood_counter(t_list):
    word_counter = {}
    for word in t_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    dominant_mood = popular_words[0]
    return dominant_mood


# get the score of your mood
# make a threshold, send message or not, give sources
# input: list of strtings from get_diary()
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
        sentence = tknzr.tokenize(sentence)
        for word in sentence:
            if word in red_flag:
                red = red + 1
    # get average score in range [-1.0, 1.0]
    score = np.array(score)
    subjectivity = np.array(subjectivity)
    mean_score = np.mean(score)+ red*(-0.2)
    mean_subjectivity = np.mean(subjectivity) 
    
    return mean_score


# if you are "negative" and the score in high, send a message
# Your Account SID from twilio.com/console
account_sid = "ACe9dcc22c9db899868a627562292d7c4b"
# Your Auth Token from twilio.com/console
auth_token  = "0071b3cf8c984f389f9eb1e1b631806b"
def send_message(dominant_mood, score):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+19258954933",
        from_="+18052629284",
        body="Hello from Zelsy! Our goal at Zelsy is to connect people and teach them about mental health.")

    print(message.sid)
    if dominant_mood in ["sadness", "angry", "fear"] and score < float(-0.6):
        
        message = client.messages.create(
            to="+19258954933",
            from_="+18052629284",
            body="Hello from Zelsy! Your friend, Erica, is in need of your friendship and support right now!")

        print(message.sid)



if __name__ == "__main__":
    file_name = "negative"
    #file_name = "text"
    #print(get_main_tone(get_diary()))
    input_text = get_diary()
    mood_list = get_main_tone(input_text)
    dominant_mood = mood_counter(mood_list)
    score = get_score(input_text)

    print("Your mood score is %f" %get_score(input_text))
    print("Your dominant mood is " + mood_counter(mood_list))
    send_message(dominant_mood, score)
