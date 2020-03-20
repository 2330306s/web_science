import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

#specifying database to read from and the txt to write the clusters too
tweets = pd.read_csv("tweets.csv")
file = open("clustered_tweets.txt", "w+")

#using scikitlearn library to manipulate data to comply with the code
vect = TfidfVectorizer(stop_words='english')

#clustering user ids
db_user_ids = tweets['user_id']
vect_user_ids = vect.fit_transform(db_user_ids)
clustered_vect_user_ids = KMeans(n_clusters=5, init='k-means++', max_iter=50, n_init=1)
clustered_user_ids = (clustered_vect_user_ids.fit(vect_user_ids)).labels_.tolist()
user_id_cluster = { 'user_id': db_user_ids, 'cluster': clustered_user_ids}
user_id_frame = pd.DataFrame(user_id_cluster, index=[clustered_user_ids], columns=['user_id', 'cluster'])
file.write("User ID Cluster: \n")
order_centroids = clustered_vect_user_ids.cluster_centers_.argsort()[:, ::-1]
for i in range(5):
    file.write(str(i+1) + "\n")
    for j in order_centroids[i, :5]:
        file.write(str(vect.get_feature_names()[i]) + "\n")

#clustering hashtags
db_hashtags = tweets['hashtags']
vect_hashtags = vect.fit_transform(db_hashtags)
clustered_vect_hashtags = KMeans(n_clusters=5, init='k-means++', max_iter=50, n_init=1)
clustered_hashtags = (clustered_vect_hashtags.fit(vect_hashtags)).labels_.tolist()
hashtags_cluster = { 'hashtags': db_hashtags, 'cluster': clustered_hashtags}
hashtags_frame = pd.DataFrame(hashtags_cluster, index=[clustered_hashtags], columns=['hashtags', 'cluster'])
file.write("Hashtag Cluster: \n")
order_centroids = clustered_vect_hashtags.cluster_centers_.argsort()[:, ::-1]
for i in range(5):
    file.write(str(i+1) + "\n")
    for j in order_centroids[i, :5]:
        file.write(str(vect.get_feature_names()[i]) + "\n")

#clustering text
db_texts = tweets['text']
vect_texts = vect.fit_transform(db_texts)
clustered_vect_texts = KMeans(n_clusters=5, init='k-means++', max_iter=50, n_init=1)
clustered_texts = clustered_vect_texts.fit(vect_texts).labels_.tolist()
text_cluster = {'text': db_texts, 'cluster': clustered_texts}
text_frame = pd.DataFrame(text_cluster, index=[clustered_texts], columns=['text', 'cluster'])
file.write("Text Cluster: \n")
order_centroids = clustered_vect_texts.cluster_centers_.argsort()[:, ::-1]
for i in range(5):
    file.write(str(i+1) + "\n")
    for j in order_centroids[i, :5]:
        file.write(str(vect.get_feature_names()[i]) + "\n")

file.close()
