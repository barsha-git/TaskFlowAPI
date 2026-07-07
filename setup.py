#!/usr/bin/env python3
"""
Automated setup script for TaskFlowAPI development environment.

This script handles:
- Virtual environment creation
- Dependency installation
- Environment configuration
- Database setup guidance
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def run_command(cmd, description, critical=True):
    """
    Run a shell command and handle errors.
    
    Args:
        cmd: Command to run (list)
        description: Description of the command
        critical: If True, exit on failure
    
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{Colors.BOLD}{description}{Colors.RESET}")
    print(f"{Colors.CYAN}Running: {' '.join(cmd)}{Colors.RESET}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print_success(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed with error code {e.returncode}")
        if critical:
            sys.exit(1)
        return False
    except FileNotFoundError as e:
        print_error(f"Command not found: {e}")
        if critical:
            sys.exit(1)
        return False


def check_python_version():
    """Check if Python version meets requirements"""
    if sys.version_info < (3, 8):
        print_error("Python 3.8+ is required")
        print_info(f"You have Python {sys.version.split()[0]}")
        sys.exit(1)
    
    print_success(f"Python {sys.version.split()[0]} detected")


def create_venv(venv_path):
    """Create virtual environment"""
    if venv_path.exists():
        print_info("Virtual environment already exists")
        return True
    
    return run_command(
        [sys.executable, "-m", "venv", str(venv_path)],
        "Creating virtual environment"
    )


def get_pip_command(venv_path, is_windows):
    """Get the pip command for the virtual environment"""
    if is_windows:
        return [str(venv_path / "Scripts" / "pip.exe")]
    else:
        return [str(venv_path / "bin" / "pip")]


def upgrade_pip(pip_cmd):
    """Upgrade pip"""
    return run_command(
        pip_cmd + ["install", "--upgrade", "pip"],
        "Upgrading pip"
    )


def install_dependencies(pip_cmd):
    """Install project dependencies"""
    if not Path("requirements.txt").exists():
        print_error("requirements.txt not found")
        sys.exit(1)
    
    return run_command(
        pip_cmd + ["install", "-r", "requirements.txt"],
        "Installing project dependencies"
    )


def setup_env_file():
    """Setup .env file from .env.example"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    print(f"\n{Colors.BOLD}Setting up environment variables{Colors.RESET}")
    
    if env_file.exists():
        print_info(".env file already exists")
        return True
    
    if not env_example.exists():
        print_error(".env.example not found")
        return False
    
    try:
        with open(env_example, 'r') as src:
            content = src.read()
        with open(env_file, 'w') as dst:
            dst.write(content)
        print_success("Created .env file from .env.example")
        print_warning("Please update .env with your actual configuration:")
        print("  - DATABASE_URL")
        print("  - SECRET_KEY (generate with: openssl rand -hex 32)")
        print("  - Other sensitive values")
        return True
    except IOError as e:
        print_error(f"Failed to create .env: {e}")
        return False


def print_activation_instructions(is_windows, venv_path):
    """Print virtual environment activation instructions"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}Virtual Environment Setup{Colors.RESET}")
    print("Activate the virtual environment with:")
    
    if is_windows:
        activate_cmd = f"{venv_path}\\Scripts\\activate"
        print(f"{Colors.YELLOW}{activate_cmd}{Colors.RESET}")
    else:
        activate_cmd = f"source {venv_path}/bin/activate"
        print(f"{Colors.YELLOW}{activate_cmd}{Colors.RESET}")


def print_next_steps():
    """Print next steps for user"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}Setup completed successfully!{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}Next steps:{Colors.RESET}\n")
    
    print("1. {Colors.CYAN}Activate virtual environment{Colors.RESET}:")
    is_windows = platform.system() == "Windows"
    if is_windows:
        print(f"   {Colors.YELLOW}.venv\\Scripts\\activate{Colors.RESET}\n")
    else:
        print(f"   {Colors.YELLOW}source .venv/bin/activate{Colors.RESET}\n")
    
    print("2. {Colors.CYAN}Update .env with your configuration{Colors.RESET}:")
    print(f"   - DATABASE_URL (PostgreSQL connection string)")
    print(f"   - SECRET_KEY (JWT secret key)")
    print(f"   - Other environment variables\n")
    
    print("3. {Colors.CYAN}Start PostgreSQL{Colors.RESET}:")
    print(f"   {Colors.YELLOW}docker-compose up -d{Colors.RESET}")
    print(f"   or start your local PostgreSQL instance\n")
    
    print("4. {Colors.CYAN}Run database migrations{Colors.RESET}:")
    print(f"   {Colors.YELLOW}alembic upgrade head{Colors.RESET}\n")
    
    print("5. {Colors.CYAN}Start the development server{Colors.RESET}:")
    print(f"   {Colors.YELLOW}python main.py{Colors.RESET}")
    print(f"   or {Colors.YELLOW}uvicorn main:app --reload{Colors.RESET}\n")
    
    print("6. {Colors.CYAN}Access the API{Colors.RESET}:")
    print(f"   {Colors.YELLOW}http://localhost:8000{Colors.RESET}")
    print(f"   Swagger: {Colors.YELLOW}http://localhost:8000/docs{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}{Colors.GREEN}Happy coding! 🚀{Colors.RESET}\n")


def main():
    """Main setup function"""
    print_header("TaskFlowAPI Development Setup")
    
    # Check Python version
    check_python_version()
    
    # Determine OS
    is_windows = platform.system() == "Windows"
    venv_path = Path(".venv")
    
    # Create virtual environment
    create_venv(venv_path)
    
    # Get pip command
    pip_cmd = get_pip_command(venv_path, is_windows)
    
    # Upgrade pip
    upgrade_pip(pip_cmd)
    
    # Install dependencies
    install_dependencies(pip_cmd)
    
    # Setup environment variables
    setup_env_file()
    
    # Print activation instructions
    print_activation_instructions(is_windows, venv_path)
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
