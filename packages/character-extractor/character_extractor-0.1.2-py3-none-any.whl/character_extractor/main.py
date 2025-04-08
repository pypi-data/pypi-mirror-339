"""
Story Character Analyzer MCP Server

A simple MCP server that:
1. Takes an input file (PDF or TXT) containing a story
2. Identifies characters (people) in the story
3. Creates a JSON output with character details
4. Uses Claude Desktop's capabilities without external APIs
"""

import os
import json
import io
import sys
from mcp.server.fastmcp import FastMCP, Context

# For PDF handling
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Create server
mcp = FastMCP("Story Character Analyzer")

@mcp.tool()
def character_extractor(file_path: str) -> str:
    """
    Analyze a story file and identify characters (people) with their details.
    
    Args:
        file_path: Path to the story file (TXT or PDF)
    
    Returns:
        A JSON string containing character details
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return json.dumps({"error": f"File not found: {file_path}"})
    
    # Read the file content
    try:
        story_content = read_file_content(file_path)
    except Exception as e:
        return json.dumps({"error": f"Error reading file: {str(e)}"})
    
    # Create a prompt for Claude to identify characters
    claude_prompt = f"""
    I need to identify all the characters (people or personified entities) in the following story.
    
    For each character, please extract:
    1. Character Name: The character's name
    2. Age: The character's age (estimate if not explicitly stated)
    3. Essence: A brief description of their role or personality
    4. Appearance: A detailed physical description, including facial features or distinguishing traits
    5. Clothing: Description of their attire
    6. Gender: The character's gender
    7. Character Image prompt : Based on the extracted character details, considering all the detail create a prompt which will be used to generate image. 
    
    Format the output as a JSON object with this structure:
    {{
        "characters": [
            {{
                "Character Name": "Name",
                "Age": "Age",
                "Essence": "Brief description",
                "Appearance": "Physical description ["trait1", "trait2", ...]",
                "Clothing": "Attire",
                "Gender": "Gender",
                "Character Image Prompt":  "Character image prompt"
            }},
            ...
        ]
    }}
    
    Only include characters that are clearly mentioned in the story. Here's the story:
    
    {story_content}
    
    Respond with ONLY the JSON object and nothing else.
    """
    
    # Return the prompt - Claude Desktop will process this and identify the characters
    # We don't need to call an external API - Claude will do the character analysis
    return claude_prompt

def read_file_content(file_path: str) -> str:
    """Read content from a file, handling different file types."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Text file
    if file_ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    
    # PDF file
    elif file_ext == '.pdf':
        if PyPDF2 is None:
            raise ImportError("PyPDF2 is required for reading PDF files. Install with 'pip install PyPDF2'")
        
        text = []
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text.append(page.extract_text())
        return '\n'.join(text)
    
    # Unsupported file type
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def main():
    print("Server started", file=sys.stderr)
    mcp.run()

