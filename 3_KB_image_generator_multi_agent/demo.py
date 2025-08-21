#!/usr/bin/env python3
"""
Demo script for Brand-Aware AI Image Generator
This script demonstrates the system's capabilities with predefined examples
Perfect for presentations and demonstrations
"""

import os
import sys
from brand_image_agent import KB, brand_context_text

def show_brand_overview():
    """Display overview of all available brands"""
    print("🏢 BRAND OVERVIEW")
    print("=" * 50)
    
    for brand_key, brand_data in KB.items():
        print(f"\n🎯 {brand_data.display_name}")
        print(f"   Key: {brand_key}")
        print(f"   Voice: {brand_data.voice}")
        print(f"   Style: {brand_data.visual_style}")
        print(f"   Colors: {', '.join(brand_data.brand_colors_hex[:3])}...")
        print(f"   Logo Position: {brand_data.default_logo_position}")

def show_brand_details(brand_key):
    """Show detailed information about a specific brand"""
    if brand_key not in KB:
        print(f"❌ Brand '{brand_key}' not found")
        return
    
    brand = KB[brand_key]
    print(f"\n📋 DETAILED BRAND ANALYSIS: {brand.display_name}")
    print("=" * 60)
    
    print(f"🎨 Visual Style: {brand.visual_style}")
    print(f"🗣️  Voice: {brand.voice}")
    print(f"🎨 Brand Colors: {', '.join(brand.brand_colors_hex)}")
    print(f"✨ Typography: {brand.typography}")
    print(f"🖼️  Image Style: {brand.image_style}")
    
    print(f"\n✅ DO's:")
    for do_item in brand.dos:
        print(f"   • {do_item}")
    
    print(f"\n❌ DON'T's:")
    for dont_item in brand.donts:
        print(f"   • {dont_item}")
    
    print(f"\n🖼️  Logo Variants:")
    for variant, path in brand.logo_variants.items():
        print(f"   • {variant}: {path}")
    
    print(f"\n📍 Default Logo Position: {brand.default_logo_position}")

def show_demo_scenarios():
    """Show example scenarios for each brand"""
    print("\n🎬 DEMO SCENARIOS")
    print("=" * 50)
    
    scenarios = {
        "acme": {
            "title": "ACME Robotics - Tech Innovation",
            "idea": "A futuristic office space with sleek robotics, metallic textures, and high-tech equipment",
            "description": "Perfect for showcasing cutting-edge technology and innovation"
        },
        "red&white": {
            "title": "Red & White - Educational Excellence",
            "idea": "Students collaborating in a modern, well-lit classroom with digital learning tools",
            "description": "Ideal for educational marketing and student recruitment"
        },
        "techflow": {
            "title": "TechFlow - Corporate Professionalism",
            "idea": "A team meeting in a clean, modern conference room with blue accents and technology",
            "description": "Great for corporate presentations and business development"
        },
        "creative_studio": {
            "title": "Creative Studio - Artistic Expression",
            "idea": "An artist working in a vibrant, colorful studio with creative tools and inspiration",
            "description": "Perfect for creative portfolios and artistic marketing"
        },
        "eco_green": {
            "title": "EcoGreen - Sustainability Focus",
            "idea": "A green office space with plants, natural light, and eco-friendly materials",
            "description": "Ideal for environmental and sustainability messaging"
        }
    }
    
    for brand_key, scenario in scenarios.items():
        print(f"\n🎨 {scenario['title']}")
        print(f"   Brand: {brand_key}")
        print(f"   Idea: {scenario['idea']}")
        print(f"   Use Case: {scenario['description']}")
        print(f"   Command: python brand_image_agent.py --company {brand_key} --idea '{scenario['idea']}'")

def show_system_workflow():
    """Explain how the multi-agent system works"""
    print("\n🤖 MULTI-AGENT SYSTEM WORKFLOW")
    print("=" * 50)
    
    workflow_steps = [
        {
            "step": 1,
            "agent": "Brand Knowledge Agent",
            "action": "Loads brand guidelines, colors, voice, and style preferences",
            "output": "Brand context message with all guidelines"
        },
        {
            "step": 2,
            "agent": "Prompt Engineering Agent",
            "action": "Creates brand-aware image descriptions using AI",
            "output": "Optimized prompt that follows brand guidelines"
        },
        {
            "step": 3,
            "agent": "Image Generation Agent",
            "action": "Generates base image using DALL-E 3",
            "output": "High-quality image matching the brand aesthetic"
        },
        {
            "step": 4,
            "agent": "Logo Compositing Agent",
            "action": "Places brand logo in specified position",
            "output": "Final branded image ready for use"
        }
    ]
    
    for step in workflow_steps:
        print(f"\n{step['step']}. 🤖 {step['agent']}")
        print(f"   Action: {step['action']}")
        print(f"   Output: {step['output']}")

def show_technical_features():
    """Highlight technical features of the system"""
    print("\n⚙️ TECHNICAL FEATURES")
    print("=" * 50)
    
    features = [
        "🎯 Brand-Aware Prompt Engineering",
        "🖼️ DALL-E 3 Integration",
        "🎨 Automatic Logo Variant Selection",
        "📍 Precise Logo Positioning",
        "🔒 Brand Guideline Enforcement",
        "📱 Multiple Image Sizes",
        "🎭 5 Different Brand Personalities",
        "🚀 Multi-Agent Workflow",
        "💾 Automatic Image Saving",
        "📊 Progress Tracking"
    ]
    
    for feature in features:
        print(f"   {feature}")

def main():
    """Main demo function"""
    print("🎬 BRAND-AWARE AI IMAGE GENERATOR DEMO")
    print("=" * 60)
    print("This script showcases the capabilities of our multi-agent AI system")
    print("Perfect for demonstrations and presentations!")
    print()
    
    # Check if brand knowledge base is loaded
    if not KB:
        print("❌ Brand knowledge base not loaded!")
        print("Make sure to run this from the project directory")
        return
    
    # Show different demo sections
    show_brand_overview()
    
    # Interactive brand selection
    print("\n" + "=" * 60)
    print("💡 INTERACTIVE DEMO")
    print("=" * 60)
    
    while True:
        print("\nAvailable commands:")
        print("  'brand <name>' - Show detailed brand info (e.g., 'brand acme')")
        print("  'scenarios' - Show demo scenarios")
        print("  'workflow' - Explain the AI workflow")
        print("  'features' - Show technical features")
        print("  'quit' - Exit demo")
        
        user_input = input("\n🎯 Enter command: ").strip().lower()
        
        if user_input.startswith("brand "):
            brand_name = user_input.split(" ", 1)[1]
            show_brand_details(brand_name)
        elif user_input == "scenarios":
            show_demo_scenarios()
        elif user_input == "workflow":
            show_system_workflow()
        elif user_input == "features":
            show_technical_features()
        elif user_input == "quit":
            print("\n👋 Thanks for exploring the Brand-Aware AI Image Generator!")
            break
        else:
            print("❌ Unknown command. Try 'brand acme', 'scenarios', 'workflow', 'features', or 'quit'")

if __name__ == "__main__":
    main()
