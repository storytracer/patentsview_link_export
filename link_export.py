#!/usr/bin/env python3
"""
PatentsView Download Link Generator

This script reads a sources.yml configuration file for PatentsView data and
generates a link list suitable for downloading the patent data files using
any download tool.
"""

import yaml
import os
import argparse
from typing import List, Dict, Any


def generate_download_urls(config: Dict[str, Any]) -> List[str]:
    """
    Generate all download URLs from the configuration.
    
    Parses the configuration dictionary to extract database URLs, URL templates,
    and table names, then generates the complete download URLs for each table.
    Skips the 'minimal' dataset type to avoid duplicate URLs, as these tables
    are already included in the 'downloads' dataset type.
    
    Args:
        config: Dictionary containing the patent data configuration
        
    Returns:
        List of fully formed download URLs
    """
    urls = []
    
    # Process both granted and pre-grant patent sections from the config
    for section_key in ['granted', 'pre-grant']:
        if section_key not in config:
            continue
            
        section = config[section_key]
        
        # Process each dataset type (downloads, brief_summary, etc.)
        for dataset_type, dataset_config in section.items():
            # Skip the 'minimal' dataset type as it's included in 'downloads'
            if dataset_type == 'minimal':
                continue
                
            # Extract the necessary components to build the URLs
            database = dataset_config.get('database', '')  # Base URL for the dataset
            url_template = dataset_config.get('url_template', '')  # Template with placeholders
            tables = dataset_config.get('tables', [])  # List of tables or years
            
            # Skip this dataset if any required field is missing
            if not database or not url_template or not tables:
                continue
                
            # Generate URLs for each table by substituting values into the template
            for table in tables:
                # Format the URL by replacing placeholders with actual values
                url = url_template.format(database=database, table=table)
                urls.append(url)
    
    return urls


def save_urls_to_file(urls: List[str], output_file: str) -> None:
    """
    Save URLs to a file, one URL per line.
    
    Args:
        urls: List of URLs to save
        output_file: Path to the output file
    """
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(f"{url}\n")


def main():
    """
    Main function that parses arguments, reads the configuration file,
    generates download URLs, and saves them to the output file.
    
    Returns:
        0 on success, 1 on error
    """
    parser = argparse.ArgumentParser(description='Generate download links for PatentsView data.')
    parser.add_argument('-s', '--sources', default='data/sources.yml',
                        help='Path to the sources.yml')
    parser.add_argument('-o', '--output', default='data/links.txt',
                        help='Output file for the URLs (default: data/links.txt)')
    args = parser.parse_args()
    
    # Validate that the configuration file exists before attempting to read it
    if not os.path.isfile(args.sources):
        print(f"Error: Config file '{args.sources}' not found.")
        return 1
    
    # Load and parse the YAML configuration file
    with open(args.sources, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return 1
    
    # Generate download URLs
    urls = generate_download_urls(config)
    
    # Save URLs to file
    save_urls_to_file(urls, args.output)
    
    print(f"Generated {len(urls)} download URLs in '{args.output}'")
    
    return 0


if __name__ == "__main__":
    exit(main())
