#!/usr/bin/env python3
"""
Demo script for Brand-Aware AI Image Generator with Verification
This script demonstrates the system's capabilities with predefined examples
Perfect for presentations and demonstrations
"""

import os
import sys
from brand_verify_agent import KB, brand_context_text

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

def show_verification_system():
    """Explain how the brand verification system works"""
    print("\n🔍 BRAND VERIFICATION SYSTEM")
    print("=" * 50)
    
    verification_steps = [
        {
            "step": 1,
            "process": "Image Analysis",
            "description": "Extracts dominant colors and analyzes visual elements",
            "output": "Color palette and style analysis"
        },
        {
            "step": 2,
            "process": "Palette Compliance",
            "description": "Compares image colors with brand color palette",
            "output": "Color distance scores and compliance status"
        },
        {
            "step": 3,
            "process": "Style Compliance",
            "description": "Checks prompt for forbidden terms and style elements",
            "output": "Content analysis and style validation"
        },
        {
            "step": 4,
            "process": "Overall Assessment",
            "description": "Combines all checks for final compliance score",
            "output": "Comprehensive compliance report"
        }
    ]
    
    for step in verification_steps:
        print(f"\n{step['step']}. 🔍 {step['process']}")
        print(f"   Description: {step['description']}")
        print(f"   Output: {step['output']}")

def show_compliance_examples():
    """Show examples of what gets verified"""
    print("\n📊 COMPLIANCE CHECKING EXAMPLES")
    print("=" * 50)
    
    compliance_checks = [
        {
            "type": "🎨 Palette Compliance",
            "checks": [
                "Dominant color extraction",
                "Brand color matching",
                "Color distance calculation",
                "Threshold-based scoring"
            ]
        },
        {
            "type": "📝 Style Compliance",
            "checks": [
                "Forbidden terms detection",
                "Required style elements",
                "Brand voice consistency",
                "Aesthetic alignment"
            ]
        },
        {
            "type": "🚫 Content Validation",
            "checks": [
                "Inappropriate content filtering",
                "Brand personality matching",
                "Style keyword presence",
                "Overall brand alignment"
            ]
        }
    ]
    
    for check in compliance_checks:
        print(f"\n{check['type']}")
        for item in check['checks']:
            print(f"   • {item}")

def show_demo_scenarios():
    """Show example scenarios for each brand with verification"""
    print("\n🎬 DEMO SCENARIOS WITH VERIFICATION")
    print("=" * 50)
    
    scenarios = {
        "acme": {
            "title": "ACME Robotics - Tech Innovation with Verification",
            "idea": "A futuristic office space with sleek robotics, metallic textures, and high-tech equipment",
            "verification": "Checks for tech-focused aesthetic, red/black color compliance, modern style elements",
            "command": "python brand_verify_agent.py --company acme --idea 'A futuristic office space with sleek robotics and metallic textures'"
        },
        "red&white": {
            "title": "Red & White - Educational Excellence with Verification",
            "idea": "Students collaborating in a modern, well-lit classroom with digital learning tools",
            "verification": "Ensures educational tone, white background compliance, friendly style elements",
            "command": "python brand_verify_agent.py --company red&white --idea 'Students collaborating in a modern, well-lit classroom'"
        },
        "techflow": {
            "title": "TechFlow - Corporate Professionalism with Verification",
            "idea": "A team meeting in a clean, modern conference room with blue accents and technology",
            "verification": "Validates corporate style, blue color compliance, professional aesthetic",
            "command": "python brand_verify_agent.py --company techflow --idea 'A team meeting in a clean, modern conference room'"
        },
        "creative_studio": {
            "title": "Creative Studio - Artistic Expression with Verification",
            "idea": "An artist working in a vibrant, colorful studio with creative tools and inspiration",
            "verification": "Checks for artistic style, vibrant color compliance, creative elements",
            "command": "python brand_verify_agent.py --company creative_studio --idea 'An artist working in a vibrant, colorful studio'"
        },
        "eco_green": {
            "title": "EcoGreen - Sustainability Focus with Verification",
            "idea": "A green office space with plants, natural light, and eco-friendly materials",
            "verification": "Ensures natural aesthetic, green color compliance, sustainable elements",
            "command": "python brand_verify_agent.py --company eco_green --idea 'A green office space with plants and natural light'"
        }
    }
    
    for brand_key, scenario in scenarios.items():
        print(f"\n🎨 {scenario['title']}")
        print(f"   Brand: {brand_key}")
        print(f"   Idea: {scenario['idea']}")
        print(f"   Verification: {scenario['verification']}")
        print(f"   Command: {scenario['command']}")

