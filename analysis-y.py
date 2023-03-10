import json
import gensim.corpora as corpora
import gensim
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

with open("articles.json", "r") as f:
    articles = json.load(f)

# texts=[]
# for article in articles:
#     texts.append(article["preprocessed"])
# texts = [article["preprocessed"] for article in articles]
# # splittokens = []
# # for text in texts:
# #     tokens = text.split()
# #     splittokens.append(tokens)
# splittokens=[text.split() for text in texts]
splittokens = [article["preprocessed"].split() for article in articles]

id2word = corpora.Dictionary(splittokens)
corpus = [id2word.doc2bow(text) for text in splittokens]
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word,
                                            num_topics=20)
# print(lda_model.print_topics(1))
# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))
# Compute Coherence Score
coherence_model_lda = gensim.models.CoherenceModel(model=lda_model,
                                                   texts=splittokens, dictionary=id2word, coherence='u_mass')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

topics_counts = []
perplexity_vals = []
coherence_vals = []

for num_topics in range(10, 31):
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word,
                                                num_topics=num_topics)
    perplexity = lda_model.log_perplexity(corpus)
    coherence_model_lda = gensim.models.CoherenceModel(model=lda_model,
                                                       texts=splittokens, dictionary=id2word, coherence='u_mass')
    coherence_lda = coherence_model_lda.get_coherence()
    topics_counts.append(num_topics)
    perplexity_vals.append(perplexity)
    coherence_vals.append(coherence_lda)
plt.figure()
plt.plot(topics_counts, perplexity_vals, 'ro-')
plt.xlabel('topics_counts')
plt.ylabel('perplexity_vals')
plt.show()

plt.figure()
plt.plot(topics_counts, coherence_vals, 'bo-')
plt.xlabel('topics_counts')
plt.ylabel(' coherence_vals')
plt.show()


def assignrank(x, y, reverse=False):
    xy = []
    for i in range(len(x)):
        xy.append((x[i], y[i]))  # [(x[i],y[i]),(x[i+1],y[i+1])]
    xy = sorted(xy, key=lambda u: u[1], reverse=reverse)
    rank = {}
    for i in range(len(xy)):
        xyi = xy[i]
        rank[xyi[0]] = i
    return rank


rank1 = assignrank(x=topics_counts, y=perplexity_vals, reverse=False)
rank2 = assignrank(x=topics_counts, y=coherence_vals, reverse=True)

weight = 0.8

best_topic_count = -1
best_rank = 10000
for topic_count in range(10, 31):
    combined_rank = weight * rank1[topic_count] + (1 - weight) * rank2[topic_count]
    if combined_rank < best_rank:
        best_rank = combined_rank
        best_topic_count = topic_count

print(best_topic_count)

lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word,
                                            num_topics=best_topic_count)

topics = lda_model.show_topics(num_topics=-1, num_words=20, formatted=False)

df = pd.DataFrame()

print(topics)

for topic in topics:
    column_name = topic[0]
    keywords = []
    for keyword in topic[1]:
        keywords.append(keyword[0])
    df[str(column_name)] = keywords
print(df)
print(df.to_latex())

### 9

documents_topics = lda_model.get_document_topics(corpus, minimum_probability=0.0)

twodarray = np.zeros((len(articles), best_topic_count))
print(twodarray)
for i in range(len(documents_topics)):
    document_topics = documents_topics[i]
    print(document_topics)
    for j in range(len(document_topics)):
        document_topic = document_topics[j]
        topic_id = document_topic[0]
        prob = document_topic[1]
        twodarray[i][topic_id] = prob
print(twodarray)

print(np.argmax(twodarray, axis=0))
print(np.argmax(twodarray, axis=1))
