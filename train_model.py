import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

data = pd.read_csv("movies.csv")

data['combined'] = data['genre'] + " " + data['description']

vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(data['combined'])

similarity = cosine_similarity(vectors)

pickle.dump(similarity, open("similarity.pkl", "wb"))
pickle.dump(data, open("movies_data.pkl", "wb"))

print("Model trained successfully")
