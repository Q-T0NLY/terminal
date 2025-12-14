#!/usr/bin/env python3
"""
Advanced Semantic Search & Discovery System
Multi-modal search with vector embeddings and intelligent ranking
Version: ∞.8
"""

import asyncio
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
import json
from datetime import datetime
import hashlib


class SearchMode(str, Enum):
    """Search modes"""
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    FUZZY = "fuzzy"
    CONTEXTUAL = "contextual"


class SearchCategory(str, Enum):
    """Search categories"""
    PLUGIN = "plugin"
    SERVICE = "service"
    FEATURE = "feature"
    CODE = "code"
    CONFIGURATION = "configuration"
    DOCUMENTATION = "documentation"
    ALL = "all"


@dataclass
class SearchResult:
    """Search result with scoring"""
    id: str
    type: str
    name: str
    description: str
    score: float
    relevance: float
    category: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    highlights: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    matched_fields: List[str] = field(default_factory=list)
    rank: int = 0


@dataclass
class SearchQuery:
    """Enhanced search query"""
    query: str
    mode: SearchMode = SearchMode.HYBRID
    categories: List[SearchCategory] = field(default_factory=lambda: [SearchCategory.ALL])
    filters: Dict[str, Any] = field(default_factory=dict)
    limit: int = 20
    offset: int = 0
    boost_fields: Dict[str, float] = field(default_factory=dict)
    personalized: bool = False
    user_context: Optional[Dict[str, Any]] = None


