import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
import fnmatch
import logging
from concurrent.futures import ThreadPoolExecutor
import mimetypes
from tqdm import tqdm
import xml.dom.minidom
import xml.etree.ElementTree as ET

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_directory_structure_xml(
    path: Path,
    parent_element: ET.Element,
    ignore_patterns: Optional[List[str]] = None
) -> None:
    """
    Generate XML elements for the directory structure.
    
    Args:
        path: Path object to generate structure from
        parent_element: Parent XML element to attach to
        ignore_patterns: List of patterns to ignore (supports fnmatch wildcards)
    """
    if ignore_patterns is None:
        ignore_patterns = [
            ".git", "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.swp",
            ".DS_Store", "*.log", ".venv", "venv",
            "node_modules", "vendor"
        ]

    # Check if this directory matches ignore patterns
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path.name, pattern):
            skipped = ET.SubElement(parent_element, "skipped")
            return

    try:
        contents = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for item in contents:
            if any(fnmatch.fnmatch(item.name, pattern) for pattern in ignore_patterns):
                if item.is_dir():
                    dir_element = ET.SubElement(parent_element, "directory")
                    dir_element.set("path", str(item.name))
                    skipped = ET.SubElement(dir_element, "skipped")
                continue

            if item.is_dir():
                dir_element = ET.SubElement(parent_element, "directory")
                dir_element.set("path", str(item.name))
                generate_directory_structure_xml(item, dir_element, ignore_patterns)
            else:
                file_element = ET.SubElement(parent_element, "file")
                file_element.set("path", str(item.name))

    except PermissionError:
        logger.warning(f"Permission denied accessing directory: {path}")
        error = ET.SubElement(parent_element, "error")
        error.text = f"Permission denied for {path}"


def generate_tree(
    path: Path,
    prefix: str = "",
    ignore_patterns: Optional[List[str]] = None
) -> str:
    """
    Generate a tree-like structure of the directory.
    
    Args:
        path: Path object to generate tree from
        prefix: Prefix for tree formatting
        ignore_patterns: List of patterns to ignore (supports fnmatch wildcards)
    
    Returns:
        A string representing the directory tree structure
    """
    if ignore_patterns is None:
        ignore_patterns = [
            ".git", "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.swp",
            ".DS_Store", "*.log", ".venv", "venv",
            "node_modules", "vendor"
        ]

    # Check if this directory matches ignore patterns
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path.name, pattern):
            return prefix + path.name + " [...]"

    output = []
    try:
        contents = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        for i, item in enumerate(contents):
            is_last = i == len(contents) - 1
            connector = "└── " if is_last else "├── "
            new_prefix = prefix + ("    " if is_last else "│   ")

            if any(fnmatch.fnmatch(item.name, pattern) for pattern in ignore_patterns):
                if item.is_dir():
                    output.append(prefix + connector + item.name + " [...]")
                continue

            output.append(prefix + connector + item.name)
            if item.is_dir():
                subtree = generate_tree(item, new_prefix, ignore_patterns)
                if subtree:
                    output.append(subtree)

    except PermissionError:
        logger.warning(f"Permission denied accessing directory: {path}")
        return prefix + f"[Error: Permission denied for {path}]"

    return "\n".join(output)

def _process_file(file_path: Path, root_path: Path, ignore_patterns: List[str]) -> Optional[Dict[str, Any]]:
    """
    Helper function to process a single file's content with path relative to root.
    
    Args:
        file_path: Path to the file
        root_path: Root directory for relative paths
        ignore_patterns: Patterns to ignore
    
    Returns:
        Dictionary with file path and content or None if skipped
    """
    rel_path = file_path.relative_to(root_path)

    if any(fnmatch.fnmatch(file_path.name, pattern) for pattern in ignore_patterns):
        return None

    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and "text" not in mime_type:
            return None

        with open(file_path, 'rb') as test_file:
            chunk = test_file.read(8192)
            if b'\0' in chunk:
                return None

        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        return {
            "path": str(rel_path),
            "content": content
        }
                
    except UnicodeDecodeError:
        logger.warning(f"Skipped non-UTF-8 file: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error processing {file_path}: {str(e)}")
        return None

