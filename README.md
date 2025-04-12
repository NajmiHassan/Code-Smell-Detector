# 🐍 Python Code Smell Detector

A user-friendly web application for detecting code quality issues in Python codebases. Analyze your Python files to find potential problems before they lead to maintenance headaches.

<div align="center">

![image](https://github.com/user-attachments/assets/fcb98d4e-414a-473d-980a-4c7de6493101)
*Preview Image 1*

![image](https://github.com/user-attachments/assets/a5539a16-cd1f-4f0f-b5d3-f0c70a63933e)
*Preview Image 2*

</div>

## 📋 Introduction

The Python Code Smell Detector is an interactive tool that helps developers identify potential issues in their Python code. It automatically detects common "code smells" that might indicate deeper problems in your codebase.

### What are Code Smells?

Code smells are patterns in code that suggest potential design or implementation problems. They're not bugs, but they might lead to bugs or make your code harder to maintain in the future.

### Why Use This Tool?

- **Improve Code Quality**: Identify problematic patterns early
- **Reduce Technical Debt**: Fix issues before they compound
- **Enhance Maintainability**: Make your codebase easier to work with
- **Learn Better Practices**: Understand common pitfalls to avoid

## Features

### 🔍 Code Smell Detection

The tool currently detects the following code smells:

- **Long Functions**: Functions that exceed a configurable line limit
- **Too Many Parameters**: Functions with excessive parameters
- **Duplicate Code**: Repeated blocks of code that could be refactored

### 📊 Analysis Report

- Visual indicators of detected issues
- Detailed explanation of each code smell
- Downloadable markdown report for sharing with your team

## 🚀 Setup

### Prerequisites

- Python 3.6+
- pip (Python package installer)

Here's the markdown code for your installation instructions:

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/code-smell-detector.git
cd code-smell-detector
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally
Start the Streamlit server:
```bash
streamlit run app.py
```
The application will open in your default web browser at `http://localhost:8501`.

## 🔧 How to Use
1. **Upload Your Python File**:
   - Click the "Choose a Python file" button
   - Select any `.py` file from your computer

2. **Configure Detection Settings (in the sidebar)**:
   - Adjust the block size for duplicate detection
   - Set the maximum function length threshold
   - Configure the maximum parameter count

3. **Review Results**:
   - The tool displays detected issues categorized by type
   - Expand duplicate code blocks to see the actual duplicated code

4. **Download Report**:
   - Click "Generate Download Report" in the sidebar
   - Save the markdown file for future reference or team sharing

## 🔮 Upcoming Features
### Automatic Refactoring
I will be working on a new feature that will not only detect issues but also suggest or automatically implement refactoring solutions:
- Extract Method transformations for long functions
- Parameter Object creation for functions with too many parameters
- Extract Duplicate code into shared functions
- Preview Changes before applying them
- Apply Refactoring directly to your code with one click

Made with ❤️ by [Najmi Hassan]
