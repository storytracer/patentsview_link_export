# PatentsView Link Export

A utility script that generates download links for PatentsView patent data based on the sources.yml configuration file.

## Overview

This tool reads a structured YAML configuration file containing information about PatentsView data sources and generates a list of download URLs. These URLs can then be used with any download tool to retrieve the patent data files.

### Source Information

The sources.yml file included in this repository:
- Was last updated in December 2024
- Originally comes from [PatentsView/PatentsView-Code-Examples](https://github.com/PatentsView/PatentsView-Code-Examples/blob/main/data-downloads/sources.yml)
- Is preserved here because the original PatentsView.org contract is being terminated and the original repository is scheduled for deletion
- A fork of the original repository is maintained at [storytracer/PatentsView-Code-Examples](https://github.com/storytracer/PatentsView-Code-Examples)

## Download Options

After generating the URLs, you can use various download tools to retrieve the files:

### Using wget

```
wget -i data/links.txt -x -c -t 3 -P downloads
```

Options:
- `-i data/links.txt`: Input file containing URLs
- `-x`: Preserve directory structure
- `-c`: Continue interrupted downloads
- `-t 3`: Number of retries on failed downloads
- `-P downloads`: Save files to the downloads directory

### Using aria2c (Recommended for Parallel Downloads)

```
aria2c -i data/links.txt -c -j 8 -x 8 -d downloads
```

Options:
- `-i data/links.txt`: Input file containing URLs
- `-c`: Continue interrupted downloads
- `-j 8`: Number of parallel downloads
- `-x 8`: Maximum connections per download
- `-d downloads`: Directory to store downloaded files

## Requirements

- Python 3.6+
- PyYAML package

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/storytracer/patentsview_link_export.git
   cd patentsview_link_export
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with default options:

```
python link_export.py
```

This will:
1. Read the configuration from `data/sources.yml`
2. Generate download URLs for all configured datasets
3. Save the URLs to `data/links.txt`

### Command-line Options

- `-s, --sources`: Path to the sources YAML file (default: `data/sources.yml`)
- `-o, --output`: Path to the output file for URLs (default: `data/links.txt`)

Example with custom paths:

```
python link_export.py --sources my_config.yml --output my_links.txt
```

## Configuration File

The `sources.yml` file contains structured information about the PatentsView data sources. It is organized into sections:

- `granted`: Contains data for granted patents
- `pre-grant`: Contains data for pre-grant publications

Each section contains dataset types (minimal, downloads, brief_summary, etc.) with the following properties:

- `database`: Base URL for the dataset
- `url_template`: Template for constructing download URLs
- `tables`: List of tables or years to generate URLs for

See the included `data/sources.yml` for a complete example.

Note: The script skips the 'minimal' dataset type to avoid duplicate URLs, as these tables are already included in the 'downloads' dataset type.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
