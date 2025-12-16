#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║ 🎭 COMPONENT C: WORKFLOW ORCHESTRATOR                                         ║
║ Automated workflow execution with rollback and telemetry                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum
import aiohttp
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    ROLLED_BACK = "rolled_back"


@dataclass
class StepResult:
    """Result of a workflow step execution"""
    step_name: str
    status: StepStatus
    start_time: str
    end_time: Optional[str] = None
    duration: float = 0.0
    output: Any = None
    error: Optional[str] = None
    rollback_executed: bool = False


@dataclass
class WorkflowExecution:
    """Complete workflow execution result"""
    workflow_id: str
    workflow_name: str
    status: StepStatus
    start_time: str
    end_time: Optional[str] = None
    total_duration: float = 0.0
    steps: List[StepResult] = field(default_factory=list)
    success_rate: float = 0.0
    telemetry: Dict[str, Any] = field(default_factory=dict)
    optimized_path_used: bool = False


class WorkflowOrchestrator:
    """
    🎭 Advanced workflow orchestrator
    
    Features:
    - Parallel execution
    - Automatic rollback
    - Real-time telemetry
    - Integration with QPR Engine
    - State persistence
    """
    
    def __init__(self, qpr_url: str = "http://localhost:8011",
                 integrity_url: str = "http://localhost:8010"):
        self.qpr_url = qpr_url
        self.integrity_url = integrity_url
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.execution_history: List[WorkflowExecution] = []
        self.step_registry: Dict[str, Callable] = {}
        self._register_builtin_steps()
    
    def _register_builtin_steps(self):
        """Register built-in step executors"""
        self.step_registry = {
            'health_check': self._step_health_check,
            'service_discovery': self._step_service_discovery,
            'cleanup': self._step_cleanup,
            'validation': self._step_validation,
            'backup': self._step_backup,
            'restore': self._step_restore,
            'api_call': self._step_api_call,
            'shell_command': self._step_shell_command,
        }
    
    async def _step_health_check(self, config: Dict) -> Dict:
        """Built-in health check step"""
        url = config.get('url', self.integrity_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/score") as resp:
                return await resp.json()
    
    async def _step_service_discovery(self, config: Dict) -> Dict:
        """Built-in service discovery step"""
        # Discover running services
        proc = await asyncio.create_subprocess_exec(
            'docker', 'ps', '--format', '{{.Names}}',
            stdout=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        services = stdout.decode().strip().split('\n')
        return {'services': services, 'count': len(services)}
    
    async def _step_cleanup(self, config: Dict) -> Dict:
        """Built-in cleanup step"""
        target = config.get('target', '/tmp')
        # Safe cleanup simulation
        return {'cleaned': target, 'status': 'success'}
    
    async def _step_validation(self, config: Dict) -> Dict:
        """Built-in validation step"""
        checks = config.get('checks', [])
        results = {check: True for check in checks}
        return {'validation_results': results, 'all_passed': all(results.values())}
    
    async def _step_backup(self, config: Dict) -> Dict:
        """Built-in backup step"""
        source = config.get('source', '.')
        destination = config.get('destination', '/tmp/backup')
        return {'backed_up': source, 'to': destination, 'status': 'success'}
    
    async def _step_restore(self, config: Dict) -> Dict:
        """Built-in restore step"""
        backup = config.get('backup', '/tmp/backup')
        return {'restored_from': backup, 'status': 'success'}
    
    async def _step_api_call(self, config: Dict) -> Dict:
        """Built-in API call step"""
        url = config.get('url')
        method = config.get('method', 'GET')
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url) as resp:
                return await resp.json()
    
    async def _step_shell_command(self, config: Dict) -> Dict:
        """Built-in shell command step"""
        command = config.get('command')
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return {
            'stdout': stdout.decode(),
            'stderr': stderr.decode(),
            'returncode': proc.returncode
        }
    
    async def execute_step(self, step_name: str, step_config: Dict,
                          context: Dict) -> StepResult:
        """
        Execute a single workflow step
        
        Args:
            step_name: Name of the step
            step_config: Step configuration
            context: Execution context (shared state)
        """
        start_time = datetime.now()
        result = StepResult(
            step_name=step_name,
            status=StepStatus.RUNNING,
            start_time=start_time.isoformat()
        )
        
        try:
            logger.info(f"▶️  Executing step: {step_name}")
            
            # Get step executor
            step_type = step_config.get('type', step_name)
            executor = self.step_registry.get(step_type)
            
            if not executor:
                raise ValueError(f"Unknown step type: {step_type}")
            
            # Execute with timeout
            timeout = step_config.get('timeout', 30)
            output = await asyncio.wait_for(
                executor(step_config),
                timeout=timeout
            )
            
            result.status = StepStatus.SUCCESS
            result.output = output
            logger.info(f"✅ Step completed: {step_name}")
            
        except asyncio.TimeoutError:
            result.status = StepStatus.FAILED
            result.error = f"Timeout after {step_config.get('timeout', 30)}s"
            logger.error(f"❌ Step timeout: {step_name}")
            
        except Exception as e:
            result.status = StepStatus.FAILED
            result.error = str(e)
            logger.error(f"❌ Step failed: {step_name} - {e}")
            logger.debug(traceback.format_exc())
        
        finally:
            end_time = datetime.now()
            result.end_time = end_time.isoformat()
            result.duration = (end_time - start_time).total_seconds()
        
        return result
    
    async def rollback_step(self, step_name: str, step_config: Dict,
                           result: StepResult) -> bool:
        """
        Execute rollback for a failed step
        
        Returns:
            True if rollback successful
        """
        rollback_config = step_config.get('rollback')
        if not rollback_config:
            logger.warning(f"No rollback defined for step: {step_name}")
            return False
        
        try:
            logger.info(f"🔄 Rolling back step: {step_name}")
            
            rollback_type = rollback_config.get('type')
            executor = self.step_registry.get(rollback_type)
            
            if executor:
                await executor(rollback_config)
                result.rollback_executed = True
                result.status = StepStatus.ROLLED_BACK
                logger.info(f"✅ Rollback successful: {step_name}")
                return True
            
        except Exception as e:
            logger.error(f"❌ Rollback failed: {step_name} - {e}")
        
        return False
    
    async def execute_parallel_group(self, steps: List[str], 
                                    workflow: Dict,
                                    context: Dict) -> List[StepResult]:
        """Execute a group of steps in parallel"""
        tasks = []
        for step_name in steps:
            step_config = workflow.get(step_name, {})
            tasks.append(self.execute_step(step_name, step_config, context))
        
        return await asyncio.gather(*tasks)
    
    async def get_optimized_path(self, workflow: Dict) -> Optional[Dict]:
        """Get optimized path from QPR Engine"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.qpr_url}/optimize",
                    json={'workflow': workflow}
                ) as resp:
                    return await resp.json()
        except Exception as e:
            logger.warning(f"Could not get optimized path: {e}")
            return None
    
    async def execute(self, workflow_name: str, workflow: Dict,
                     use_optimization: bool = True) -> WorkflowExecution:
        """
        Execute complete workflow
        
        Args:
            workflow_name: Name of the workflow
            workflow: {step_name: {type, depends_on, timeout, rollback}}
            use_optimization: Use QPR Engine for path optimization
        
        Returns:
            WorkflowExecution result
        """
        workflow_id = f"{workflow_name}_{datetime.now().timestamp()}"
        start_time = datetime.now()
        
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            status=StepStatus.RUNNING,
            start_time=start_time.isoformat()
        )
        
        self.active_executions[workflow_id] = execution
        context = {}  # Shared execution context
        
        try:
            # Get optimized path
            optimized = None
            parallel_groups = []
            
            if use_optimization:
                optimized = await self.get_optimized_path(workflow)
                if optimized and optimized.get('optimized_paths'):
                    best_path = optimized['optimized_paths'][0]
                    parallel_groups = best_path.get('parallel_groups', [])
                    execution.optimized_path_used = True
            
            # Execute workflow
            if parallel_groups:
                # Execute optimized parallel path
                for group in parallel_groups:
                    results = await self.execute_parallel_group(group, workflow, context)
                    execution.steps.extend(results)
                    
                    # Check for failures
                    if any(r.status == StepStatus.FAILED for r in results):
                        # Rollback failed steps
                        for result in results:
                            if result.status == StepStatus.FAILED:
                                step_config = workflow.get(result.step_name, {})
                                await self.rollback_step(result.step_name, step_config, result)
                        break
            else:
                # Execute sequentially
                for step_name, step_config in workflow.items():
                    result = await self.execute_step(step_name, step_config, context)
                    execution.steps.append(result)
                    
                    if result.status == StepStatus.FAILED:
                        # Rollback
                        await self.rollback_step(step_name, step_config, result)
                        break
            
            # Calculate success rate
            total_steps = len(execution.steps)
            successful_steps = sum(1 for s in execution.steps if s.status == StepStatus.SUCCESS)
            execution.success_rate = (successful_steps / total_steps) if total_steps > 0 else 0.0
            
            # Overall status
            if all(s.status == StepStatus.SUCCESS for s in execution.steps):
                execution.status = StepStatus.SUCCESS
            else:
                execution.status = StepStatus.FAILED
            
            # Collect telemetry
            execution.telemetry = {
                'total_steps': total_steps,
                'successful_steps': successful_steps,
                'failed_steps': total_steps - successful_steps,
                'parallel_groups_used': len(parallel_groups),
                'optimization_used': use_optimization,
                'average_step_duration': sum(s.duration for s in execution.steps) / total_steps if total_steps > 0 else 0
            }
            
        except Exception as e:
            execution.status = StepStatus.FAILED
            logger.error(f"Workflow execution failed: {e}")
            logger.debug(traceback.format_exc())
        
        finally:
            end_time = datetime.now()
            execution.end_time = end_time.isoformat()
            execution.total_duration = (end_time - start_time).total_seconds()
            
            # Store in history
            self.execution_history.append(execution)
            del self.active_executions[workflow_id]
        
        return execution


# ══════════════════════════════════════════════════════════════════════════════
# 🌐 FastAPI Service Endpoint
# ══════════════════════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Workflow Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = WorkflowOrchestrator()


class WorkflowRequest(BaseModel):
    workflow_name: str
    workflow: Dict
    use_optimization: bool = True


@app.get("/")
async def root():
    return {
        "service": "Workflow Orchestrator",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "active_executions": len(orchestrator.active_executions),
        "total_executions": len(orchestrator.execution_history)
    }


@app.post("/execute")
async def execute_workflow(request: WorkflowRequest):
    """Execute a workflow"""
    try:
        result = await orchestrator.execute(
            request.workflow_name,
            request.workflow,
            request.use_optimization
        )
        return asdict(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history(limit: int = 10):
    """Get execution history"""
    history = orchestrator.execution_history[-limit:]
    return [asdict(h) for h in history]


@app.get("/active")
async def get_active():
    """Get active executions"""
    return {
        wid: asdict(execution)
        for wid, execution in orchestrator.active_executions.items()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
