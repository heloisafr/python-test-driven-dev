# Python Test Driven Development Sample

## Requirements
- python 3.12
- fastapi
- pytest

## Files
Tests sending files through HTTP requisition:
  - file/required: One file parameter - required
  - file/optional: One file parameter - not required
  - file/multiple-file-parameter: Two file parameters. One required and other optional.
  - file/multiple/required: One parameter for multiple files - required
  - file/multiple/optional: One parameter for multiple files - not required
  - file/mix/optional: 3 parameter, 1 string, 1 file, 1 list of file. None of them are required
  - file/mix/required: 3 parameter, 1 string, 1 file, 1 list of file. All are required
