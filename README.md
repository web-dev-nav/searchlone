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

    
## How to Use
Run the script:

To start the search tool, run the following command in your terminal:

   ```bash
   python searchlone.py

# Follow the interactive prompts:

The tool will guide you through the search process with interactive prompts:

Enter the project path: Specify the path to the project directory where you want to search.
Specify the search term: Enter the keyword or pattern you want to search for.
Optionally modify search settings:
Skip folders: Choose directories to exclude from the search (e.g., vendor, node_modules).
File extensions: Define which file types to search (e.g., .php, .blade.php, .html).
Search Execution:

The tool will search through the files and display matches with context.
The search results will include line numbers for easy reference.
You can monitor the search progress through a progress bar, especially useful for larger projects.
View Results:

The results will be displayed in the terminal, showing the file name, the pattern found, and the context (lines surrounding the match).
JSON Output: After the search is complete, detailed results will be saved in a JSON file in your directory for further analysis.
Example output:

```txt
Copy code
? resources/views/welcome.blade.php
Pattern: blade_var
Line: 15
13: <div class="container">
14: <h1>Welcome</h1>
15: {{ $searchTerm }}
16: </div>

----------------------------------------
Default Configuration
The tool comes with sensible defaults for web development projects:

Skip Folders: vendor, node_modules, storage, bootstrap/cache, .git, public/build
Supported Extensions: .php, .blade.php, .html
