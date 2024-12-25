import os
import re
from pathlib import Path
import json
import time
from tqdm import tqdm

# Folders to skip during search
SKIP_FOLDERS = {
    'vendor',
    'node_modules',
    'storage',
    'bootstrap/cache',
    '.git',
    'public/build'
}

# File extensions to search in
VALID_EXTENSIONS = {'.php', '.blade.php', '.html'}

def get_search_config():
    """Get search configuration from user input."""
    print("\n=== Search Configuration ===")
    
    # Get search term
    search_term = input("Enter the character or word to search for: ").strip()
    
    # Show current skip folders and allow modification
    print(f"\nCurrent folders to skip: {', '.join(SKIP_FOLDERS)}")
    modify_skip = input("Would you like to modify skip folders? (y/n): ").lower()
    
    if modify_skip == 'y':
        print("Enter folder names to skip (one per line, press Enter twice when done):")
        new_skip_folders = set()
        while True:
            folder = input().strip()
            if not folder:
                break
            new_skip_folders.add(folder)
        if new_skip_folders:
            SKIP_FOLDERS.update(new_skip_folders)
    
    # Show current file extensions and allow modification
    print(f"\nCurrent file extensions to search: {', '.join(VALID_EXTENSIONS)}")
    modify_ext = input("Would you like to modify file extensions? (y/n): ").lower()
    
    if modify_ext == 'y':
        print("Enter file extensions (including dot, one per line, press Enter twice when done):")
        new_extensions = set()
        while True:
            ext = input().strip()
            if not ext:
                break
            if not ext.startswith('.'):
                ext = '.' + ext
            new_extensions.add(ext)
        if new_extensions:
            VALID_EXTENSIONS.update(new_extensions)
    
    return search_term

def count_searchable_files(base_path):
    """Count total number of files to be searched."""
    count = 0
    for path in Path(base_path).rglob('*'):
        # Skip specified folders
        if any(skip_folder in str(path) for skip_folder in SKIP_FOLDERS):
            continue
        if path.is_file() and path.suffix in VALID_EXTENSIONS:
            count += 1
    return count

def create_search_patterns(search_term):
    """Create various search patterns based on the search term."""
    return {
        'standalone': fr'\b{re.escape(search_term)}\b',  # Word boundary
        'html_tag': fr'>{re.escape(search_term)}<',  # Between HTML tags
        'blade_var': fr'{{[\s]*{re.escape(search_term)}[\s]*}}',  # Blade syntax
        'echo_statement': fr'echo[\s]*[\'\"]{re.escape(search_term)}[\'\"]',  # PHP echo
        'attribute': fr'=[\s]*[\'\"][^\'\"]*{re.escape(search_term)}[^\'\"]*[\'\"]',  # HTML attributes
        'variable': fr'\${re.escape(search_term)}\b',  # PHP variable
        'print_statement': fr'print[\s]*[\'\"]{re.escape(search_term)}[\'\"]',  # PHP print
        'debug_statement': fr'dd\([\'\"]{re.escape(search_term)}[\'\"]',  # Laravel debug
        'raw_output': fr'!![\s]*{re.escape(search_term)}[\s]*!!'  # Blade raw output
    }

def search_files(base_path, search_patterns):
    """Search through files for specific patterns."""
    results = {}
    
    def get_line_context(lines, line_num, context=2):
        start = max(0, line_num - context)
        end = min(len(lines), line_num + context + 1)
        return lines[start:end]
    
    def check_file_content(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.splitlines()
                
                for pattern_name, pattern in search_patterns.items():
                    matches = re.finditer(pattern, content)
                    
                    for match in matches:
                        line_num = content.count('\n', 0, match.start())
                        context_lines = get_line_context(lines, line_num)
                        
                        if file_path not in results:
                            results[str(file_path)] = []
                            
                        results[str(file_path)].append({
                            'pattern': pattern_name,
                            'line_number': line_num + 1,
                            'context': context_lines,
                            'match': match.group()
                        })
        except UnicodeDecodeError:
            pass
        except Exception as e:
            print(f"\nError processing {file_path}: {str(e)}")
    
    total_files = count_searchable_files(base_path)
    print(f"\nFound {total_files} files to search.")
    
    with tqdm(total=total_files, desc="Searching files", unit="file") as pbar:
        for path in Path(base_path).rglob('*'):
            if any(skip_folder in str(path) for skip_folder in SKIP_FOLDERS):
                continue
            if path.is_file() and path.suffix in VALID_EXTENSIONS:
                check_file_content(path)
                pbar.update(1)
    
    return results

def main():
    print("=== Dynamic File Content Searcher ===")
    
    # Get project path
    project_path = input("Enter the project path: ").strip()
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist.")
        return
    
    # Get search configuration
    search_term = get_search_config()
    
    # Create search patterns
    patterns = create_search_patterns(search_term)
    
    # Start search
    print(f"\nStarting search for '{search_term}'...")
    start_time = time.time()
    
    results = search_files(project_path, patterns)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Output results
    if not results:
        print(f"\nNo occurrences found. Search completed in {elapsed_time:.2f} seconds.")
        return
    
    print(f"\nSearch completed in {elapsed_time:.2f} seconds.")
    print("\nMatches found:\n")
    
    for file_path, findings in sorted(results.items()):
        relative_path = os.path.relpath(file_path, project_path)
        print(f"\n📁 {relative_path}")
        
        for finding in findings:
            print(f"\n  Pattern: {finding['pattern']}")
            print(f"  Line: {finding['line_number']}")
            print("  Context:")
            for i, line in enumerate(finding['context']):
                line_num = finding['line_number'] - len(finding['context'])//2 + i
                print(f"    {line_num}: {line.strip()}")
            print("  " + "-"*40)
    
    # Save results to file
    output_file = f"search_results_{search_term}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to {output_file}")

if __name__ == "__main__":
    main()