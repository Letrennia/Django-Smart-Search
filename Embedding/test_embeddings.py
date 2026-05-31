import json
import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity


# MODEL READING

model_path = "ibm-granite/granite-embedding-small-english-r2"

model = AutoModel.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()


# QUESTIONS
# query = "How do I create a django project?"
query = "should i change debug before deploy"



tokenized_queries = tokenizer([query], padding=True, truncation=True, return_tensors="pt")

with torch.no_grad():
    output = model(**tokenized_queries)

query_embedding = output.last_hidden_state[:, 0]

query_embedding = torch.nn.functional.normalize(query_embedding, dim=1)


query_embedding = query_embedding.float().cpu().numpy()

query_embedding = query_embedding.squeeze()



# COMPARE WITH COSINE SIMILARITY

articles = []

with open("clean_embeddings.jsonl", "r") as f:
    for line in f:
        row = json.loads(line)

        emb = np.array(row["embedding"], dtype=np.float32)
        score = cosine_similarity(query_embedding.reshape(1, -1), emb.reshape(1, -1))[0][0]

        articles.append({"file": row["file"],
                         "chunk": row["chunk"],
                         "score": float(score)})


articles.sort(key=lambda x: x["score"], reverse=True)



# WRITE OUT
for art in articles[:20]:
    print(
        f"score={art['score']} "
        f"file={art['file']} "
        f"chunk={art['chunk']}\n"
    )