#!/usr/bin/env python3
"""
Development setup script for LucienAI
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors gracefully."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up LucienAI development environment...")
    
    # Check if we're in the right directory
    if not Path("Lucien.py").exists():
        print("❌ Error: Please run this script from the LucienAI root directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing main dependencies"):
        sys.exit(1)
    
    if not run_command("pip install -r requirements-dev.txt", "Installing development dependencies"):
        print("⚠️ Warning: Some dev dependencies failed to install")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        try:
            with open("env.example", "r") as f:
                template = f.read()
            with open(".env", "w") as f:
                f.write(template)
            print("✅ Created .env file - please add your GROQ_API_KEY")
        except FileNotFoundError:
            print("⚠️ Warning: env.example not found, creating basic .env")
            with open(".env", "w") as f:
                f.write("GROQ_API_KEY=\nUSE_INTERNET=true\n")
    
    # Run tests
    print("🧪 Running tests...")
    if run_command("python -m pytest -q", "Running tests"):
        print("✅ All tests passed!")
    else:
        print("⚠️ Some tests failed - this is normal if services are not available")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Add your GROQ_API_KEY to the .env file")
    print("2. Run 'python Lucien.py' to start Lucien")
    print("3. Type 'help' for available commands")

if __name__ == "__main__":
    main()
