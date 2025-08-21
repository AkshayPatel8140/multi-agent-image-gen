#!/usr/bin/env python3
"""
Setup script for Simple Math and Search Agent
============================================

This script helps you set up the environment and dependencies for the agent.
Run it with: python setup.py
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print a nice header for the setup process."""
    print("🤖 Simple Math and Search Agent Setup")
    print("=" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected.")
        print("   This project requires Python 3.8 or higher.")
        print("   Please upgrade Python and try again.")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    print("\n🔧 Setting up virtual environment...")
    
    if os.path.exists(".venv"):
        print("✅ Virtual environment already exists.")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment.")
        return False

def get_activation_command():
    """Get the appropriate activation command for the current OS."""
    if platform.system() == "Windows":
        return ".venv\\Scripts\\activate"
    else:
        return "source .venv/bin/activate"

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Determine the pip command to use
    if platform.system() == "Windows":
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        pip_cmd = ".venv/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        print("   Try running manually: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is set."""
    print("\n🔑 Checking API key configuration...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        # Mask the API key for security
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"✅ OpenAI API key found: {masked_key}")
        return True
    else:
        print("⚠️  OpenAI API key not found in environment variables.")
        print("   You'll need to set it before running the agent.")
        return False

def create_env_file():
    """Create a .env file template."""
    print("\n📝 Creating environment file template...")
    
    env_content = """# Environment Variables for Simple Math and Search Agent
# =====================================================
#
# Copy this file to .env and fill in your actual values
# cp .env.example .env

# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# Alternative Language Model Providers (uncomment and configure as needed)
# ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
# GOOGLE_API_KEY=your-google-api-key-here
# COHERE_API_KEY=your-cohere-api-key-here

# Optional: Model Configuration
# OPENAI_MODEL=gpt-4o-mini
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
# GOOGLE_MODEL=gemini-1.5-flash

# Optional: Logging and Debug
# LOG_LEVEL=INFO
# DEBUG_MODE=false
"""
    
    try:
        with open(".env.example", "w") as f:
            f.write(env_content)
        print("✅ .env.example file created!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env.example: {e}")
        return False

def print_next_steps():
    """Print the next steps for the user."""
    print("\n🎯 Next Steps:")
    print("=" * 30)
    
    activation_cmd = get_activation_command()
    
    print("1. Activate the virtual environment:")
    print(f"   {activation_cmd}")
    print()
    
    print("2. Set your OpenAI API key:")
    if platform.system() == "Windows":
        print("   set OPENAI_API_KEY=sk-your-api-key-here")
    else:
        print("   export OPENAI_API_KEY=sk-your-api-key-here")
    print()
    
    print("3. Run the agent:")
    print("   python simple_agent.py")
    print()
    
    print("4. For more help, check the README.md file")
    print()

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Create environment file template
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Dependencies installation failed, but you can try manually.")
    
    # Check API key
    check_api_key()
    
    # Print next steps
    print_next_steps()
    
    print("🎉 Setup complete! Follow the steps above to get started.")

if __name__ == "__main__":
    main()
