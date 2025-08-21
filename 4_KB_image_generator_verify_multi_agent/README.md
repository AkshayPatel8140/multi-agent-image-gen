# Brand-Aware AI Image Generator with Verification

**The Ultimate AI-Powered Brand Consistency System** that not only creates perfectly branded images but also **verifies they meet your brand guidelines**!

This system combines the power of **5 AI agents** working together to:
1. **Load brand knowledge** (colors, voice, dos/donts, logo variants, typography, style)
2. **Engineer brand-aware prompts** that follow your style guidelines
3. **Generate base images** using OpenAI's DALL-E 3 API
4. **Composite brand logos** exactly as specified without distortion
5. **🔍 VERIFY brand compliance** and output detailed reports

---

## 🎯 What Makes This System Special

### **Multi-Agent Workflow + Brand Verification**
- **5 AI Agents**: Each specialized in a specific aspect of brand image creation
- **Real-Time Verification**: Automatically checks if generated images match brand criteria
- **Compliance Reports**: Detailed JSON reports showing what's compliant and what needs improvement
- **Quality Assurance**: Ensures every image meets your brand standards

### **Brand Verification Features**
- **🎨 Palette Compliance**: Checks if image colors match your brand palette
- **📝 Style Compliance**: Verifies prompts follow brand guidelines
- **🚫 Forbidden Terms**: Ensures no unwanted content appears
- **✅ Required Elements**: Confirms brand-appropriate style elements
- **📊 Detailed Reports**: Comprehensive compliance analysis

---

