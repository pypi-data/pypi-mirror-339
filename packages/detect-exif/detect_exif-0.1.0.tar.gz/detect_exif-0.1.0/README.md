# detect-exif

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python tool that detects and optionally removes sensitive EXIF metadata from
image files. Works as both a standalone command-line utility and a pre-commit
hook to prevent accidentally committing images with private data.

## Why detect-exif?

Images often contain hidden metadata like:

- GPS coordinates of where a photo was taken
- Camera make, model, and serial number
- Date and time information
- Software/firmware details
- Copyright information
- Names, comments, and other personally identifiable data

This tool helps protect your privacy by:

1. Detecting sensitive EXIF data in your images
1. Highlighting specifically concerning information (GPS data, device details)
1. Optionally removing all metadata while preserving the image itself

## Features

- Detects various types of sensitive EXIF data in JPG, PNG, and WebP images
- Special checking for GPS coordinates with human-readable output
- Preserves image orientation when removing EXIF data
- Works as a pre-commit hook to detect images with sensitive metadata before
  commit
- Optional automatic removal of EXIF data (both in CLI and pre-commit hook)
- Integrated with pre-commit hook ecosystem

## Installation

```bash
pip install detect-exif
```

## Usage

### As a Command-Line Tool

Check images for EXIF data (standard output):

```bash
detect-exif path/to/image.jpg path/to/another.jpg
```

Remove EXIF data:

```bash
detect-exif --remove path/to/image.jpg path/to/another.jpg
```

For quieter output (useful in scripts and pre-commit hooks):

```bash
detect-exif --quiet path/to/image.jpg
```

For detailed output with full information:

```bash
detect-exif --verbose path/to/image.jpg
```

### As a Pre-Commit Hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/olipinski/detect-exif
    rev: v0.1.0  # Use the latest version
    hooks:
      - id: detect-exif
        # By default, the hook only detects EXIF data with minimal output
        # To enable automatic removal, add:
        # args: [--remove]
        # For detailed output, add:
        # args: [--verbose]
        # For both removal and detailed output:
        # args: [--remove, --verbose]
```

## License

MIT License - See LICENSE file for details
