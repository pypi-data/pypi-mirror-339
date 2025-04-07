#!/usr/bin/env python3
"""
Documentation Synchronization Tool

This tool finds documentation files in the base directory and updates them
with content from a specified GitHub repository.
"""
import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional

from git import Repo

def find_docs(base_dir: str, extensions: List[str] = ['.md', '.mdx', '.rst']) -> List[Path]:
    """
    Find all documentation files in the base directory with the specified extensions.
    
    Args:
        base_dir: The base directory to search for docs
        extensions: File extensions to consider as documentation
        
    Returns:
        List of Path objects for documentation files
    """
    docs_files = []
    base_path = Path(base_dir)
    
    for ext in extensions:
        docs_files.extend(base_path.glob(f"**/*{ext}"))
    
    return docs_files


def clone_repo(repo_url: str, branch: Optional[str] = None) -> Path:
    """
    Clone the specified GitHub repository to a temporary directory.
    
    Args:
        repo_url: The URL of the GitHub repository
        branch: Optional branch/commit hash to checkout
        
    Returns:
        Path to the cloned repository
    """
    # If repo_url is a local path, just return it
    if os.path.exists(repo_url):
        return Path(repo_url)
    
    # Otherwise, clone the repository
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Clone the repository
        repo = Repo.clone_from(repo_url, temp_dir)
        
        # Checkout specific branch or commit if provided
        if branch:
            repo.git.checkout(branch)
        
        return Path(temp_dir)
    except Exception as e:
        # Clean up the temporary directory if cloning fails
        shutil.rmtree(temp_dir)
        raise e


def sync_docs(base_dir: str, repo_url: str, branch: Optional[str] = None, docs_subdir: str = "docs") -> int:
    """
    Sync documentation files from the repo to the base directory.
    
    Args:
        base_dir: The base directory containing local docs
        repo_url: URL or path to the repository
        branch: Optional branch or commit hash
        docs_subdir: Subdirectory in the repo containing docs
        
    Returns:
        Number of files updated
    """
    print(f"Finding docs in {base_dir}...")
    local_docs = find_docs(base_dir)
    print(f"Found {len(local_docs)} documentation files")
    
    print(f"Getting repository: {repo_url}...")
    repo_dir = clone_repo(repo_url, branch)
    is_temp = not os.path.exists(repo_url)  # Flag to determine if we need to clean up
    
    try:
        source_docs_dir = repo_dir / docs_subdir
        target_docs_dir = Path(base_dir) / "docs"
        
        # Skip if source and target are the same
        if os.path.abspath(source_docs_dir) == os.path.abspath(target_docs_dir):
            print("Source and target directories are the same. No sync needed.")
            return 0
            
        # Ensure target directory exists
        target_docs_dir.mkdir(exist_ok=True)
        
        print("Syncing documentation files...")
        # Copy all files from source to target
        updated_count = 0
        for src_file in source_docs_dir.glob("**/*"):
            if src_file.is_file():
                # Get relative path from source docs dir
                rel_path = src_file.relative_to(source_docs_dir)
                
                # Create target path
                dst_file = target_docs_dir / rel_path
                
                # Skip if source and destination are the same file
                if os.path.abspath(src_file) == os.path.abspath(dst_file):
                    print(f"Skipping: {dst_file} (same as source)")
                    continue
                
                # Ensure parent directories exist
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(src_file, dst_file)
                updated_count += 1
                print(f"Updated: {dst_file}")
        
        return updated_count
    finally:
        # Clean up the temporary directory if we created one
        if is_temp:
            shutil.rmtree(repo_dir) 