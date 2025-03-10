# llmao
A collection of random tools that I often use when working with LLMs.

## Tools

1. **`concat_files.py`** - Concatenate multiple text files into a single file

- Useful when feeding nonsense to NotebookLM

2. **`split_file.py`** - Split a large text file into multiple smaller files at paragraph boundaries

- NotebookLM has an implicit file size limit. Splitting one 35mb text file into many 35 1mb files worked.

## Usage

### Concatenate Files

Combine all text files from a directory into a single file:

```bash
./concat_files.py /path/to/input/directory output.txt
```

Options:

- `-d, --delimiter TEXT` - Set the delimiter string (default: `===`)

Example output:

```
=== File: document1.txt ===

Content of document1...

=== File: document2.txt ===

Content of document2...
```

### Split File

Split a large text file into multiple smaller files of approximately equal size:

```bash
./split_file.py large_document.txt 10MB
```

This will create files like:

- `large_document_part001.txt`
- `large_document_part002.txt`
- etc.

Options:

- `-o, --output-dir DIRECTORY` - Output directory (default: same as input file)
- `-p, --prefix TEXT` - Prefix for output files (default: input filename without extension)

The script splits files at paragraph boundaries (double line breaks) to ensure content isn't cut off mid-paragraph.


## License

MIT

