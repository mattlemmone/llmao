#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path
import math

def get_file_size(file_path):
    """Get file size in bytes"""
    return os.path.getsize(file_path)

def convert_size_to_bytes(size_str):
    """Convert human-readable size to bytes"""
    size_str = size_str.upper()
    units = {'B': 1, 'KB': 1024, 'MB': 1024*1024, 'GB': 1024*1024*1024}
    
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                size = float(size_str[:-len(unit)]) * multiplier
                return int(size)
            except ValueError:
                pass
    
    # If no unit specified, assume bytes
    try:
        return int(float(size_str))
    except ValueError:
        raise ValueError(f"Invalid size format: {size_str}")

def human_readable_size(size_in_bytes):
    """Convert bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024 or unit == 'GB':
            return f"{size_in_bytes:.2f}{unit}"
        size_in_bytes /= 1024

def split_file(input_file, batch_size, output_dir=None, output_prefix=None):
    """
    Split a large text file into multiple files of approximately batch_size,
    ensuring splits occur at paragraph boundaries (line breaks).
    """
    input_path = Path(input_file)
    
    # Setup output directory and prefix
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
    if output_prefix is None:
        output_prefix = input_path.stem
    
    # Get input file size
    total_size = get_file_size(input_path)
    
    # Calculate number of parts
    num_parts = math.ceil(total_size / batch_size)
    print(f"Input file: {input_path} ({human_readable_size(total_size)})")
    print(f"Target batch size: {human_readable_size(batch_size)}")
    print(f"Splitting into approximately {num_parts} parts...")
    
    # Read file in binary mode to avoid encoding issues when seeking
    with open(input_path, 'rb') as infile:
        content = infile.read()
    
    # Decode the content (try UTF-8 first, fallback to latin-1)
    try:
        text_content = content.decode('utf-8')
    except UnicodeDecodeError:
        text_content = content.decode('latin-1')
        print("Note: File decoded using latin-1 encoding (UTF-8 failed)")
    
    # Split content into paragraphs (defined by line breaks)
    paragraphs = text_content.split('\n\n')
    
    # Initialize variables for splitting
    current_part = 1
    current_size = 0
    current_content = []
    output_files = []
    
    # Process each paragraph
    for paragraph in paragraphs:
        # Add a double newline if this isn't the first paragraph in the current batch
        if current_content:
            paragraph_with_break = '\n\n' + paragraph
            paragraph_size = len(paragraph_with_break.encode('utf-8'))
        else:
            paragraph_size = len(paragraph.encode('utf-8'))
        
        # If adding this paragraph would exceed batch size and we already have content,
        # write the current batch and start a new one
        if current_content and current_size + paragraph_size > batch_size:
            # Create output file name with padding for proper sorting
            output_file = output_dir / f"{output_prefix}_part{current_part:03d}.txt"
            
            # Write the content
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write('\n\n'.join(current_content))
            
            output_files.append((output_file, current_size))
            print(f"Created: {output_file} ({human_readable_size(current_size)})")
            
            # Start new batch
            current_part += 1
            current_size = paragraph_size
            current_content = [paragraph]
        else:
            # Add paragraph to current batch
            if current_content:
                current_size += paragraph_size
                current_content.append(paragraph)
            else:
                current_size = paragraph_size
                current_content = [paragraph]
    
    # Write the last batch if there's anything left
    if current_content:
        output_file = output_dir / f"{output_prefix}_part{current_part:03d}.txt"
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('\n\n'.join(current_content))
        
        output_files.append((output_file, current_size))
        print(f"Created: {output_file} ({human_readable_size(current_size)})")
    
    return output_files

def main():
    parser = argparse.ArgumentParser(description='Split a large text file into multiple files at paragraph boundaries.')
    parser.add_argument('input_file', help='Input text file to split')
    parser.add_argument('batch_size', help='Target size for each output file (e.g., "10MB", "500KB")')
    parser.add_argument('-o', '--output-dir', help='Output directory (default: same as input file)')
    parser.add_argument('-p', '--prefix', help='Prefix for output files (default: input filename without extension)')
    
    args = parser.parse_args()
    
    # Convert batch size to bytes
    try:
        batch_size_bytes = convert_size_to_bytes(args.batch_size)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    # Split the file
    split_file(args.input_file, batch_size_bytes, args.output_dir, args.prefix)
    return 0

if __name__ == "__main__":
    sys.exit(main())