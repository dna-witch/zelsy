t_list = ["kill","hurt","cut","hate","worst","horrible","awful","repulsive",
                "loathsome","obnoxious","disgusting","pesky","sad","crying","depressed",
                "anxious","scared","afraid","lethal","die","harm","pointless","fatal","injure",
                "violent","toxic","murder","suicidal"]
def mood_counter(t_list):
    word_counter = {}
    for word in t_list:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    dominate_mood = popular_words[0]
    return dominate_mood


print(mood_counter(t_list))