def process_directories(
    directories: List[str],
    root_directory: str,
    output_file: str = "output.txt",
    ignore_patterns: Optional[List[str]] = None,
    force_overwrite: bool = False,
    show_progress: bool = False,
    output_format: str = "text"
) -> None:
    """
    Process all files in multiple directories and their subdirectories.
    
    Args:
        directories: List of directories to process files from
        root_directory: The root directory for generating tree structure and relative paths
        output_file: The output file path
        ignore_patterns: List of patterns to ignore (supports fnmatch wildcards)
        force_overwrite: Whether to overwrite existing output file
        show_progress: Whether to show a progress bar
        output_format: Output format ('text' or 'xml')
    """
    if ignore_patterns is None:
        ignore_patterns = [
            ".git", "__pycache__", "*.pyc", "*.pyo", "*.pyd",
            ".DS_Store", "*.log", ".venv", "venv",
            "node_modules", "vendor"
        ]

    output_path = Path(output_file)
    if output_path.exists() and not force_overwrite:
        raise FileExistsError(
            f"Output file '{output_file}' already exists. "
            "Use -f/--force to overwrite existing file."
        )

    root_path = Path(root_directory).resolve()
    
    # For XML output
    if output_format.lower() == "xml":
        project = ET.Element("project")
        project_name = ET.SubElement(project, "name")
        project_name.text = root_path.name
        
        # Generate structure
        structure = ET.SubElement(project, "structure")
        generate_directory_structure_xml(root_path, structure, ignore_patterns)
        
        # Contents section
        contents = ET.SubElement(project, "contents")
        
        # Collect all files from specified directories
        all_files = []
        for directory in directories:
            base_path = Path(directory).resolve()
            if not base_path.exists() or not base_path.is_dir():
                logger.warning(f"Skipping invalid directory: {directory}")
                continue
            for root, dirs, files in os.walk(base_path):
                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)]
                for file in files:
                    file_path = Path(root) / file
                    if not any(fnmatch.fnmatch(file, p) for p in ignore_patterns):
                        all_files.append(file_path)

        # Process files in parallel
        with ThreadPoolExecutor() as executor:
            file_contents = list(executor.map(
                lambda f: _process_file(f, root_path, ignore_patterns),
                tqdm(all_files, desc="Processing files", unit="file") if show_progress else all_files
            ))
        
        # Add file contents to XML
        for file_info in file_contents:
            if file_info:
                file_element = ET.SubElement(contents, "file")
                file_element.set("path", file_info["path"])
                content_element = ET.SubElement(file_element, "content")
                content_element.text = file_info["content"]
        
        # Write XML to file
        xml_str = ET.tostring(project, encoding='unicode')
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(pretty_xml)
        
    else:  # Text output (original format)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Write directory tree structure
            outfile.write("Project Directory Structure:\n")
            outfile.write("==========================\n\n")
            outfile.write(root_path.name + "\n")
            tree_structure = generate_tree(root_path, ignore_patterns=ignore_patterns)
            outfile.write(tree_structure)
            outfile.write("\n\n")
            
            # Write file contents section header
            outfile.write("File Contents from Selected Directories:\n")
            outfile.write("===================================\n\n")
            
            # Collect all files from specified directories
            all_files = []
            for directory in directories:
                base_path = Path(directory).resolve()
                if not base_path.exists() or not base_path.is_dir():
                    logger.warning(f"Skipping invalid directory: {directory}")
                    continue
                for root, dirs, files in os.walk(base_path):
                    dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)]
                    for file in files:
                        file_path = Path(root) / file
                        if not any(fnmatch.fnmatch(file, p) for p in ignore_patterns):
                            all_files.append(file_path)

            # Process files in parallel
            with ThreadPoolExecutor() as executor:
                file_infos = list(executor.map(
                    lambda f: _process_file(f, root_path, ignore_patterns),
                    all_files
                ))

            # Write contents with optional progress bar
            if show_progress:
                for file_info in tqdm(file_infos, desc="Writing files", unit="file"):
                    if file_info:
                        outfile.write(f"\n====\nFile: {file_info['path']}\n----\n\n{file_info['content']}\n")
            else:
                for file_info in file_infos:
                    if file_info:
                        outfile.write(f"\n====\nFile: {file_info['path']}\n----\n\n{file_info['content']}\n")

if __name__ == "__main__":
    process_directories(
        directories=["tests"],
        root_directory=".",
        output_file="output_test.xml",
        force_overwrite=True,
        show_progress=True,
        output_format="xml"  # 更改為 "xml" 來產生 XML 輸出
    )
