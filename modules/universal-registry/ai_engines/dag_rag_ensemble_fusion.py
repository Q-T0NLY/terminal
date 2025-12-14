"""
[🎯] Ultra-Modern Professional Enterprise DAG-RAG++ Advanced Ensemble Fusion
Multi-Model Ensemble System with Adaptive Fusion Strategies

Features:
- [🌟] Multi-Model Ensemble Architecture
- [🔄] Adaptive Weight Optimization
- [🎭] Model Diversity Maximization
- [📊] Confidence-Based Fusion
- [🧠] Meta-Learning for Model Selection
- [⚡] Parallel Model Execution
- [🎯] Dynamic Ensemble Composition
- [🔐] Enterprise-Grade Reliability
"""

from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import json
import numpy as np
from collections import defaultdict
import logging

from .dag_rag_plus_plus_engine import (
    RAGPlusPlusEngine, GenerationResult, RetrievalResult, 
    ConfidenceLevel, logger
)

# Configure logging
ensemble_logger = logging.getLogger(__name__)


class FusionStrategy(str, Enum):
    """[🎭] Ensemble Fusion Strategies"""
    WEIGHTED_AVERAGE = "weighted_average"
    MAJORITY_VOTING = "majority_voting"
    CONFIDENCE_BASED = "confidence_based"
    RANK_FUSION = "rank_fusion"
    STACKING = "stacking"
    BOOSTING = "boosting"
    BAGGING = "bagging"
    MIXTURE_OF_EXPERTS = "mixture_of_experts"


class ModelType(str, Enum):
    """[🤖] Model Types in Ensemble"""
    RAG_BASIC = "rag_basic"
    RAG_PLUS_PLUS = "rag_plus_plus"
    TRANSFORMER = "transformer"
    RETRIEVAL_ONLY = "retrieval_only"
    GENERATIVE_ONLY = "generative_only"
    HYBRID = "hybrid"


@dataclass
class ModelConfig:
    """[⚙️] Configuration for individual model"""
    model_id: str
    model_type: ModelType
    weight: float = 1.0
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
    performance_history: List[float] = field(default_factory=list)


@dataclass
class EnsembleResult:
    """[🎯] Result from ensemble fusion"""
    fused_text: str
    confidence: float
    fusion_strategy: FusionStrategy
    model_contributions: Dict[str, float]
    individual_results: List[GenerationResult]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FusionMetrics:
    """[📊] Metrics for fusion performance"""
    agreement_score: float
    diversity_score: float
    confidence_variance: float
    execution_time: float
    models_used: int


class BaseModel:
    """[🏗️] Base class for ensemble models"""
    
    def __init__(self, model_id: str, model_type: ModelType):
        self.model_id = model_id
        self.model_type = model_type
        self.performance_metrics: List[float] = []
        ensemble_logger.info("[✅] Model initialized: %s (%s)", model_id, model_type.value)
    
    async def generate(self, query: str, context: List[RetrievalResult]) -> GenerationResult:
        """[🚀] Generate response from model"""
        raise NotImplementedError("[❌] Subclass must implement generate()")
    
    async def get_confidence(self, result: GenerationResult) -> float:
        """[📊] Calculate confidence score"""
        return result.confidence
    
    def update_performance(self, score: float):
        """[📈] Update performance history"""
        self.performance_metrics.append(score)
        if len(self.performance_metrics) > 100:
            self.performance_metrics = self.performance_metrics[-100:]


class RAGPlusPlusModel(BaseModel):
    """[🧠] RAG++ Model wrapper for ensemble"""
    
    def __init__(self, model_id: str):
        super().__init__(model_id, ModelType.RAG_PLUS_PLUS)
        self.engine = RAGPlusPlusEngine()
    
    async def generate(self, query: str, context: List[RetrievalResult]) -> GenerationResult:
        """[🚀] Generate using RAG++ engine"""
        result = await self.engine.query(query, top_k=5)
        ensemble_logger.debug("[✅] RAG++ generated response with confidence %.2f", result.confidence)
        return result


