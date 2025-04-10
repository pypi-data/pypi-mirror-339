# Tela Client

A Python client library for interacting with the Tela API.

## Installation

```bash
pip install tela-client
```

## Overview

Tela Client provides a simple interface for processing documents (particularly PDFs) using Tela's "canvas" workflows. Key features include:

- Easy integration with Tela API
- Execute predefined workflows (canvases) with various inputs
- File upload to Tela's vault storage
- Batch processing for multiple files
- Flexible output formats (JSON or Pandas DataFrame)
- Local response caching for improved performance
- Lifecycle hooks for customizing execution flow
- Folder monitoring for automatic processing
- Utility functions for PDF handling

## Basic Usage

```python
from tela_client import TelaClient, file

# Initialize the client
api_key = "your-tela-api-key"
client = TelaClient(api_key)

# Create a canvas instance
canvas_id = "your-canvas-id"
canvas = client.new_canvas(canvas_id, expected_input=['document'])

# Process a file
result = canvas.run(document=file("./example.pdf"))

# Access results
print(result)
```

## Batch Processing

```python
# Prepare multiple inputs
inputs = [
    {'document': file("./doc1.pdf")},
    {'document': file("./doc2.pdf")},
    {'document': file("./doc3.pdf")}
]

# Process all files
results = canvas.run_batch(inputs)
```

## Using Hooks

```python
from tela_client import TelaClient, file, hooks

# Define custom hooks
def on_before_run(input_data):
    print(f"Processing file: {input_data['document'].filename}")
    return input_data

def on_success(result):
    print(f"Successfully processed with score: {result.get('score')}")
    return result

# Apply hooks to canvas
canvas = client.new_canvas("your-canvas-id", expected_input=['document'])
canvas.add_hook(hooks.BEFORE_RUN, on_before_run)
canvas.add_hook(hooks.ON_SUCCESS, on_success)

# Run with hooks
result = canvas.run(document=file("./example.pdf"))
```

## Folder Monitoring

```python
from tela_client import TelaClient, folder_watcher

client = TelaClient("your-api-key")
canvas = client.new_canvas("your-canvas-id", expected_input=['document'])

# Watch a folder and process new files automatically
watcher = folder_watcher.watch(
    "/path/to/watch",
    canvas=canvas,
    input_key="document",
    file_pattern="*.pdf"
)

# Start monitoring (blocking call)
watcher.start()
```

## License

[License information]

## Documentation

For more detailed information, refer to the full documentation.