# AI Image Generator - Two Agent System

This script demonstrates how two AI agents work together to create images from text descriptions. Perfect for demonstrations and learning about multi-agent systems.

## 🎯 How It Works

1. **Prompt Engineer Agent**: Takes your simple idea and turns it into a detailed, professional image description
2. **Image Generator Agent**: Uses that detailed description to create an actual image using OpenAI's DALL-E API

## 🚀 Quick Start

### 1. Create and Activate Virtual Environment

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Verify activation (you should see (.venv) in your terminal)
which python
```

**On Windows:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Command Prompt)
.venv\Scripts\activate

# OR activate virtual environment (PowerShell)
.venv\Scripts\Activate.ps1

# Verify activation (you should see (.venv) in your terminal)
where python
```

### 2. Install Dependencies
```bash
# Make sure your virtual environment is activated
pip install -r requirements.txt
```

### 3. Set Your OpenAI API Key

**On macOS/Linux:**
```bash
export OPENAI_API_KEY=your_api_key_here
```

**On Windows Command Prompt:**
```bash
set OPENAI_API_KEY=your_api_key_here
```

**On Windows PowerShell:**
```bash
$env:OPENAI_API_KEY="your_api_key_here"
```

### 4. Run the Script
```bash
python mulit_agent_image_generation.py
```

### 5. Deactivate Virtual Environment (when done)
```bash
deactivate
```

## 🔄 Complete Setup Example

Here's the complete sequence for a fresh setup:

```bash
# 1. Clone or download the project
cd path/to/your/project

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set API key
export OPENAI_API_KEY=sk-your-actual-key-here

# 6. Run the script
python mulit_agent_image_generation.py

# 7. When finished, deactivate
deactivate
```

## 💡 Example Usage

When you run the script:
1. Enter a simple idea like "a cozy library"
2. The first agent will create a detailed description
3. The second agent will generate the actual image
4. Your image is saved with a timestamp

## 📁 Project Structure

```
├── mulit_agent_image_generation.py  # Main script
├── requirements.txt                  # Dependencies
├── README.md                        # This file
└── generated_images/                # Output folder (created automatically)
```

## 🔧 What You Can Customize

- **AI Models**: Change `CHAT_MODEL` and `IMAGE_MODEL` variables
- **Image Size**: Modify the size parameter in the image generation function
- **Output Folder**: Change the folder name where images are saved

## 🎯 Perfect for Learning

This code is ideal for learning because:
- Clear, readable structure
- Shows real multi-agent AI interaction
- Immediate visual results
- Easy to understand step by step
- Demonstrates advanced AI concepts simply

## 📚 Key Concepts Demonstrated

- **Multi-Agent Systems**: How agents communicate and pass data
- **LangGraph**: Building agent workflows
- **OpenAI API**: Image generation with DALL-E
- **State Management**: Tracking conversation between agents
- **Error Handling**: Graceful failure management

## 🆘 Troubleshooting

**"Module not found" errors:**
- Make sure your virtual environment is activated (you should see (.venv) in terminal)
- Install requirements: `pip install -r requirements.txt`

**"OpenAI API key not set" errors:**
- Set your API key: `export OPENAI_API_KEY=your_key_here`
- Make sure to set it AFTER activating your virtual environment

**"Python command not found" errors:**
- Make sure Python is installed on your system
- Try using `python3` instead of `python` on macOS/Linux

**Image generation fails:**
- Check your internet connection
- Verify your OpenAI account has credits
- Ensure your prompt follows OpenAI's content policy

## 🔗 Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new secret key
5. Copy and use it in your environment
