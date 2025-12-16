#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   WORKFLOW ORCHESTRATOR ENGINE                                ║
║              Phase-based System Transformation Manager                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Component C: High-level workflow orchestration for system transformation
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from enum import Enum

# Import our other components
try:
    from .system_integrity_scorer import SystemIntegrityScorer, HealthScore
    from .qpr_engine import QuantumPathReconstructor, QPRReport
except ImportError:
    # Fallback for standalone testing
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from system_integrity_scorer import SystemIntegrityScorer, HealthScore
    from qpr_engine import QuantumPathReconstructor, QPRReport

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowPhase(Enum):
    """Workflow execution phases"""
    INITIALIZATION = "initialization"
    PRE_ASSESSMENT = "pre_assessment"
    PATH_RECONSTRUCTION = "path_reconstruction"
    DOTFILE_MIGRATION = "dotfile_migration"
    SYMLINK_CLEANUP = "symlink_cleanup"
    ALIAS_OPTIMIZATION = "alias_optimization"
    POST_ASSESSMENT = "post_assessment"
    VALIDATION = "validation"
    FINALIZATION = "finalization"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class PhaseResult:
    """Result from a single workflow phase"""
    phase: str
    success: bool
    duration_seconds: float
    score: Optional[float]
    messages: List[str]
    errors: List[str]
    data: Dict[str, Any]
    timestamp: str


@dataclass
class WorkflowReport:
    """Complete workflow execution report"""
    workflow_id: str
    start_time: str
    end_time: str
    total_duration: float
    current_phase: str
    phases_completed: List[str]
    phases_failed: List[str]
    overall_success: bool
    pre_score: Optional[float]
    post_score: Optional[float]
    improvement: Optional[float]
    phase_results: List[PhaseResult]
    rollback_performed: bool
    backup_location: str
    recommendations: List[str]


