import argparse
from pathlib import Path
from .core import process_directories

def main():
    """
    Main entry point for the command line interface
    """
    parser = argparse.ArgumentParser(
        description="Bundle code files from multiple directories into a single file for AI analysis, including directory structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with one directory
  promptpack-for-code /path/to/code
  
  # Multiple directories
  promptpack-for-code dir1 dir2 dir3
  
  # Specify custom output file
  promptpack-for-code /path/to/code -o result.txt
  
  # Specify root directory for tree structure
  promptpack-for-code /path/to/src -r /path/to/project/root
  
  # Ignore specific patterns
  promptpack-for-code /path/to/code --ignore "*.log" "*.tmp"
  
  # Show progress bar
  promptpack-for-code /path/to/code --progress
  
  # Generate XML output instead of text
  promptpack-for-code /path/to/code --format xml
"""
    )
    parser.add_argument(
        "directories",
        type=str,
        nargs="+",  # 接受多個目錄
        help="Directories containing the code files to process"
    )
    parser.add_argument(
        "-r", "--root",
        type=str,
        help="Root directory for generating tree structure (defaults to current directory if not specified)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output.xml",
        help="Output file path (default: output.xml)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force overwrite output file without asking"
    )
    parser.add_argument(
        "--ignore",
        type=str,
        nargs="+",
        help="Patterns to ignore for both tree and content (e.g., *.txt *.md)",
        default=[".git", "__pycache__", "*.pyc", "*.pyo", "*.pyd", ".DS_Store", "*.log", ".venv", "venv", "node_modules", "vendor", "*.swp", "*.egg-info"]
    )
    parser.add_argument(
        "--ignore-extensions",
        type=str,
        nargs="+",
        help="File extensions to ignore content only (e.g., jpg png gif)",
        default=[]
    )
    parser.add_argument(
        "--ignore-keywords",
        type=str,
        nargs="+",
        help="Keywords in filename to ignore content only (e.g., test backup temp)",
        default=[]
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar while processing files"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "xml"],
        default="xml",
        help="Output format (xml or text, default: xml)"
    )

    args = parser.parse_args()

    # Validate directories
    for directory in args.directories:
        if not Path(directory).is_dir():
            print(f"Error: {directory} is not a valid directory")
            return 1

    try:
        root_dir = args.root if args.root else "."
        if not Path(root_dir).is_dir():
            print(f"Error: {root_dir} is not a valid directory")
            return 1

        output_path = Path(args.output)
        
        # 自動調整檔案名稱與輸出格式一致
        output_filename = str(output_path)
        if args.format.lower() == "xml" and not output_filename.lower().endswith(".xml"):
            if "." in output_path.name:
                print(f"Warning: XML output format selected but output file has non-XML extension. Using {output_path}")
            else:
                output_path = Path(output_filename + ".xml")
                print(f"XML output format selected, using filename: {output_path}")
        elif args.format.lower() == "text" and not output_filename.lower().endswith(".txt"):
            if "." in output_path.name:
                print(f"Warning: Text output format selected but output file has non-TXT extension. Using {output_path}")
            else:
                output_path = Path(output_filename + ".txt")
                print(f"Text output format selected, using filename: {output_path}")
                
        # 如果使用預設檔名但使用不同格式，則切換檔名
        if args.output == "output.xml" and args.format.lower() == "text":
            output_path = Path("output.txt")
            print(f"Text output format selected with default filename, using: {output_path}")
        elif args.output == "output.txt" and args.format.lower() == "xml":
            output_path = Path("output.xml")
            print(f"XML output format selected with default filename, using: {output_path}")
            
        if output_path.parent != Path('.'):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
        process_directories(
            directories=args.directories,
            root_directory=root_dir,
            output_file=str(output_path),
            ignore_patterns=args.ignore,
            force_overwrite=args.force,
            show_progress=args.progress,
            output_format=args.format
        )
        print(f"Successfully created {output_path}")
        return 0
    except FileExistsError as e:
        print(f"Error: {str(e)}")
        print("Options:")
        print("  1. Use a different output path: -o new_output.txt")
        print("  2. Use -f/--force to overwrite existing file")
        print("  3. Remove the existing file manually")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
