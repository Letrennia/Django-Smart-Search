import json
import os
import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_articles = os.path.join(BASE_DIR, "clean_embeddings.jsonl")

def find_similar_embeddings(query):
    # MODEL READING
    model_path = "ibm-granite/granite-embedding-small-english-r2"

    model = AutoModel.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model.eval()

    tokenized_queries = tokenizer([query], padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        output = model(**tokenized_queries)

    query_embedding = output.last_hidden_state[:, 0]
    query_embedding = torch.nn.functional.normalize(query_embedding, dim=1)

    query_embedding = query_embedding.float().cpu().numpy()
    query_embedding = query_embedding.squeeze()

    # COMPARE WITH COSINE SIMILARITY
    articles = []

    with open(input_articles, "r") as f:
        for line in f:
            row = json.loads(line)

            emb = np.array(row["embedding"], dtype=np.float32)
            score = cosine_similarity(query_embedding.reshape(1, -1), emb.reshape(1, -1))[0][0]

            articles.append({"file": row["file"],
                             "chunk": row["chunk"],
                             "score": float(score)})


    articles.sort(key=lambda x: x["score"], reverse=True)

    seen = set()
    no_duplicates = []

    for article in articles:
        filename = article["file"]
        if filename not in seen:
            no_duplicates.append(article)
            seen.add(filename)

    return no_duplicates





# articles_found = find_similar_embeddings('should i change debug before deploy')


# WRITE OUT
# for art in articles_found[:20]:
#     print(
#         f"score={art['score']} "
#         f"file={art['file']} "
#         f"chunk={art['chunk']}"
#     )