import nltk
from textblob import TextBlob
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException
import json



text = "It was a rough day, I hate my teacher he is a dick. i need to see my friends i miss them. i am sad. "

tone_analyzer = ToneAnalyzerV3(
				version='2017-09-21',
				username='ericawu3811@hotmail.com',
				password='1qaZ2wsX',
				url='https://gateway.watsonplatform.net/tone-analyzer/api')

tone_analysis = tone_analyzer.tone({'text': text}, 'application/json').get_result() 


print(json.dumps(tone_analysis, indent=2))

"""


blob1 = TextBlob("i hate monday but i love california")
print (format(blob1.sentiment))
"""