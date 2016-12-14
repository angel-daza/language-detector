# -*- coding: utf-8 -*-
from collections import defaultdict
from modules import utils

### FUNCTIONS FOR BUILDING PROFILES...

#Iterates a list of lines, tokenizes each line and returns a list of with
#the individual tokens
def get_tokens(lines):
    bad_chars = u'«»(){}[]<>¡!¿?“”".,_:;0123456789'
    toks = []
    wordcount,charcount = 0,0
    for line in lines:
        words = line.split()
        wordcount += len(words)
        for w in words:
            ww = "".join(ch for ch in w if ch not in bad_chars)
            toks.append(ww.lower())
            charcount += len(ww)
    print("Found {} words and {} characters...".format(wordcount,charcount))
    return toks

#Takes any word and any given size and produces a list of all the possible n-grams
#for that word from 1 to size
def ngramize(word,size):
    ngrams = []
    word = "_"+word
    for i in range(size):
        word += "_"
    for j in range(len(word)-size):
        ngrams.append(word[j:j+size])
    return ngrams

#Takes a list of tokens, produces all possible 1-grams,2-grams,3-grams,4-grams & 5-grams
#and returns a dictionary containing all unique n-grams with their frequency counts
def build_ngram_dict(lang_toks):
    token_counts = defaultdict(int)
    for token in lang_toks:
        for i in range(1,5):
            ngrams = ngramize(token,i)
            for ng in ngrams:
                token_counts[ng]+=1
    return token_counts

#Takes a language_sample object (name and source_file) and builds the language model
#for that split_sample.
#Language model is a list of unique 1-grams to 5-grams ranked by their frequency
def build_language_profile(lang_sample):
    print("******** Building model for {} ********".format(lang_sample["name"].upper()))
    lang_toks = get_tokens(lang_sample["training"])
    lang_dict = build_ngram_dict(lang_toks)
    sorted_counts = sorted(lang_dict.items(),key=lambda x: x[1], reverse=True)
    print("Found with {} different n-grams, but only top {} will be considered...".format(len(sorted_counts),TOP_NGRAMS))
    sorted_counts = sorted_counts[:TOP_NGRAMS]
    lang_profile = {}
    for i in range(len(sorted_counts)):
        lang_profile[sorted_counts[i][0]] = {"rank":i+1,"count":sorted_counts[i][1]}
    return {"name":lang_sample["name"],"profile":lang_profile}

#Takes a string and builds a profile for it,
#in the same manner as the language model profile of a file
def build_text_profile(text):
    lang_toks = get_tokens([text])
    lang_dict = build_ngram_dict(lang_toks)
    sorted_counts = sorted(lang_dict.items(),key=lambda x: x[1], reverse=True)
    sorted_counts = sorted_counts[:TOP_NGRAMS]
    lang_profile = {}
    for i in range(len(sorted_counts)):
        lang_profile[sorted_counts[i][0]] = {"rank":i+1,"count":sorted_counts[i][1]}
    return {"name":"test_case","profile":lang_profile}

### TESTING FUNCTIONS...

#Returns the ranking of an n-gram in a given profile
def get_rank_in_profile(ngram,lang_profile):
    elem = lang_profile.get(ngram,None)
    if elem:
        #print("Ranked {} in lang_model".format(elem["rank"]))
        return elem["rank"]
    else:
        #print("Not Ranked in lang_model")
        return None

#Takes two profiles and return the distance between them.
#Distance is calculated as the number of 'misplacements' that exist between
#the rankings of both profiles.
def compare_profiles(test_profile,lang_profile):
    total_distance = 0
    for ngram in test_profile.keys():
        out_of_place = DEFAULT_PENALTY
        #print("Looking for {}, ranked {} in test profile".format(ngram,test_profile[ngram]["rank"]))
        ranked_in_profile = get_rank_in_profile(ngram,lang_profile)
        if ranked_in_profile: out_of_place = abs(test_profile[ngram]["rank"] - ranked_in_profile)
        total_distance += out_of_place
        #print("Adding {} to distance...".format(out_of_place))
    return total_distance

