import re
import pandas as pd

def preprocess(data):
    # Define the regex pattern for splitting the data based on date-time information
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)?\s?-\s'

    # Split messages and capture the dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create the DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Try parsing the message_date column with a more flexible approach
    # This will attempt to infer the datetime format and handle both 12-hour and 24-hour formats
    df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce', dayfirst=True)

    # Check if any rows could not be parsed and print them out (for debugging)
    if df['message_date'].isnull().sum() > 0:
        print(f"Warning: {df['message_date'].isnull().sum()} rows could not be parsed correctly.")

    # Rename 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    
    # Split the user messages
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # User name is found
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # Group notification
            users.append('group_notification')
            messages.append(entry[0])

    # Add user and message columns
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date-time features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['am_pm'] = df['date'].dt.strftime('%p')  # AM/PM column

    # Create period column (e.g., '01-02', '02-03', etc.) and handle AM/PM logic
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append('11-12 PM')
        elif hour == 0:
            period.append('12-1 AM')
        elif hour < 12:
            period.append(f'{hour}-{hour+1} AM')
        else:
            period.append(f'{hour-12}-{hour-11} PM')

    df['period'] = period

    return df
