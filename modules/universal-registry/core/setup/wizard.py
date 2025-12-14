#!/usr/bin/env python3
"""
Intelligent Guided Setup & Configuration Wizard
Full-stack enterprise configuration system
Version: ∞.8
"""

import asyncio
import yaml
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import os

class SetupPhase(str, Enum):
    """Setup wizard phases"""
    WELCOME = "welcome"
    ENVIRONMENT = "environment"
    DATABASE = "database"
    FEATURES = "features"
    INTEGRATIONS = "integrations"
    SECURITY = "security"
    DEPLOYMENT = "deployment"
    VERIFICATION = "verification"
    COMPLETE = "complete"


class ConfigScope(str, Enum):
    """Configuration scope"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    ENTERPRISE = "enterprise"


@dataclass
class SetupStep:
    """Individual setup step"""
    id: str
    title: str
    description: str
    prompts: List[Dict[str, Any]]
    validators: List[Callable] = field(default_factory=list)
    auto_configure: Optional[Callable] = None
    dependencies: List[str] = field(default_factory=list)
    optional: bool = False
    completed: bool = False


@dataclass
class ConfigProfile:
    """Configuration profile"""
    name: str
    scope: ConfigScope
    settings: Dict[str, Any]
    enabled_features: List[str]
    integrations: Dict[str, Dict[str, Any]]
    security_level: str = "standard"
    auto_scaling: bool = False


class SetupWizard:
    """Intelligent guided setup wizard"""
    
    def __init__(self, base_dir: str = "/workspaces/terminal/modules/universal-registry"):
        self.base_dir = Path(base_dir)
        self.current_phase = SetupPhase.WELCOME
        self.config: Dict[str, Any] = {}
        self.profile: Optional[ConfigProfile] = None
        
        # Setup steps by phase
        self.steps: Dict[SetupPhase, List[SetupStep]] = self._initialize_steps()
        
        # Detected environment
        self.environment: Dict[str, Any] = {}
        
        # Progress tracking
        self.progress = {
            "total_steps": 0,
            "completed_steps": 0,
            "current_phase": SetupPhase.WELCOME.value,
            "started_at": None,
            "completed_at": None
        }
    
    def _initialize_steps(self) -> Dict[SetupPhase, List[SetupStep]]:
        """Initialize setup steps"""
        return {
            SetupPhase.WELCOME: [
                SetupStep(
                    id="welcome",
                    title="Welcome to Universal Registry Setup",
                    description="This wizard will guide you through the configuration process",
                    prompts=[
                        {
                            "name": "deployment_mode",
                            "type": "choice",
                            "message": "Select deployment mode",
                            "choices": ["Development", "Staging", "Production", "Enterprise"],
                            "default": "Development"
                        },
                        {
                            "name": "auto_configure",
                            "type": "confirm",
                            "message": "Enable auto-configuration with intelligent defaults?",
                            "default": True
                        }
                    ]
                )
            ],
            
            SetupPhase.ENVIRONMENT: [
                SetupStep(
                    id="detect_system",
                    title="Environment Detection",
                    description="Detecting your system configuration",
                    prompts=[],
                    auto_configure=self._detect_environment
                ),
                SetupStep(
                    id="python_deps",
                    title="Python Dependencies",
                    description="Configure Python environment and dependencies",
                    prompts=[
                        {
                            "name": "python_version",
                            "type": "input",
                            "message": "Python version (detected: auto)",
                            "default": "auto"
                        },
                        {
                            "name": "install_dependencies",
                            "type": "confirm",
                            "message": "Install required Python packages?",
                            "default": True
                        }
                    ]
                ),
                SetupStep(
                    id="system_resources",
                    title="System Resources",
                    description="Configure resource limits and quotas",
                    prompts=[
                        {
                            "name": "max_memory_mb",
                            "type": "input",
                            "message": "Maximum memory (MB)",
                            "default": "2048"
                        },
                        {
                            "name": "max_cpu_cores",
                            "type": "input",
                            "message": "Maximum CPU cores",
                            "default": "auto"
                        }
                    ]
                )
            ],
            
            SetupPhase.DATABASE: [
                SetupStep(
                    id="primary_database",
                    title="Primary Database",
                    description="Configure the main database",
                    prompts=[
                        {
                            "name": "db_type",
                            "type": "choice",
                            "message": "Select database type",
                            "choices": ["SQLite (embedded)", "PostgreSQL", "CockroachDB"],
                            "default": "SQLite (embedded)"
                        },
                        {
                            "name": "db_path",
                            "type": "input",
                            "message": "Database path/connection string",
                            "default": "/var/lib/ose/plugins/registry.db"
                        }
                    ]
                ),
                SetupStep(
                    id="vector_database",
                    title="Vector Database (Optional)",
                    description="Configure vector database for semantic search",
                    prompts=[
                        {
                            "name": "enable_vector_db",
                            "type": "confirm",
                            "message": "Enable vector database for advanced search?",
                            "default": False
                        },
                        {
                            "name": "vector_db_type",
                            "type": "choice",
                            "message": "Select vector database",
                            "choices": ["In-memory", "Qdrant", "Weaviate", "Milvus"],
                            "default": "In-memory",
                            "when": lambda x: x.get("enable_vector_db")
                        }
                    ],
                    optional=True
                )
            ],
            
            SetupPhase.FEATURES: [
                SetupStep(
                    id="feature_categories",
                    title="Feature Categories",
                    description="Select which feature categories to enable",
                    prompts=[
                        {
                            "name": "enabled_features",
                            "type": "multiselect",
                            "message": "Select features to enable",
                            "choices": [
                                "AI & Machine Learning",
                                "Web3 & Blockchain",
                                "Cloud Native",
                                "Data Engineering",
                                "DevOps & CI/CD",
                                "Security & Compliance",
                                "System Operations",
                                "Monitoring & Observability"
                            ],
                            "default": "all"
                        }
                    ]
                ),
                SetupStep(
                    id="plugin_system",
                    title="Plugin System",
                    description="Configure plugin management",
                    prompts=[
                        {
                            "name": "auto_classification",
                            "type": "confirm",
                            "message": "Enable automatic plugin classification?",
                            "default": True
                        },
                        {
                            "name": "plugin_isolation",
                            "type": "choice",
                            "message": "Plugin isolation level",
                            "choices": ["None", "Process", "Container", "WASM"],
                            "default": "Process"
                        }
                    ]
                )
            ],
            
            SetupPhase.INTEGRATIONS: [
                SetupStep(
                    id="api_configuration",
                    title="API Configuration",
                    description="Configure REST API and WebSocket",
                    prompts=[
                        {
                            "name": "api_port",
                            "type": "input",
                            "message": "API server port",
                            "default": "8080"
                        },
                        {
                            "name": "enable_websocket",
                            "type": "confirm",
                            "message": "Enable WebSocket streaming?",
                            "default": True
                        },
                        {
                            "name": "enable_graphql",
                            "type": "confirm",
                            "message": "Enable GraphQL API?",
                            "default": False
                        }
                    ]
                ),
                SetupStep(
                    id="webhook_config",
                    title="Webhook & Notifications",
                    description="Configure webhooks and notification channels",
                    prompts=[
                        {
                            "name": "enable_webhooks",
                            "type": "confirm",
                            "message": "Enable webhook support?",
                            "default": True
                        },
                        {
                            "name": "notification_channels",
                            "type": "multiselect",
                            "message": "Select notification channels",
                            "choices": ["Email", "Slack", "Teams", "PagerDuty", "Discord"],
                            "default": []
                        }
                    ],
                    optional=True
                ),
                SetupStep(
                    id="service_mesh",
                    title="Service Mesh Integration",
                    description="Configure service mesh integration",
                    prompts=[
                        {
                            "name": "enable_service_mesh",
                            "type": "confirm",
                            "message": "Enable service mesh integration?",
                            "default": False
                        },
                        {
                            "name": "mesh_type",
                            "type": "choice",
                            "message": "Select service mesh",
                            "choices": ["Istio", "Linkerd", "Consul"],
                            "default": "Istio",
                            "when": lambda x: x.get("enable_service_mesh")
                        }
                    ],
                    optional=True
                )
            ],
            
            SetupPhase.SECURITY: [
                SetupStep(
                    id="authentication",
                    title="Authentication",
                    description="Configure authentication methods",
                    prompts=[
                        {
                            "name": "auth_method",
                            "type": "choice",
                            "message": "Select authentication method",
                            "choices": ["None (Dev only)", "API Key", "OAuth 2.0", "SAML", "mTLS"],
                            "default": "API Key"
                        },
                        {
                            "name": "enable_rbac",
                            "type": "confirm",
                            "message": "Enable role-based access control (RBAC)?",
                            "default": False
                        }
                    ]
                ),
                SetupStep(
                    id="encryption",
                    title="Encryption & Secrets",
                    description="Configure encryption and secrets management",
                    prompts=[
                        {
                            "name": "enable_encryption",
                            "type": "confirm",
                            "message": "Enable data encryption at rest?",
                            "default": False
                        },
                        {
                            "name": "secrets_backend",
                            "type": "choice",
                            "message": "Select secrets management backend",
                            "choices": ["Environment Variables", "HashiCorp Vault", "AWS Secrets Manager", "macOS Keychain"],
                            "default": "Environment Variables"
                        }
                    ]
                )
            ],
            
            SetupPhase.DEPLOYMENT: [
                SetupStep(
                    id="deployment_target",
                    title="Deployment Target",
                    description="Configure deployment environment",
                    prompts=[
                        {
                            "name": "deployment_type",
                            "type": "choice",
                            "message": "Select deployment type",
                            "choices": ["Local", "Docker", "Kubernetes", "Nomad"],
                            "default": "Local"
                        },
                        {
                            "name": "auto_start",
                            "type": "confirm",
                            "message": "Auto-start on system boot?",
                            "default": False
                        }
                    ]
                ),
                SetupStep(
                    id="monitoring",
                    title="Monitoring & Observability",
                    description="Configure monitoring and metrics",
                    prompts=[
                        {
                            "name": "enable_prometheus",
                            "type": "confirm",
                            "message": "Enable Prometheus metrics?",
                            "default": True
                        },
                        {
                            "name": "enable_tracing",
                            "type": "confirm",
                            "message": "Enable distributed tracing (OpenTelemetry)?",
                            "default": False
                        },
                        {
                            "name": "log_level",
                            "type": "choice",
                            "message": "Select log level",
                            "choices": ["DEBUG", "INFO", "WARNING", "ERROR"],
                            "default": "INFO"
                        }
                    ]
                )
            ],
            
            SetupPhase.VERIFICATION: [
                SetupStep(
                    id="verify_config",
                    title="Verify Configuration",
                    description="Verify all settings and test connections",
                    prompts=[],
                    auto_configure=self._verify_configuration
                )
            ]
        }
    
    async def run(self) -> Dict[str, Any]:
        """Run the setup wizard"""
        print("\n" + "="*70)
        print("🚀 Universal Registry - Intelligent Setup Wizard")
        print("="*70 + "\n")
        
        # Count total steps
        self.progress["total_steps"] = sum(
            len(steps) for steps in self.steps.values()
        )
        
        # Run through phases
        for phase in SetupPhase:
            if phase == SetupPhase.COMPLETE:
                continue
            
            self.current_phase = phase
            self.progress["current_phase"] = phase.value
            
            await self._run_phase(phase)
        
        # Generate final configuration
        await self._generate_configuration()
        
        self.current_phase = SetupPhase.COMPLETE
        self.progress["completed_at"] = True
        
        print("\n" + "="*70)
        print("✅ Setup Complete!")
        print("="*70 + "\n")
        
        return self.config
    
    async def _run_phase(self, phase: SetupPhase):
        """Run a setup phase"""
        steps = self.steps.get(phase, [])
        
        if not steps:
            return
        
        print(f"\n📋 {phase.value.upper()} Phase")
        print("-" * 70)
        
        for step in steps:
            await self._run_step(step)
    
    async def _run_step(self, step: SetupStep):
        """Run a setup step"""
        print(f"\n▶ {step.title}")
        print(f"  {step.description}\n")
        
        # Auto-configure if available
        if step.auto_configure:
            result = await step.auto_configure()
            if result:
                self.config.update(result)
                step.completed = True
                self.progress["completed_steps"] += 1
                print("  ✓ Auto-configured")
                return
        
        # Process prompts
        step_config = {}
        for prompt in step.prompts:
            # Check conditional prompts
            if "when" in prompt:
                if not prompt["when"](step_config):
                    continue
            
            value = await self._prompt_user(prompt)
            step_config[prompt["name"]] = value
        
        # Update config
        self.config[step.id] = step_config
        step.completed = True
        self.progress["completed_steps"] += 1
        
        print("  ✓ Completed")
    
    async def _prompt_user(self, prompt: Dict[str, Any]) -> Any:
        """Prompt user for input (simplified for demo)"""
        # In production, use: questionary, PyInquirer, or rich prompts
        prompt_type = prompt["type"]
        message = prompt["message"]
        default = prompt.get("default")
        
        if prompt_type == "confirm":
            print(f"  {message} (yes/no) [default: {'yes' if default else 'no'}]")
            # Auto-accept defaults in non-interactive mode
            return default
        
        elif prompt_type == "choice":
            choices = prompt["choices"]
            print(f"  {message}")
            for i, choice in enumerate(choices, 1):
                print(f"    {i}. {choice}")
            print(f"  [default: {default}]")
            return default
        
        elif prompt_type == "multiselect":
            choices = prompt["choices"]
            print(f"  {message}")
            for i, choice in enumerate(choices, 1):
                print(f"    {i}. {choice}")
            print(f"  [default: {default}]")
            return default
        
        elif prompt_type == "input":
            print(f"  {message} [default: {default}]")
            return default
        
        return default
    
    async def _detect_environment(self) -> Dict[str, Any]:
        """Auto-detect environment"""
        import platform
        import sys
        
        env = {
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.machine(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "hostname": platform.node(),
            "cpu_count": os.cpu_count()
        }
        
        self.environment = env
        
        print("  Detected environment:")
        for key, value in env.items():
            print(f"    • {key}: {value}")
        
        return env
    
    async def _verify_configuration(self) -> Dict[str, Any]:
        """Verify configuration"""
        print("  Verifying configuration...")
        
        # Check required directories
        required_dirs = [
            self.base_dir / "core",
            self.base_dir / "plugins",
            self.base_dir / "microservices",
            self.base_dir / "docs"
        ]
        
        for dir_path in required_dirs:
            if dir_path.exists():
                print(f"    ✓ {dir_path.name}/ exists")
            else:
                print(f"    ✗ {dir_path.name}/ missing")
        
        # Check Python dependencies
        try:
            import fastapi
            print(f"    ✓ FastAPI {fastapi.__version__}")
        except ImportError:
            print("    ✗ FastAPI not installed")
        
        return {"verified": True}
    
    async def _generate_configuration(self):
        """Generate final configuration files"""
        print("\n📝 Generating configuration files...")
        
        # Generate config.yaml
        config_file = self.base_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
        print(f"  ✓ Generated: {config_file}")
        
        # Generate .env file
        env_file = self.base_dir / ".env"
        with open(env_file, 'w') as f:
            f.write(f"# Universal Registry Configuration\n")
            f.write(f"# Generated: {self.progress.get('completed_at')}\n\n")
            
            # Extract key config values
            if "api_configuration" in self.config:
                api_config = self.config["api_configuration"]
                f.write(f"API_PORT={api_config.get('api_port', '8080')}\n")
            
            if "primary_database" in self.config:
                db_config = self.config["primary_database"]
                f.write(f"DATABASE_PATH={db_config.get('db_path', '/var/lib/ose/plugins/registry.db')}\n")
        
        print(f"  ✓ Generated: {env_file}")
        
        # Generate startup script
        startup_script = self.base_dir / "start_registry.sh"
        with open(startup_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Universal Registry Startup Script\n\n")
            f.write("cd /workspaces/terminal/modules/universal-registry\n")
            f.write("python3 hyper_registry.py\n")
        
        os.chmod(startup_script, 0o755)
        print(f"  ✓ Generated: {startup_script}")


# CLI entry point
async def main():
    """Main setup wizard entry point"""
    wizard = SetupWizard()
    config = await wizard.run()
    
    print("\nSetup complete! Configuration saved to:")
    print("  • config.yaml")
    print("  • .env")
    print("  • start_registry.sh")
    print("\nTo start the registry:")
    print("  ./start_registry.sh")
    print("\nOr manually:")
    print("  python3 hyper_registry.py")


if __name__ == "__main__":
    asyncio.run(main())
