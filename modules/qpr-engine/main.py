#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║ ⚡ COMPONENT B: QPR (Quick Path Resolution) ENGINE                            ║
║ Intelligent workflow path optimization with ML-based prediction               ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, Counter
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WorkflowPath:
    """Optimized workflow execution path"""
    path_id: str
    steps: List[str]
    estimated_time: float  # seconds
    success_probability: float  # 0-1
    dependencies: List[str]
    parallel_groups: List[List[str]]
    risk_score: float  # 0-1
    recommended: bool


@dataclass
class PathOptimization:
    """Path optimization result"""
    original_path: List[str]
    optimized_paths: List[WorkflowPath]
    time_saved: float  # seconds
    parallel_opportunities: int
    recommendations: List[str]
    confidence: float


class QPREngine:
    """
    ⚡ Quick Path Resolution Engine
    
    Optimization Algorithm:
    1. Dependency Analysis (DAG construction)
    2. Critical Path Identification
    3. Parallelization Detection
    4. ML-based Success Prediction
    5. Risk Assessment
    """
    
    def __init__(self, history_file: str = "/tmp/qpr_history.json"):
        self.history_file = Path(history_file)
        self.execution_history: List[Dict] = []
        self.success_patterns: Dict[str, float] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.load_history()
    
    def load_history(self):
        """Load execution history for ML training"""
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    self.execution_history = json.load(f)
                self._train_model()
            except:
                logger.warning("Could not load history, starting fresh")
    
    def save_history(self):
        """Save execution history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.execution_history[-1000:], f, indent=2)
        except Exception as e:
            logger.error(f"Could not save history: {e}")
    
    def _train_model(self):
        """Train success prediction model from history"""
        # Count success rates for each step pattern
        pattern_results = defaultdict(list)
        
        for record in self.execution_history:
            steps = record.get('steps', [])
            success = record.get('success', False)
            
            # Create patterns (single steps and pairs)
            for step in steps:
                pattern_results[step].append(1 if success else 0)
            
            # Step pairs (sequence patterns)
            for i in range(len(steps) - 1):
                pair = f"{steps[i]}→{steps[i+1]}"
                pattern_results[pair].append(1 if success else 0)
        
        # Calculate success probabilities
        for pattern, results in pattern_results.items():
            self.success_patterns[pattern] = sum(results) / len(results)
    
    def build_dependency_graph(self, workflow: Dict) -> Dict[str, List[str]]:
        """
        Build DAG of workflow dependencies
        
        Returns: {step: [dependencies]}
        """
        graph = {}
        
        for step_name, step_config in workflow.items():
            dependencies = step_config.get('depends_on', [])
            graph[step_name] = dependencies if isinstance(dependencies, list) else [dependencies]
        
        return graph
    
    def find_parallel_groups(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        Identify steps that can run in parallel
        
        Algorithm: Group steps with no mutual dependencies
        """
        parallel_groups = []
        processed = set()
        
        # Topological sort to get execution levels
        levels = []
        remaining = set(graph.keys())
        
        while remaining:
            # Find steps with no remaining dependencies
            ready = []
            for step in remaining:
                deps = graph[step]
                if all(d in processed for d in deps):
                    ready.append(step)
            
            if not ready:
                # Circular dependency detected
                logger.warning(f"Circular dependency in remaining steps: {remaining}")
                break
            
            levels.append(ready)
            processed.update(ready)
            remaining -= set(ready)
        
        return levels
    
    def calculate_critical_path(self, graph: Dict[str, List[str]], 
                                durations: Dict[str, float]) -> Tuple[List[str], float]:
        """
        Calculate critical path (longest path) through workflow
        
        Returns: (critical_path, total_time)
        """
        # Use dynamic programming to find longest path
        memo = {}
        
        def longest_path(step: str) -> Tuple[float, List[str]]:
            if step in memo:
                return memo[step]
            
            deps = graph.get(step, [])
            if not deps:
                result = (durations.get(step, 1.0), [step])
            else:
                max_time = 0
                max_path = []
                
                for dep in deps:
                    dep_time, dep_path = longest_path(dep)
                    if dep_time > max_time:
                        max_time = dep_time
                        max_path = dep_path
                
                result = (max_time + durations.get(step, 1.0), max_path + [step])
            
            memo[step] = result
            return result
        
        # Find overall critical path
        max_time = 0
        critical_path = []
        
        for step in graph.keys():
            time, path = longest_path(step)
            if time > max_time:
                max_time = time
                critical_path = path
        
        return critical_path, max_time
    
    def predict_success_probability(self, steps: List[str]) -> float:
        """
        Predict success probability using ML model
        
        Combines:
        - Individual step success rates
        - Sequential pattern success rates
        - Historical baseline
        """
        if not steps:
            return 1.0
        
        probabilities = []
        
        # Individual step probabilities
        for step in steps:
            prob = self.success_patterns.get(step, 0.95)  # Default 95% if unknown
            probabilities.append(prob)
        
        # Sequential pattern probabilities
        for i in range(len(steps) - 1):
            pair = f"{steps[i]}→{steps[i+1]}"
            prob = self.success_patterns.get(pair, 0.90)
            probabilities.append(prob)
        
        # Combined probability (geometric mean for dependencies)
        if probabilities:
            product = 1.0
            for p in probabilities:
                product *= p
            return product ** (1.0 / len(probabilities))
        
        return 0.95
    
    def calculate_risk_score(self, path: WorkflowPath) -> float:
        """
        Calculate risk score for a path
        
        Risk factors:
        - Number of steps (more = riskier)
        - Success probability (lower = riskier)
        - Parallel complexity (more = riskier)
        """
        step_risk = min(len(path.steps) / 20.0, 1.0)  # Normalize to 20 steps
        success_risk = 1.0 - path.success_probability
        parallel_risk = min(len(path.parallel_groups) / 10.0, 0.5)  # Cap at 0.5
        
        # Weighted combination
        risk = (step_risk * 0.3 + success_risk * 0.5 + parallel_risk * 0.2)
        return min(risk, 1.0)
    
    async def optimize(self, workflow: Dict, 
                      constraints: Optional[Dict] = None) -> PathOptimization:
        """
        Main optimization entry point
        
        Args:
            workflow: {step_name: {depends_on: [], estimated_time: float}}
            constraints: {max_parallel: int, timeout: float}
        
        Returns:
            PathOptimization with multiple optimized paths
        """
        constraints = constraints or {}
        
        # Build dependency graph
        graph = self.build_dependency_graph(workflow)
        self.dependency_graph = graph
        
        # Extract durations
        durations = {name: config.get('estimated_time', 1.0) 
                    for name, config in workflow.items()}
        
        # Find critical path (sequential execution)
        critical_path, sequential_time = self.calculate_critical_path(graph, durations)
        
        # Find parallel execution groups
        parallel_groups = self.find_parallel_groups(graph)
        
        # Calculate parallel execution time
        parallel_time = sum(
            max(durations.get(step, 1.0) for step in group) 
            for group in parallel_groups
        )
        
        # Generate optimized paths
        optimized_paths = []
        
        # Path 1: Maximum parallelization
        max_parallel_path = WorkflowPath(
            path_id=self._generate_path_id("max_parallel"),
            steps=critical_path,
            estimated_time=parallel_time,
            success_probability=self.predict_success_probability(critical_path),
            dependencies=list(graph.keys()),
            parallel_groups=parallel_groups,
            risk_score=0.0,  # Will be calculated
            recommended=True
        )
        max_parallel_path.risk_score = self.calculate_risk_score(max_parallel_path)
        optimized_paths.append(max_parallel_path)
        
        # Path 2: Conservative (less parallelization)
        conservative_groups = [group[:2] for group in parallel_groups]  # Limit parallel tasks
        conservative_time = sequential_time * 0.7  # Estimate
        conservative_path = WorkflowPath(
            path_id=self._generate_path_id("conservative"),
            steps=critical_path,
            estimated_time=conservative_time,
            success_probability=self.predict_success_probability(critical_path) * 1.05,
            dependencies=list(graph.keys()),
            parallel_groups=conservative_groups,
            risk_score=0.0,
            recommended=False
        )
        conservative_path.risk_score = self.calculate_risk_score(conservative_path)
        optimized_paths.append(conservative_path)
        
        # Path 3: Sequential (no parallelization)
        sequential_path = WorkflowPath(
            path_id=self._generate_path_id("sequential"),
            steps=critical_path,
            estimated_time=sequential_time,
            success_probability=self.predict_success_probability(critical_path) * 1.1,
            dependencies=list(graph.keys()),
            parallel_groups=[],
            risk_score=0.0,
            recommended=False
        )
        sequential_path.risk_score = self.calculate_risk_score(sequential_path)
        optimized_paths.append(sequential_path)
        
        # Sort by success probability and time
        optimized_paths.sort(key=lambda p: (p.success_probability, -p.estimated_time), reverse=True)
        
        # Generate recommendations
        recommendations = []
        time_saved = sequential_time - parallel_time
        
        if time_saved > 10:
            recommendations.append(f"⚡ Parallelization can save {time_saved:.1f}s ({time_saved/sequential_time*100:.1f}%)")
        
        if len(parallel_groups) > 5:
            recommendations.append(f"🔧 Consider batching {len(parallel_groups)} parallel groups")
        
        if optimized_paths[0].risk_score > 0.7:
            recommendations.append("⚠️ High complexity detected - consider simplification")
        
        return PathOptimization(
            original_path=critical_path,
            optimized_paths=optimized_paths,
            time_saved=time_saved,
            parallel_opportunities=len(parallel_groups),
            recommendations=recommendations,
            confidence=optimized_paths[0].success_probability
        )
    
    def _generate_path_id(self, variant: str) -> str:
        """Generate unique path ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(f"{variant}_{timestamp}".encode()).hexdigest()[:12]
    
    async def record_execution(self, path_id: str, steps: List[str], 
                              success: bool, duration: float):
        """Record execution result for ML training"""
        record = {
            'path_id': path_id,
            'steps': steps,
            'success': success,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        
        self.execution_history.append(record)
        self._train_model()  # Retrain with new data
        self.save_history()


# ══════════════════════════════════════════════════════════════════════════════
# 🌐 FastAPI Service Endpoint
# ══════════════════════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="QPR Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qpr = QPREngine()


class WorkflowRequest(BaseModel):
    workflow: Dict
    constraints: Optional[Dict] = None


class ExecutionRecord(BaseModel):
    path_id: str
    steps: List[str]
    success: bool
    duration: float


@app.get("/")
async def root():
    return {
        "service": "QPR Engine",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "history_records": len(qpr.execution_history)}


@app.post("/optimize")
async def optimize_workflow(request: WorkflowRequest):
    """Optimize workflow execution path"""
    try:
        result = await qpr.optimize(request.workflow, request.constraints)
        return asdict(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/record")
async def record_execution(record: ExecutionRecord):
    """Record execution result for ML training"""
    await qpr.record_execution(
        record.path_id,
        record.steps,
        record.success,
        record.duration
    )
    return {"status": "recorded", "total_records": len(qpr.execution_history)}


@app.get("/patterns")
async def get_patterns():
    """Get learned success patterns"""
    return {
        "patterns": qpr.success_patterns,
        "total_records": len(qpr.execution_history)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
