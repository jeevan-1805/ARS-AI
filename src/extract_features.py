from src.reusables import FEATURE_DESCRIPTIONS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

TOP_K = 5
def retrieve_top_k_blocks(feature_name, block_text, block_embeddings, embedding_model, top_k=TOP_K):
    feature_description = FEATURE_DESCRIPTIONS[feature_name]
    feature_embedding = embedding_model.encode([feature_description])
    similarities = cosine_similarity(feature_embedding, block_embeddings)[0]

    top_count = min(top_k, len(similarities))

    top_positions = np.argsort(similarities)[-top_count:][::-1]

    results = []

    for position in top_positions:
        results.append({"block": block_text[position], "similarity": similarities[position]})

    return results

def extract_candidate_feature_blocks(block_text, block_embeddings, embedding_model):
    retrieved_features = {}

    for feature_name in FEATURE_DESCRIPTIONS:

        top_blocks = retrieve_top_k_blocks(feature_name=feature_name, block_text=block_text, block_embeddings=block_embeddings, embedding_model=embedding_model)
        retrieved_features[feature_name] = top_blocks
    return retrieved_features
