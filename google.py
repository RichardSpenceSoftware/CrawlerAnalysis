# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 16:26:08 2022

@author: Richard.Spence
"""
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import mysql.connector

db = mysql.connector.connect(host="localhost", user="newuser", passwd="Password123")
pointer = db.cursor()
pointer.execute("use sys")
pointer.execute("SELECT * FROM google")
googleframe = pointer.fetchall()
googleframe = DataFrame(googleframe,columns =['Review Id','Review','Star Rating','Date','Likes','Company'])
googleframe['DATE'] = pd.to_datetime(googleframe['Date'])
googleframe["Star Rating"] = pd.to_numeric(googleframe["Star Rating"])
googleframe = googleframe.sort_values(by="Date")
plt.plot(googleframe['Date'], googleframe['Star Rating'])
plt.title('Average Star Rating per Year')
plt.xlabel('Date')
plt.ylabel('Star Rating')
plt.axhline(googleframe["Star Rating"].mean(), color='green', linestyle='--')
plt.show()

googleframe.plot.scatter(x = 'Likes', y = 'Star Rating')
plt.show()

googleframe['Length'] = googleframe['Review'].apply(len)

googleframe.plot.scatter(x = 'Length', y = 'Star Rating')
plt.show()


import nltk, re, numpy as np, pandas as pd
from nltk.tokenize import word_tokenize as wt, sent_tokenize as st
import pyLDAvis
import pyLDAvis.gensim_models
import gensim
import string
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import gensim.corpora
import matplotlib.colors as mcolors
import matplotlib.dates
from wordcloud import WordCloud
from dateutil import parser

df = googleframe
df.columns=['REVIEW ID','REVIEW','RATING','DATE','LIKES','COMPANY','Date','LENGTH']


df.dropna(subset =["DATE","REVIEW"],inplace=True)
stopList = list(nltk.corpus.stopwords.words('english'))
#additional stopwords
stopList.extend(['get','netflix','u','ve'])
lemmatizer = WordNetLemmatizer()
punct = string.punctuation +"``“”£"

def untokenize(doc):
    review = " ".join(doc)
    
    return review 
   
reviews = list(df['REVIEW'].values)
ratings = list(df['RATING'].values)
dates = list(df['DATE'].values)
dates = [parser.parse(date) for date in dates]
df['DATE'] = dates

########### SENTIMENT ANALYSIS ##################
sents = []
subs = []
for doc in reviews:
    sentiment = TextBlob(doc).sentiment
    polarity = sentiment.polarity
    subj = sentiment.subjectivity
    sents.append(polarity)
    subs.append(subj)
df['Polarity'] = sents
df['Subjectivity'] = subs

## plot of review sentiment as a function of time

dates = matplotlib.dates.date2num(df['DATE'])
plt.plot_date(dates, df['Polarity'])
plt.title("sentiment over time")
plt.ylabel('Polarity')
plt.show()

reviewWords = [wt(review) for review in reviews]
all_unfiltered = []
for doc in reviewWords:
    for word in doc:
        all_unfiltered.append(word)
#apply sentence tokenizing before punctuation removal to preserve sentence structure

#sents = [st(review) for review in reviews]

        
############## NGRAMMER ###############


bigram_phrases = gensim.models.Phrases(reviewWords, min_count=6, threshold=50)    
trigram_phrases = gensim.models.Phrases(bigram_phrases[reviewWords],min_count=3, threshold=50)
bigram = gensim.models.phrases.Phraser(bigram_phrases)
trigram =  gensim.models.phrases.Phraser(trigram_phrases)

def make_bigrams(texts):
    return(bigram[doc] for doc in texts)

def make_trigrams(texts):
    return(trigram[doc] for doc in texts)
  
data_bigrams = make_bigrams(reviewWords)
data_bigrams_trigrams = make_trigrams(data_bigrams)
bigrams_list = []
for i in data_bigrams:
    bigrams_list.append(i)

filtered_bigrams = []
for review in bigrams_list:
    filtered = [w.lower() for w in review if w not in stopList]
    filtered_bigrams.append(filtered)
    
def clean_text_round1(text):
    #lowercase
    
    #replace square brackets and content inside with ''
    text = re.sub('\[.*?\]', '', text)
    #remove instances of punctuation
    text = re.sub('[%s]' % re.escape(punct), '', text)
    #remove numbers and words attached to numbers
    text = re.sub('\w*\d\w*', '', text)
    
    return text
clean_bigrams = []
for doc in filtered_bigrams:
    doc = [clean_text_round1(word) for word in doc if word not in stopList]
    doc = list(filter(None, doc))
    #clean_bigram = pos_tag(doc)
    clean_bigrams.append(doc)



############### LEMMATIZER #########################

    
def lemmatize_with_postag(sentence):
    sent = TextBlob(sentence)
    tag_dict = {"J": 'a', 
                "N": 'n', 
                "V": 'v', 
                "R": 'r'}
    words_and_tags = [(w, tag_dict.get(pos[0], 'n')) for w, pos in sent.tags]    
    lemmatized_list = [wd.lemmatize(tag) for wd, tag in words_and_tags]
    return " ".join(lemmatized_list)    
    


lems = []
all_words = []

for doc in clean_bigrams:
    lem = [lemmatize_with_postag(word) for word in doc]
    for word in lem:
        if word not in stopList:
            all_words.append(word)
    lems.append(lem)
    
    
    
    
df['Lemmas'] = lems    
df.to_csv('netflixAnalyzed.csv', encoding='utf-8')
# pos_revs = []
# neg_revs = []
# for i in range(len(lems)):
#         if ratings[i] == 'neg':
#             neg_revs.append(lems[i])
#         elif ratings[i] == 'pos':
#             pos_revs.append(lems[i])
# cs_pos = 0
# cs_neg = 0
# test = 'problem'
# for doc in pos_revs:
    
#     if test in doc:
#         cs_pos = cs_pos + 1
    
#     pos_percent = cs_pos/len(pos_revs)*100    
        
# for doc in neg_revs:
    
#     if test in doc:
#         cs_neg = cs_neg + 1
#     neg_percent = cs_neg/len(neg_revs)*100    
    
    
# plt.bar(['positive','negative'],[pos_percent,neg_percent])
# plt.title("occurrences of: "+test+" in doc")
# plt.ylabel("percentage occurence")       
# plt.show() 
#random.shuffle(lems)  

############ WORD2VEC MODEL ##############


# model = Word2Vec(lems, workers=4,  min_count=5, window=10, sample=1e-3)
# #print("Words that are similar to customerservice:" , model.wv.most_similar('service',topn=6))
# #print("Words that are similar to problem:" , model.wv.most_similar('problem',topn=6))

# vocab = list(model.wv.key_to_index)
# X = model.wv[vocab]

# tsne = TSNE(n_components=2)
# X_tsne = tsne.fit_transform(X)

# w2v_dataframe = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
# Xvec = w2v_dataframe['x']
# Yvec = w2v_dataframe['y']
# fig = plt.figure()
# ax = fig.add_subplot(111)

# ax.scatter(Xvec,Yvec)
# ax.scatter(Xvec[10],Yvec[10],s=10, c='r', marker="o", label='second')
# plt.show()

################## LDA MODEL #################

#create a dictionary of all the words found 
words = gensim.corpora.Dictionary([d for d in lems])
#change the number of topics to look for here
LDAtopics = 16
#converts to bag of words
corpus = [words.doc2bow(doc) for doc in lems]

LDA = gensim.models.ldamodel.LdaModel(corpus = corpus,
                                      id2word = words,
                                      num_topics = LDAtopics,
                                      random_state=2,
                                      update_every=1,
                                      passes=10,
                                      alpha='auto',
                                      per_word_topics=True)
LDA.print_topics()
#minimize this for maximum efficiency of LDA model
print('LDA model perplexity: ', LDA.log_perplexity(corpus))
# coherence_model_lda = CoherenceModel(model=LDA, texts=lems, dictionary=words, coherence='c_v')
# coherence_lda = coherence_model_lda.get_coherence()
# print('\nCoherence Score: ', coherence_lda)




lda_vis = pyLDAvis.gensim_models.prepare(LDA, corpus, words)
pyLDAvis.display(lda_vis)
pyLDAvis.save_html(lda_vis, './FileModel'+ str(LDAtopics) +'.html')

def format_topics_sentences(ldamodel=LDA, corpus=corpus, texts=lems):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)


df_topic_sents_keywords = format_topics_sentences(ldamodel=LDA, corpus=corpus, texts=lems)

df['Dominant_topic'] = df_topic_sents_keywords.Dominant_Topic
df['Topic_contribution'] = df_topic_sents_keywords.Perc_Contribution

doc_model = [LDA.get_document_topics(doc) for doc in corpus]
xs = []
ys = []
multis = []
topics = [0 for i in range(LDAtopics)]
labels = ['topic '+str(i) for i in range(LDAtopics)]
for i in doc_model:
    
        theta = i[0][0]
        topics[theta] += 1
        r = i[0][1]
        xs.append(theta)
        ys.append(r)
area = 200
colors = 2 * np.pi * np.random.rand(len(xs))

#venn_labels = venn.get_labels(doc_model,fill=['logic','number'])
#fig, ax = venn.venn2(venn_labels, names=labels)
#fig.savefig('venn2.png', bbox_inches='tight')
#plt.close()
#plots = plt.figure()
#ax = plots.add_subplot(projection='polar',label="Document-topic allocation")

#c = ax.scatter(xs, ys, c=colors, s=area, cmap='hsv', alpha=0.75)



plt.bar(labels,topics)
plt.title("Document-topic allocation")
plt.ylabel("doc count. Total: "+str(len(xs)))
plt.show()

for topic in LDA.print_topics():
    print("Topic: ")
    print(topic)

################## WORDCLOUD ##########################


cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

cloud = WordCloud(stopwords=stopList,
                  background_color='white',
                  width=2500,
                  height=1800,
                  max_words=10,
                  colormap='tab10',
                  color_func=lambda *args, **kwargs: cols[i],
                  prefer_horizontal=1.0)

topics = LDA.show_topics(formatted=False)

fig, axes = plt.subplots(1, 2, figsize=(10,10), sharex=True, sharey=True)

for i, ax in enumerate(axes.flatten()):
    fig.add_subplot(ax)
    topic_words = dict(topics[i][1])
    cloud.generate_from_frequencies(topic_words, max_font_size=300)
    plt.gca().imshow(cloud)
    plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
    plt.gca().axis('off')


plt.subplots_adjust(wspace=0, hspace=0)
plt.axis('off')
plt.margins(x=0, y=0)
plt.tight_layout()
plt.show()


############ FREQUENCY PLOT #################
print(len(all_unfiltered)-len(all_words))

frequency_graph = nltk.FreqDist(all_words)
frequency_graph.plot(20,cumulative=False)



########### DOCUMENT-TERM MATRIX #############




untokes = []

for i in df.Lemmas:
    dtm_rev = untokenize(i)
    untokes.append(dtm_rev)
    

from sqlalchemy import create_engine

hostname="localhost"
dbname="sys"
uname="newuser"
pwd="Password123"

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

df.to_sql('PilotTrust', engine, index=False)
