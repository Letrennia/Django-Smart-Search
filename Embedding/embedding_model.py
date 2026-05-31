import torch
from transformers import AutoTokenizer, AutoModel
import os
import json


def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as f_c:
        file_content = f_c.read()
        start = file_content.find('[TEXT]')
        end = file_content.find('[VECTOR]')

        text_content = file_content[start + 6:end].strip()

    return text_content


def process_batch(chunks_batch, meta_batch):
    tokenized = tokenizer(chunks_batch, padding=True, truncation=True, return_tensors='pt')

    with torch.no_grad():
        model_output = model(**tokenized)
        query_embeddings = model_output[0][:, 0]

    embeddings = torch.nn.functional.normalize(query_embeddings, dim=1)

    for (file, chunk_id), emb in zip(meta_batch, embeddings):
        data_to_write = {
            'file': file,
            f'chunk': chunk_id,
            'embedding': emb.tolist()
        }

        with open('clean_embeddings.jsonl', 'a') as f:
            json.dump(data_to_write, f)
            f.write('\n')



input_dir = "../clean_data"
model_path = 'ibm-granite/granite-embedding-small-english-r2'

model = AutoModel.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()

chunks_batch = []
meta_batch = []
batch_size = 32


for file in os.listdir(input_dir)[3467:]:
    if not file.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, file)
    content = read_file_content(input_path)
    words = content.split()

    chunk_size = 2000
    start = 0
    overlap = 50
    which_chunk = 1
    
    while(start < len(words)):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        chunks_batch.append(chunk)
        meta_batch.append((file, which_chunk))

        if len(chunks_batch) == batch_size:
            process_batch(chunks_batch, meta_batch)
            chunks_batch = []
            meta_batch = []



        which_chunk += 1
        start += chunk_size - overlap

if chunks_batch:
    process_batch(chunks_batch, meta_batch)