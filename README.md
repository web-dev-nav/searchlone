# searchlone

**Dynamic File Content Searcher** is a command-line tool that helps developers search through their project files for specific content patterns. What sets it apart is its ability to recognize various programming patterns, particularly in PHP, Laravel, and HTML files. The tool provides context-aware searching with features specifically designed for web development projects.

## Key Features

- **Smart Pattern Recognition**: Automatically searches for different variations of your search term, including:
  - Standalone words
  - Content between HTML tags
  - Blade template variables
  - PHP echo statements
  - HTML attributes
  - PHP variables
  - Debug statements
  - And more!

- **Configurable Search Parameters**:
  - Customize which folders to skip
  - Define which file extensions to search
  - Easy-to-modify search settings

- **Developer-Friendly Output**:
  - Shows context around each match
  - Displays line numbers
  - Saves results in JSON format
  - Progress bar for large projects

## Installation and Setup

1. Install Python if you haven't already.

2. Install the required package:

   ```bash
   pip install tqdm
