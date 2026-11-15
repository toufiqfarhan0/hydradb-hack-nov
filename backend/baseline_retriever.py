"""
BM25 / TF-IDF Vector Retriever Baseline with Query Decomposition & Learned Score Boosting
Provides an honest, hardened semantic search baseline modeled on production tool search
systems (e.g., LangChain / LlamaIndex / Claude Tool Search) over 500 MCP tools.
"""
import math
import re
from typing import List, Dict, Tuple, Any, Optional
from backend.models import ToolNode

class VectorEmbeddingRetriever:
    """
    Computes TF-IDF vector embeddings and cosine similarity across 500 MCP tools.
    Supports query decomposition (sub-query splitting) and dynamic learned score boosting
    to provide the strongest possible non-graph baseline for empirical comparison.
    """
    def __init__(self, tools: List[ToolNode]):
        self.tools = {t.id: t for t in tools}
        self.tool_list = tools
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        self.learned_boosts: Dict[str, float] = {}
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

    def apply_feedback_boost(self, tool_id: str, boost: float):
        """Allow vector retriever to learn from feedback via score multipliers."""
        self.learned_boosts[tool_id] = self.learned_boosts.get(tool_id, 1.0) * boost

    def _score_query(self, q_tokens: List[str], with_boost: bool = False) -> List[Tuple[ToolNode, float]]:
        if not q_tokens:
            return [(t, 0.0) for t in self.tool_list]

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
            
            if with_boost:
                sim *= self.learned_boosts.get(t_id, 1.0)

            scores.append((self.tools[t_id], sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def retrieve_top_k(
        self,
        query: str,
        k: int = 4,
        decompose: bool = False,
        with_boost: bool = False
    ) -> List[Tuple[ToolNode, float]]:
        """
        Compute top-k tool retrieval.
        - decompose=True: splits compound multi-intent prompts into sub-clauses and pools top matches.
        - with_boost=True: applies learned preference multipliers to show learned vector behavior.
        """
        if not decompose:
            q_tokens = self._tokenize(query)
            return self._score_query(q_tokens, with_boost=with_boost)[:k]

        # Decompose composite prompt into sub-clauses (e.g. "and", "then", punctuation)
        clauses = [c.strip() for c in re.split(r'[,;.\n]|\band\b|\bthen\b|\bwhile\b', query, flags=re.IGNORECASE) if len(c.strip()) > 3]
        if not clauses:
            clauses = [query]

        pooled_scores: Dict[str, float] = {}
        for clause in clauses:
            q_toks = self._tokenize(clause)
            if not q_toks:
                continue
            sub_scores = self._score_query(q_toks, with_boost=with_boost)[:max(k // len(clauses) + 2, 2)]
            for tool, score in sub_scores:
                pooled_scores[tool.id] = max(pooled_scores.get(tool.id, 0.0), score)

        sorted_tools = sorted(
            [(self.tools[tid], s) for tid, s in pooled_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_tools[:k]
