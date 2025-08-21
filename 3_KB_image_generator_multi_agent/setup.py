#!/usr/bin/env python3
"""
Setup script for Brand-Aware AI Image Generator
This script helps you get everything ready to run the brand image generator
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")
        return True

def install_requirements():
    """Install required packages in a virtual environment"""
    print("📦 Creating and activating virtual environment...")
    try:
        # Create virtual environment
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
        print("✅ Virtual environment created")
        
        # Determine the activation script path
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(".venv", "Scripts", "activate.bat")
            pip_path = os.path.join(".venv", "Scripts", "pip")
        else:  # Unix/Linux/macOS
            activate_script = os.path.join(".venv", "bin", "activate")
            pip_path = os.path.join(".venv", "bin", "pip")
        
        # Activate virtual environment and install requirements
        if os.name == 'nt':  # Windows
            subprocess.check_call([activate_script, "&&", pip_path, "install", "-r", "requirements.txt"], shell=True)
        else:  # Unix/Linux/macOS
            subprocess.check_call(f"source {activate_script} && {pip_path} install -r requirements.txt", shell=True, executable="/bin/bash")
        
        print("✅ Packages installed successfully in virtual environment!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_api_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key is set")
        return True
    else:
        print("⚠️  OpenAI API key not set")
        print("Please set your API key:")
        print("   export OPENAI_API_KEY=your_api_key_here")
        return False

def check_brand_kb():
    """Check if brand knowledge base exists"""
    brand_kb_path = os.path.join("brand_kb", "brand_kb.json")
    if os.path.exists(brand_kb_path):
        print("✅ Brand knowledge base found")
        return True
    else:
        print("❌ Brand knowledge base not found")
        print("Make sure brand_kb/brand_kb.json exists")
        return False

def check_logos():
    """Check if logo directories exist"""
    logo_dirs = ["acme", "red&white", "techflow", "creative_studio", "eco_green"]
    logos_path = os.path.join("brand_kb", "logos")
    
    if not os.path.exists(logos_path):
        print("❌ Logos directory not found")
        return False
    
    missing_logos = []
    for brand in logo_dirs:
        brand_logo_path = os.path.join(logos_path, brand)
        if not os.path.exists(brand_logo_path):
            missing_logos.append(brand)
    
    if missing_logos:
        print(f"⚠️  Missing logo directories: {', '.join(missing_logos)}")
        return False
    
    print("✅ Logo directories found")
    return True

def create_directories():
    """Create necessary directories"""
    try:
        os.makedirs("generated_brand_image", exist_ok=True)
        print("✅ Output directory created")
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def show_usage_examples():
    """Show example usage commands"""
    print("\n🚀 Setup complete! Here are some example commands:")
    print("=" * 50)
    print("1. Generate ACME Robotics image:")
    print("   python brand_image_agent.py --company acme --idea 'A futuristic office space'")
    print()
    print("2. Generate Red & White education image:")
    print("   python brand_image_agent.py --company red&white --idea 'Students in a modern classroom' --size 1792x1024")
    print()
    print("3. Generate TechFlow corporate image:")
    print("   python brand_image_agent.py --company techflow --idea 'Team collaboration meeting' --position top-left")
    print()
    print("4. Generate Creative Studio artistic image:")
    print("   python brand_image_agent.py --company creative_studio --idea 'An artist working in a colorful studio'")
    print()
    print("5. Generate EcoGreen sustainability image:")
    print("   python brand_image_agent.py --company eco_green --idea 'A green office with plants and natural light'")
    print()
    print("Note: After setup, you need to activate the virtual environment and run the script from within it.")
    print("   source .venv/bin/activate  # For Unix/Linux/macOS")
    print("   .venv\Scripts\activate  # For Windows")

def main():
    """Main setup function"""
    print("🚀 Setting up Brand-Aware AI Image Generator")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check brand knowledge base
    if not check_brand_kb():
        return
    
    # Check logos
    if not check_logos():
        print("Note: You can add logo files later")
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create directories
    if not create_directories():
        return
    
    # Check API key
    check_api_key()
    
    print("\n🎉 Setup complete!")
    print("To run the brand image generator:")
    print("   python brand_image_agent.py --company <brand> --idea '<description>'")
    print()
    print("Note: After setup, you need to activate the virtual environment and run the script from within it.")
    print("   source .venv/bin/activate  # For Unix/Linux/macOS")
    print("   .venv\Scripts\activate  # For Windows")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Remember to set your OpenAI API key before running!")
    
    show_usage_examples()

if __name__ == "__main__":
    main()
