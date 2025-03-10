#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path

def concat_files(input_dir, output_file, delimiter):
    """
    Concatenate all text files in input_dir into output_file,
    with delimiter and filename annotations between files.
    """
    # Get list of all .txt files in the directory
    input_path = Path(input_dir)
    text_files = list(input_path.glob('*.txt'))
    
    # If no text files found, check for any file (without extension filtering)
    if not text_files:
        text_files = [f for f in input_path.iterdir() if f.is_file()]
    
    if not text_files:
        print(f"No files found in {input_dir}")
        return
    
    # Open output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Process each file
        for i, file_path in enumerate(text_files):
            # Add delimiter before file content (except for first file)
            if i > 0:
                outfile.write(f"\n{delimiter} File: {file_path.name} {delimiter}\n\n")
            else:
                outfile.write(f"{delimiter} File: {file_path.name} {delimiter}\n\n")
            
            # Read and write the file content
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except UnicodeDecodeError:
                # Try with a different encoding if UTF-8 fails
                try:
                    with open(file_path, 'r', encoding='latin-1') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"\nError reading file {file_path.name}: {str(e)}\n")
            except Exception as e:
                outfile.write(f"\nError reading file {file_path.name}: {str(e)}\n")
    
    print(f"Successfully concatenated {len(text_files)} files into {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Concatenate all text files in a directory.')
    parser.add_argument('input_dir', help='Input directory containing text files')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('-d', '--delimiter', default='===', help='Delimiter string (default: ===)')
    
    args = parser.parse_args()
    
    concat_files(args.input_dir, args.output_file, args.delimiter)

if __name__ == "__main__":
    main()