class WorkflowOrchestrator:
    """
    High-level workflow orchestrator for system transformation.
    
    Orchestration Flow:
    1. INITIALIZATION: Setup environment, create backup
    2. PRE_ASSESSMENT: Baseline health scoring
    3. PATH_RECONSTRUCTION: Optimize PATH variable
    4. DOTFILE_MIGRATION: Migrate and merge dotfiles
    5. SYMLINK_CLEANUP: Fix broken/circular symlinks
    6. ALIAS_OPTIMIZATION: Optimize shell aliases
    7. POST_ASSESSMENT: Final health scoring
    8. VALIDATION: Verify improvements
    9. FINALIZATION: Cleanup and report generation
    
    Features:
    - Phase-based execution with rollback support
    - Real-time progress tracking
    - Comprehensive error handling
    - Automatic validation
    - Detailed reporting
    """
    
    # Minimum improvement threshold (percentage points)
    MIN_IMPROVEMENT = 5.0
    
    # Maximum phase retries
    MAX_RETRIES = 3
    
    def __init__(self, dry_run: bool = False, auto_rollback: bool = True):
        """Initialize workflow orchestrator"""
        self.dry_run = dry_run
        self.auto_rollback = auto_rollback
        self.workflow_id = self._generate_workflow_id()
        self.current_phase = WorkflowPhase.INITIALIZATION
        
        # Components
        self.scorer = SystemIntegrityScorer()
        self.qpr = QuantumPathReconstructor(dry_run=dry_run)
        
        # State tracking
        self.start_time = None
        self.end_time = None
        self.phase_results: List[PhaseResult] = []
        self.pre_score: Optional[HealthScore] = None
        self.post_score: Optional[HealthScore] = None
        self.qpr_report: Optional[QPRReport] = None
        self.backup_location = None
        self.rollback_performed = False
        
        # Phase definitions
        self.phases = [
            (WorkflowPhase.INITIALIZATION, self._phase_initialization),
            (WorkflowPhase.PRE_ASSESSMENT, self._phase_pre_assessment),
            (WorkflowPhase.PATH_RECONSTRUCTION, self._phase_path_reconstruction),
            (WorkflowPhase.DOTFILE_MIGRATION, self._phase_dotfile_migration),
            (WorkflowPhase.SYMLINK_CLEANUP, self._phase_symlink_cleanup),
            (WorkflowPhase.ALIAS_OPTIMIZATION, self._phase_alias_optimization),
            (WorkflowPhase.POST_ASSESSMENT, self._phase_post_assessment),
            (WorkflowPhase.VALIDATION, self._phase_validation),
            (WorkflowPhase.FINALIZATION, self._phase_finalization),
        ]
        
        logger.info(f"🎭 Workflow Orchestrator initialized (ID: {self.workflow_id})")
    
    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"workflow_{timestamp}"
    
    # ==================== PHASE IMPLEMENTATIONS ====================
    
    def _phase_initialization(self) -> PhaseResult:
        """Phase 1: Initialize environment and create backup"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("📦 Creating system backup...")
            self.backup_location = self.qpr.create_backup()
            messages.append(f"Backup created: {self.backup_location}")
            
            logger.info("✅ Initialization complete")
            
            return PhaseResult(
                phase=WorkflowPhase.INITIALIZATION.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={'backup_location': self.backup_location},
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.INITIALIZATION.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_pre_assessment(self) -> PhaseResult:
        """Phase 2: Baseline health assessment"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("🔍 Running pre-transformation assessment...")
            self.pre_score = self.scorer.calculate_health_score()
            
            messages.append(f"Baseline health score: {self.pre_score.overall_score:.1f}/100")
            messages.append(f"Risk level: {self.pre_score.risk_level}")
            
            logger.info(f"✅ Pre-assessment complete: {self.pre_score.overall_score:.1f}/100")
            
            return PhaseResult(
                phase=WorkflowPhase.PRE_ASSESSMENT.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=self.pre_score.overall_score,
                messages=messages,
                errors=errors,
                data=asdict(self.pre_score),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Pre-assessment failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.PRE_ASSESSMENT.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_path_reconstruction(self) -> PhaseResult:
        """Phase 3: Optimize PATH variable"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("🛤️  Reconstructing PATH...")
            path_analysis = self.qpr.analyze_path()
            self.qpr.reconstruct_path(path_analysis)
            
            messages.append(f"PATH optimization score: {path_analysis.optimization_score:.1f}/100")
            messages.append(f"Duplicates removed: {len(path_analysis.duplicates)}")
            messages.append(f"Non-existent paths removed: {len(path_analysis.non_existent)}")
            
            logger.info(f"✅ PATH reconstruction complete: {path_analysis.optimization_score:.1f}/100")
            
            return PhaseResult(
                phase=WorkflowPhase.PATH_RECONSTRUCTION.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=path_analysis.optimization_score,
                messages=messages,
                errors=errors,
                data=asdict(path_analysis),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ PATH reconstruction failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.PATH_RECONSTRUCTION.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_dotfile_migration(self) -> PhaseResult:
        """Phase 4: Migrate and merge dotfiles"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("📄 Migrating dotfiles...")
            dotfile_analysis = self.qpr.analyze_dotfiles()
            self.qpr.migrate_dotfiles(dotfile_analysis)
            
            messages.append(f"Files found: {len(dotfile_analysis.files_found)}")
            messages.append(f"Migrations performed: {len(dotfile_analysis.merge_candidates)}")
            messages.append(f"Conflicts detected: {len(dotfile_analysis.conflicts)}")
            
            logger.info("✅ Dotfile migration complete")
            
            return PhaseResult(
                phase=WorkflowPhase.DOTFILE_MIGRATION.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data=asdict(dotfile_analysis),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Dotfile migration failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.DOTFILE_MIGRATION.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_symlink_cleanup(self) -> PhaseResult:
        """Phase 5: Clean up broken symlinks"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("🔗 Cleaning up symlinks...")
            symlink_analysis = self.qpr.analyze_symlinks()
            self.qpr.reconstruct_symlinks(symlink_analysis)
            
            messages.append(f"Total scanned: {symlink_analysis.total_scanned}")
            messages.append(f"Broken removed: {len(symlink_analysis.broken_symlinks)}")
            messages.append(f"Circular removed: {len(symlink_analysis.circular_symlinks)}")
            
            logger.info("✅ Symlink cleanup complete")
            
            return PhaseResult(
                phase=WorkflowPhase.SYMLINK_CLEANUP.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data=asdict(symlink_analysis),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Symlink cleanup failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.SYMLINK_CLEANUP.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_alias_optimization(self) -> PhaseResult:
        """Phase 6: Optimize shell aliases"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("🎯 Optimizing aliases...")
            alias_analysis = self.qpr.analyze_aliases()
            self.qpr.optimize_aliases(alias_analysis)
            
            messages.append(f"Aliases found: {len(alias_analysis.current_aliases)}")
            messages.append(f"Duplicates removed: {len(alias_analysis.duplicates)}")
            messages.append(f"Obsolete removed: {len(alias_analysis.obsolete)}")
            messages.append(f"Suggestions added: {len(alias_analysis.suggestions)}")
            
            logger.info(f"✅ Alias optimization complete: {alias_analysis.optimization_score:.1f}/100")
            
            return PhaseResult(
                phase=WorkflowPhase.ALIAS_OPTIMIZATION.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=alias_analysis.optimization_score,
                messages=messages,
                errors=errors,
                data=asdict(alias_analysis),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Alias optimization failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.ALIAS_OPTIMIZATION.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_post_assessment(self) -> PhaseResult:
        """Phase 7: Post-transformation health assessment"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("🔍 Running post-transformation assessment...")
            self.post_score = self.scorer.calculate_health_score()
            
            improvement = None
            if self.pre_score:
                improvement = self.post_score.overall_score - self.pre_score.overall_score
                messages.append(f"Pre-score: {self.pre_score.overall_score:.1f}/100")
                messages.append(f"Post-score: {self.post_score.overall_score:.1f}/100")
                messages.append(f"Improvement: {improvement:+.1f} points")
            else:
                messages.append(f"Post-score: {self.post_score.overall_score:.1f}/100")
            
            logger.info(f"✅ Post-assessment complete: {self.post_score.overall_score:.1f}/100")
            
            return PhaseResult(
                phase=WorkflowPhase.POST_ASSESSMENT.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=self.post_score.overall_score,
                messages=messages,
                errors=errors,
                data={
                    'post_score': asdict(self.post_score),
                    'improvement': improvement
                },
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Post-assessment failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.POST_ASSESSMENT.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_validation(self) -> PhaseResult:
        """Phase 8: Validate improvements"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("✔️  Validating transformation results...")
            
            valid = True
            
            # Validate improvement
            if self.pre_score and self.post_score:
                improvement = self.post_score.overall_score - self.pre_score.overall_score
                
                if improvement < self.MIN_IMPROVEMENT:
                    messages.append(f"⚠️ Improvement ({improvement:.1f} points) below threshold ({self.MIN_IMPROVEMENT} points)")
                    
                    if self.auto_rollback:
                        messages.append("Auto-rollback triggered")
                        self._perform_rollback()
                        valid = False
                else:
                    messages.append(f"✅ Improvement validated: {improvement:+.1f} points")
            
            # Validate no critical degradation
            if self.post_score and self.post_score.risk_level == 'CRITICAL':
                messages.append("⚠️ System entered CRITICAL risk level")
                errors.append("Post-transformation risk level is CRITICAL")
                
                if self.auto_rollback:
                    messages.append("Auto-rollback triggered")
                    self._perform_rollback()
                    valid = False
            
            if valid:
                logger.info("✅ Validation passed")
            else:
                logger.warning("⚠️ Validation failed")
            
            return PhaseResult(
                phase=WorkflowPhase.VALIDATION.value,
                success=valid,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={'validated': valid},
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.VALIDATION.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    def _phase_finalization(self) -> PhaseResult:
        """Phase 9: Finalize and generate report"""
        phase_start = time.time()
        messages = []
        errors = []
        
        try:
            logger.info("📝 Finalizing workflow...")
            
            # Generate recommendations
            recommendations = self._generate_recommendations()
            messages.extend(recommendations)
            
            logger.info("✅ Workflow finalized")
            
            return PhaseResult(
                phase=WorkflowPhase.FINALIZATION.value,
                success=True,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={'recommendations': recommendations},
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            logger.error(f"❌ Finalization failed: {e}")
            errors.append(str(e))
            
            return PhaseResult(
                phase=WorkflowPhase.FINALIZATION.value,
                success=False,
                duration_seconds=time.time() - phase_start,
                score=None,
                messages=messages,
                errors=errors,
                data={},
                timestamp=datetime.now().isoformat()
            )
    
    # ==================== WORKFLOW EXECUTION ====================
    
    def execute(self) -> WorkflowReport:
        """Execute complete workflow"""
        logger.info(f"🚀 Starting workflow execution: {self.workflow_id}")
        self.start_time = datetime.now()
        
        try:
            # Execute phases sequentially
            for phase_enum, phase_func in self.phases:
                self.current_phase = phase_enum
                logger.info(f"\n{'='*80}\n🎯 Phase: {phase_enum.value.upper()}\n{'='*80}")
                
                result = phase_func()
                self.phase_results.append(result)
                
                # Check if phase failed
                if not result.success:
                    logger.error(f"❌ Phase {phase_enum.value} failed!")
                    
                    # Perform rollback if enabled
                    if self.auto_rollback and self.backup_location:
                        logger.info("🔄 Triggering automatic rollback...")
                        self._perform_rollback()
                    
                    self.current_phase = WorkflowPhase.FAILED
                    break
            
            # Mark as completed if all phases succeeded
            if self.current_phase != WorkflowPhase.FAILED:
                self.current_phase = WorkflowPhase.COMPLETED
            
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {e}")
            self.current_phase = WorkflowPhase.FAILED
            
            if self.auto_rollback and self.backup_location:
                logger.info("🔄 Triggering automatic rollback...")
                self._perform_rollback()
        
        finally:
            self.end_time = datetime.now()
            report = self._generate_report()
            self._save_report(report)
            
            return report
    
    def _perform_rollback(self):
        """Perform system rollback"""
        try:
            logger.info("🔄 Performing rollback...")
            self.qpr.rollback()
            self.rollback_performed = True
            self.current_phase = WorkflowPhase.ROLLED_BACK
            logger.info("✅ Rollback completed")
        except Exception as e:
            logger.error(f"❌ Rollback failed: {e}")
    
    def _generate_recommendations(self) -> List[str]:
        """Generate final recommendations"""
        recommendations = []
        
        if self.post_score:
            # Add recommendations from health score
            recommendations.extend(self.post_score.recommendations[:3])
        
        # Add workflow-specific recommendations
        if self.pre_score and self.post_score:
            improvement = self.post_score.overall_score - self.pre_score.overall_score
            
            if improvement > 20:
                recommendations.append("🎉 Excellent improvement! System is significantly healthier")
            elif improvement > 10:
                recommendations.append("✅ Good improvement! Consider periodic maintenance")
            elif improvement > 0:
                recommendations.append("📊 Modest improvement. Monitor system and re-run if needed")
        
        recommendations.append("💡 Restart your terminal to apply all changes")
        recommendations.append("📚 Review backup at: " + (self.backup_location or "N/A"))
        
        return recommendations
    
    def _generate_report(self) -> WorkflowReport:
        """Generate comprehensive workflow report"""
        phases_completed = [r.phase for r in self.phase_results if r.success]
        phases_failed = [r.phase for r in self.phase_results if not r.success]
        
        pre_score_value = self.pre_score.overall_score if self.pre_score else None
        post_score_value = self.post_score.overall_score if self.post_score else None
        
        improvement = None
        if pre_score_value is not None and post_score_value is not None:
            improvement = post_score_value - pre_score_value
        
        # Get recommendations from finalization phase
        recommendations = []
        for result in self.phase_results:
            if result.phase == WorkflowPhase.FINALIZATION.value:
                recommendations = result.data.get('recommendations', [])
        
        total_duration = 0
        if self.start_time and self.end_time:
            total_duration = (self.end_time - self.start_time).total_seconds()
        
        return WorkflowReport(
            workflow_id=self.workflow_id,
            start_time=self.start_time.isoformat() if self.start_time else '',
            end_time=self.end_time.isoformat() if self.end_time else '',
            total_duration=total_duration,
            current_phase=self.current_phase.value,
            phases_completed=phases_completed,
            phases_failed=phases_failed,
            overall_success=self.current_phase == WorkflowPhase.COMPLETED,
            pre_score=pre_score_value,
            post_score=post_score_value,
            improvement=improvement,
            phase_results=self.phase_results,
            rollback_performed=self.rollback_performed,
            backup_location=self.backup_location or '',
            recommendations=recommendations
        )
    
    def _save_report(self, report: WorkflowReport):
        """Save workflow report to file"""
        report_path = Path(f"/tmp/{self.workflow_id}_report.json")
        
        try:
            with open(report_path, 'w') as f:
                json.dump(asdict(report), f, indent=2, default=str)
            
            logger.info(f"📄 Report saved: {report_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")


def main():
    """CLI interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Workflow Orchestrator')
    parser.add_argument('--dry-run', action='store_true', help='Simulate without making changes')
    parser.add_argument('--no-rollback', action='store_true', help='Disable automatic rollback')
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("🎭 WORKFLOW ORCHESTRATOR - System Transformation")
    print("="*80 + "\n")
    
    orchestrator = WorkflowOrchestrator(
        dry_run=args.dry_run,
        auto_rollback=not args.no_rollback
    )
    
    report = orchestrator.execute()
    
    print("\n" + "="*80)
    print("📊 WORKFLOW SUMMARY")
    print("="*80 + "\n")
    
    print(f"Workflow ID: {report.workflow_id}")
    print(f"Success: {'✅ YES' if report.overall_success else '❌ NO'}")
    print(f"Duration: {report.total_duration:.1f}s")
    print(f"Rollback: {'⚠️ YES' if report.rollback_performed else '✅ NO'}")
    
    if report.pre_score is not None and report.post_score is not None:
        print(f"\n📈 Health Scores:")
        print(f"  Before:      {report.pre_score:.1f}/100")
        print(f"  After:       {report.post_score:.1f}/100")
        print(f"  Improvement: {report.improvement:+.1f} points")
    
    print(f"\n✅ Completed Phases ({len(report.phases_completed)}):")
    for phase in report.phases_completed:
        print(f"  • {phase}")
    
    if report.phases_failed:
        print(f"\n❌ Failed Phases ({len(report.phases_failed)}):")
        for phase in report.phases_failed:
            print(f"  • {phase}")
    
    print(f"\n💡 Recommendations:")
    for rec in report.recommendations:
        print(f"  {rec}")
    
    print(f"\n📦 Backup: {report.backup_location}")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
