import json
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import plotly.express as px
import pandas as pd


file_embeddings = defaultdict(list)

with open("../Embedding/clean_embeddings.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        file_name = row["file"]
        embedding = np.array(row["embedding"], dtype=np.float32)
        file_embeddings[file_name].append(embedding)


names = []
vectors = []

for file_name, embs in file_embeddings.items():
    mean_emb = np.mean(embs, axis=0)

    names.append(file_name)
    vectors.append(mean_emb)

vectors = np.array(vectors)
vectors = normalize(vectors)
n_clusters = 6

kmeans = KMeans(
    n_clusters=n_clusters,
    random_state=42,
    n_init="auto"
)

labels = kmeans.fit_predict(vectors)
vectors_pca = PCA(
    n_components=30,
    random_state=42
).fit_transform(vectors)

tsne = TSNE(
    n_components=2,
    perplexity=2,
    init="pca",
    random_state=42
)

coords = tsne.fit_transform(vectors_pca)

df = pd.DataFrame({
    "x": coords[:, 0],
    "y": coords[:, 1],
    "file": names,
    "cluster": labels.astype(str)
})

fig = px.scatter(
    df,
    x="x",
    y="y",
    color="cluster",
    hover_name="file",
    title="KMeans, t-SNE embeddingów",
    opacity=0.8
)

fig.update_layout(
    height=750,
    margin=dict(r=250, l=20, t=50, b=20),
    legend=dict(
        title="Cluster",
        x=1.02,
        y=1,
        bgcolor="rgba(255,255,255,0.7)"
    )
)

fig.show()