#Takes a test string and the constructed language profiles. Computes the distance between
#the test string and each of the profiles
def get_text_language(test_case,lang_profiles):
    print("********************************************************************")
    # Receive a text as input and return its language (closest lang_profile)
    test_profile = build_text_profile(test_case)
    scores = [(lang["name"],compare_profiles(test_profile["profile"],lang["profile"])) for lang in lang_profiles]
    sorted_scores = sorted(scores,key=lambda x: x[1])
    #print(sorted_scores)
    #print("")
    print("{}\n\n\tYour Text is Written in {}!".format(test_case,sorted_scores[0][0]))
    return sorted_scores[0][0]

#Used to run the auto-tests from the sample sets. It takes the constructed profiles and
#tries to guess the text language from the test cases (which are already tagged with the answer)
#and then compares the guessed result with the actual one. Return also a True Positive Rate score
def test_language_profiles(profiles,test_set):
    tp,fn = 0,0
    for tag,test_case in test_set:
        result = get_text_language(test_case,profiles)
        if result != tag:
            fn += 1
        else:
            tp+=1
    TPR = tp/float(fn+tp)
    print("\n\nTPR in testing cases was: {}\n".format(TPR))
    return TPR

#Function that keeps the script running interactively in the terminal  until the user quits.
#It lets a user to input any given custom string, and also to input a filepath
#to test a whole document
def interactive_test(language_profiles,language_samples):
    keep_going = True
    while keep_going:
        user_response = input("\nWant to test another TEXT string yourself? (enter option number):\n\t1) Test a string\n\t2) Test the content inside 'test.txt' file\n\t3) Test any document file\n\tPress Any Key to EXIT!\n")
        if user_response == "1":
            print("\nAvailable Languages: {}\n".format(", ".join([l["name"] for l in language_samples])))
            test_string = input("Please write a piece of text:\n\n")
            get_text_language(test_string,language_profiles)
        elif user_response == "2":
            content_list = utils.read_file("test.txt")
            content = " ".join(content_list)
            get_text_language(content,language_profiles)
        elif user_response == "3":
            filepath = input("Please give a valid path for your document:\n\n")
            try:
                content_list = utils.read_file(filepath)
                content = " ".join(content_list)
                get_text_language(content,language_profiles)
            except:
                print("\nI'm sorry I can't find your file! Please TRY AGAIN...")
        else:
            print("\nSee you next time!\n")
            keep_going = False

##################################################################
#################### BUILD MODELS AND TEST THEM ##################
##################################################################
# Configuration Paramaters!
TEST_ENABLED = True
TOP_NGRAMS = 400
DEFAULT_PENALTY = 250
LANGUAGE_SAMPLES = [{"name":"English","file":"resources/english_sample.txt"},
                    {"name":"French","file":"resources/french_sample.txt"},
                    {"name":"German","file":"resources/german_sample.txt"},
                    {"name":"Spanish","file":"resources/spanish_sample.txt"}]

if __name__ == "__main__":
    language_profiles = []
    testing_samples = []
    #1) Build Language Models (Profiles)
    for samp in LANGUAGE_SAMPLES:
        lines = utils.read_file(samp["file"])
        if TEST_ENABLED:
            samp["training"],testing_sample = utils.split_sample(lines,split=0.8)
            testing_samples.extend([(samp["name"],t) for t in testing_sample])
        else:
            samp["training"] = lines
        lang_profile = build_language_profile(samp)
        language_profiles.append(lang_profile)
    #2) Test Models... (If Enabled)
    if TEST_ENABLED:
        test_language_profiles(language_profiles,testing_samples)
        print("--- THE END ---")
    #3) Interactive Console (test user inputs...)
    interactive_test(language_profiles,LANGUAGE_SAMPLES)