## 📂 Project Structure
```
4_KB_image_generator_verify_multi_agent/
├── brand_verify_agent.py          # Main 5-agent script with verification
├── brand_kb/
│   ├── brand_kb.json            # Enhanced brand guidelines database
│   └── logos/                   # Company logo PNGs
│       ├── acme/                # ACME Robotics logos
│       ├── red&white/           # Red & White Skill Education logos
│       ├── techflow/            # TechFlow Solutions logos
│       ├── creative_studio/     # Creative Studio Arts logos
│       └── eco_green/           # EcoGreen Sustainability logos
├── generated_brand_image/        # Output folder for generated images
├── verification_results/         # Brand compliance reports
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 Quick Start

### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your OpenAI API Key
```bash
export OPENAI_API_KEY=your_api_key_here  # macOS/Linux
# OR
set OPENAI_API_KEY=your_api_key_here     # Windows
```

### 4. Run the Brand Image Generator with Verification
```bash
python brand_verify_agent.py --company acme --idea "A futuristic office space with green plants"
```

---

## 🤖 The 5 AI Agents

### **Agent 1: Brand Knowledge Agent**
- Loads and analyzes your complete brand guidelines
- Provides context for all downstream agents
- Ensures brand consistency throughout the process

### **Agent 2: Prompt Engineering Agent**
- Creates brand-aware image descriptions using AI
- Follows your voice, style, and color guidelines
- Generates prompts that match your brand personality

### **Agent 3: Image Generation Agent**
- Uses DALL-E 3 to create high-quality base images
- Applies the engineered prompts for brand consistency
- Generates images in your specified dimensions

### **Agent 4: Logo Compositing Agent**
- Places your brand logo in the exact position specified
- Automatically chooses light/dark logo variants for best contrast
- Preserves logo quality without distortion

### **Agent 5: Brand Verification Agent** 🆕
- **Analyzes the final image** for brand compliance
- **Checks color palette** against your brand colors
- **Verifies style elements** in the generated prompt
- **Outputs detailed reports** with compliance scores

---

## 🏢 Available Brands

The system comes pre-configured with 5 brands, each with comprehensive guidelines:

### **ACME Robotics**
- **Style**: Modern, high contrast, tech-focused
- **Colors**: Red (#FF3B3B), Black (#111111), White (#FFFFFF), Blue (#00D4FF)
- **Voice**: Innovative, confident, minimal, futuristic

### **Red & White Skill Education**
- **Style**: Clean, educational, white backgrounds
- **Colors**: Red (#E50914), White (#FFFFFF), Dark Gray (#1F1F1F)
- **Voice**: Friendly, instructional, trustworthy, encouraging

### **TechFlow Solutions**
- **Style**: Corporate, clean, blue-focused, trustworthy
- **Colors**: Blue (#2563EB), Dark Blue (#1E40AF), White (#FFFFFF)
- **Voice**: Professional, reliable, innovative, approachable

### **Creative Studio Arts**
- **Style**: Colorful, artistic, creative, dynamic
- **Colors**: Purple (#8B5CF6), Pink (#EC4899), Orange (#F59E0B), Green (#10B981)
- **Voice**: Creative, artistic, vibrant, expressive

### **EcoGreen Sustainability**
- **Style**: Natural, organic, green-focused, sustainable
- **Colors**: Green (#059669), Light Green (#10B981), Mint (#34D399), Cream (#FEF3C7)
- **Voice**: Natural, sustainable, trustworthy, eco-friendly

---

## 🔍 Brand Verification System

### **What Gets Verified**

#### **1. Palette Compliance**
- Extracts dominant colors from generated images
- Compares against your brand color palette
- Calculates color distance scores
- Sets compliance threshold (default: 80.0)

#### **2. Style Compliance**
- Checks generated prompts for forbidden terms
- Verifies presence of required style elements
- Ensures brand voice consistency
- Validates overall aesthetic alignment

#### **3. Content Analysis**
- Scans for inappropriate content
- Verifies brand-appropriate language
- Checks style keyword presence
- Ensures brand personality match

### **Verification Output**

The system generates **detailed JSON reports** containing:

```json
{
  "verification_report": {
    "overall_compliant": true/false,
    "palette_compliance": {
      "compliant": true/false,
      "threshold": 80.0,
      "dominant_to_palette_distances": [...],
      "brand_colors": [...]
    },
    "style_compliance": {
      "forbidden_terms_found": [],
      "style_elements_present": [...],
      "brand_colors_mentioned": [...],
      "overall_style_compliant": true/false
    }
  },
  "generation_details": {
    "prompt": "Generated prompt text",
    "image_path": "Path to generated image",
    "generated_at": "ISO timestamp",
    "image_hash": "SHA256 hash for verification"
  },
  "summary": {
    "brand_compliant": true/false,
    "palette_compliant": true/false,
    "style_compliant": true/false
  }
}
```

---

## 🎨 Command Line Usage

### Basic Usage
```bash
python brand_verify_agent.py --company <brand> --idea "<image description>"
```

### Full Options
```bash
python brand_verify_agent.py \
  --company acme \
  --idea "A futuristic office space with green plants and modern technology" \
  --size 1024x1024 \
  --position top-right
```

### Parameters
- `--company`: Brand name (acme, red&white, techflow, creative_studio, eco_green)
- `--idea`: Your image description
- `--size`: Image dimensions (1024x1024, 1792x1024, 1024x1792)
- `--position`: Logo position (top-left, top-right, top-center, center, bottom-center, bottom-left, bottom-right)

### Real Examples
```bash
# ACME Robotics - Tech Innovation with Verification
python brand_verify_agent.py --company acme --idea "A futuristic office space with sleek robotics and metallic textures"

# Red & White - Educational Excellence with Verification
python brand_verify_agent.py --company red&white --idea "Students collaborating in a modern, well-lit classroom"