def show_output_structure():
    """Show what output files and reports are generated"""
    print("\n📁 OUTPUT STRUCTURE")
    print("=" * 50)
    
    output_structure = {
        "generated_brand_image/": [
            "base_YYYYMMDD_HHMMSS.png - Base image before logo",
            "acme_final_YYYYMMDD_HHMMSS.png - Final branded image",
            "red&white_final_YYYYMMDD_HHMMSS.png - Final branded image"
        ],
        "verification_results/": [
            "verification_report_YYYYMMDD_HHMMSS.json - Detailed compliance report",
            "Contains: palette compliance, style compliance, overall score"
        ]
    }
    
    for directory, files in output_structure.items():
        print(f"\n📂 {directory}")
        for file in files:
            print(f"   📄 {file}")

def show_verification_report_sample():
    """Show a sample verification report structure"""
    print("\n📊 SAMPLE VERIFICATION REPORT")
    print("=" * 50)
    
    sample_report = {
        "verification_report": {
            "overall_compliant": True,
            "palette_compliance": {
                "compliant": True,
                "threshold": 80.0,
                "dominant_to_palette_distances": [
                    {"dominant_color": "(255, 59, 59)", "closest_distance": 45.2},
                    {"dominant_color": "(17, 17, 17)", "closest_distance": 32.1}
                ],
                "brand_colors": ["#FF3B3B", "#111111", "#FFFFFF"]
            },
            "style_compliance": {
                "forbidden_terms_found": [],
                "style_elements_present": ["modern", "innovative"],
                "brand_colors_mentioned": ["#FF3B3B"],
                "overall_style_compliant": True
            }
        },
        "summary": {
            "brand_compliant": True,
            "palette_compliant": True,
            "style_compliant": True
        }
    }
    
    print("The system generates comprehensive JSON reports like this:")
    print("✅ Overall Compliance: True/False")
    print("🎨 Palette Compliance: Color matching scores")
    print("📝 Style Compliance: Content and style validation")
    print("📊 Summary: Quick compliance overview")

def main():
    """Main demo function"""
    print("🎬 BRAND-AWARE AI IMAGE GENERATOR WITH VERIFICATION DEMO")
    print("=" * 70)
    print("This script showcases the capabilities of our 5-agent AI system with brand verification!")
    print("Perfect for demonstrations and presentations!")
    print()
    
    # Check if brand knowledge base is loaded
    if not KB:
        print("❌ Brand knowledge base not loaded!")
        print("Make sure to run this from the project directory")
        return
    
    # Show different demo sections
    show_brand_overview()
    
    # Interactive demo
    print("\n" + "=" * 70)
    print("💡 INTERACTIVE DEMO")
    print("=" * 70)
    
    while True:
        print("\nAvailable commands:")
        print("  'brand <name>' - Show detailed brand info (e.g., 'brand acme')")
        print("  'verification' - Explain the verification system")
        print("  'compliance' - Show compliance checking examples")
        print("  'scenarios' - Show demo scenarios with verification")
        print("  'output' - Show output file structure")
        print("  'report' - Show sample verification report")
        print("  'quit' - Exit demo")
        
        user_input = input("\n🎯 Enter command: ").strip().lower()
        
        if user_input.startswith("brand "):
            brand_name = user_input.split(" ", 1)[1]
            show_brand_details(brand_name)
        elif user_input == "verification":
            show_verification_system()
        elif user_input == "compliance":
            show_compliance_examples()
        elif user_input == "scenarios":
            show_demo_scenarios()
        elif user_input == "output":
            show_output_structure()
        elif user_input == "report":
            show_verification_report_sample()
        elif user_input == "quit":
            print("\n👋 Thanks for exploring the Brand-Aware AI Image Generator with Verification!")
            break
        else:
            print("❌ Unknown command. Try 'brand acme', 'verification', 'compliance', 'scenarios', 'output', 'report', or 'quit'")

if __name__ == "__main__":
    main()
