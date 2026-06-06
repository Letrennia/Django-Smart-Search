from BM25.BM25_score_function import query_score
from Embedding.find_embeddings import find_similar_embeddings


def hybrid_search(ask):

    # BM25
    scores_bm25 = query_score(ask)

    values = list(scores_bm25.values())

    # CASE: EMPTY BM25 (EX. CLICKJACKING)
    if values is None or len(values) == 0:
        scores_embeddings = find_similar_embeddings(ask)
        sorted_final_scores = sorted(scores_embeddings, key=lambda x: x['score'], reverse=True)
        return [(item['file'], item["chunk"], item['score']) for item in sorted_final_scores]
        # return [(item['file'], item['score']) for item in sorted_final_scores]


    min_score = min(values)
    max_score = max(values)
    scaled_scores_bm25 = {}

    for doc, score in scores_bm25.items():
        scaled = (score - min_score) / (max_score - min_score)
        scaled_scores_bm25[doc] = scaled

    # EMBEDDINGS
    scores_embeddings = find_similar_embeddings(ask)
    sorted_embeddings = sorted(scores_embeddings, key=lambda x: x['score'], reverse=True)



    # HYBRID SEARCH
    bm25_weight = 0.09
    vector_weight = 0.9
    final_scores = {}

    for file_emb in sorted_embeddings[:30]:
        for doc, score_bm25 in scaled_scores_bm25.items():
            if file_emb['file'] == doc:
                final_score = (bm25_weight * score_bm25) + (vector_weight * file_emb['score'])
                # final_scores[doc] = final_score
                final_scores[doc] = (final_score, file_emb["chunk"])


    sorted_final_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    return [(doc, score, chunk) for doc, (score, chunk) in sorted_final_scores]
    # return sorted_final_scores



# TEST
# hybrid_results = hybrid_search('should i change debug before the deploy')
#
# for file, score in hybrid_results[:20]:
#     print(f'{file} {score}')

