import os
import re
import nltk
from nltk.corpus import stopwords
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer

input_dir = "../clean_data"
texts = []
nltk.download("stopwords")

for filename in os.listdir(input_dir):
    path = os.path.join(input_dir, filename)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "[TEXT]" in content:
        text = content.split("[TEXT]")[1].split("[VECTOR]")[0].strip()
        texts.append(text)


stopwords_en = set(stopwords.words("english"))
remove_words = {"django", "use", "example"}

def clean_text(t):
    words = re.findall(r"\b\w+\b", t.lower())
    return " ".join(
        w for w in words
        if w not in stopwords_en and w not in remove_words
    )

texts_clean = [clean_text(t) for t in texts]

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

umap_model = UMAP(
    n_neighbors=15,
    n_components=10,
    min_dist=0.1,
    metric="cosine",
    low_memory=True
)

hdbscan_model = HDBSCAN(
    min_cluster_size=80,
    min_samples=15,
    metric="euclidean",
    cluster_selection_method="eom",
    prediction_data=False
)

vectorizer_model = CountVectorizer(stop_words=list(stopwords_en | remove_words))
ctfidf_model = ClassTfidfTransformer()

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    calculate_probabilities=False,
    verbose=True
)

topics, probs = topic_model.fit_transform(texts_clean)

topic_model.visualize_topics()
topic_model.visualize_heatmap()
topic_model.visualize_barchart(top_n_topics=20)