class VectorIndex:
    """Simple in-memory vector index (can be replaced with Qdrant/Weaviate)"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectors: Dict[str, np.ndarray] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        
    def add(self, doc_id: str, vector: List[float], metadata: Dict[str, Any]):
        """Add vector to index"""
        self.vectors[doc_id] = np.array(vector)
        self.metadata[doc_id] = metadata
    
    def search(self, query_vector: List[float], k: int = 10) -> List[Tuple[str, float]]:
        """Cosine similarity search"""
        if not self.vectors:
            return []
        
        query_vec = np.array(query_vector)
        query_vec = query_vec / (np.linalg.norm(query_vec) + 1e-8)
        
        results = []
        for doc_id, vec in self.vectors.items():
            vec_norm = vec / (np.linalg.norm(vec) + 1e-8)
            similarity = np.dot(query_vec, vec_norm)
            results.append((doc_id, float(similarity)))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def remove(self, doc_id: str):
        """Remove from index"""
        self.vectors.pop(doc_id, None)
        self.metadata.pop(doc_id, None)
    
    def size(self) -> int:
        """Index size"""
        return len(self.vectors)


class SemanticSearchEngine:
    """Advanced semantic search with multi-modal support"""
    
    def __init__(self):
        # Vector index for semantic search
        self.vector_index = VectorIndex()
        
        # Keyword index (inverted index)
        self.keyword_index: Dict[str, set] = {}
        
        # Document store
        self.documents: Dict[str, Dict[str, Any]] = {}
        
        # Search statistics
        self.stats = {
            "total_searches": 0,
            "avg_response_time": 0.0,
            "popular_queries": {},
            "zero_results": 0
        }
        
        # User search history for personalization
        self.user_history: Dict[str, List[Dict[str, Any]]] = {}
    
    async def index_document(self, doc_id: str, document: Dict[str, Any]):
        """Index a document for search"""
        # Store document
        self.documents[doc_id] = document
        
        # Generate embedding (simplified - use real embedding model in production)
        text = self._extract_searchable_text(document)
        embedding = self._generate_embedding(text)
        
        # Add to vector index
        self.vector_index.add(doc_id, embedding, {
            "type": document.get("type"),
            "category": document.get("category"),
            "indexed_at": datetime.utcnow().isoformat()
        })
        
        # Add to keyword index
        tokens = self._tokenize(text)
        for token in tokens:
            if token not in self.keyword_index:
                self.keyword_index[token] = set()
            self.keyword_index[token].add(doc_id)
    
    async def search(self, query: SearchQuery) -> List[SearchResult]:
        """Execute search query"""
        start_time = datetime.utcnow()
        
        # Update stats
        self.stats["total_searches"] += 1
        query_hash = hashlib.md5(query.query.encode()).hexdigest()[:8]
        self.stats["popular_queries"][query_hash] = \
            self.stats["popular_queries"].get(query_hash, 0) + 1
        
        results = []
        
        if query.mode == SearchMode.SEMANTIC:
            results = await self._semantic_search(query)
        elif query.mode == SearchMode.KEYWORD:
            results = await self._keyword_search(query)
        elif query.mode == SearchMode.HYBRID:
            results = await self._hybrid_search(query)
        elif query.mode == SearchMode.FUZZY:
            results = await self._fuzzy_search(query)
        elif query.mode == SearchMode.CONTEXTUAL:
            results = await self._contextual_search(query)
        
        # Apply filters
        results = self._apply_filters(results, query.filters)
        
        # Apply category filters
        if SearchCategory.ALL not in query.categories:
            results = [r for r in results if r.category in [c.value for c in query.categories]]
        
        # Personalize if requested
        if query.personalized and query.user_context:
            results = self._personalize_results(results, query.user_context)
        
        # Re-rank results
        results = self._rerank_results(results, query)
        
        # Assign ranks
        for i, result in enumerate(results):
            result.rank = i + 1
        
        # Apply pagination
        paginated = results[query.offset:query.offset + query.limit]
        
        # Update stats
        if not results:
            self.stats["zero_results"] += 1
        
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        self.stats["avg_response_time"] = \
            (self.stats["avg_response_time"] * (self.stats["total_searches"] - 1) + elapsed) / \
            self.stats["total_searches"]
        
        return paginated
    
    async def _semantic_search(self, query: SearchQuery) -> List[SearchResult]:
        """Semantic vector search"""
        query_embedding = self._generate_embedding(query.query)
        vector_results = self.vector_index.search(query_embedding, k=query.limit * 2)
        
        results = []
        for doc_id, similarity in vector_results:
            if doc_id in self.documents:
                doc = self.documents[doc_id]
                results.append(SearchResult(
                    id=doc_id,
                    type=doc.get("type", "unknown"),
                    name=doc.get("name", ""),
                    description=doc.get("description", ""),
                    score=similarity,
                    relevance=similarity,
                    category=doc.get("category", "unknown"),
                    metadata=doc.get("metadata", {}),
                    embedding=query_embedding,
                    matched_fields=["embedding"]
                ))
        
        return results
    
    async def _keyword_search(self, query: SearchQuery) -> List[SearchResult]:
        """Keyword-based search"""
        tokens = self._tokenize(query.query.lower())
        
        # Find documents containing any token
        doc_scores: Dict[str, float] = {}
        doc_matches: Dict[str, set] = {}
        
        for token in tokens:
            if token in self.keyword_index:
                for doc_id in self.keyword_index[token]:
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = 0.0
                        doc_matches[doc_id] = set()
                    
                    # TF-IDF-like scoring
                    term_freq = 1.0
                    doc_freq = len(self.keyword_index[token])
                    idf = np.log(len(self.documents) / (doc_freq + 1))
                    doc_scores[doc_id] += term_freq * idf
                    doc_matches[doc_id].add(token)
        
        results = []
        for doc_id, score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True):
            if doc_id in self.documents:
                doc = self.documents[doc_id]
                highlights = self._generate_highlights(doc, doc_matches[doc_id])
                
                results.append(SearchResult(
                    id=doc_id,
                    type=doc.get("type", "unknown"),
                    name=doc.get("name", ""),
                    description=doc.get("description", ""),
                    score=score,
                    relevance=score / (len(tokens) + 1),
                    category=doc.get("category", "unknown"),
                    metadata=doc.get("metadata", {}),
                    highlights=highlights,
                    matched_fields=list(doc_matches[doc_id])
                ))
        
        return results
    
    async def _hybrid_search(self, query: SearchQuery) -> List[SearchResult]:
        """Hybrid search combining semantic and keyword"""
        # Run both searches
        semantic_results = await self._semantic_search(query)
        keyword_results = await self._keyword_search(query)
        
        # Combine results with weighted scoring
        combined: Dict[str, SearchResult] = {}
        
        # Weight: 60% semantic, 40% keyword
        for result in semantic_results:
            result.score = result.score * 0.6
            combined[result.id] = result
        
        for result in keyword_results:
            if result.id in combined:
                combined[result.id].score += result.score * 0.4
                combined[result.id].matched_fields.extend(result.matched_fields)
                combined[result.id].highlights.extend(result.highlights)
            else:
                result.score = result.score * 0.4
                combined[result.id] = result
        
        # Sort by combined score
        results = sorted(combined.values(), key=lambda x: x.score, reverse=True)
        return results
    
    async def _fuzzy_search(self, query: SearchQuery) -> List[SearchResult]:
        """Fuzzy search with typo tolerance"""
        # Start with keyword search
        results = await self._keyword_search(query)
        
        # If no results, try fuzzy matching
        if not results:
            fuzzy_tokens = self._fuzzy_tokenize(query.query)
            fuzzy_query = SearchQuery(
                query=" ".join(fuzzy_tokens),
                mode=SearchMode.KEYWORD,
                categories=query.categories,
                filters=query.filters,
                limit=query.limit
            )
            results = await self._keyword_search(fuzzy_query)
        
        return results
    
    async def _contextual_search(self, query: SearchQuery) -> List[SearchResult]:
        """Context-aware search using user history"""
        # Start with hybrid search
        results = await self._hybrid_search(query)
        
        # Boost based on user context
        if query.user_context:
            user_id = query.user_context.get("user_id")
            if user_id and user_id in self.user_history:
                # Boost previously accessed items
                history_ids = {h["doc_id"] for h in self.user_history[user_id][-10:]}
                for result in results:
                    if result.id in history_ids:
                        result.score *= 1.2
        
        return results
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate text embedding (simplified - use SentenceTransformers in production)"""
        # Simple hash-based embedding for demo
        # In production, use: sentence-transformers, OpenAI embeddings, etc.
        tokens = self._tokenize(text.lower())
        embedding = np.zeros(384)
        
        for i, token in enumerate(tokens[:50]):
            # Simple character-based hashing
            hash_val = hash(token) % 384
            embedding[hash_val] += 1.0 / (i + 1)
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding.tolist()
    
    def _extract_searchable_text(self, document: Dict[str, Any]) -> str:
        """Extract searchable text from document"""
        parts = []
        
        # Extract key fields
        for field in ["name", "display_name", "description", "tags", "category", "feature"]:
            if field in document:
                value = document[field]
                if isinstance(value, list):
                    parts.extend([str(v) for v in value])
                else:
                    parts.append(str(value))
        
        # Extract from metadata
        if "metadata" in document:
            metadata_str = json.dumps(document["metadata"])
            parts.append(metadata_str)
        
        return " ".join(parts)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        # Simple tokenization
        tokens = re.findall(r'\w+', text.lower())
        # Remove stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
        return tokens
    
    def _fuzzy_tokenize(self, text: str) -> List[str]:
        """Fuzzy tokenization with typo correction"""
        tokens = self._tokenize(text)
        # Simple: try common variations
        fuzzy_tokens = []
        for token in tokens:
            fuzzy_tokens.append(token)
            # Add variations (simplified)
            if len(token) > 3:
                fuzzy_tokens.append(token[:-1])  # Remove last char
                fuzzy_tokens.append(token + "s")  # Add plural
        return fuzzy_tokens
    
    def _apply_filters(self, results: List[SearchResult], filters: Dict[str, Any]) -> List[SearchResult]:
        """Apply filters to results"""
        if not filters:
            return results
        
        filtered = []
        for result in results:
            match = True
            for key, value in filters.items():
                if key in result.metadata:
                    if isinstance(value, list):
                        if result.metadata[key] not in value:
                            match = False
                            break
                    elif result.metadata[key] != value:
                        match = False
                        break
            if match:
                filtered.append(result)
        
        return filtered
    
    def _personalize_results(self, results: List[SearchResult], user_context: Dict[str, Any]) -> List[SearchResult]:
        """Personalize results based on user context"""
        user_preferences = user_context.get("preferences", {})
        
        for result in results:
            # Boost based on preferred categories
            if result.category in user_preferences.get("categories", []):
                result.score *= 1.3
            
            # Boost based on preferred features
            if result.metadata.get("feature") in user_preferences.get("features", []):
                result.score *= 1.2
        
        return results
    
    def _rerank_results(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """Re-rank results with field boosting"""
        if not query.boost_fields:
            return sorted(results, key=lambda x: x.score, reverse=True)
        
        for result in results:
            for field, boost in query.boost_fields.items():
                if field in result.matched_fields:
                    result.score *= boost
        
        return sorted(results, key=lambda x: x.score, reverse=True)
    
    def _generate_highlights(self, document: Dict[str, Any], matched_tokens: set) -> List[str]:
        """Generate search highlights"""
        highlights = []
        text = self._extract_searchable_text(document)
        
        for token in matched_tokens:
            pattern = re.compile(rf'\b\w*{re.escape(token)}\w*\b', re.IGNORECASE)
            matches = pattern.findall(text)
            highlights.extend(matches[:3])
        
        return highlights[:5]
    
    async def suggest(self, prefix: str, limit: int = 10) -> List[str]:
        """Auto-suggest based on prefix"""
        suggestions = []
        prefix_lower = prefix.lower()
        
        for token in self.keyword_index.keys():
            if token.startswith(prefix_lower):
                suggestions.append(token)
        
        # Sort by frequency
        suggestions.sort(key=lambda x: len(self.keyword_index.get(x, [])), reverse=True)
        return suggestions[:limit]
    
    async def get_related(self, doc_id: str, limit: int = 5) -> List[SearchResult]:
        """Find related documents"""
        if doc_id not in self.documents:
            return []
        
        doc = self.documents[doc_id]
        
        # Use document's embedding for similarity search
        if doc_id in self.vector_index.vectors:
            embedding = self.vector_index.vectors[doc_id].tolist()
            similar = self.vector_index.search(embedding, k=limit + 1)
            
            results = []
            for sim_id, score in similar:
                if sim_id != doc_id and sim_id in self.documents:
                    sim_doc = self.documents[sim_id]
                    results.append(SearchResult(
                        id=sim_id,
                        type=sim_doc.get("type", "unknown"),
                        name=sim_doc.get("name", ""),
                        description=sim_doc.get("description", ""),
                        score=score,
                        relevance=score,
                        category=sim_doc.get("category", "unknown"),
                        metadata=sim_doc.get("metadata", {})
                    ))
            
            return results[:limit]
        
        return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        return {
            **self.stats,
            "indexed_documents": len(self.documents),
            "vector_index_size": self.vector_index.size(),
            "keyword_terms": len(self.keyword_index)
        }


# Global search engine instance
search_engine = SemanticSearchEngine()
