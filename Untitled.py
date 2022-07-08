#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd


# In[2]:


f = open('WhatsApp Chat with Official Third Year.txt','r', encoding='utf-8')


# In[3]:


data =f.read()


# In[4]:


print(data)


# In[5]:


pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'


# In[6]:


messages= re.split(pattern , data)[1:]
messages


# In[7]:


dates = re.findall(pattern , data)
dates


# In[8]:


df = pd.DataFrame({'user_message':messages, 'message_date':dates})
#convert message_data type
df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

df.rename(columns={'message_date': 'date'}, inplace=True)
df.head()


# In[9]:


df.shape


# In[10]:


#separate users and messages
users = []
messages =[]
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]:#user name
        users.append(entry[1])
        messages.append(entry[2])
    else:
        users.append('group_notification')
        messages.append(entry[0])
        
df['user'] = users
df['message'] = messages
df.drop(columns=['user_message'], inplace=True)
df.head()


# In[11]:


df['year'] = df['date'].dt.year


# In[12]:


df.head()


# In[13]:


df['month'] = df['date'].dt.month_name()


# In[14]:


df['day'] = df['date'].dt.day


# In[15]:


df['hour'] = df['date'].dt.hour


# In[16]:


df['minute'] = df['date'].dt.minute


# In[17]:


df.head()


# In[18]:


df


# In[19]:


df[df['user'] == 'Prof. Pravin Maliviya']


# In[20]:


df[df['user'] == 'Prof. Pravin Maliviya'].shape


# In[21]:


#for message in df['message']:
    #print(message.split())
    
words = []
for message in df['message']:
    words.extend(message.split())


# In[22]:


len(words)


# In[23]:


from urlextract import URLExtract

extractor = URLExtract()
urls = extractor.find_urls("Let's www.gmail.com have URL stackoverflow.com as an example google.com, http://facebook.com")
urls


# In[24]:


links = []

for message in df['message']:
    links.extend(extractor.find_urls(message))


# In[25]:


links


# In[26]:


len(links)


# In[27]:


df


# In[28]:


x =df['user'].value_counts().head()


# In[29]:


import matplotlib.pyplot as plt


# In[30]:


name = x.index
count = x.values


# In[31]:


plt.bar(name, count)
plt.xticks(rotation='vertical')
plt.show()


# In[32]:


round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})


# In[42]:


temp = df[df['user'] != 'group_notification']
temp = temp[temp['message'] != '<Media omitted>\n']


# In[46]:


f = open('hinglish.txt','r')
stop_words = f.read()


# In[52]:


words = []
for message in temp['message']:
    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)


# In[53]:


from collections import Counter 
pd.DataFrame(Counter(words).most_common(20))


# In[56]:


pip install emoji


# In[57]:


import emoji


# In[58]:


emojis =[]
for message in df['message']:
    emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])


# In[59]:


pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


# In[60]:


df['month_num'] = df['date'].dt.month


# In[65]:


timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()


# In[66]:


timeline


# In[70]:


time = []
for i in range(timeline.shape[0]):
    time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))


# In[72]:


timeline['time'] = time


# In[73]:


timeline


# In[77]:


plt.plot(timeline['time'],timeline['message'])
plt.xticks(rotation='vertical')
plt.show()


# In[78]:


df['only_date'] = df['date'].dt.date


# In[80]:


daily_timeline = df.groupby('only_date').count()['message'].reset_index()


# In[82]:


plt.figure(figsize=(18,10))
plt.plot(daily_timeline['only_date'],daily_timeline['message'])


# In[83]:


df.head()


# In[85]:


df['day_name'] = df['date'].dt.day_name()


# In[86]:


df['day_name'].value_counts()


# In[87]:


df.head()


# In[89]:


period =[]
for hour in df[['day_name','hour']]['hour']:
    if hour ==23:
        period.append(str(hour) + "-" + str('00'))
    elif hour == 0:
        period.append(str('00') + "-" + str(hour+1))
    else:
        period.append(str(hour) + "-" + str(hour+1))


# In[90]:


df['period'] = period


# In[92]:


df.sample(5)


# In[93]:


import seaborn as sns 
plt.figure(figsize=(20,6))
sns.heatmap(df.pivot_table(index='day_name', columns='period', values='message',aggfunc='count').fillna(0))
plt.yticks(rotation='horizontal')
plt.show()


# In[94]:


df.pivot_table(index='day_name', columns='period', values='message',aggfunc='count').fillna(0)


# In[ ]:




