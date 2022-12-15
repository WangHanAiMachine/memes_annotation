# import sqlite3
# import pandas as pd

# import csv


# tweet = pd.read_csv("questionBank/tweet.csv")
# hate_exp_wo = pd.read_csv("questionBank/tweetHateExplanation.csv")
# nonhate_exp_wo = pd.read_csv("questionBank/tweetNonHateExplanation.csv")
# hate_exp_step = pd.read_csv("questionBank/tweetHateExplanationWithDetails.csv")
# nonhate_exp_step = pd.read_csv("questionBank/tweetNonHateExplanationWithDetails.csv")
# contxt_exp = pd.read_csv("questionBank/tweetContextExplanation.csv")

# tweet = csv.reader(open('questionBank/tweet.csv')) 
# lines = list(tweet)
# newLines = list()
# for i in range(len(lines)):
#     if((i+1) % 11 != 0):
#         newLines.append(lines[i])
    
# for  i in range(len(newLines)-1):
#     # print(lines)
#     newLines[i+1][0] = i


# writer = csv.writer(open('tweet.csv', 'w'))
# writer.writerows(newLines)



# tweet = csv.reader(open('questionBank/tweetHateExplanation.csv')) 
# lines = list(tweet)
# newLines = list()
# for i in range(len(lines)):
#     if((i+1) % 11 != 0):
#         newLines.append(lines[i])
    
# for  i in range(len(newLines)-1):
#     # print(lines)
#     newLines[i+1][0] = i


# writer = csv.writer(open('tweetHateExplanation.csv', 'w'))
# writer.writerows(newLines)



# tweet = csv.reader(open('questionBank/tweetNonHateExplanation.csv')) 
# lines = list(tweet)
# newLines = list()
# for i in range(len(lines)):
#     if((i+1) % 11 != 0):
#         newLines.append(lines[i])
    
# for  i in range(len(newLines)-1):
#     # print(lines)
#     newLines[i+1][0] = i


# writer = csv.writer(open('tweetNonHateExplanation.csv', 'w'))
# writer.writerows(newLines)



# tweet = csv.reader(open('questionBank/tweetHateExplanationWithDetails.csv')) 
# lines = list(tweet)
# newLines = list()
# for i in range(len(lines)):
#     if((i+1) % 11 != 0):
#         newLines.append(lines[i])
    
# for  i in range(len(newLines)-1):
#     # print(lines)
#     newLines[i+1][0] = i


# writer = csv.writer(open('tweetHateExplanationWithDetails.csv', 'w'))
# writer.writerows(newLines)



# tweet = csv.reader(open('questionBank/tweetNonHateExplanationWithDetails.csv')) 
# lines = list(tweet)
# newLines = list()
# for i in range(len(lines)):
#     if((i+1) % 11 != 0):
#         newLines.append(lines[i])
    
# for  i in range(len(newLines)-1):
#     # print(lines)
#     newLines[i+1][0] = i

# writer = csv.writer(open('tweetNonHateExplanationWithDetails.csv', 'w'))
# writer.writerows(newLines)



# tweet = csv.reader(open('questionBank/tweetContextExplanation.csv')) 
# lines = list(tweet)
# newLines = list()
# for i in range(len(lines)):
#     if((i+1) % 11 != 0):
#         newLines.append(lines[i])
    
# for  i in range(len(newLines)-1):
#     # print(lines)
#     newLines[i+1][0] = i

# writer = csv.writer(open('tweetContextExplanation.csv', 'w'))
# writer.writerows(newLines)