# TechFlow - Corporate Professionalism with Verification
python brand_verify_agent.py --company techflow --idea "A team meeting in a clean, modern conference room"
```

---

## 📊 Understanding Verification Results

### **Compliance Scores**

#### **✅ COMPLIANT**
- Image colors match brand palette within threshold
- No forbidden terms in prompt
- Style elements align with brand guidelines
- Overall aesthetic matches brand personality

#### **❌ NOT COMPLIANT**
- Image colors deviate significantly from brand palette
- Forbidden terms detected in prompt
- Style elements don't match brand guidelines
- Overall aesthetic doesn't align with brand

### **Improvement Suggestions**

When images are non-compliant, the verification report provides:
- **Specific color distance scores** for palette issues
- **List of forbidden terms found** for content issues
- **Missing style elements** for aesthetic issues
- **Detailed analysis** for targeted improvements

---

## 📋 Requirements

- **Python 3.8+**
- **OpenAI API key** with DALL-E 3 access
- **Transparent PNG logos** for each brand
- **Internet connection** for API calls

---

## 🎯 Perfect for Learning

This system demonstrates:
- **Advanced AI workflows** with 5 specialized agents
- **Real-time brand verification** and compliance checking
- **Professional image generation** with DALL-E 3
- **Quality assurance** through automated verification
- **Comprehensive reporting** for business applications
- **Brand consistency** in AI-generated content

---

## 🆘 Troubleshooting

**"Brand not found" errors:**
- Check brand name spelling in `brand_kb.json`
- Ensure brand name matches exactly (case-sensitive)

**"Logo file not found" errors:**
- Verify logo files exist in the correct paths
- Check that logos are transparent PNGs

**"OpenAI API key not set" errors:**
- Set your API key: `export OPENAI_API_KEY=your_key_here`
- Make sure to set it AFTER activating your virtual environment

**Verification issues:**
- Check the verification report JSON for detailed analysis
- Adjust color threshold if needed (default: 80.0)
- Review brand guidelines for style compliance

**Image generation fails:**
- Check your internet connection
- Verify your OpenAI account has credits
- Ensure your prompt follows OpenAI's content policy

---

## 🔧 Advanced Usage

### **Custom Verification Thresholds**
You can modify the color compliance threshold in the code:
```python
def check_palette_compliance(image: Image.Image, brand: BrandKBItem, threshold: float = 80.0):
    # Lower threshold = stricter color matching
    # Higher threshold = more lenient color matching
```

### **Adding New Verification Rules**
Extend the verification system by adding new checks:
```python
def check_custom_compliance(image: Image.Image, brand: BrandKBItem):
    # Add your custom verification logic here
    pass
```

### **Batch Verification**
Process multiple images and generate compliance reports:
```python
# You can extend the system to verify multiple images
# and generate comparative compliance reports
```

---

## 🚀 What's New in This Version

- ✅ **5 AI Agents**: Enhanced workflow with specialized verification agent
- ✅ **Brand Verification**: Automatic compliance checking for all generated images
- ✅ **Detailed Reports**: Comprehensive JSON reports with compliance scores
- ✅ **Color Analysis**: Advanced palette matching with distance calculations
- ✅ **Style Validation**: Content and aesthetic compliance checking
- ✅ **Quality Assurance**: Ensures every image meets brand standards
- ✅ **Professional Output**: Ready for business and marketing use

---

## 🎯 Use Cases

### **Marketing Teams**
- Generate brand-consistent social media images
- Ensure all content meets brand guidelines
- Automate quality control for visual assets

### **Design Agencies**
- Maintain client brand consistency
- Generate multiple variations with verification
- Professional quality assurance

### **Brand Managers**
- Enforce brand guidelines automatically
- Monitor visual asset compliance
- Generate compliant content at scale

### **Content Creators**
- Create branded content with confidence
- Ensure visual consistency
- Professional image generation

---

## 🔮 Future Enhancements

- **Machine Learning Verification**: AI-powered compliance scoring
- **Real-Time Feedback**: Live verification during generation
- **Brand Evolution**: Learning from compliance patterns
- **Multi-Format Support**: Video, 3D, and interactive content
- **Collaborative Workflows**: Team-based brand management

---

This system represents the **future of AI-powered brand management** - combining creative generation with intelligent verification for perfect brand consistency! 🎉