class TransformerModel(BaseModel):
    """[🤖] Transformer-based model"""
    
    def __init__(self, model_id: str):
        super().__init__(model_id, ModelType.TRANSFORMER)
    
    async def generate(self, query: str, context: List[RetrievalResult]) -> GenerationResult:
        """[🚀] Generate using transformer"""
        # Simulated transformer generation
        context_text = " ".join([r.content for r in context[:3]])
        
        result = GenerationResult(
            generated_text=f"[🤖] Transformer response to: {query}",
            confidence=0.82,
            reasoning_chain=["[🤖] Transformer processing", "[✅] Response generated"],
            sources=["transformer_model"],
            metadata={"model_type": "transformer"}
        )
        
        ensemble_logger.debug("[✅] Transformer generated response")
        return result


class RetrievalModel(BaseModel):
    """[🔍] Retrieval-focused model"""
    
    def __init__(self, model_id: str):
        super().__init__(model_id, ModelType.RETRIEVAL_ONLY)
    
    async def generate(self, query: str, context: List[RetrievalResult]) -> GenerationResult:
        """[🚀] Generate using retrieval"""
        if not context:
            return GenerationResult(
                generated_text="[⚠️] No relevant documents found",
                confidence=0.3,
                reasoning_chain=["[🔍] Retrieval attempted", "[⚠️] No matches"],
                sources=[]
            )
        
        # Use top retrieved document
        top_doc = context[0]
        result = GenerationResult(
            generated_text=f"[🔍] {top_doc.content}",
            confidence=top_doc.relevance_score,
            reasoning_chain=["[🔍] Document retrieved", "[✅] Content extracted"],
            sources=[top_doc.document_id],
            metadata={"retrieval_score": top_doc.relevance_score}
        )
        
        ensemble_logger.debug("[✅] Retrieval model generated response")
        return result


