#!/usr/bin/env python3
"""
Setup script for Brand-Aware AI Image Generator with Verification
This script helps you get everything ready to run the brand image generator with verification
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
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
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
        os.makedirs("verification_results", exist_ok=True)
        print("✅ Output directories created")
        return True
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        return False

def show_verification_features():
    """Highlight the verification features"""
    print("\n🔍 BRAND VERIFICATION FEATURES")
    print("=" * 50)
    
    features = [
        "🎨 Palette Compliance: Checks image colors against brand palette",
        "📝 Style Compliance: Validates prompts follow brand guidelines",
        "🚫 Content Filtering: Ensures no forbidden terms appear",
        "✅ Quality Assurance: Guarantees brand-consistent output",
        "📊 Detailed Reports: Comprehensive compliance analysis",
        "🤖 5 AI Agents: Specialized workflow with verification"
    ]
    
    for feature in features:
        print(f"   {feature}")

def show_usage_examples():
    """Show example usage commands"""
    print("\n🚀 Setup complete! Here are some example commands:")
    print("=" * 60)
    print("1. Generate ACME Robotics image with verification:")
    print("   python brand_verify_agent.py --company acme --idea 'A futuristic office space'")
    print()
    print("2. Generate Red & White education image with verification:")
    print("   python brand_verify_agent.py --company red&white --idea 'Students in a modern classroom' --size 1792x1024")
    print()
    print("3. Generate TechFlow corporate image with verification:")
    print("   python brand_verify_agent.py --company techflow --idea 'Team collaboration meeting' --position top-left")
    print()
    print("4. Explore the system capabilities:")
    print("   python demo.py")
    print()
    print("5. Check verification results:")
    print("   ls verification_results/")

def main():
    """Main setup function"""
    print("🚀 Setting up Brand-Aware AI Image Generator with Verification")
    print("=" * 70)
    print("This system creates perfectly branded images AND verifies compliance!")
    print()
    
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
    
    # Show verification features
    show_verification_features()
    
    print("\n🎉 Setup complete!")
    print("To run the brand image generator with verification:")
    print("   python brand_verify_agent.py --company <brand> --idea '<description>'")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Remember to set your OpenAI API key before running!")
    
    show_usage_examples()
    
    print("\n🔍 What Happens After Generation:")
    print("1. Image is created and logo composited")
    print("2. Brand verification runs automatically")
    print("3. Compliance report saved to verification_results/")
    print("4. Overall compliance score displayed")
    print("5. Detailed analysis available in JSON report")

if __name__ == "__main__":
    main()
