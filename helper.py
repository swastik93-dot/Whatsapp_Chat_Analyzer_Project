import pandas as pd
import os
from wordcloud import WordCloud
from collections import Counter
def fetch_stats(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  # fetch total number of messages
  num_messages = df.shape[0]

  # fetch total number of words
  words = []
  for message in df['message']:
    words.extend(message.split())

  # fetch total number of media messages
  num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

  return num_messages, len(words), num_media_messages

def most_busy_users(df):
  x = df['user'].value_counts().head()
  df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
       columns = {'index':'name','user':'percent'})
  return x,df


def create_wordcloud(selected_user, df):


  file_path = os.path.join(os.path.dirname(__file__), 'stop_hinglish.txt')
  f = open(file_path, 'r')

  stop_words = f.read()
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  temp = df[df['user'] != 'group_notification']
  temp = temp[temp['message'] != '<Media omitted>\n']

  wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
  df_wc = wc.generate(' '.join(temp['message'].tolist()))
  return df_wc


def most_common_words(selected_user,df):
  # stop_words == file
  # stop_wordss == variable

  file_path = os.path.join(os.path.dirname(__file__), 'stop_hinglish.txt')
  f = open(file_path, 'r')

  stop_words = f.read()
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  temp =  df[df['user'] != 'group_notification']
  temp = temp[temp['message'] != '<Media omitted>\n']

  words = []
  for message in temp['message']:
    for word in message.lower().split():
      if word not in stop_words:
        words.append(word)

  most_common_df = pd.DataFrame(Counter(words).most_common(20))
  return  most_common_df