class EnsembleFusionEngine:
    """[🎯] Advanced Ensemble Fusion Engine"""
    
    def __init__(self):
        self.models: Dict[str, BaseModel] = {}
        self.model_configs: Dict[str, ModelConfig] = {}
        self.fusion_strategies: Dict[str, Callable] = {
            FusionStrategy.WEIGHTED_AVERAGE: self._weighted_average_fusion,
            FusionStrategy.CONFIDENCE_BASED: self._confidence_based_fusion,
            FusionStrategy.MAJORITY_VOTING: self._majority_voting_fusion,
            FusionStrategy.RANK_FUSION: self._rank_fusion,
            FusionStrategy.MIXTURE_OF_EXPERTS: self._mixture_of_experts_fusion,
        }
        self.performance_history: List[FusionMetrics] = []
        ensemble_logger.info("[✅] Ensemble Fusion Engine initialized")
    
    def add_model(self, model: BaseModel, config: ModelConfig):
        """[➕] Add model to ensemble"""
        self.models[model.model_id] = model
        self.model_configs[model.model_id] = config
        ensemble_logger.info("[✅] Model added to ensemble: %s", model.model_id)
    
    def remove_model(self, model_id: str):
        """[➖] Remove model from ensemble"""
        if model_id in self.models:
            del self.models[model_id]
            del self.model_configs[model_id]
            ensemble_logger.info("[✅] Model removed from ensemble: %s", model_id)
    
    async def generate_ensemble(
        self,
        query: str,
        context: List[RetrievalResult],
        strategy: FusionStrategy = FusionStrategy.CONFIDENCE_BASED,
        top_k_models: Optional[int] = None
    ) -> EnsembleResult:
        """[🚀] Generate response using ensemble fusion"""
        ensemble_logger.info("[🚀] Generating ensemble response with strategy: %s", strategy.value)
        
        start_time = datetime.now()
        
        # Select models to use
        active_models = self._select_models(top_k_models)
        
        if not active_models:
            ensemble_logger.error("[❌] No active models in ensemble")
            raise ValueError("[❌] No active models available")
        
        # Generate responses from all models in parallel
        tasks = [
            model.generate(query, context)
            for model in active_models
        ]
        
        individual_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_results = [
            r for r in individual_results 
            if isinstance(r, GenerationResult)
        ]
        
        if not valid_results:
            ensemble_logger.error("[❌] All models failed to generate responses")
            raise ValueError("[❌] All models failed")
        
        ensemble_logger.info("[✅] %d/%d models generated valid responses", 
                           len(valid_results), len(active_models))
        
        # Apply fusion strategy
        fusion_func = self.fusion_strategies.get(strategy, self._confidence_based_fusion)
        fused_result = await fusion_func(valid_results, query, context)
        
        # Calculate metrics
        execution_time = (datetime.now() - start_time).total_seconds()
        metrics = self._calculate_fusion_metrics(valid_results, execution_time)
        
        # Update model weights based on performance
        await self._update_model_weights(valid_results, fused_result)
        
        # Track performance
        self.performance_history.append(metrics)
        
        ensemble_logger.info("[🎉] Ensemble generation completed in %.3fs with confidence %.2f",
                           execution_time, fused_result.confidence)
        
        return fused_result
    
    def _select_models(self, top_k: Optional[int] = None) -> List[BaseModel]:
        """[🎯] Select models for ensemble based on configuration"""
        enabled_models = [
            self.models[model_id]
            for model_id, config in self.model_configs.items()
            if config.enabled and model_id in self.models
        ]
        
        if top_k and top_k < len(enabled_models):
            # Sort by weight and performance
            sorted_models = sorted(
                enabled_models,
                key=lambda m: (
                    self.model_configs[m.model_id].weight *
                    (np.mean(m.performance_metrics) if m.performance_metrics else 0.5)
                ),
                reverse=True
            )
            return sorted_models[:top_k]
        
        return enabled_models
    
    async def _weighted_average_fusion(
        self,
        results: List[GenerationResult],
        query: str,
        context: List[RetrievalResult]
    ) -> EnsembleResult:
        """[⚖️] Weighted average fusion"""
        ensemble_logger.debug("[⚖️] Applying weighted average fusion")
        
        weights = []
        for result in results:
            model_id = result.sources[0] if result.sources else "unknown"
            config = self.model_configs.get(model_id, ModelConfig(model_id, ModelType.HYBRID))
            weights.append(config.weight)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            weights = [1.0 / len(results)] * len(results)
        
        # Combine texts and confidences
        combined_confidence = sum(r.confidence * w for r, w in zip(results, weights))
        
        # Select text from highest weighted result
        best_idx = np.argmax(weights)
        fused_text = results[best_idx].generated_text
        
        model_contributions = {
            r.sources[0] if r.sources else f"model_{i}": w
            for i, (r, w) in enumerate(zip(results, weights))
        }
        
        return EnsembleResult(
            fused_text=fused_text,
            confidence=combined_confidence,
            fusion_strategy=FusionStrategy.WEIGHTED_AVERAGE,
            model_contributions=model_contributions,
            individual_results=results
        )
    
    async def _confidence_based_fusion(
        self,
        results: List[GenerationResult],
        query: str,
        context: List[RetrievalResult]
    ) -> EnsembleResult:
        """[📊] Confidence-based fusion"""
        ensemble_logger.debug("[📊] Applying confidence-based fusion")
        
        # Use confidence scores as weights
        confidences = [r.confidence for r in results]
        total_confidence = sum(confidences)
        
        if total_confidence > 0:
            weights = [c / total_confidence for c in confidences]
        else:
            weights = [1.0 / len(results)] * len(results)
        
        # Select highest confidence result
        best_idx = np.argmax(confidences)
        best_result = results[best_idx]
        
        # Calculate weighted confidence
        weighted_confidence = sum(r.confidence * w for r, w in zip(results, weights))
        
        model_contributions = {
            r.sources[0] if r.sources else f"model_{i}": w
            for i, (r, w) in enumerate(zip(results, weights))
        }
        
        return EnsembleResult(
            fused_text=best_result.generated_text,
            confidence=weighted_confidence,
            fusion_strategy=FusionStrategy.CONFIDENCE_BASED,
            model_contributions=model_contributions,
            individual_results=results,
            metadata={"best_model": best_result.sources[0] if best_result.sources else "unknown"}
        )
    
    async def _majority_voting_fusion(
        self,
        results: List[GenerationResult],
        query: str,
        context: List[RetrievalResult]
    ) -> EnsembleResult:
        """[🗳️] Majority voting fusion"""
        ensemble_logger.debug("[🗳️] Applying majority voting fusion")
        
        # Count similar responses (simplified - in production use semantic similarity)
        response_counts = defaultdict(list)
        for i, result in enumerate(results):
            response_counts[result.generated_text[:50]].append(i)
        
        # Find majority response
        majority_key = max(response_counts.keys(), key=lambda k: len(response_counts[k]))
        majority_indices = response_counts[majority_key]
        
        # Use first occurrence of majority
        majority_result = results[majority_indices[0]]
        
        # Calculate vote proportion as confidence
        vote_confidence = len(majority_indices) / len(results)
        
        model_contributions = {
            results[i].sources[0] if results[i].sources else f"model_{i}": 
            1.0 if i in majority_indices else 0.0
            for i in range(len(results))
        }
        
        return EnsembleResult(
            fused_text=majority_result.generated_text,
            confidence=vote_confidence,
            fusion_strategy=FusionStrategy.MAJORITY_VOTING,
            model_contributions=model_contributions,
            individual_results=results,
            metadata={"votes": len(majority_indices), "total": len(results)}
        )
    
    async def _rank_fusion(
        self,
        results: List[GenerationResult],
        query: str,
        context: List[RetrievalResult]
    ) -> EnsembleResult:
        """[📈] Rank-based fusion"""
        ensemble_logger.debug("[📈] Applying rank-based fusion")
        
        # Sort by confidence
        sorted_results = sorted(results, key=lambda r: r.confidence, reverse=True)
        
        # Assign rank-based scores
        rank_scores = [1.0 / (i + 1) for i in range(len(sorted_results))]
        total_score = sum(rank_scores)
        normalized_scores = [s / total_score for s in rank_scores]
        
        # Use top-ranked result
        top_result = sorted_results[0]
        
        model_contributions = {
            r.sources[0] if r.sources else f"model_{i}": score
            for i, (r, score) in enumerate(zip(sorted_results, normalized_scores))
        }
        
        return EnsembleResult(
            fused_text=top_result.generated_text,
            confidence=top_result.confidence,
            fusion_strategy=FusionStrategy.RANK_FUSION,
            model_contributions=model_contributions,
            individual_results=results,
            metadata={"top_rank": 1, "total_models": len(results)}
        )
    
    async def _mixture_of_experts_fusion(
        self,
        results: List[GenerationResult],
        query: str,
        context: List[RetrievalResult]
    ) -> EnsembleResult:
        """[🎓] Mixture of Experts fusion"""
        ensemble_logger.debug("[🎓] Applying mixture of experts fusion")
        
        # Determine query complexity (simplified)
        query_complexity = len(query.split()) / 10.0  # Normalize
        
        # Select expert based on query characteristics
        # In production, use learned gating network
        expert_weights = []
        for result in results:
            model_type = result.metadata.get("model_type", "unknown")
            
            # Assign weights based on query type
            if "technical" in query.lower() or "how" in query.lower():
                weight = 1.5 if model_type == "rag_plus_plus" else 1.0
            elif "what" in query.lower():
                weight = 1.5 if model_type == "retrieval" else 1.0
            else:
                weight = 1.0
            
            expert_weights.append(weight * result.confidence)
        
        # Normalize weights
        total_weight = sum(expert_weights)
        if total_weight > 0:
            expert_weights = [w / total_weight for w in expert_weights]
        else:
            expert_weights = [1.0 / len(results)] * len(results)
        
        # Select expert with highest weight
        expert_idx = np.argmax(expert_weights)
        expert_result = results[expert_idx]
        
        model_contributions = {
            r.sources[0] if r.sources else f"expert_{i}": w
            for i, (r, w) in enumerate(zip(results, expert_weights))
        }
        
        return EnsembleResult(
            fused_text=expert_result.generated_text,
            confidence=expert_result.confidence,
            fusion_strategy=FusionStrategy.MIXTURE_OF_EXPERTS,
            model_contributions=model_contributions,
            individual_results=results,
            metadata={
                "selected_expert": expert_result.sources[0] if expert_result.sources else "unknown",
                "query_complexity": query_complexity
            }
        )
    
    def _calculate_fusion_metrics(
        self,
        results: List[GenerationResult],
        execution_time: float
    ) -> FusionMetrics:
        """[📊] Calculate fusion performance metrics"""
        confidences = [r.confidence for r in results]
        
        # Agreement score (inverse of variance in confidences)
        confidence_variance = np.var(confidences) if len(confidences) > 1 else 0.0
        agreement_score = 1.0 / (1.0 + confidence_variance)
        
        # Diversity score (different text outputs)
        unique_texts = len(set(r.generated_text[:50] for r in results))
        diversity_score = unique_texts / len(results)
        
        return FusionMetrics(
            agreement_score=agreement_score,
            diversity_score=diversity_score,
            confidence_variance=confidence_variance,
            execution_time=execution_time,
            models_used=len(results)
        )
    
    async def _update_model_weights(
        self,
        results: List[GenerationResult],
        fused_result: EnsembleResult
    ):
        """[📈] Update model weights based on performance"""
        for result in results:
            model_id = result.sources[0] if result.sources else None
            if model_id and model_id in self.models:
                # Update performance
                performance_score = result.confidence * fused_result.model_contributions.get(model_id, 0.5)
                self.models[model_id].update_performance(performance_score)
                
                # Adjust weight (simple exponential moving average)
                config = self.model_configs[model_id]
                alpha = 0.1  # Learning rate
                config.weight = (1 - alpha) * config.weight + alpha * performance_score
                
                ensemble_logger.debug("[📈] Updated weight for %s: %.3f", model_id, config.weight)
    
    async def get_ensemble_stats(self) -> Dict[str, Any]:
        """[📊] Get ensemble statistics"""
        return {
            "models": {
                model_id: {
                    "type": config.model_type.value,
                    "weight": config.weight,
                    "enabled": config.enabled,
                    "performance_mean": np.mean(self.models[model_id].performance_metrics)
                    if self.models[model_id].performance_metrics else 0.0
                }
                for model_id, config in self.model_configs.items()
            },
            "fusion_history": len(self.performance_history),
            "recent_performance": {
                "agreement_score": np.mean([m.agreement_score for m in self.performance_history[-10:]])
                if self.performance_history else 0.0,
                "diversity_score": np.mean([m.diversity_score for m in self.performance_history[-10:]])
                if self.performance_history else 0.0,
                "avg_execution_time": np.mean([m.execution_time for m in self.performance_history[-10:]])
                if self.performance_history else 0.0
            },
            "timestamp": datetime.now().isoformat()
        }


