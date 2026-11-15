"""
Embedding-Based Top-K Semantic Retriever Baseline
Simulates production vector embedding retrieval (e.g., text-embedding-3-small / BM25)
over 500 MCP tool descriptions to compare against HydraDB GraphBLAS multi-hop traversal.
"""
import math
import re
from typing import List, Dict, Tuple, Any
from backend.models import ToolNode

class VectorEmbeddingRetriever:
    """
    Computes TF-IDF vector embeddings and cosine similarity across 500 MCP tools.
    Provides standard semantic search baseline used by LangChain / LlamaIndex / Claude Tool Search.
    """
    def __init__(self, tools: List[ToolNode]):
        self.tools = {t.id: t for t in tools}
        self.tool_list = tools
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text)]

    def _build_index(self):
        doc_freqs: Dict[str, int] = {}
        num_docs = len(self.tool_list)

        for t in self.tool_list:
            text = f"{t.name} {t.description} {t.server_id}"
            tokens = set(self._tokenize(text))
            for tok in tokens:
                doc_freqs[tok] = doc_freqs.get(tok, 0) + 1

        # Calculate IDF
        for tok, df in doc_freqs.items():
            self.idf[tok] = math.log((num_docs + 1) / (df + 1)) + 1.0

        # Build normalized TF-IDF vectors
        for t in self.tool_list:
            text = f"{t.name} {t.description} {t.server_id}"
            tokens = self._tokenize(text)
            tf: Dict[str, float] = {}
            for tok in tokens:
                tf[tok] = tf.get(tok, 0.0) + 1.0
            
            vec: Dict[str, float] = {}
            norm_sq = 0.0
            for tok, count in tf.items():
                tfidf = (count / len(tokens)) * self.idf.get(tok, 1.0)
                vec[tok] = tfidf
                norm_sq += tfidf * tfidf
            
            norm = math.sqrt(norm_sq) or 1.0
            self.doc_vectors[t.id] = {tok: v / norm for tok, v in vec.items()}

    def retrieve_top_k(self, query: str, k: int = 4) -> List[Tuple[ToolNode, float]]:
        """Compute cosine similarity between query and all tools, return top k."""
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return [(self.tool_list[i], 0.0) for i in range(min(k, len(self.tool_list)))]

        q_tf: Dict[str, float] = {}
        for tok in q_tokens:
            q_tf[tok] = q_tf.get(tok, 0.0) + 1.0

        q_vec: Dict[str, float] = {}
        norm_sq = 0.0
        for tok, count in q_tf.items():
            tfidf = (count / len(q_tokens)) * self.idf.get(tok, 1.0)
            q_vec[tok] = tfidf
            norm_sq += tfidf * tfidf
        norm = math.sqrt(norm_sq) or 1.0
        norm_q_vec = {tok: v / norm for tok, v in q_vec.items()}

        scores = []
        for t_id, d_vec in self.doc_vectors.items():
            sim = 0.0
            for tok, q_val in norm_q_vec.items():
                if tok in d_vec:
                    sim += q_val * d_vec[tok]
            scores.append((self.tools[t_id], sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]
