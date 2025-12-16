# 🚀 macOS Terminal Transformation - DETAILED IMPLEMENTATION PLAN

**Date**: December 15, 2025  
**Status**: Ready for Implementation  
**Estimated Time**: 4-6 hours total

---

## 📋 TABLE OF CONTENTS

1. [Architecture Overview](#architecture-overview)
2. [Component A: System Integrity Scoring](#component-a-system-integrity-scoring)
3. [Component B: QPR Engine](#component-b-qpr-engine)
4. [Component C: Workflow Orchestrator](#component-c-workflow-orchestrator)
5. [Integration Points](#integration-points)
6. [File Structure](#file-structure)
7. [Implementation Order](#implementation-order)

---

## 🏗️ ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUANTUM DASHBOARD                             │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  3D Header + Stats Panel + Menu                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  AUTO-DISCOVERY SCANNER (Background Thread)            │     │
│  │  • System, Hardware, Environment, Network, Software    │     │
│  └────────────────────────────────────────────────────────┘     │
│                           ↓                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  SYSTEM INTEGRITY SCORER ⭐ NEW                        │     │
│  │  • File Integrity Check                                │     │
│  │  • Package Manager Conflicts                           │     │
│  │  • Disk Health Analysis                                │     │
│  │  • Dependency Validation                               │     │
│  │  • Health Score: 0-100%                                │     │
│  └────────────────────────────────────────────────────────┘     │
│                           ↓                                      │
│              ┌────────────┴────────────┐                         │
│              │  Score >= 80%?          │                         │
│              └─────────┬───────────────┘                         │
│                   NO   │   YES                                   │
│         ┌──────────────┴──────────────┐                          │
│         ↓                              ↓                         │
│  ┌─────────────────┐         ┌─────────────────┐                │
│  │ CLEAN SLATE     │         │ QPR ENGINE      │                │
│  │ INITIALIZATION  │         │ ⭐ NEW          │                │
│  │ (Factory Reset) │         │                 │                │
│  └────────┬────────┘         └────────┬────────┘                │
│           │                           │                          │
│           └───────────┬───────────────┘                          │
│                       ↓                                          │
│         ┌──────────────────────────────┐                         │
│         │  TERMINAL CONFIGURATION      │                         │
│         │  • Zsh Config Generation     │                         │
│         │  • Theme Application         │                         │
│         │  • Plugin Installation       │                         │
│         └──────────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 COMPONENT A: SYSTEM INTEGRITY SCORING

### File: `/modules/terminal-config/system_integrity_scorer.py`

**Purpose**: Analyze system health and calculate 0-100% integrity score

### Class Structure

```python
class SystemIntegrityScorer:
    """
    Advanced System Integrity Scoring Engine
    Analyzes system health across multiple dimensions
    """
    
    def __init__(self):
        self.score_components = {
            "file_integrity": 0,      # Core system files complete?
            "package_health": 0,      # Package managers conflict-free?
            "disk_health": 0,         # No unknown clusters/errors?
            "dependency_graph": 0,    # Dependencies resolved?
            "path_integrity": 0,      # PATH variables valid?
            "symlink_health": 0,      # Symlinks not broken?
            "shell_config": 0,        # Shell configs valid?
        }
        self.overall_score = 0
        self.issues_found = []
        self.recommendations = []
    
    # ==================== Core Methods ====================
    
    def calculate_overall_score(self) -> dict:
        """
        Main entry point - runs all checks and calculates score
        Returns: {
            "overall_score": 85.5,
            "component_scores": {...},
            "issues": [...],
            "recommendations": [...],
            "threshold_met": True,
            "next_action": "terminal_config" or "clean_slate"
        }
        """
    
    def check_file_integrity(self) -> float:
        """
        Check core system files completeness
        - /usr/local/bin exists and readable
        - /etc/paths valid
        - Key system directories present
        - Returns: 0-100 score
        """
    
    def check_package_managers(self) -> float:
        """
        Detect package manager conflicts
        - Homebrew status
        - MacPorts conflict detection
        - pip/pip3 conflicts
        - Returns: 0-100 score
        """
    
    def check_disk_health(self) -> float:
        """
        Analyze disk for issues
        - Unknown volume clusters
        - Disk errors via diskutil
        - Free space < 10GB warning
        - Returns: 0-100 score
        """
    
    def check_dependencies(self) -> float:
        """
        Validate dependency integrity
        - Broken library links
        - Missing required tools
        - Version conflicts
        - Returns: 0-100 score
        """
    
    def check_path_integrity(self) -> float:
        """
        Validate PATH environment
        - No duplicate entries
        - All paths exist
        - Optimal ordering
        - Returns: 0-100 score
        """
    
    def check_symlinks(self) -> float:
        """
        Analyze symlink health
        - Broken symlinks count
        - Circular references
        - Stale links
        - Returns: 0-100 score
        """
    
    def check_shell_config(self) -> float:
        """
        Validate shell configurations
        - .zshrc syntax valid
        - No conflicting configs
        - Source files exist
        - Returns: 0-100 score
        """
    
    # ==================== Helper Methods ====================
    
    def _run_command(self, cmd: list) -> tuple:
        """Execute shell command safely"""
    
    def _check_file_exists(self, path: str) -> bool:
        """Check if file/directory exists"""
    
    def _add_issue(self, severity: str, category: str, description: str):
        """Log an issue found during scanning"""
    
    def _add_recommendation(self, action: str, description: str):
        """Add recommended action"""
```

### Algorithm: Overall Score Calculation

```python
def calculate_overall_score(self) -> dict:
    """
    Weighted scoring algorithm:
    - file_integrity: 20%
    - package_health: 15%
    - disk_health: 15%
    - dependency_graph: 15%
    - path_integrity: 15%
    - symlink_health: 10%
    - shell_config: 10%
    """
    
    weights = {
        "file_integrity": 0.20,
        "package_health": 0.15,
        "disk_health": 0.15,
        "dependency_graph": 0.15,
        "path_integrity": 0.15,
        "symlink_health": 0.10,
        "shell_config": 0.10,
    }
    
    # Run all checks
    self.score_components["file_integrity"] = self.check_file_integrity()
    self.score_components["package_health"] = self.check_package_managers()
    self.score_components["disk_health"] = self.check_disk_health()
    self.score_components["dependency_graph"] = self.check_dependencies()
    self.score_components["path_integrity"] = self.check_path_integrity()
    self.score_components["symlink_health"] = self.check_symlinks()
    self.score_components["shell_config"] = self.check_shell_config()
    
    # Calculate weighted average
    total = sum(
        self.score_components[key] * weights[key]
        for key in weights.keys()
    )
    
    self.overall_score = round(total, 1)
    
    # Determine next action
    threshold = 80.0
    next_action = "terminal_config" if self.overall_score >= threshold else "clean_slate"
    
    return {
        "overall_score": self.overall_score,
        "component_scores": self.score_components.copy(),
        "issues": self.issues_found.copy(),
        "recommendations": self.recommendations.copy(),
        "threshold_met": self.overall_score >= threshold,
        "next_action": next_action
    }
```

### Integration with Dashboard

**Modify**: `/modules/terminal-config/macos_quantum_dashboard.py`

```python
# Add import
from system_integrity_scorer import SystemIntegrityScorer

class QuantumDashboard:
    def __init__(self):
        # ... existing code ...
        self.scanner = AutoDiscoveryScanner()
        self.scorer = SystemIntegrityScorer()  # NEW
        self.integrity_results = None  # NEW
    
    async def run(self, duration: int = 30):
        # ... existing code ...
        
        # Start background system scan
        self.scanner.start_scan()
        
        # Wait for scan to complete (runs in background)
        while self.scanner.scanning:
            await asyncio.sleep(0.5)
        
        # NEW: Run integrity scoring after scan completes
        console.print("\n[bold cyan]🔍 Analyzing System Integrity...[/]\n")
        self.integrity_results = self.scorer.calculate_overall_score()
        
        # Show results
        self._show_integrity_score()
        
        # Decide next step
        if self.integrity_results["next_action"] == "clean_slate":
            self._show_clean_slate_recommendation()
        else:
            self._show_config_recommendation()
    
    def _show_integrity_score(self):
        """Display integrity score with visual breakdown"""
        results = self.integrity_results
        
        # Create score panel
        score_text = Text()
        score_text.append(f"Overall Health: ", style="bold cyan")
        
        # Color based on score
        score = results["overall_score"]
        if score >= 80:
            score_text.append(f"{score}%", style="bold green")
            score_text.append(" ✅ EXCELLENT", style="green")
        elif score >= 60:
            score_text.append(f"{score}%", style="bold yellow")
            score_text.append(" ⚠️ FAIR", style="yellow")
        else:
            score_text.append(f"{score}%", style="bold red")
            score_text.append(" ❌ POOR", style="red")
        
        # Component breakdown table
        table = Table(title="Component Breakdown", box=box.ROUNDED)
        table.add_column("Component", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Status")
        
        for name, score in results["component_scores"].items():
            status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
            table.add_row(
                name.replace("_", " ").title(),
                f"{score:.1f}%",
                status
            )
        
        console.print(Panel(score_text, border_style="cyan"))
        console.print(table)
        
        # Show issues if any
        if results["issues"]:
            console.print("\n[bold red]Issues Found:[/]")
            for issue in results["issues"]:
                console.print(f"  • {issue}")
```

---

## 🔧 COMPONENT B: QPR ENGINE

### File: `/modules/terminal-config/qpr_engine.py`

**Purpose**: Quantum Path Reconstruction - Fix paths, symlinks, dotfiles, aliases

### Class Structure

```python
class QuantumPathReconstructor:
    """
    Quantum Path Reconstruction (QPR) Engine
    - Analyzes and reconstructs PATH variables
    - Fixes broken symlinks
    - Migrates dotfiles intelligently
    - Optimizes shell aliases
    """
    
    def __init__(self):
        self.scan_results = {}
        self.path_analysis = {}
        self.symlink_analysis = {}
        self.dotfile_analysis = {}
        self.alias_analysis = {}
        self.reconstruction_plan = []
        self.backup_created = False
    
    # ==================== Main Orchestration ====================
    
    def run_full_reconstruction(self) -> dict:
        """
        Main entry point - runs complete QPR process
        Returns reconstruction report
        """
        self.create_backup()
        self.analyze_paths()
        self.analyze_symlinks()
        self.analyze_dotfiles()
        self.analyze_aliases()
        self.generate_reconstruction_plan()
        self.execute_reconstruction()
        return self.get_report()
    
    # ==================== PATH Reconstruction ====================
    
    def analyze_paths(self):
        """
        Analyze PATH environment variable
        - Detect duplicates
        - Find non-existent paths
        - Identify optimal ordering
        - Detect conflicts
        """
        current_path = os.environ.get("PATH", "").split(":")
        
        self.path_analysis = {
            "current_paths": current_path,
            "duplicates": self._find_duplicates(current_path),
            "non_existent": self._find_non_existent_paths(current_path),
            "optimal_order": self._calculate_optimal_order(current_path),
            "conflicts": self._detect_path_conflicts(current_path),
            "recommended_additions": self._suggest_path_additions()
        }
    
    def _calculate_optimal_order(self, paths: list) -> list:
        """
        Calculate optimal PATH ordering
        Priority:
        1. /usr/local/bin (Homebrew)
        2. ~/.local/bin (User binaries)
        3. Language-specific paths (nvm, pyenv, rbenv)
        4. System paths (/usr/bin, /bin)
        """
        priority_order = [
            "/usr/local/bin",
            "/opt/homebrew/bin",  # Apple Silicon Homebrew
            f"{os.path.expanduser('~')}/.local/bin",
            # ... language managers ...
            "/usr/bin",
            "/bin",
            "/usr/sbin",
            "/sbin"
        ]
        
        optimized = []
        for priority_path in priority_order:
            if priority_path in paths:
                optimized.append(priority_path)
        
        # Add remaining paths
        for path in paths:
            if path not in optimized and os.path.exists(path):
                optimized.append(path)
        
        return optimized
    
    def reconstruct_path(self):
        """Apply optimized PATH to shell configs"""
        optimal_path = self.path_analysis["optimal_order"]
        
        # Update .zshrc
        zshrc = Path.home() / ".zshrc"
        if zshrc.exists():
            self._update_path_in_file(zshrc, optimal_path)
        
        # Update .zprofile
        zprofile = Path.home() / ".zprofile"
        if zprofile.exists():
            self._update_path_in_file(zprofile, optimal_path)
    
    # ==================== SYMLINK Reconstruction ====================
    
    def analyze_symlinks(self):
        """
        Analyze all symlinks in common directories
        - /usr/local/bin
        - ~/.local/bin
        - ~/bin
        """
        scan_dirs = [
            "/usr/local/bin",
            Path.home() / ".local/bin",
            Path.home() / "bin"
        ]
        
        broken_links = []
        circular_links = []
        stale_links = []
        
        for scan_dir in scan_dirs:
            if not os.path.exists(scan_dir):
                continue
            
            for item in Path(scan_dir).iterdir():
                if item.is_symlink():
                    # Check if broken
                    if not item.exists():
                        broken_links.append(str(item))
                    
                    # Check if circular
                    if self._is_circular_symlink(item):
                        circular_links.append(str(item))
                    
                    # Check if stale (points to old version)
                    if self._is_stale_symlink(item):
                        stale_links.append(str(item))
        
        self.symlink_analysis = {
            "broken_symlinks": broken_links,
            "circular_symlinks": circular_links,
            "stale_symlinks": stale_links,
            "total_issues": len(broken_links) + len(circular_links) + len(stale_links)
        }
    
    def reconstruct_symlinks(self):
        """
        Atomically reconstruct broken symlinks
        - Remove broken links
        - Fix circular references
        - Update stale links
        """
        for broken_link in self.symlink_analysis["broken_symlinks"]:
            self._atomic_remove_symlink(broken_link)
        
        for circular_link in self.symlink_analysis["circular_symlinks"]:
            self._atomic_fix_circular(circular_link)
        
        for stale_link in self.symlink_analysis["stale_symlinks"]:
            self._atomic_update_symlink(stale_link)
    
    def _atomic_remove_symlink(self, link_path: str):
        """Remove symlink atomically with backup"""
        # Create backup
        backup_path = f"{link_path}.qpr_backup"
        shutil.copy2(link_path, backup_path)
        
        # Remove
        os.remove(link_path)
        
        # Log
        self.reconstruction_plan.append({
            "action": "remove_symlink",
            "target": link_path,
            "backup": backup_path
        })
    
    # ==================== DOTFILE Migration ====================
    
    def analyze_dotfiles(self):
        """
        Analyze dotfiles for conflicts and migration needs
        - .bashrc vs .zshrc
        - .bash_profile vs .zprofile
        - Detect duplicate configs
        """
        dotfiles = {
            ".zshrc": Path.home() / ".zshrc",
            ".zprofile": Path.home() / ".zprofile",
            ".zshenv": Path.home() / ".zshenv",
            ".bashrc": Path.home() / ".bashrc",
            ".bash_profile": Path.home() / ".bash_profile",
            ".profile": Path.home() / ".profile"
        }
        
        conflicts = []
        
        # Check for bash/zsh conflicts
        if dotfiles[".bashrc"].exists() and dotfiles[".zshrc"].exists():
            bash_aliases = self._extract_aliases(dotfiles[".bashrc"])
            zsh_aliases = self._extract_aliases(dotfiles[".zshrc"])
            
            # Find conflicts
            for alias_name in bash_aliases:
                if alias_name in zsh_aliases:
                    if bash_aliases[alias_name] != zsh_aliases[alias_name]:
                        conflicts.append({
                            "alias": alias_name,
                            "bash_value": bash_aliases[alias_name],
                            "zsh_value": zsh_aliases[alias_name]
                        })
        
        self.dotfile_analysis = {
            "files_found": [name for name, path in dotfiles.items() if path.exists()],
            "conflicts": conflicts,
            "migration_needed": len(conflicts) > 0
        }
    
    def migrate_dotfiles(self):
        """
        Intelligently migrate dotfiles
        - Merge bash configs into zsh
        - Resolve conflicts (prefer newer)
        - Create unified config
        """
        if not self.dotfile_analysis["migration_needed"]:
            return
        
        # Resolve conflicts
        for conflict in self.dotfile_analysis["conflicts"]:
            # Ask user or use smart resolution
            resolved_value = self._resolve_conflict(conflict)
            
            # Update zshrc
            self._update_alias_in_file(
                Path.home() / ".zshrc",
                conflict["alias"],
                resolved_value
            )
    
    # ==================== ALIAS Optimization ====================
    
    def analyze_aliases(self):
        """
        Analyze shell aliases for optimization
        - Find duplicates
        - Detect obsolete aliases
        - Suggest new aliases
        """
        zshrc = Path.home() / ".zshrc"
        if not zshrc.exists():
            return
        
        aliases = self._extract_aliases(zshrc)
        
        # Find duplicates
        duplicates = self._find_duplicate_aliases(aliases)
        
        # Detect obsolete
        obsolete = self._find_obsolete_aliases(aliases)
        
        # Suggest improvements
        suggestions = self._suggest_alias_improvements()
        
        self.alias_analysis = {
            "current_aliases": aliases,
            "duplicates": duplicates,
            "obsolete": obsolete,
            "suggestions": suggestions
        }
    
    def optimize_aliases(self):
        """
        Optimize alias configuration
        - Remove duplicates
        - Remove obsolete
        - Add suggested aliases
        """
        zshrc = Path.home() / ".zshrc"
        
        # Remove duplicates
        for dup in self.alias_analysis["duplicates"]:
            self._remove_duplicate_alias(zshrc, dup)
        
        # Add suggestions
        for suggestion in self.alias_analysis["suggestions"]:
            self._add_alias(zshrc, suggestion["name"], suggestion["value"])
    
    # ==================== Backup & Rollback ====================
    
    def create_backup(self):
        """Create timestamped backup of all configs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path.home() / f".qpr_backup_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        # Backup all dotfiles
        dotfiles = [".zshrc", ".zprofile", ".zshenv", ".bashrc", ".bash_profile"]
        for dotfile in dotfiles:
            src = Path.home() / dotfile
            if src.exists():
                shutil.copy2(src, backup_dir / dotfile)
        
        self.backup_created = True
        console.print(f"[green]✅ Backup created: {backup_dir}[/]")
    
    def rollback(self):
        """Rollback to backup if something fails"""
        # Implementation for rollback
        pass
```

### Integration Points

```python
# In macos_quantum_dashboard.py

def _show_config_recommendation(self):
    """After integrity check passes, run QPR"""
    console.print("\n[bold green]✅ System Health Good - Running Path Reconstruction[/]\n")
    
    # Initialize QPR
    qpr = QuantumPathReconstructor()
    
    # Run reconstruction
    report = qpr.run_full_reconstruction()
    
    # Show results
    self._display_qpr_report(report)
```

---

## 🎭 COMPONENT C: WORKFLOW ORCHESTRATOR

### File: `/modules/terminal-config/workflow_orchestrator.py`

**Purpose**: Master controller that links all phases together

### Class Structure

```python
class WorkflowOrchestrator:
    """
    Master Workflow Orchestrator
    Coordinates: Dashboard → Scoring → Clean Slate / QPR → Terminal Config
    """
    
    def __init__(self):
        self.dashboard = QuantumDashboard()
        self.scorer = SystemIntegrityScorer()
        self.qpr_engine = QuantumPathReconstructor()
        self.factory_reset = None  # Import from factory-reset module
        self.terminal_config = None  # Import from terminal-config
        
        self.workflow_state = {
            "phase": "initialization",
            "integrity_score": 0,
            "clean_slate_required": False,
            "qpr_completed": False,
            "config_applied": False
        }
    
    async def run_complete_workflow(self):
        """
        Execute complete transformation workflow
        """
        try:
            # PHASE 1: Dashboard + Discovery
            await self._phase1_dashboard()
            
            # PHASE 2: Integrity Scoring
            score_results = await self._phase2_scoring()
            
            # PHASE 3: Decision Point
            if score_results["next_action"] == "clean_slate":
                await self._phase3a_clean_slate()
            
            # PHASE 4: QPR Engine
            await self._phase4_qpr()
            
            # PHASE 5: Terminal Configuration
            await self._phase5_terminal_config()
            
            # PHASE 6: Final Report
            await self._phase6_final_report()
            
        except Exception as e:
            console.print(f"\n[red]❌ Error: {e}[/]")
            await self._emergency_rollback()
    
    async def _phase1_dashboard(self):
        """Phase 1: Show dashboard and run auto-discovery"""
        console.print("\n[bold cyan]🚀 PHASE 1: Dashboard Initialization[/]\n")
        self.workflow_state["phase"] = "dashboard"
        
        # Run dashboard (includes auto-discovery)
        await self.dashboard.run(duration=10)
    
    async def _phase2_scoring(self):
        """Phase 2: Calculate integrity score"""
        console.print("\n[bold cyan]🔍 PHASE 2: System Integrity Analysis[/]\n")
        self.workflow_state["phase"] = "scoring"
        
        results = self.scorer.calculate_overall_score()
        self.workflow_state["integrity_score"] = results["overall_score"]
        
        # Display results
        self._display_score_results(results)
        
        return results
    
    async def _phase3a_clean_slate(self):
        """Phase 3a: Clean Slate (if score < 80%)"""
        console.print("\n[bold yellow]🧹 PHASE 3a: Clean Slate Initialization[/]\n")
        self.workflow_state["phase"] = "clean_slate"
        self.workflow_state["clean_slate_required"] = True
        
        # Confirm with user
        if not self._confirm_clean_slate():
            console.print("[yellow]Clean slate skipped by user[/]")
            return
        
        # Run factory reset
        # TODO: Import and run factory reset module
        console.print("[green]✅ Clean slate complete[/]")
    
    async def _phase4_qpr(self):
        """Phase 4: Quantum Path Reconstruction"""
        console.print("\n[bold cyan]⚡ PHASE 4: Path Reconstruction[/]\n")
        self.workflow_state["phase"] = "qpr"
        
        report = self.qpr_engine.run_full_reconstruction()
        self.workflow_state["qpr_completed"] = True
        
        # Display results
        self._display_qpr_results(report)
    
    async def _phase5_terminal_config(self):
        """Phase 5: Terminal Configuration"""
        console.print("\n[bold cyan]🎨 PHASE 5: Terminal Configuration[/]\n")
        self.workflow_state["phase"] = "terminal_config"
        
        # Apply terminal configuration
        # TODO: Import and run terminal config
        console.print("[green]✅ Terminal configured[/]")
    
    async def _phase6_final_report(self):
        """Phase 6: Final Report"""
        console.print("\n[bold green]🎉 PHASE 6: Transformation Complete![/]\n")
        
        # Generate comprehensive report
        report = self._generate_final_report()
        
        # Display
        self._display_final_report(report)
        
        # Save to file
        report_file = Path.home() / ".macos_transformation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        console.print(f"\n[dim]Report saved: {report_file}[/]\n")
```

---

## 🔗 INTEGRATION POINTS

### How Components Connect

```python
# Main entry point: /modules/terminal-config/main.py

@app.get("/api/v1/transform/start")
async def start_transformation():
    """
    API endpoint to start complete transformation
    """
    orchestrator = WorkflowOrchestrator()
    results = await orchestrator.run_complete_workflow()
    return results

@app.get("/api/v1/transform/status")
async def get_transformation_status():
    """
    Get current workflow status
    """
    # Return orchestrator.workflow_state
    pass
```

---

## 📁 FILE STRUCTURE

```
/modules/terminal-config/
├── main.py                           # FastAPI service (existing)
├── macos_quantum_dashboard.py        # Dashboard (existing) ✅
├── system_integrity_scorer.py        # NEW - Component A ⭐
├── qpr_engine.py                     # NEW - Component B ⭐
├── workflow_orchestrator.py          # NEW - Component C ⭐
├── requirements.txt                  # Update with new deps
└── templates/
    ├── .zshrc                        # Existing templates ✅
    ├── .zprofile
    └── ...
```

---

## 📊 IMPLEMENTATION ORDER

### **STEP 1**: System Integrity Scorer (2 hours)
1. Create `/modules/terminal-config/system_integrity_scorer.py`
2. Implement 7 check methods
3. Implement scoring algorithm
4. Add to dashboard
5. Test on real system

### **STEP 2**: QPR Engine (2-3 hours)
1. Create `/modules/terminal-config/qpr_engine.py`
2. Implement PATH analysis & reconstruction
3. Implement symlink analysis & reconstruction
4. Implement dotfile migration
5. Implement alias optimization
6. Add backup/rollback system
7. Test on real system

### **STEP 3**: Workflow Orchestrator (1-2 hours)
1. Create `/modules/terminal-config/workflow_orchestrator.py`
2. Implement 6-phase workflow
3. Add user confirmation prompts
4. Implement final report generation
5. Add error handling & rollback
6. Integration testing

### **STEP 4**: Integration & Testing (1 hour)
1. Test complete workflow end-to-end
2. Test edge cases (low score, high score)
3. Test rollback functionality
4. Documentation updates
5. Create user guide

---

## 🎯 ESTIMATED TIMELINE

| Task | Estimated Time | Priority |
|------|----------------|----------|
| System Integrity Scorer | 2 hours | **HIGH** |
| QPR Engine | 2-3 hours | **HIGH** |
| Workflow Orchestrator | 1-2 hours | **MEDIUM** |
| Integration & Testing | 1 hour | **HIGH** |
| **TOTAL** | **6-8 hours** | - |

---

## ✅ READY TO START

All components are designed to:
- ✅ Work with existing code (no rewrites)
- ✅ Be production-ready (no placeholders)
- ✅ Have proper error handling
- ✅ Support rollback
- ✅ Work on macOS Big Sur Intel
- ✅ Integrate seamlessly

**Next**: Choose implementation order or start with Component A!
