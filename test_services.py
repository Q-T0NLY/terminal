#!/usr/bin/env python3
"""
🧪 OSE Platform Integration Tests
Comprehensive testing for all microservices
"""

import requests
import json
import time
from typing import Dict, Any
from colorama import Fore, Style, init

init(autoreset=True)

BASE_URLS = {
    "discovery": "http://localhost:8001",
    "factory-reset": "http://localhost:8002",
    "reinstallation": "http://localhost:8003",
    "optimization": "http://localhost:8004",
    "terminal-config": "http://localhost:8005"
}


def print_header(text: str):
    """Print test header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def print_success(text: str):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")


def print_error(text: str):
    """Print error message"""
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")


def print_info(text: str):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")


def test_service_health(service: str, url: str) -> bool:
    """Test service health endpoint"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"{service}: {data.get('status', 'unknown')}")
            return True
        else:
            print_error(f"{service}: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"{service}: {str(e)}")
        return False


def test_discovery_service():
    """Test Discovery Service"""
    print_header("Testing Discovery Service")
    
    url = BASE_URLS["discovery"]
    
    # Test hardware discovery
    print_info("Testing hardware discovery...")
    try:
        response = requests.get(f"{url}/api/v1/discover/hardware", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"CPU cores: {data['cpu']['cores_logical']}")
            print_success(f"Memory: {data['memory']['total_gb']} GB")
            print_success(f"Disks: {len(data['disk']['partitions'])}")
        else:
            print_error(f"Hardware discovery failed: {response.status_code}")
    except Exception as e:
        print_error(f"Hardware discovery error: {e}")
    
    # Test full scan
    print_info("Testing full system scan...")
    try:
        response = requests.post(
            f"{url}/api/v1/scan",
            json={"scan_type": "quick"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print_success(f"Scan completed: {data['scan_id']}")
            print_success(f"Hardware detected: {'✓' if data.get('hardware') else '✗'}")
            print_success(f"Software detected: {'✓' if data.get('software') else '✗'}")
        else:
            print_error(f"Scan failed: {response.status_code}")
    except Exception as e:
        print_error(f"Scan error: {e}")


def test_factory_reset_service():
    """Test Factory Reset Service"""
    print_header("Testing Factory Reset Service")
    
    url = BASE_URLS["factory-reset"]
    
    # Test profiles
    print_info("Testing reset profiles...")
    try:
        response = requests.get(f"{url}/api/v1/reset/profiles", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Profiles available: {len(data['profiles'])}")
            for profile in data['profiles']:
                print(f"  - {profile['name']}: {profile['description']}")
        else:
            print_error(f"Profiles failed: {response.status_code}")
    except Exception as e:
        print_error(f"Profiles error: {e}")
    
    # Test analysis
    print_info("Testing reset analysis...")
    try:
        response = requests.get(f"{url}/api/v1/reset/analyze", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Total items: {data['total_items']}")
            print_success(f"Total size: {data['total_size_mb']} MB")
            print_success(f"Components: {len(data['components'])}")
            for component in data['components'][:3]:
                print(f"  - {component['name']}: {component['size_mb']} MB ({component['risk_level']})")
        else:
            print_error(f"Analysis failed: {response.status_code}")
    except Exception as e:
        print_error(f"Analysis error: {e}")


def test_reinstallation_service():
    """Test Reinstallation Service"""
    print_header("Testing Reinstallation Service")
    
    url = BASE_URLS["reinstallation"]
    
    # Test templates
    print_info("Testing config templates...")
    try:
        response = requests.get(f"{url}/api/v1/config/templates", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Templates available: {data['total']}")
            for template in data['templates']:
                print(f"  - {template['name']}: {template['description']}")
        else:
            print_error(f"Templates failed: {response.status_code}")
    except Exception as e:
        print_error(f"Templates error: {e}")
    
    # Test config generation
    print_info("Testing config generation...")
    try:
        response = requests.post(
            f"{url}/api/v1/config/generate",
            json={
                "template_id": "nginx",
                "variables": {"worker_connections": 2048},
                "output_path": "/tmp/nginx.conf"
            },
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print_success(f"Config generated for: {data['template_id']}")
            print_success(f"Output path: {data['output_path']}")
        else:
            print_error(f"Config generation failed: {response.status_code}")
    except Exception as e:
        print_error(f"Config generation error: {e}")


def test_optimization_service():
    """Test Optimization Service"""
    print_header("Testing Optimization Service")
    
    url = BASE_URLS["optimization"]
    
    # Test recommendations
    print_info("Testing optimization recommendations...")
    try:
        response = requests.get(f"{url}/api/v1/optimize/recommendations", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Recommendations: {data['total_recommendations']}")
            for rec in data['recommendations'][:5]:
                print(f"  - {rec['title']} (impact: {rec['impact_score']}/10)")
        else:
            print_error(f"Recommendations failed: {response.status_code}")
    except Exception as e:
        print_error(f"Recommendations error: {e}")
    
    # Test benchmark
    print_info("Testing benchmark...")
    try:
        response = requests.post(
            f"{url}/api/v1/benchmark/run",
            json={"categories": ["cpu", "memory"], "duration_seconds": 5},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            print_success(f"CPU score: {data['cpu_score']}")
            print_success(f"Memory score: {data['memory_score']}")
            print_success(f"Overall score: {data['overall_score']}")
        else:
            print_error(f"Benchmark failed: {response.status_code}")
    except Exception as e:
        print_error(f"Benchmark error: {e}")


def test_terminal_config_service():
    """Test Terminal Config Service"""
    print_header("Testing Terminal Config Service")
    
    url = BASE_URLS["terminal-config"]
    
    # Test profiles
    print_info("Testing config profiles...")
    try:
        response = requests.get(f"{url}/api/v1/profiles", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Profiles available: {len(data['profiles'])}")
            for profile in data['profiles']:
                print(f"  - {profile['name']}: {profile['description']}")
        else:
            print_error(f"Profiles failed: {response.status_code}")
    except Exception as e:
        print_error(f"Profiles error: {e}")
    
    # Test themes
    print_info("Testing themes...")
    try:
        response = requests.get(f"{url}/api/v1/themes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Themes available: {len(data['themes'])}")
            for theme in data['themes'][:3]:
                print(f"  - {theme['name']} by {theme['author']}")
        else:
            print_error(f"Themes failed: {response.status_code}")
    except Exception as e:
        print_error(f"Themes error: {e}")
    
    # Test config generation
    print_info("Testing config generation...")
    try:
        response = requests.post(
            f"{url}/api/v1/config/generate",
            json={
                "profile": "enterprise",
                "theme": "powerlevel10k",
                "plugins": ["zsh-autosuggestions", "zsh-syntax-highlighting"]
            },
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print_success(f"Config ID: {data['config_id']}")
            print_success(f"Files generated: {len(data['generated_files'])}")
        else:
            print_error(f"Config generation failed: {response.status_code}")
    except Exception as e:
        print_error(f"Config generation error: {e}")


def main():
    """Main test runner"""
    print(f"{Fore.CYAN}")
    print("🧪 OSE Platform Integration Tests")
    print("=" * 60)
    print(Style.RESET_ALL)
    
    # Test health
    print_header("Health Checks")
    results = {}
    for service, url in BASE_URLS.items():
        results[service] = test_service_health(service, url)
    
    # Summary
    healthy = sum(results.values())
    total = len(results)
    print(f"\n{Fore.CYAN}Health Summary: {healthy}/{total} services healthy{Style.RESET_ALL}")
    
    if healthy < total:
        print_error(f"\n{total - healthy} service(s) are not responding!")
        print_info("Make sure all services are running: docker-compose up -d")
        return
    
    # Run individual tests
    test_discovery_service()
    test_factory_reset_service()
    test_reinstallation_service()
    test_optimization_service()
    test_terminal_config_service()
    
    # Final summary
    print_header("Test Summary")
    print_success("All integration tests completed!")
    print_info("Check the output above for any failures")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print_error(f"Test suite error: {e}")
