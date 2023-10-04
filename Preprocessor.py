import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split messages based on the timestamp pattern
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    user = []
    messages = []
    for message in df['user_message']:
        # Extract the user and message content based on different formats
        if re.search('([\w\w]+?):\s', message):
            entry = re.split('([\w\w]+?):\s', message)
            user.append(entry[1])
            messages.append(entry[2])
        elif re.search('([\w\w\s]+?) joined the group', message):
            user.append('group_notification')
            messages.append('joined the group')
        else:
            user.append('group_notification')
            messages.append(message)

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df.sort_values('date', inplace=True)  # Sort DataFrame by date

    return df
