import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle):

    twitter_consumer_key = '9VSguSseAFetKCYzWONhaWD4b'
    twitter_consumer_secret = 'uFhK6cLddaeokNt2r65vXiLTQLfwLsYi7btnjVS37db2lQkQAH'
    twitter_access_token = '980916831358783488-NwtW6sAIql66zbxKEphFWWBa8MVCZXa'
    twitter_access_secret = '1UBtANdCVCVVcNb9R84YFPjGJDiKpzIZh3vkgdwGQ5SPc'

    twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                  consumer_secret=twitter_consumer_secret,
                  access_token_key=twitter_access_token,
                  access_token_secret=twitter_access_secret)


    statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

    text = "" 
    for s in statuses:
        if (s.lang =='en'):
            text += s.text.encode('utf-8')

    pi_username = '8363e7d3-be33-413b-9946-5591356c676f'
    pi_password = 'l5IsZA4g0hOH'

    personality_insights = PersonalityInsights(username=pi_username,password=pi_password)

    pi_result = personality_insights.profile(text)

    return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
  
def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data
  
user_handle = "@Cristiano"
celebrity_handle = "@KingJames"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

#First, flatten the results from the Watson PI API
user = flatten(user_result)
celebrity = flatten(celebrity_result)

#Then, compare the results of the Watson PI API by calculating the distance between traits
compared_results = compare(user,celebrity)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    print keys,
    print(user[keys]),
    print ('->'),
    print (celebrity[keys]),
    print ('->'),
    print (compared_results[keys])