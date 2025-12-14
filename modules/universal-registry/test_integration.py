#!/usr/bin/env python3
"""
Universal Registry - Integration Test
Tests the unified platform control interface
"""

import requests
import time
import subprocess
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
API_URL = f"{BASE_URL}/api/v1"

class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

def print_test(name: str):
    print(f"\n{Colors.CYAN}🧪 Testing: {name}{Colors.NC}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")

def check_health() -> bool:
    """Check if registry is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def test_health_endpoint() -> bool:
    """Test health check endpoint"""
    print_test("Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check: {data.get('status', 'unknown')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_plugin_api() -> bool:
    """Test plugin management API"""
    print_test("Plugin Management API")
    
    try:
        # Test 1: List plugins
        response = requests.get(f"{API_URL}/plugins/")
        if response.status_code == 200:
            print_success(f"List plugins: {response.status_code}")
        else:
            print_error(f"List plugins failed: {response.status_code}")
            return False
        
        # Test 2: Register plugin
        plugin_data = {
            "id": "test-plugin-001",
            "name": "Test Plugin",
            "version": "1.0.0",
            "feature": "system",
            "description": "Test plugin for integration testing",
            "author": "Test Suite"
        }
        response = requests.post(f"{API_URL}/plugins/register", json=plugin_data)
        if response.status_code == 200:
            print_success(f"Register plugin: {response.status_code}")
        else:
            print_error(f"Register plugin failed: {response.status_code}")
            return False
        
        # Test 3: Get plugin details
        response = requests.get(f"{API_URL}/plugins/test-plugin-001")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Get plugin details: {data['name']}")
        else:
            print_error(f"Get plugin failed: {response.status_code}")
            return False
        
        # Test 4: Install plugin
        response = requests.post(f"{API_URL}/plugins/test-plugin-001/install")
        if response.status_code == 200:
            print_success("Install plugin: 200")
        else:
            print_error(f"Install plugin failed: {response.status_code}")
            return False
        
        # Test 5: Activate plugin
        response = requests.post(f"{API_URL}/plugins/test-plugin-001/activate")
        if response.status_code == 200:
            print_success("Activate plugin: 200")
        else:
            print_error(f"Activate plugin failed: {response.status_code}")
            return False
        
        # Test 6: Check plugin health
        response = requests.get(f"{API_URL}/plugins/test-plugin-001/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Plugin health: {data.get('health', 'unknown')}")
        else:
            print_error(f"Plugin health check failed: {response.status_code}")
            return False
        
        # Test 7: Get plugin logs
        response = requests.get(f"{API_URL}/plugins/test-plugin-001/logs")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Plugin logs: {data['total_logs']} entries")
        else:
            print_error(f"Get plugin logs failed: {response.status_code}")
            return False
        
        # Test 8: Deactivate plugin
        response = requests.post(f"{API_URL}/plugins/test-plugin-001/deactivate")
        if response.status_code == 200:
            print_success("Deactivate plugin: 200")
        else:
            print_error(f"Deactivate plugin failed: {response.status_code}")
            return False
        
        # Test 9: Uninstall plugin
        response = requests.delete(f"{API_URL}/plugins/test-plugin-001")
        if response.status_code == 200:
            print_success("Uninstall plugin: 200")
        else:
            print_error(f"Uninstall plugin failed: {response.status_code}")
            return False
        
        return True
    
    except Exception as e:
        print_error(f"Plugin API test error: {e}")
        return False

def test_microservices_api() -> bool:
    """Test microservices management API"""
    print_test("Microservices Management API")
    
    try:
        # Test 1: List services
        response = requests.get(f"{API_URL}/services")
        if response.status_code == 200:
            data = response.json()
            print_success(f"List services: {len(data.get('services', {}))} services")
        else:
            print_error(f"List services failed: {response.status_code}")
            return False
        
        # Test 2: Register service
        service_data = {
            "id": "test-service",
            "name": "Test Service",
            "port": 9999,
            "description": "Test service",
            "category": "application"
        }
        response = requests.post(f"{API_URL}/services/register", json=service_data)
        if response.status_code == 200:
            print_success("Register service: 200")
        else:
            print_error(f"Register service failed: {response.status_code}")
            return False
        
        return True
    
    except Exception as e:
        print_error(f"Microservices API test error: {e}")
        return False

def test_streams_api() -> bool:
    """Test event streams API"""
    print_test("Event Streams API")
    
    try:
        # Test: Get stream stats
        response = requests.get(f"{API_URL}/streams/stats")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Stream stats: {data.get('total_events', 0)} events")
        else:
            print_error(f"Stream stats failed: {response.status_code}")
            return False
        
        return True
    
    except Exception as e:
        print_error(f"Streams API test error: {e}")
        return False

def test_webhooks_api() -> bool:
    """Test webhooks API"""
    print_test("Webhooks API")
    
    try:
        # Test: List webhooks
        response = requests.get(f"{API_URL}/webhooks")
        if response.status_code == 200:
            data = response.json()
            print_success(f"List webhooks: {len(data.get('webhooks', []))} registered")
        else:
            print_error(f"List webhooks failed: {response.status_code}")
            return False
        
        return True
    
    except Exception as e:
        print_error(f"Webhooks API test error: {e}")
        return False

def test_search_api() -> bool:
    """Test search API"""
    print_test("Search API")
    
    try:
        # Test: Get search stats
        response = requests.get(f"{API_URL}/search/stats")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Search stats: {data.get('total_documents', 0)} documents")
        else:
            print_error(f"Search stats failed: {response.status_code}")
            return False
        
        return True
    
    except Exception as e:
        print_error(f"Search API test error: {e}")
        return False

def test_plugin_statistics() -> bool:
    """Test plugin statistics endpoint"""
    print_test("Plugin Statistics")
    
    try:
        response = requests.get(f"{API_URL}/plugins/stats/overview")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Total plugins: {data.get('total_plugins', 0)}")
            print_success(f"By status: {data.get('by_status', {})}")
            print_success(f"By feature: {data.get('by_feature', {})}")
            return True
        else:
            print_error(f"Plugin stats failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Plugin stats error: {e}")
        return False

def test_cli_commands() -> bool:
    """Test CLI commands"""
    print_test("CLI Commands")
    
    try:
        # Test: CLI version
        result = subprocess.run(
            ["universal-registry-cli", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "Universal Hyper Registry CLI" in result.stdout:
            print_success("CLI version command works")
        else:
            print_warning("CLI version command output unexpected")
        
        # Test: CLI help
        result = subprocess.run(
            ["universal-registry-cli", "help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "PLUGIN MANAGEMENT" in result.stdout:
            print_success("CLI help command works")
        else:
            print_warning("CLI help command output unexpected")
        
        return True
    
    except Exception as e:
        print_error(f"CLI test error: {e}")
        return False

def main():
    """Run all integration tests"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print("Universal Registry - Integration Test Suite")
    print(f"{'='*60}{Colors.NC}\n")
    
    # Check if registry is running
    if not check_health():
        print_error("Registry is not running!")
        print_warning("Start with: python3 /workspaces/terminal/modules/universal-registry/hyper_registry.py")
        sys.exit(1)
    
    print_success("Registry is running\n")
    
    # Run tests
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Plugin API", test_plugin_api),
        ("Microservices API", test_microservices_api),
        ("Event Streams API", test_streams_api),
        ("Webhooks API", test_webhooks_api),
        ("Search API", test_search_api),
        ("Plugin Statistics", test_plugin_statistics),
        ("CLI Commands", test_cli_commands),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name} failed with exception: {e}")
            results.append((name, False))
    
    # Print summary
    print(f"\n{Colors.CYAN}{'='*60}")
    print("Test Summary")
    print(f"{'='*60}{Colors.NC}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✓ PASSED{Colors.NC}" if result else f"{Colors.RED}✗ FAILED{Colors.NC}"
        print(f"{status} - {name}")
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"{Colors.GREEN}✓ All tests passed!{Colors.NC}")
        sys.exit(0)
    else:
        print(f"{Colors.RED}✗ Some tests failed{Colors.NC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
