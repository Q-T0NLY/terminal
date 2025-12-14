#!/usr/bin/env python3
"""
🚀 OSE TUI - Ultra-Advanced Interactive Terminal User Interface
Modern, Responsive CLI with Real-time Status Monitoring

The All-in-One System Management Interface
"""

import sys
import asyncio
import platform
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Rich imports for beautiful terminal UI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich import box
from rich.style import Style

console = Console()

# Service Mesh API Configuration
SERVICE_MESH_URL = "http://localhost:8000"


class OSETuiManager:
    """Ultra-Advanced OSE Terminal User Interface Manager"""
    
    def __init__(self):
        self.console = Console()
        self.current_menu = "main"
        self.system_status = self._get_system_status()
        
    def _get_system_status(self) -> Dict[str, Any]:
        """Get real-time system status"""
        return {
            "os": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def fetch_service_mesh_data(self) -> Optional[Dict[str, Any]]:
        """Fetch real-time data from Service Mesh API"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/health/comprehensive", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def fetch_ai_recommendations(self) -> List[Dict[str, Any]]:
        """Fetch AI recommendations from Service Mesh"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/ai/recommendations", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return data.get("recommendations", [])
        except:
            pass
        return []
    
    def send_nlp_query(self, query: str) -> Optional[Dict[str, Any]]:
        """Send NLP query to Service Mesh"""
        try:
            response = requests.post(
                f"{SERVICE_MESH_URL}/api/v1/nlp/query",
                json={"query": query},
                timeout=3
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def fetch_topology_data(self) -> Optional[Dict[str, Any]]:
        """Fetch topology graph data"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/topology/graph", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def fetch_heartbeat_status(self) -> Optional[Dict[str, Any]]:
        """Fetch heartbeat monitoring status"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/heartbeat/status", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def fetch_heartbeat_summary(self) -> Optional[Dict[str, Any]]:
        """Fetch heartbeat health summary"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/heartbeat/summary", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def fetch_dependencies_graph(self) -> Optional[Dict[str, Any]]:
        """Fetch service dependency graph"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/dependencies/graph", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def fetch_dependencies_mermaid(self) -> Optional[str]:
        """Fetch Mermaid diagram of dependencies"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/dependencies/visualize/mermaid", timeout=3)
            if response.status_code == 200:
                return response.json().get("mermaid", "")
        except:
            pass
        return None
    
    def fetch_messagebus_status(self) -> Optional[Dict[str, Any]]:
        """Fetch message bus connection status"""
        try:
            response = requests.get(f"{SERVICE_MESH_URL}/api/v1/messagebus/status", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def clear_screen(self):
        """Clear terminal screen"""
        self.console.clear()
    
    def show_header(self):
        """Display ultra-modern header with gradient effect"""
        header = """
[bold cyan]╔════════════════════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]                                                                            [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold yellow]███████╗ ███████╗ ███████╗[/bold yellow]     [bold white]OmniSystem Enhancer[/bold white]                  [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold yellow]██╔════╝ ██╔════╝ ██╔════╝[/bold yellow]     [dim]Ultra-Advanced System Management[/dim]       [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold yellow]██║  ███╗███████╗ █████╗[/bold yellow]       [dim]Microservices Architecture[/dim]           [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold yellow]██║   ██║╚════██║ ██╔══╝[/bold yellow]       [dim]Enterprise-Ready Platform[/dim]            [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]    [bold yellow]╚██████╔╝███████║ ███████╗[/bold yellow]                                         [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]     [bold yellow]╚═════╝ ╚══════╝ ╚══════╝[/bold yellow]     [bold green]v2.0.0[/bold green] [dim]|[/dim] [bold magenta]Production Ready[/bold magenta]      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                            [bold cyan]║[/bold cyan]
[bold cyan]╚════════════════════════════════════════════════════════════════════════════╝[/bold cyan]
"""
        self.console.print(header)
        
    def show_system_info_bar(self):
        """Display system information bar"""
        info_items = [
            f"[bold cyan]●[/bold cyan] {self.system_status['os']} {self.system_status['release']}",
            f"[bold yellow]●[/bold yellow] {self.system_status['hostname']}",
            f"[bold green]●[/bold green] {self.system_status['architecture']}",
            f"[bold magenta]●[/bold magenta] Python {self.system_status['python_version']}",
            f"[bold blue]●[/bold blue] {self.system_status['timestamp']}"
        ]
        
        info_bar = " [dim]|[/dim] ".join(info_items)
        panel = Panel(
            Align.center(info_bar),
            style="dim",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(panel)
        self.console.print()
    
    def create_main_menu(self) -> Table:
        """Create ultra-modern main menu"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]🎯 Main System Menu[/bold white]",
            title_style="bold cyan",
            padding=(0, 2)
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("System Module", style="bold cyan", width=35)
        table.add_column("Description", style="white", width=50)
        table.add_column("Status", style="bold green", width=12, justify="center")
        
        menu_items = [
            ("1", "🔍 System Services Mesh", "Microservices orchestration & management", "🟢 Active"),
            ("2", "🧹 Clean Slate Initialization", "Complete system setup using 5 independent services", "🟢 Ready"),
            ("3", "⚙️  System Wide Setup", "Discovery, scanning & configuration", "🟢 Ready"),
            ("4", "🖥️  Terminal Profile Regeneration", "ZSH configuration & theme management", "🟢 Ready"),
            ("5", "📦 Package Management System", "Install, reinstall & dependency management", "🟢 Ready"),
            ("6", "⚡ Performance Optimization", "CPU, memory, kernel & network tuning", "🟢 Ready"),
            ("7", "🔐 Security Audit & Hardening", "System security analysis & compliance", "🟡 Beta"),
            ("8", "💾 Backup & Restore System", "Automated backup with encryption", "🟡 Beta"),
            ("9", "📊 Monitoring Dashboard", "Real-time metrics & observability", "🟢 Active"),
            ("10", "🛠️  Advanced Utilities", "Developer tools & system utilities", "🟢 Ready"),
        ]
        
        for num, name, desc, status in menu_items:
            table.add_row(num, name, desc, status)
        
        return table
    
    def create_services_mesh_menu(self, mesh_data: Optional[Dict[str, Any]] = None) -> Table:
        """Create System Services Mesh submenu with real-time data"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]🔍 Ultra-Advanced Service Mesh[/bold white]",
            title_style="bold cyan"
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("Service", style="bold cyan", width=28)
        table.add_column("Port", style="green", width=6, justify="center")
        table.add_column("Status", style="bold", width=10, justify="center")
        table.add_column("Health Score", style="bold", width=12, justify="center")
        table.add_column("Details", style="white", width=30)
        
        if mesh_data and "services" in mesh_data:
            services_info = [
                ("discovery", "🔍 Discovery Service", 8001),
                ("factory-reset", "🧹 Factory Reset Service", 8002),
                ("reinstallation", "📦 Reinstallation Service", 8003),
                ("optimization", "⚡ Optimization Service", 8004),
                ("terminal-config", "🖥️ Terminal Config Service", 8005),
                ("metrics-collector", "📊 Metrics Collector", 8006),
                ("postgres", "🐘 PostgreSQL Database", 5432),
                ("redis", "⚡ Redis Cache", 6379),
                ("rabbitmq", "🐰 RabbitMQ Queue", 5672),
                ("prometheus", "🔥 Prometheus Metrics", 9090),
                ("grafana", "📈 Grafana Dashboard", 3000),
                ("loki", "📝 Loki Logging", 3100),
            ]
            
            for idx, (service_id, service_name, port) in enumerate(services_info, 1):
                service_data = mesh_data["services"].get(service_id, {})
                status = service_data.get("status", "unknown")
                health_score = service_data.get("health_score", {})
                overall = health_score.get("overall", 0)
                
                # Status badge
                if status == "healthy":
                    status_badge = "[bold green]🟢 UP[/bold green]"
                elif status == "degraded":
                    status_badge = "[bold yellow]🟡 SLOW[/bold yellow]"
                else:
                    status_badge = "[bold red]🔴 DOWN[/bold red]"
                
                # Health score display
                if overall > 0:
                    if overall >= 90:
                        score_display = f"[bold green]{int(overall)}[/bold green]"
                    elif overall >= 70:
                        score_display = f"[bold yellow]{int(overall)}[/bold yellow]"
                    else:
                        score_display = f"[bold red]{int(overall)}[/bold red]"
                else:
                    score_display = "[dim]N/A[/dim]"
                
                # Details
                metrics = service_data.get("metrics", {})
                if metrics:
                    cpu = metrics.get("cpu_percent", 0)
                    mem = metrics.get("memory_percent", 0)
                    details = f"CPU: {int(cpu)}% | Mem: {int(mem)}%"
                else:
                    details = "No metrics available"
                
                table.add_row(str(idx), service_name, str(port), status_badge, score_display, details)
        else:
            # Fallback: Service Mesh not available
            services = [
                ("1", "🔍 Discovery Service", "8001", "[dim]Offline[/dim]", "[dim]-[/dim]", "Service Mesh unavailable"),
                ("2", "🧹 Factory Reset Service", "8002", "[dim]Offline[/dim]", "[dim]-[/dim]", "Service Mesh unavailable"),
                ("3", "📦 Reinstallation Service", "8003", "[dim]Offline[/dim]", "[dim]-[/dim]", "Service Mesh unavailable"),
                ("4", "⚡ Optimization Service", "8004", "[dim]Offline[/dim]", "[dim]-[/dim]", "Service Mesh unavailable"),
                ("5", "🖥️ Terminal Config Service", "8005", "[dim]Offline[/dim]", "[dim]-[/dim]", "Service Mesh unavailable"),
                ("6", "📊 Metrics Collector", "8006", "[dim]Offline[/dim]", "[dim]-[/dim]", "Service Mesh unavailable"),
            ]
            for num, name, port, status, health, details in services:
                table.add_row(num, name, port, status, health, details)
        
        return table
    
    def create_clean_slate_menu(self) -> Table:
        """Create Clean Slate Initialization submenu - Complete System Setup"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="yellow",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]🧹 Clean Slate Initialization - Complete System Setup[/bold white]",
            title_style="bold yellow",
            caption="[dim]Uses: Discovery + Factory Reset + Reinstallation + Optimization + Terminal Config[/dim]"
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("Workflow Step", style="bold yellow", width=30)
        table.add_column("Description", style="white", width=40)
        table.add_column("Service", style="cyan", width=15)
        
        workflow = [
            ("1", "🔍 Full Setup (Auto)", "Complete clean slate using all 5 services", "All Services"),
            ("2", "📊 System Discovery", "Scan hardware, software, packages", "Discovery"),
            ("3", "🧹 Factory Reset", "Clean/reset system (4 profiles)", "Factory Reset"),
            ("4", "📦 Reinstall Packages", "Reinstall detected packages", "Reinstallation"),
            ("5", "⚡ System Optimization", "Optimize CPU, memory, network", "Optimization"),
            ("6", "🖥️  Terminal Setup", "Configure ZSH with themes", "Terminal Config"),
            ("", "━━━━━━━━━━━━━━━━━━━━", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "━━━━━━━━━"),
            ("7", "⚙️  Custom Setup", "Select specific services to use", "Manual"),
            ("8", "🔍 Dry-Run Analysis", "Analyze without changes", "Read-only"),
            ("9", "📋 Generate Report", "Full system report", "All Services"),
        ]
        
        for num, step, desc, service in workflow:
            if num:
                table.add_row(num, step, desc, service)
            else:
                table.add_row(num, step, desc, service, style="dim")
        
        return table
    
    def create_system_setup_menu(self) -> Table:
        """Create System Wide Setup submenu"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="green",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]⚙️  System Wide Setup[/bold white]",
            title_style="bold green"
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("Setup Module", style="bold green", width=30)
        table.add_column("Description", style="white", width=45)
        
        modules = [
            ("1", "🔍 Full System Discovery", "Scan hardware, software, network, security"),
            ("2", "🏗️  Initial Configuration", "Auto-configure system settings"),
            ("3", "📦 Detect Packages", "Analyze installed packages & dependencies"),
            ("4", "🌐 Network Setup", "Configure network, DNS, firewall"),
            ("5", "🔐 Security Baseline", "Apply security hardening & compliance"),
            ("6", "⚡ Performance Tuning", "Optimize system for workload"),
            ("7", "🗂️  Directory Structure", "Create standard directory layout"),
            ("8", "🔧 Install Essentials", "Install core tools & utilities"),
            ("9", "📋 Generate Report", "Comprehensive system report"),
        ]
        
        for num, name, desc in modules:
            table.add_row(num, name, desc)
        
        return table
    
    def create_terminal_profile_menu(self) -> Table:
        """Create Terminal Profile Regeneration submenu"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]🖥️  Terminal Profile Regeneration[/bold white]",
            title_style="bold blue"
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("Profile Type", style="bold blue", width=30)
        table.add_column("Features", style="white", width=45)
        
        profiles = [
            ("1", "⚡ Minimal Profile", "Fast, lightweight, essential features only"),
            ("2", "🎨 Balanced Profile", "Good performance + useful features"),
            ("3", "🚀 Power User Profile", "Full features, plugins, integrations"),
            ("4", "💼 Enterprise Profile", "Security, compliance, audit logging"),
            ("5", "🎭 Theme Selection", "Choose from 10+ themes (p10k, starship, etc)"),
            ("6", "🔌 Plugin Manager", "Enable/disable plugins interactively"),
            ("7", "⚙️  Custom Aliases", "Create personal command shortcuts"),
            ("8", "🔄 Restore Defaults", "Reset to factory terminal config"),
            ("9", "💾 Backup Current", "Save current configuration"),
            ("10", "📤 Export Config", "Export to share with other systems"),
        ]
        
        for num, name, features in profiles:
            table.add_row(num, name, features)
        
        return table
    
    def create_package_management_menu(self) -> Table:
        """Create Package Management submenu"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="magenta",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]📦 Package Management System[/bold white]",
            title_style="bold magenta"
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("Action", style="bold magenta", width=30)
        table.add_column("Description", style="white", width=45)
        
        actions = [
            ("1", "📋 List Packages", "Show all installed packages"),
            ("2", "🔍 Search Packages", "Find packages by name or keyword"),
            ("3", "📥 Install Packages", "Install new packages with dependencies"),
            ("4", "♻️  Reinstall All", "Reinstall all detected packages"),
            ("5", "🗑️  Remove Packages", "Uninstall packages safely"),
            ("6", "🔄 Update Packages", "Update all packages to latest"),
            ("7", "🧹 Clean Dependencies", "Remove orphaned dependencies"),
            ("8", "📊 Generate Config", "Create config files (nginx, postgres, etc)"),
            ("9", "💾 Backup Package List", "Save package list for restore"),
        ]
        
        for num, action, desc in actions:
            table.add_row(num, action, desc)
        
        return table
    
    def create_optimization_menu(self) -> Table:
        """Create Performance Optimization submenu"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="red",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]⚡ Performance Optimization[/bold white]",
            title_style="bold red"
        )
        
        table.add_column("#", style="bold yellow", width=4, justify="center")
        table.add_column("Optimization Category", style="bold red", width=30)
        table.add_column("Tweaks", style="white", width=45)
        
        categories = [
            ("1", "🧠 CPU Optimization", "Governor, frequency scaling, affinity"),
            ("2", "💾 Memory Tuning", "Swappiness, cache pressure, huge pages"),
            ("3", "💿 Disk I/O", "Scheduler, read-ahead, file system tuning"),
            ("4", "🌐 Network Stack", "TCP tuning, buffers, congestion control"),
            ("5", "🐧 Kernel Parameters", "Sysctl tuning, kernel modules"),
            ("6", "🖥️  Terminal Performance", "Shell startup, plugin optimization"),
            ("7", "🎯 Apply Profile", "Conservative/Balanced/Aggressive/Extreme"),
            ("8", "📊 Benchmark System", "Run performance benchmarks"),
            ("9", "📈 Show Recommendations", "AI-powered optimization suggestions"),
        ]
        
        for num, category, tweaks in categories:
            table.add_row(num, category, tweaks)
        
        return table
    
    def show_action_panel(self, actions: List[str]):
        """Display available actions panel"""
        actions_text = " [dim]|[/dim] ".join(f"[bold cyan]{action}[/bold cyan]" for action in actions)
        panel = Panel(
            Align.center(actions_text),
            title="[bold white]Available Actions[/bold white]",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print()
        self.console.print(panel)
    
    def show_footer(self):
        """Display footer with help information"""
        footer = Panel(
            Align.center(
                "[dim]Type number to select • [bold cyan]b[/bold cyan] = Back • "
                "[bold yellow]h[/bold yellow] = Help • [bold green]s[/bold green] = Status • "
                "[bold red]q[/bold red] = Quit[/dim]"
            ),
            style="dim",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print()
        self.console.print(footer)
    
    def display_main_menu(self):
        """Display main menu interface"""
        self.clear_screen()
        self.show_header()
        self.show_system_info_bar()
        
        menu = self.create_main_menu()
        self.console.print(menu)
        
        self.show_action_panel([
            "Select 1-10", "h: Help", "s: Status", "q: Quit"
        ])
        self.show_footer()
    
    def display_services_mesh(self):
        """Display ultra-advanced services mesh interface"""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_system_info_bar()
            
            # Fetch real-time data
            with self.console.status("[bold green]Fetching service mesh data..."):
                mesh_data = self.fetch_service_mesh_data()
            
            # Display connection status
            if mesh_data:
                connection_panel = Panel(
                    f"[bold green]✓ Connected to Service Mesh[/bold green] • "
                    f"Overall Health: [bold cyan]{int(mesh_data.get('overall_health_score', 0))}[/bold cyan] • "
                    f"Services: {mesh_data.get('total_services', 0)} • "
                    f"Healthy: [bold green]{mesh_data.get('healthy_services', 0)}[/bold green] • "
                    f"Down: [bold red]{mesh_data.get('down_services', 0)}[/bold red]",
                    border_style="green",
                    box=box.ROUNDED
                )
            else:
                connection_panel = Panel(
                    f"[bold yellow]⚠️ Service Mesh Offline[/bold yellow] • "
                    f"URL: {SERVICE_MESH_URL} • Start with: [cyan]docker-compose up -d service-mesh[/cyan]",
                    border_style="yellow",
                    box=box.ROUNDED
                )
            self.console.print(connection_panel)
            self.console.print()
            
            # Display services table
            menu = self.create_services_mesh_menu(mesh_data)
            self.console.print(menu)
            
            # Action panel
            self.show_action_panel([
                "Select service (1-12)", "r: Refresh", "ai: AI Recommendations",
                "nlp: Ask AI", "topo: Topology", "hb: Heartbeat", 
                "deps: Dependencies", "bus: Message Bus", "web: Dashboard", "b: Back"
            ])
            self.show_footer()
            
            choice = Prompt.ask(
                "\n[bold cyan]Enter your choice[/bold cyan]",
                default="b"
            )
            
            if choice.lower() == "b":
                break
            elif choice.lower() == "r":
                continue  # Refresh by relooping
            elif choice.lower() == "ai":
                self.show_ai_recommendations()
            elif choice.lower() == "nlp":
                self.interactive_nlp_query()
            elif choice.lower() == "topo":
                self.show_topology_info()
            elif choice.lower() == "hb":
                self.show_heartbeat_monitor()
            elif choice.lower() == "deps":
                self.show_dependencies_graph()
            elif choice.lower() == "bus":
                self.show_messagebus_status()
            elif choice.lower() == "web":
                self.console.print(f"\n[bold cyan]Opening dashboard in browser:[/bold cyan] {SERVICE_MESH_URL}")
                import webbrowser
                try:
                    webbrowser.open(SERVICE_MESH_URL)
                    self.console.print("[bold green]✓ Browser opened[/bold green]")
                except:
                    self.console.print("[bold yellow]⚠️ Could not open browser automatically[/bold yellow]")
                input("\nPress Enter to continue...")
            elif choice.isdigit() and 1 <= int(choice) <= 12:
                self.show_service_details(int(choice), mesh_data)
            else:
                self.console.print(f"[yellow]Invalid choice: {choice}[/yellow]")
                input("\nPress Enter to continue...")
    
    def show_ai_recommendations(self):
        """Display AI recommendations from Service Mesh"""
        self.clear_screen()
        self.show_header()
        
        with self.console.status("[bold green]Fetching AI recommendations..."):
            recommendations = self.fetch_ai_recommendations()
        
        if not recommendations:
            self.console.print(Panel(
                "[bold yellow]⚠️ No AI recommendations available[/bold yellow]\n\n"
                "Service Mesh may be offline or no recommendations generated yet.",
                title="[bold white]AI Recommendations[/bold white]",
                border_style="yellow"
            ))
            input("\nPress Enter to continue...")
            return
        
        # Display recommendations
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            box=box.DOUBLE_EDGE,
            expand=True,
            title=f"[bold white]🤖 AI-Powered Recommendations ({len(recommendations)})[/bold white]"
        )
        
        table.add_column("#", style="bold yellow", width=3, justify="center")
        table.add_column("Priority", style="bold", width=10, justify="center")
        table.add_column("Service", style="cyan", width=15)
        table.add_column("Title", style="bold white", width=30)
        table.add_column("Impact", style="green", width=8, justify="center")
        table.add_column("Effort", style="yellow", width=8, justify="center")
        
        for idx, rec in enumerate(recommendations[:10], 1):  # Show top 10
            priority = rec.get("priority", "medium")
            if priority == "critical":
                priority_badge = "[bold red]🔴 CRITICAL[/bold red]"
            elif priority == "high":
                priority_badge = "[bold yellow]🟠 HIGH[/bold yellow]"
            elif priority == "medium":
                priority_badge = "[bold blue]🔵 MEDIUM[/bold blue]"
            else:
                priority_badge = "[bold green]🟢 LOW[/bold green]"
            
            table.add_row(
                str(idx),
                priority_badge,
                rec.get("service", "N/A"),
                rec.get("title", "No title"),
                f"{rec.get('impact_score', 0):.1f}/10",
                f"{rec.get('effort_score', 0):.1f}/10"
            )
        
        self.console.print(table)
        
        # Show detail option
        self.console.print()
        detail_choice = Prompt.ask(
            "[bold cyan]Enter recommendation # for details, or Enter to continue[/bold cyan]",
            default=""
        )
        
        if detail_choice.isdigit() and 1 <= int(detail_choice) <= len(recommendations):
            rec = recommendations[int(detail_choice) - 1]
            detail_panel = Panel(
                f"[bold cyan]{rec.get('title', 'N/A')}[/bold cyan]\n\n"
                f"[bold white]Description:[/bold white]\n{rec.get('description', 'N/A')}\n\n"
                f"[bold white]Estimated Improvement:[/bold white] {rec.get('estimated_improvement', 'N/A')}\n\n"
                f"[bold white]Action Items:[/bold white]\n" +
                "\n".join(f"  {i+1}. {item}" for i, item in enumerate(rec.get('action_items', []))),
                title=f"[bold white]Recommendation Details[/bold white]",
                border_style="cyan"
            )
            self.console.print()
            self.console.print(detail_panel)
        
        input("\nPress Enter to continue...")
    
    def interactive_nlp_query(self):
        """Interactive NLP query interface"""
        self.clear_screen()
        self.show_header()
        
        self.console.print(Panel(
            "[bold cyan]Ask AI anything about your services![/bold cyan]\n\n"
            "Example queries:\n"
            "  • 'What is the status of all services?'\n"
            "  • 'Why is the discovery service important?'\n"
            "  • 'How can I optimize performance?'\n"
            "  • 'Show me critical services'\n\n"
            "[dim]Type 'exit' to go back[/dim]",
            title="[bold white]🤖 NLP Query Interface[/bold white]",
            border_style="cyan"
        ))
        
        while True:
            query = Prompt.ask("\n[bold cyan]Your question[/bold cyan]", default="exit")
            
            if query.lower() == "exit":
                break
            
            with self.console.status("[bold green]Processing query..."):
                response = self.send_nlp_query(query)
            
            if response:
                result_panel = Panel(
                    f"[bold green]Intent:[/bold green] {response.get('intent', 'N/A')} "
                    f"([bold cyan]{int(response.get('confidence', 0) * 100)}%[/bold cyan] confidence)\n\n"
                    f"[bold white]Answer:[/bold white]\n{response.get('answer', 'No answer')}\n\n" +
                    (f"[bold yellow]Suggested Actions:[/bold yellow]\n" +
                     "\n".join(f"  • {action}" for action in response.get('suggested_actions', []))
                     if response.get('suggested_actions') else ""),
                    title="[bold white]AI Response[/bold white]",
                    border_style="green"
                )
                self.console.print()
                self.console.print(result_panel)
            else:
                self.console.print("\n[bold red]❌ Failed to get response from AI[/bold red]")
                self.console.print("[dim]Service Mesh may be offline[/dim]")
    
    def show_topology_info(self):
        """Display topology information"""
        self.clear_screen()
        self.show_header()
        
        with self.console.status("[bold green]Fetching topology data..."):
            topology = self.fetch_topology_data()
        
        if not topology:
            self.console.print(Panel(
                "[bold yellow]⚠️ Topology data not available[/bold yellow]",
                border_style="yellow"
            ))
            input("\nPress Enter to continue...")
            return
        
        # Display topology summary
        summary = Panel(
            f"[bold cyan]Topology Graph Summary[/bold cyan]\n\n"
            f"Total Nodes: [bold white]{len(topology.get('nodes', []))}[/bold white]\n"
            f"Total Edges: [bold white]{len(topology.get('edges', []))}[/bold white]\n"
            f"Clusters: [bold white]{len(topology.get('clusters', []))}[/bold white]\n"
            f"Critical Paths: [bold white]{len(topology.get('critical_paths', []))}[/bold white]\n\n"
            f"[dim]Generated: {topology.get('generated_at', 'N/A')}[/dim]",
            title="[bold white]🔮 3D Service Topology[/bold white]",
            border_style="cyan"
        )
        self.console.print(summary)
        
        # Show clusters
        if topology.get('clusters'):
            self.console.print()
            clusters_table = Table(
                title="[bold white]Service Clusters[/bold white]",
                border_style="cyan",
                box=box.ROUNDED
            )
            clusters_table.add_column("Cluster", style="bold cyan")
            clusters_table.add_column("Services", style="white")
            
            for cluster in topology['clusters']:
                services = ", ".join(cluster.get('services', []))
                clusters_table.add_row(cluster.get('category', 'N/A'), services)
            
            self.console.print(clusters_table)
        
        # Show critical paths
        if topology.get('critical_paths'):
            self.console.print()
            paths_panel = Panel(
                "\n".join(f"Path {i+1}: {' → '.join(path)}" 
                         for i, path in enumerate(topology['critical_paths'][:5])),
                title="[bold white]Critical Dependency Paths[/bold white]",
                border_style="yellow"
            )
            self.console.print(paths_panel)
        
        self.console.print()
        self.console.print(f"[bold cyan]View full 3D visualization at:[/bold cyan] {SERVICE_MESH_URL}")
        
        input("\nPress Enter to continue...")
    
    def show_service_details(self, service_num: int, mesh_data: Optional[Dict[str, Any]]):
        """Show detailed information for a specific service"""
        self.clear_screen()
        self.show_header()
        
        if not mesh_data:
            self.console.print("[bold red]Service Mesh data not available[/bold red]")
            input("\nPress Enter to continue...")
            return
        
        service_map = {
            1: "discovery", 2: "factory-reset", 3: "reinstallation",
            4: "optimization", 5: "terminal-config", 6: "metrics-collector",
            7: "postgres", 8: "redis", 9: "rabbitmq",
            10: "prometheus", 11: "grafana", 12: "loki"
        }
        
        service_id = service_map.get(service_num)
        if not service_id or service_id not in mesh_data.get("services", {}):
            self.console.print(f"[bold yellow]Service {service_num} not found[/bold yellow]")
            input("\nPress Enter to continue...")
            return
        
        service = mesh_data["services"][service_id]
        health = service.get("health_score", {})
        metrics = service.get("metrics", {})
        
        # Service info panel
        info_panel = Panel(
            f"[bold cyan]{service.get('service', 'Unknown')}[/bold cyan]\n\n"
            f"[bold white]Status:[/bold white] {service.get('status', 'unknown').upper()}\n"
            f"[bold white]Overall Health:[/bold white] {int(health.get('overall', 0))}/100\n\n"
            f"[bold green]Health Breakdown:[/bold green]\n"
            f"  • Availability: {int(health.get('availability', 0))}/100\n"
            f"  • Performance: {int(health.get('performance', 0))}/100\n"
            f"  • Reliability: {int(health.get('reliability', 0))}/100\n"
            f"  • Efficiency: {int(health.get('efficiency', 0))}/100\n"
            f"  • Security: {int(health.get('security', 0))}/100\n"
            f"  • Predicted (1h): {int(health.get('predicted_1h', 0))}/100\n\n" +
            (f"[bold yellow]Metrics:[/bold yellow]\n"
             f"  • CPU: {metrics.get('cpu_percent', 0):.1f}%\n"
             f"  • Memory: {metrics.get('memory_percent', 0):.1f}%\n"
             f"  • Latency (P95): {metrics.get('p95_latency', 0):.0f}ms\n"
             if metrics else ""),
            title=f"[bold white]Service Details[/bold white]",
            border_style="cyan"
        )
        
        self.console.print(info_panel)
        input("\nPress Enter to continue...")    
    def display_clean_slate(self):
        """Display clean slate interface - Complete System Setup"""
        self.clear_screen()
        self.show_header()
        self.show_system_info_bar()
        
        # Show service info
        workflow_info = Panel(
            "[bold cyan]Clean Slate Initialization[/bold cyan] sets up your system using 5 independent microservices:\n\n"
            "[bold green]• Discovery Service[/bold green] (Port 8001) - Scan system state\n"
            "[bold yellow]• Factory Reset Service[/bold yellow] (Port 8002) - Clean/reset system\n"
            "[bold blue]• Reinstallation Service[/bold blue] (Port 8003) - Reinstall packages\n"
            "[bold magenta]• Optimization Service[/bold magenta] (Port 8004) - Optimize performance\n"
            "[bold cyan]• Terminal Config Service[/bold cyan] (Port 8005) - Configure terminal\n\n"
            "[dim]Each service can be used independently or together for complete system setup[/dim]",
            title="[bold white]🔗 Independent Microservices[/bold white]",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(workflow_info)
        self.console.print()
        
        menu = self.create_clean_slate_menu()
        self.console.print(menu)
        
        warning = Panel(
            "[bold yellow]⚠️  WARNING[/bold yellow]: Factory reset operations are irreversible. "
            "Always backup important data before proceeding!",
            style="yellow",
            border_style="yellow",
            box=box.ROUNDED
        )
        self.console.print()
        self.console.print(warning)
        
        self.show_action_panel([
            "Select option", "1: Full auto setup", "analyze: Dry run", "b: Back"
        ])
        self.show_footer()
    
    def display_system_setup(self):
        """Display system setup interface"""
        self.clear_screen()
        self.show_header()
        self.show_system_info_bar()
        
        menu = self.create_system_setup_menu()
        self.console.print(menu)
        
        self.show_action_panel([
            "Select module", "auto: Auto setup", "b: Back"
        ])
        self.show_footer()
    
    def display_terminal_profile(self):
        """Display terminal profile interface"""
        self.clear_screen()
        self.show_header()
        self.show_system_info_bar()
        
        menu = self.create_terminal_profile_menu()
        self.console.print(menu)
        
        self.show_action_panel([
            "Select profile", "preview: Preview config", "b: Back"
        ])
        self.show_footer()
    
    def display_package_management(self):
        """Display package management interface"""
        self.clear_screen()
        self.show_header()
        self.show_system_info_bar()
        
        menu = self.create_package_management_menu()
        self.console.print(menu)
        
        self.show_action_panel([
            "Select action", "b: Back"
        ])
        self.show_footer()
    
    def display_optimization(self):
        """Display optimization interface"""
        self.clear_screen()
        self.show_header()
        self.show_system_info_bar()
        
        menu = self.create_optimization_menu()
        self.console.print(menu)
        
        self.show_action_panel([
            "Select category", "profile: Quick profile", "b: Back"
        ])
        self.show_footer()
    
    def show_progress_demo(self, operation: str):
        """Show progress bar for operations"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"[cyan]{operation}...", total=100)
            import time
            for i in range(100):
                time.sleep(0.02)
                progress.update(task, advance=1)
    
    def show_help(self):
        """Display help screen"""
        self.clear_screen()
        self.show_header()
        
        help_text = """
# 📚 OSE TUI Help

## Navigation
- Use **number keys** to select menu items
- Press **b** to go back to previous menu
- Press **q** to quit the application
- Press **h** to show this help screen
- Press **s** to view system status

## Main Menu Options

### 1. System Services Mesh
Manage all microservices (5 app services + 7 infrastructure services)
- View service status and health
- Start/stop individual services
- View logs and metrics

### 2. Clean Slate Initialization
Factory reset with granular control
- Choose from 4 reset profiles (Light → Nuclear)
- Dry-run analysis mode
- Backup before reset

### 3. System Wide Setup
Initial system discovery and configuration
- Hardware/software detection
- Network configuration
- Security baseline

### 4. Terminal Profile Regeneration
ZSH configuration management
- Choose from 4 profiles (Minimal → Enterprise)
- Theme selection (Powerlevel10k, Starship, etc)
- Plugin management

### 5. Package Management
Install, remove, and manage packages
- Multi-platform support (APT, DNF, RPM)
- Dependency resolution
- Config generation

### 6. Performance Optimization
System tuning and benchmarking
- CPU, memory, disk, network optimization
- Apply optimization profiles
- AI-powered recommendations

## Tips
- Start with System Discovery to understand your system
- Use dry-run/analyze modes before making changes
- Always backup before factory reset operations
- Check service health regularly in Services Mesh

Press Enter to continue...
"""
        md = Markdown(help_text)
        self.console.print(Panel(md, title="[bold cyan]Help Documentation[/bold cyan]", border_style="cyan"))
        input()
    
    def show_heartbeat_monitor(self):
        """Display heartbeat monitoring dashboard"""
        self.clear_screen()
        self.show_header()
        
        with self.console.status("[bold green]Fetching heartbeat data..."):
            heartbeat_data = self.fetch_heartbeat_status()
            summary = self.fetch_heartbeat_summary()
        
        if not heartbeat_data:
            self.console.print(Panel(
                "[bold yellow]⚠️ Heartbeat monitoring not available[/bold yellow]\n\n"
                "Service Mesh may be offline or heartbeat monitoring not initialized.",
                title="[bold white]🫀 Heartbeat Monitor[/bold white]",
                border_style="yellow"
            ))
            input("\nPress Enter to continue...")
            return
        
        # Display summary panel
        if summary:
            summary_panel = Panel(
                f"[bold white]Total Services:[/bold white] {summary.get('total_services', 0)} • "
                f"[bold green]Healthy:[/bold green] {summary.get('healthy', 0)} • "
                f"[bold yellow]Degraded:[/bold yellow] {summary.get('degraded', 0)} • "
                f"[bold red]Critical:[/bold red] {summary.get('critical', 0)} • "
                f"[bold dim]Dead:[/bold dim] {summary.get('dead', 0)} • "
                f"[bold cyan]Health:[/bold cyan] {summary.get('overall_health_percentage', 0)}%",
                title="[bold white]🫀 Heartbeat Summary[/bold white]",
                border_style="cyan",
                box=box.ROUNDED
            )
            self.console.print(summary_panel)
            self.console.print()
        
        # Display heartbeat table
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            box=box.DOUBLE_EDGE,
            expand=True,
            title="[bold white]Service Heartbeat Status[/bold white]"
        )
        
        table.add_column("Service", style="bold cyan", width=25)
        table.add_column("Status", style="bold", width=12, justify="center")
        table.add_column("Heartbeats", style="white", width=10, justify="right")
        table.add_column("Missed", style="yellow", width=8, justify="right")
        table.add_column("Avg Latency", style="green", width=12, justify="right")
        table.add_column("Uptime %", style="cyan", width=10, justify="right")
        table.add_column("Last Seen", style="dim", width=12, justify="right")
        
        for service_id, data in heartbeat_data.items():
            if not data:
                continue
            
            status = data.get('status', 'unknown')
            metrics = data.get('metrics', {})
            
            # Color-code status
            if status == 'healthy':
                status_display = "[bold green]🟢 HEALTHY[/bold green]"
            elif status == 'degraded':
                status_display = "[bold yellow]🟡 DEGRADED[/bold yellow]"
            elif status == 'critical':
                status_display = "[bold red]🔴 CRITICAL[/bold red]"
            elif status == 'dead':
                status_display = "[bold dim]⚫ DEAD[/bold dim]"
            else:
                status_display = "[dim]⚪ UNKNOWN[/dim]"
            
            table.add_row(
                data.get('service_name', service_id),
                status_display,
                str(metrics.get('heartbeat_count', 0)),
                str(metrics.get('missed_heartbeats', 0)),
                f"{metrics.get('average_latency_ms', 0):.1f}ms",
                f"{metrics.get('uptime_percentage', 0):.1f}%",
                f"{metrics.get('seconds_since_last', 0):.0f}s ago"
            )
        
        self.console.print(table)
        self.console.print()
        
        # Action panel
        panel = Panel(
            "[bold cyan]r[/bold cyan] = Refresh • "
            "[bold yellow]d[/bold yellow] = Details • "
            "[bold green]web[/bold green] = Open Dashboard • "
            "[bold red]b[/bold red] = Back",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(panel)
        
        choice = Prompt.ask("\n[bold cyan]Action[/bold cyan]", default="b")
        
        if choice.lower() == "r":
            self.show_heartbeat_monitor()  # Recursive refresh
        elif choice.lower() == "web":
            import webbrowser
            webbrowser.open(f"{SERVICE_MESH_URL}/heartbeat-dashboard")
            input("\nPress Enter to continue...")
    
    def show_dependencies_graph(self):
        """Display service dependency graph"""
        self.clear_screen()
        self.show_header()
        
        with self.console.status("[bold green]Analyzing service dependencies..."):
            deps_data = self.fetch_dependencies_graph()
            mermaid = self.fetch_dependencies_mermaid()
        
        if not deps_data:
            self.console.print(Panel(
                "[bold yellow]⚠️ Dependency graph not available[/bold yellow]\n\n"
                "Service Mesh may be offline or dependency mapping not initialized.",
                title="[bold white]🔗 Service Dependencies[/bold white]",
                border_style="yellow"
            ))
            input("\nPress Enter to continue...")
            return
        
        # Display summary
        summary_panel = Panel(
            f"[bold white]Total Services:[/bold white] {deps_data.get('total_services', 0)} • "
            f"[bold cyan]Dependencies:[/bold cyan] {deps_data.get('total_dependencies', 0)} • "
            f"[bold magenta]Clusters:[/bold magenta] {len(deps_data.get('clusters', {}))} • "
            f"[bold yellow]Circular:[/bold yellow] {len(deps_data.get('circular_dependencies', []))}",
            title="[bold white]🔗 Dependency Graph Summary[/bold white]",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(summary_panel)
        self.console.print()
        
        # Display hub services
        hub_services = deps_data.get('hub_services', [])
        if hub_services:
            hub_text = ", ".join(f"[bold cyan]{s}[/bold cyan]" for s in hub_services)
            self.console.print(Panel(
                f"[bold yellow]Hub Services (High Dependency Count):[/bold yellow]\n{hub_text}",
                border_style="yellow",
                box=box.ROUNDED
            ))
            self.console.print()
        
        # Display clusters
        clusters = deps_data.get('clusters', {})
        if clusters:
            cluster_table = Table(
                show_header=True,
                header_style="bold magenta",
                border_style="green",
                box=box.ROUNDED,
                title="[bold white]Service Clusters[/bold white]"
            )
            
            cluster_table.add_column("Cluster", style="bold yellow", width=20)
            cluster_table.add_column("Services", style="cyan", width=60)
            
            for cluster_name, services in clusters.items():
                cluster_table.add_row(
                    cluster_name.upper(),
                    ", ".join(services)
                )
            
            self.console.print(cluster_table)
            self.console.print()
        
        # Display critical path
        critical_path = deps_data.get('critical_path', [])
        if critical_path:
            path_text = " → ".join(f"[bold cyan]{s}[/bold cyan]" for s in critical_path)
            self.console.print(Panel(
                f"[bold red]Critical Dependency Path:[/bold red]\n{path_text}",
                border_style="red",
                box=box.ROUNDED
            ))
            self.console.print()
        
        # Display circular dependencies warning
        circular = deps_data.get('circular_dependencies', [])
        if circular:
            circular_text = "\n".join(
                " → ".join(f"[yellow]{s}[/yellow]" for s in path)
                for path in circular
            )
            self.console.print(Panel(
                f"[bold red]⚠️ Circular Dependencies Detected:[/bold red]\n\n{circular_text}",
                border_style="red",
                box=box.HEAVY
            ))
            self.console.print()
        
        # Display Mermaid diagram if available
        if mermaid:
            self.console.print(Panel(
                f"[dim]{mermaid}[/dim]",
                title="[bold white]Mermaid Diagram (Copy to visualize)[/bold white]",
                border_style="dim",
                box=box.ROUNDED
            ))
            self.console.print()
        
        # Action panel
        panel = Panel(
            "[bold cyan]r[/bold cyan] = Refresh • "
            "[bold green]web[/bold green] = Interactive Graph • "
            "[bold red]b[/bold red] = Back",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(panel)
        
        choice = Prompt.ask("\n[bold cyan]Action[/bold cyan]", default="b")
        
        if choice.lower() == "r":
            self.show_dependencies_graph()  # Recursive refresh
        elif choice.lower() == "web":
            import webbrowser
            webbrowser.open(f"{SERVICE_MESH_URL}/dependencies")
            input("\nPress Enter to continue...")
    
    def show_messagebus_status(self):
        """Display message bus status and controls"""
        self.clear_screen()
        self.show_header()
        
        with self.console.status("[bold green]Checking message bus..."):
            bus_status = self.fetch_messagebus_status()
        
        if not bus_status:
            self.console.print(Panel(
                "[bold yellow]⚠️ Message bus not available[/bold yellow]\n\n"
                "Service Mesh may be offline or RabbitMQ not connected.",
                title="[bold white]💬 Message Bus[/bold white]",
                border_style="yellow"
            ))
            input("\nPress Enter to continue...")
            return
        
        # Display connection status
        is_connected = bus_status.get('connected', False)
        if is_connected:
            status_panel = Panel(
                f"[bold green]✓ Connected to RabbitMQ[/bold green]\n\n"
                f"[bold white]Host:[/bold white] {bus_status.get('host', 'unknown')}\n"
                f"[bold white]Port:[/bold white] {bus_status.get('port', 0)}\n"
                f"[bold white]Active Consumers:[/bold white] {bus_status.get('active_consumers', 0)}",
                title="[bold white]💬 Message Bus Status[/bold white]",
                border_style="green",
                box=box.ROUNDED
            )
        else:
            status_panel = Panel(
                f"[bold red]✗ Not Connected to RabbitMQ[/bold red]\n\n"
                f"Message bus is offline. Start RabbitMQ to enable event-driven communication.",
                title="[bold white]💬 Message Bus Status[/bold white]",
                border_style="red",
                box=box.ROUNDED
            )
        
        self.console.print(status_panel)
        self.console.print()
        
        # Display exchanges
        exchanges = bus_status.get('exchanges', [])
        if exchanges:
            exchange_table = Table(
                show_header=True,
                header_style="bold magenta",
                border_style="cyan",
                box=box.ROUNDED,
                title="[bold white]Declared Exchanges[/bold white]"
            )
            
            exchange_table.add_column("Exchange", style="bold cyan", width=30)
            exchange_table.add_column("Type", style="yellow", width=20)
            exchange_table.add_column("Purpose", style="dim", width=40)
            
            purpose_map = {
                "ose.events": "Service lifecycle events",
                "ose.tasks": "Background task queue",
                "ose.logs": "Centralized logging"
            }
            
            for exchange_name in exchanges:
                exchange_table.add_row(
                    exchange_name,
                    "topic" if "events" in exchange_name else "direct" if "tasks" in exchange_name else "fanout",
                    purpose_map.get(exchange_name, "Custom exchange")
                )
            
            self.console.print(exchange_table)
            self.console.print()
        
        # Display queues
        queues = bus_status.get('queues', [])
        if queues:
            queue_table = Table(
                show_header=True,
                header_style="bold magenta",
                border_style="green",
                box=box.ROUNDED,
                title="[bold white]Declared Queues[/bold white]"
            )
            
            queue_table.add_column("Queue", style="bold green", width=40)
            queue_table.add_column("Messages", style="cyan", width=15, justify="right")
            
            for queue_name in queues:
                queue_table.add_row(queue_name, "0")  # Would need RabbitMQ API for actual count
            
            self.console.print(queue_table)
            self.console.print()
        
        # Event publishing panel
        publish_panel = Panel(
            "[bold white]Publish Test Event:[/bold white]\n\n"
            "Use [bold cyan]'p'[/bold cyan] to publish a test event to the message bus.\n"
            "This will broadcast a health check event to all services.",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(publish_panel)
        self.console.print()
        
        # Action panel
        panel = Panel(
            "[bold cyan]r[/bold cyan] = Refresh • "
            "[bold yellow]p[/bold yellow] = Publish Test Event • "
            "[bold green]web[/bold green] = RabbitMQ Admin • "
            "[bold red]b[/bold red] = Back",
            border_style="cyan",
            box=box.ROUNDED
        )
        self.console.print(panel)
        
        choice = Prompt.ask("\n[bold cyan]Action[/bold cyan]", default="b")
        
        if choice.lower() == "r":
            self.show_messagebus_status()  # Recursive refresh
        elif choice.lower() == "p":
            # Publish test event
            try:
                response = requests.post(
                    f"{SERVICE_MESH_URL}/api/v1/messagebus/publish",
                    json={
                        "exchange": "ose.events",
                        "event_type": "tui.test.event",
                        "source_service": "ose-tui",
                        "payload": {
                            "message": "Test event from TUI",
                            "timestamp": datetime.now().isoformat()
                        },
                        "routing_key": "tui.test",
                        "priority": 5
                    },
                    timeout=3
                )
                if response.status_code == 200:
                    self.console.print("\n[bold green]✓ Test event published successfully![/bold green]")
                else:
                    self.console.print(f"\n[bold yellow]⚠️ Failed to publish event: {response.status_code}[/bold yellow]")
            except Exception as e:
                self.console.print(f"\n[bold red]❌ Error publishing event: {e}[/bold red]")
            input("\nPress Enter to continue...")
            self.show_messagebus_status()
        elif choice.lower() == "web":
            import webbrowser
            webbrowser.open("http://localhost:15672")  # RabbitMQ management interface
            input("\nPress Enter to continue...")
    
    def run(self):
        """Main TUI loop"""
        self.display_main_menu()
        
        while True:
            choice = Prompt.ask(
                "\n[bold cyan]Enter your choice[/bold cyan]",
                choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "h", "s", "q", "b"],
                show_choices=False
            )
            
            if choice == "q":
                self.console.print("\n[bold green]👋 Thank you for using OSE! Goodbye![/bold green]\n")
                break
            elif choice == "h":
                self.show_help()
                self.display_main_menu()
            elif choice == "s":
                self.show_progress_demo("Fetching system status")
                self.display_main_menu()
            elif choice == "1":
                self.display_services_mesh()
                # Already handles its own loop, returns when user presses 'b'
                self.display_main_menu()
            elif choice == "2":
                self.display_clean_slate()
                input("\nPress Enter to continue...")
                self.display_main_menu()
            elif choice == "3":
                self.display_system_setup()
                input("\nPress Enter to continue...")
                self.display_main_menu()
            elif choice == "4":
                self.display_terminal_profile()
                input("\nPress Enter to continue...")
                self.display_main_menu()
            elif choice == "5":
                self.display_package_management()
                input("\nPress Enter to continue...")
                self.display_main_menu()
            elif choice == "6":
                self.display_optimization()
                input("\nPress Enter to continue...")
                self.display_main_menu()
            elif choice in ["7", "8", "9", "10"]:
                self.console.print(f"\n[yellow]Module {choice} coming soon![/yellow]")
                input("\nPress Enter to continue...")
                self.display_main_menu()
            elif choice == "b":
                self.display_main_menu()


def main():
    """Main entry point"""
    try:
        tui = OSETuiManager()
        tui.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]⚠️  Interrupted by user[/bold yellow]")
        console.print("[bold green]👋 Goodbye![/bold green]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