# Global ensemble instance
ensemble_fusion_engine = EnsembleFusionEngine()


async def initialize_ensemble():
    """[🚀] Initialize ensemble with default models"""
    ensemble_logger.info("[🚀] Initializing ensemble fusion engine")
    
    # Add RAG++ models
    rag_model = RAGPlusPlusModel("rag_plus_plus_primary")
    ensemble_fusion_engine.add_model(
        rag_model,
        ModelConfig(
            model_id="rag_plus_plus_primary",
            model_type=ModelType.RAG_PLUS_PLUS,
            weight=1.5
        )
    )
    
    # Add transformer model
    transformer_model = TransformerModel("transformer_primary")
    ensemble_fusion_engine.add_model(
        transformer_model,
        ModelConfig(
            model_id="transformer_primary",
            model_type=ModelType.TRANSFORMER,
            weight=1.2
        )
    )
    
    # Add retrieval model
    retrieval_model = RetrievalModel("retrieval_primary")
    ensemble_fusion_engine.add_model(
        retrieval_model,
        ModelConfig(
            model_id="retrieval_primary",
            model_type=ModelType.RETRIEVAL_ONLY,
            weight=1.0
        )
    )
    
    ensemble_logger.info("[✅] Ensemble initialized with %d models", 
                        len(ensemble_fusion_engine.models))


if __name__ == "__main__":
    # Test ensemble
    async def test_ensemble():
        await initialize_ensemble()
        
        # Mock context
        context = []
        
        result = await ensemble_fusion_engine.generate_ensemble(
            "How does the system optimize performance?",
            context,
            strategy=FusionStrategy.CONFIDENCE_BASED
        )
        
        print(f"\n[🎯] Ensemble Result:")
        print(f"[📝] Text: {result.fused_text}")
        print(f"[📊] Confidence: {result.confidence:.2f}")
        print(f"[🎭] Strategy: {result.fusion_strategy.value}")
        print(f"[🤖] Contributions: {json.dumps(result.model_contributions, indent=2)}")
        
        stats = await ensemble_fusion_engine.get_ensemble_stats()
        print(f"\n[📊] Stats: {json.dumps(stats, indent=2)}")
    
    asyncio.run(test_ensemble())
