#!/usr/bin/env python3
"""
🚀 OSE - OmniSystem Enhancer
The All-in-One System Optimization & Factory Reset Suite

Usage:
    ose                    # Launch interactive dashboard
    ose cleanup            # System cleanup module  
    ose optimize           # System optimization module
    ose reset              # Factory reset module
    ose backup             # Quantum backup module
    ose pkg                # Package manager module
    ose scan               # Diagnostic scan
    ose --version          # Show version
    ose --help             # Show help
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def show_banner():
    """Display OSE banner"""
    banner = """
[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ███████╗███████╗                               ║
║  ██╔═══██╗██╔════╝██╔════╝                               ║
║  ██║   ██║███████╗█████╗                                 ║
║  ██║   ██║╚════██║██╔══╝                                 ║
║  ╚██████╔╝███████║███████╗                               ║
║   ╚═════╝ ╚══════╝╚══════╝                               ║
║                                                           ║
║  [bold yellow]OmniSystem Enhancer[/bold yellow]                                   ║
║  [dim]The All-in-One System Optimization Suite[/dim]              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]
"""
    console.print(banner)


def show_main_menu():
    """Display main menu"""
    table = Table(
        title="🎯 OSE Command Center",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Module", style="cyan", width=20)
    table.add_column("Command", style="green", width=20)
    table.add_column("Description", style="white", width=40)
    
    table.add_row(
        "🧹 Cleanup",
        "ose cleanup",
        "Free disk space (caches, temp files, logs, duplicates)"
    )
    table.add_row(
        "⚡ Optimization",
        "ose optimize",
        "Improve performance (startup, kernel, memory, services)"
    )
    table.add_row(
        "🔄 Factory Reset",
        "ose reset",
        "Reset system to clean state (packages, configs, data)"
    )
    table.add_row(
        "📦 Package Manager",
        "ose pkg",
        "Advanced package management and migration"
    )
    table.add_row(
        "💾 Quantum Backup",
        "ose backup",
        "Complete system snapshot and recovery"
    )
    table.add_row(
        "🔍 Diagnostic Scan",
        "ose scan",
        "Comprehensive system health analysis"
    )
    
    console.print(table)
    console.print()
    console.print("[dim]Type a command or press Ctrl+C to exit[/dim]")


def show_version():
    """Display version information"""
    from ose import __version__, __author__
    
    console.print(Panel.fit(
        f"[bold cyan]OSE v{__version__}[/bold cyan]\n"
        f"[dim]By {__author__}[/dim]",
        title="Version",
        border_style="cyan"
    ))


async def run_cleanup_module():
    """Run cleanup module via Factory Reset Service"""
    console.print("\n[bold green][🧹] Cleanup Module (Factory Reset Service)[/bold green]\n")
    
    import httpx
    
    BASE_URL = "http://localhost:8002"
    
    # Show menu
    console.print("[bold]Cleanup Operations (via Factory Reset Service):[/bold]")
    console.print("1. Clean all caches")
    console.print("2. Clean temporary files")
    console.print("3. Clean old logs")
    console.print("4. Find duplicate files")
    console.print("5. Privacy cleanup")
    console.print("6. Empty trash")
    console.print("7. Run all cleanup operations")
    console.print("0. Back to main menu")
    
    choice = console.input("\n[bold cyan]Select operation:[/bold cyan] ")
    
    try:
        async with httpx.AsyncClient() as client:
            if choice == "1":
                console.print("\n[yellow][⚙️] Cleaning caches via API...[/yellow]")
                response = await client.get(f"{BASE_URL}/api/v1/cleanup/cache")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[✅] [green]Freed {data['freed_space_mb']:.2f} MB[/green]")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
                    
            elif choice == "2":
                console.print("\n[yellow][⚙️] Cleaning temporary files via API...[/yellow]")
                response = await client.get(f"{BASE_URL}/api/v1/cleanup/temp")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[✅] [green]Freed {data['freed_space_mb']:.2f} MB[/green]")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
                    
            elif choice == "3":
                console.print("\n[yellow][⚙️] Cleaning old logs via API...[/yellow]")
                response = await client.get(f"{BASE_URL}/api/v1/cleanup/logs")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[✅] [green]Freed {data['freed_space_mb']:.2f} MB[/green]")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
                    
            elif choice == "4":
                console.print("\n[yellow][🔍] Finding duplicate files via API...[/yellow]")
                response = await client.get(f"{BASE_URL}/api/v1/cleanup/duplicates")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[📊] [green]Found {data['duplicate_groups']} duplicate groups[/green]")
                    console.print(f"[💾] [yellow]Potential space: {data['potential_space_mb']:.2f} MB[/yellow]")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
                    
            elif choice == "5":
                console.print("\n[yellow][🔐] Cleaning privacy data via API...[/yellow]")
                response = await client.get(f"{BASE_URL}/api/v1/cleanup/privacy")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[✅] [green]Freed {data['freed_space_mb']:.2f} MB[/green]")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
                    
            elif choice == "6":
                console.print("\n[yellow][🗑️] Emptying trash via API...[/yellow]")
                response = await client.get(f"{BASE_URL}/api/v1/cleanup/trash")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[✅] [green]Freed {data['freed_space_mb']:.2f} MB[/green]")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
                    
            elif choice == "7":
                console.print("\n[bold yellow][⚡] Running full cleanup via API...[/bold yellow]\n")
                response = await client.post(f"{BASE_URL}/api/v1/cleanup/all")
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[bold green][🎉] Total space freed: {data['total_freed_space_mb']:.2f} MB[/bold green]")
                    console.print("\n[cyan][📊] Details:[/cyan]")
                    for category, details in data.get('details', {}).items():
                        freed = details.get('total_freed_mb', 0)
                        console.print(f"  [•] {category}: {freed:.2f} MB")
                else:
                    console.print(f"[❌] [red]Error: {response.status_code}[/red]")
    
    except httpx.ConnectError:
        console.print("[red][❌] Error: Factory Reset Service not running. Start with:[/red]")
        console.print("[yellow][💡] docker-compose up factory-reset[/yellow]")


async def run_diagnostic_scan():
    """Run diagnostic scan"""
    from ose.core.orchestrator import OSEOrchestrator
    
    console.print("\n[bold cyan]🔍 Running Diagnostic Scan...[/bold cyan]\n")
    
    orchestrator = OSEOrchestrator()
    
    with console.status("[bold green]Analyzing system...", spinner="dots"):
        results = await orchestrator.diagnostic_scan()
        
    # Display results
    console.print(Panel.fit(
        f"[bold green]System Health: {results['health_score']}%[/bold green]\n\n"
        f"📊 Disk Usage:\n"
        f"  • Total: {CacheCleaner.format_size(results['disk_usage']['total'])}\n"
        f"  • Used: {CacheCleaner.format_size(results['disk_usage']['used'])}\n"
        f"  • Junk: {CacheCleaner.format_size(results['disk_usage']['junk'])}\n\n"
        f"⚡ Performance:\n"
        f"  • Boot Time: {results['performance']['boot_time']}s\n"
        f"  • Startup Apps: {results['performance']['startup_apps']}\n"
        f"  • Memory Usage: {results['performance']['memory_usage']}%\n\n"
        f"📦 Packages:\n"
        f"  • Total: {results['packages']['total']}\n"
        f"  • User Installed: {results['packages']['user_installed']}\n"
        f"  • Orphaned: {results['packages']['orphaned']}",
        title="📊 Diagnostic Results",
        border_style="green"
    ))


async def run_optimize_module():
    """Run optimization module"""
    from ose.optimize import (
        StartupManager,
        KernelTuner,
        MemoryOptimizer,
        ServiceAnalyzer,
        CPUGovernor,
        NetworkTuner
    )
    
    console.print("\n[bold cyan][🚀] System Optimization Module[/bold cyan]\n")
    
    # Create menu
    menu = Table.grid(padding=(0, 4))
    menu.add_row("[bold]1.[/bold] 🎯 Startup Optimization", "- Manage startup apps & boot time")
    menu.add_row("[bold]2.[/bold] 🔧 Kernel Tuning", "- Optimize kernel parameters")
    menu.add_row("[bold]3.[/bold] 💾 Memory Optimization", "- Optimize RAM and swap")
    menu.add_row("[bold]4.[/bold] ⚙️  Service Analysis", "- Analyze & optimize services")
    menu.add_row("[bold]5.[/bold] ⚡ CPU Governor", "- Manage CPU frequency scaling")
    menu.add_row("[bold]6.[/bold] 🌐 Network Tuning", "- Optimize network stack")
    menu.add_row("[bold]7.[/bold] 🚀 Full Optimization", "- Run all optimizations")
    menu.add_row("[bold]0.[/bold] ⬅️  Back", "")
    
    console.print(Panel(menu, title="[bold]Optimization Options[/bold]", border_style="cyan"))
    
    choice = console.input("\n[bold]Select option:[/bold] ").strip()
    
    if choice == "1":
        # Startup optimization
        console.print("\n[bold yellow][🎯] Startup Optimization[/bold yellow]\n")
        manager = StartupManager()
        
        with console.status("Analyzing boot time...", spinner="dots"):
            boot_info = manager.analyze_boot_time()
            
        if boot_info:
            console.print(f"⏱️  Total boot time: [bold]{boot_info.get('total_time', 'N/A')}[/bold]")
            console.print(f"🐧 Kernel time: {boot_info.get('kernel_time', 'N/A')}")
            console.print(f"👤 Userspace time: {boot_info.get('userspace_time', 'N/A')}\n")
            
            if boot_info.get('slow_services'):
                console.print("[bold]Slowest services:[/bold]")
                for service in boot_info['slow_services'][:5]:
                    console.print(f"  • {service}")
                    
        optimize = console.input("\n[yellow]Optimize boot sequence? (y/n):[/yellow] ").lower()
        if optimize == 'y':
            target = console.input("Target boot time in seconds [15]: ").strip() or "15"
            
            with console.status("Optimizing...", spinner="dots"):
                result = manager.optimize_boot(target_time=int(target))
                
            console.print(f"\n[✅] [green]Disabled {len(result['disabled'])} services[/green]")
            console.print(f"[⏱️] Estimated boot time: [bold]{result['estimated_time']}s[/bold]")
            
    elif choice == "2":
        # Kernel tuning
        console.print("\n[bold yellow][🔧] Kernel Tuning[/bold yellow]\n")
        tuner = KernelTuner()
        
        console.print("Available profiles:")
        console.print("  1. Desktop - General desktop usage")
        console.print("  2. Server - Server workloads")
        console.print("  3. Gaming - Low latency gaming\n")
        
        profile_choice = console.input("Select profile (1-3): ").strip()
        profiles = {"1": "desktop", "2": "server", "3": "gaming"}
        profile = profiles.get(profile_choice, "desktop")
        
        with console.status(f"Applying {profile} profile...", spinner="dots"):
            result = tuner.apply_profile(profile)
            
        if result["success"]:
            console.print(f"\n[✅] [green]Applied {len(result['applied'])} kernel parameters[/green]")
            console.print(f"[📋] Profile: [bold]{profile}[/bold]")
        else:
            console.print(f"\n[❌] [red]Failed to apply profile[/red]")
            
    elif choice == "3":
        # Memory optimization
        console.print("\n[bold yellow][💾] Memory Optimization[/bold yellow]\n")
        optimizer = MemoryOptimizer()
        
        mem_info = optimizer.get_memory_info()
        console.print(f"📊 Memory Status:")
        console.print(f"  • Total: {optimizer.format_bytes(mem_info.total)}")
        console.print(f"  • Used: {optimizer.format_bytes(mem_info.used)} ({mem_info.usage_percent:.1f}%)")
        console.print(f"  • Available: {optimizer.format_bytes(mem_info.available)}")
        console.print(f"  • Swap: {optimizer.format_bytes(mem_info.swap_used)} / {optimizer.format_bytes(mem_info.swap_total)}\n")
        
        console.print("Optimization options:")
        console.print("  1. Clear caches")
        console.print("  2. Optimize swap settings")
        console.print("  3. Enable zram")
        console.print("  4. All of the above\n")
        
        opt_choice = console.input("Select option (1-4): ").strip()
        
        if opt_choice in ["1", "4"]:
            with console.status("Clearing caches...", spinner="dots"):
                result = optimizer.clear_caches("all")
            console.print(f"[✅] [green]Freed {optimizer.format_bytes(result['freed'])}[/green]")
            
        if opt_choice in ["2", "4"]:
            with console.status("Optimizing swap...", spinner="dots"):
                result = optimizer.optimize_swap()
            console.print(f"[✅] [green]Optimized swap settings[/green]")
            
        if opt_choice in ["3", "4"]:
            enable_zram = console.input("Enable zram (compressed RAM swap)? (y/n): ").lower()
            if enable_zram == 'y':
                with console.status("Configuring zram...", spinner="dots"):
                    result = optimizer.configure_zram(enable=True)
                if result["success"]:
                    console.print(f"[✅] [green]zram enabled ({result['size_mb']}MB)[/green]")
                    
    elif choice == "4":
        # Service analysis
        console.print("\n[bold yellow][⚙️] Service Analysis[/bold yellow]\n")
        analyzer = ServiceAnalyzer()
        
        with console.status("Analyzing services...", spinner="dots"):
            analysis = analyzer.analyze_services()
            
        console.print(f"📊 Service Status:")
        console.print(f"  • Total: {analysis['total_services']}")
        console.print(f"  • Active: {analysis['active']}")
        console.print(f"  • Failed: {analysis['failed']}")
        console.print(f"  • Safe to disable: {len(analysis['safe_to_disable'])}\n")
        
        for rec in analysis["recommendations"]:
            console.print(f"  {rec}")
            
        optimize = console.input("\n[yellow]Auto-optimize services? (y/n):[/yellow] ").lower()
        if optimize == 'y':
            with console.status("Optimizing services...", spinner="dots"):
                result = analyzer.optimize_services()
            console.print(f"\n[✅] [green]Disabled {len(result['disabled'])} services[/green]")
            console.print(f"[⏹️] Stopped {len(result['stopped'])} failed services[/green]")
            
    elif choice == "5":
        # CPU governor
        console.print("\n[bold yellow][⚡] CPU Governor[/bold yellow]\n")
        governor = CPUGovernor()
        
        cpus = governor.get_cpu_info()
        if cpus:
            console.print(f"💻 CPU Information:")
            console.print(f"  • CPUs: {len(cpus)}")
            console.print(f"  • Current governor: [bold]{cpus[0].governor}[/bold]")
            console.print(f"  • Frequency: {cpus[0].current_freq}MHz")
            console.print(f"  • Available governors: {', '.join(cpus[0].available_governors)}\n")
            
            console.print("Profiles:")
            console.print("  1. Performance - Maximum performance")
            console.print("  2. Balanced - Balance performance & power")
            console.print("  3. Powersave - Maximum battery life\n")
            
            profile_choice = console.input("Select profile (1-3): ").strip()
            profiles = {"1": "performance", "2": "balanced", "3": "powersave"}
            profile = profiles.get(profile_choice, "balanced")
            
            with console.status(f"Applying {profile} profile...", spinner="dots"):
                result = governor.apply_profile(profile)
                
            if result["success"]:
                console.print(f"\n[✅] [green]Applied {profile} profile[/green]")
                console.print(f"[⚙️] Governor: {result['governor']}")
        else:
            console.print("[❌] [red]CPU frequency scaling not available[/red]")
            
    elif choice == "6":
        # Network tuning
        console.print("\n[bold yellow][🌐] Network Tuning[/bold yellow]\n")
        tuner = NetworkTuner()
        
        console.print("Profiles:")
        console.print("  1. Low Latency - Gaming, VoIP")
        console.print("  2. High Throughput - Downloads, streaming")
        console.print("  3. Server - Server workloads")
        console.print("  4. WiFi - WiFi optimization\n")
        
        profile_choice = console.input("Select profile (1-4): ").strip()
        profiles = {"1": "low_latency", "2": "high_throughput", "3": "server", "4": "wifi"}
        profile = profiles.get(profile_choice, "low_latency")
        
        with console.status(f"Applying {profile} profile...", spinner="dots"):
            result = tuner.apply_profile(profile)
            
        if result["success"]:
            console.print(f"\n[✅] [green]Applied {len(result['applied'])} network parameters[/green]")
            console.print(f"[📋] Profile: [bold]{profile}[/bold]")
            console.print(f"[📖] {result['description']}")
        else:
            console.print(f"\n[❌] [red]Failed to apply profile[/red]")
            
    elif choice == "7":
        # Full optimization
        console.print("\n[bold yellow][🚀] Full System Optimization[/bold yellow]\n")
        console.print("[yellow][⚠️] WARNING[/yellow]: This will apply optimizations across all areas")
        confirm = console.input("Continue? (y/n): ").lower()
        
        if confirm == 'y':
            # Startup
            console.print("\n[1️⃣] [cyan][⚡] Optimizing startup...[/cyan]")
            startup = StartupManager()
            boot_result = startup.optimize_boot(target_time=15)
            console.print(f"   [✅] Boot optimization complete")
            
            # Kernel
            console.print("\n[2️⃣] [cyan][🔧] Tuning kernel...[/cyan]")
            kernel = KernelTuner()
            kernel_result = kernel.apply_profile("desktop")
            console.print(f"   [✅] Kernel tuning complete")
            
            # Memory
            console.print("\n[3️⃣] [cyan][💾] Optimizing memory...[/cyan]")
            memory = MemoryOptimizer()
            memory.clear_caches("all")
            memory.optimize_swap()
            console.print(f"   [✅] Memory optimization complete")
            
            # Services
            console.print("\n[4️⃣] [cyan][⚙️] Optimizing services...[/cyan]")
            services = ServiceAnalyzer()
            service_result = services.optimize_services()
            console.print(f"   [✅] Service optimization complete")
            
            # CPU
            console.print("\n[5️⃣] [cyan][⚡] Configuring CPU...[/cyan]")
            cpu = CPUGovernor()
            cpu_result = cpu.apply_profile("balanced")
            console.print(f"   [✅] CPU configuration complete")
            
            # Network
            console.print("\n[6️⃣] [cyan][🌐] Tuning network...[/cyan]")
            network = NetworkTuner()
            net_result = network.apply_profile("low_latency")
            console.print(f"   [✅] Network tuning complete")
            
            console.print("\n[bold green][🎉] Full system optimization complete![/bold green]")
            console.print("[dim][💡] Consider rebooting for all changes to take effect[/dim]")


async def run_diagnostic_scan():
    """Run diagnostic scan"""
    from ose.core.orchestrator import OSEOrchestrator
    
    console.print("\n[bold cyan]🔍 Running Diagnostic Scan...[/bold cyan]\n")
    
    orchestrator = OSEOrchestrator()
    
    with console.status("[bold green]Analyzing system...", spinner="dots"):
        results = await orchestrator.diagnostic_scan()
        
    # Display results
    console.print(Panel.fit(
        f"[bold green]System Health: {results['health_score']}%[/bold green]\n\n"
        f"📊 Disk Usage:\n"
        f"  • Total: {CacheCleaner.format_size(results['disk_usage']['total'])}\n"
        f"  • Used: {CacheCleaner.format_size(results['disk_usage']['used'])}\n"
        f"  • Junk: {CacheCleaner.format_size(results['disk_usage']['junk'])}\n\n"
        f"⚡ Performance:\n"
        f"  • Boot Time: {results['performance']['boot_time']}s\n"
        f"  • Startup Apps: {results['performance']['startup_apps']}\n"
        f"  • Memory Usage: {results['performance']['memory_usage']}%\n\n"
        f"📦 Packages:\n"
        f"  • Total: {results['packages']['total']}\n"
        f"  • User Installed: {results['packages']['user_installed']}\n"
        f"  • Orphaned: {results['packages']['orphaned']}",
        title="📊 Diagnostic Results",
        border_style="green"
    ))


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ['--version', '-v']:
            show_version()
            return
            
        elif command in ['--help', '-h']:
            console.print(__doc__)
            return
            
        elif command == 'cleanup':
            asyncio.run(run_cleanup_module())
            return
            
        elif command == 'scan':
            asyncio.run(run_diagnostic_scan())
            return
            
        elif command == 'optimize':
            asyncio.run(run_optimize_module())
            return
            
        elif command in ['reset', 'backup', 'pkg']:
            console.print(f"\n[yellow][⚠️] Module '{command}' coming soon![/yellow]\n")
            return
            
        else:
            console.print(f"\n[red][❌] Unknown command: {command}[/red]\n")
            console.print("[dim][📚] Run 'ose --help' for usage information[/dim]\n")
            return
    
    # Interactive mode
    show_banner()
    show_main_menu()
    
    try:
        while True:
            command = console.input("\n[bold cyan]ose>[/bold cyan] ").strip().lower()
            
            if command in ['exit', 'quit', 'q']:
                console.print("\n[dim][👋] Goodbye![/dim]\n")
                break
                
            elif command == 'cleanup':
                asyncio.run(run_cleanup_module())
                
            elif command == 'scan':
                asyncio.run(run_diagnostic_scan())
                
            elif command == 'optimize':
                asyncio.run(run_optimize_module())
                
            elif command in ['reset', 'backup', 'pkg']:
                console.print(f"\n[yellow]⚠️  Module '{command}' coming soon![/yellow]\n")
                
            elif command == 'help':
                show_main_menu()
                
            elif command == '':
                continue
                
            else:
                console.print(f"\n[red][❌] Unknown command: {command}[/red]")
                console.print("[dim][💡] Type 'help' for available commands[/dim]\n")
                
    except KeyboardInterrupt:
        console.print("\n\n[dim][⚠️] Interrupted. [👋] Goodbye![/dim]\n")
        
    except Exception as e:
        console.print(f"\n[bold red][❌] Error: {e}[/bold red]\n")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
