#!/usr/bin/env python3
"""
Test script for CSV batch email finding
"""

from email_finder import process_csv_file

def main():
    """
    Example of using CSV batch processing.
    """
    print("=" * 80)
    print("CSV Batch Email Finder - Test Script")
    print("=" * 80)
    print()

    # Example 1: Basic CSV processing with MX validation (faster for testing)
    print("Example 1: Processing sample_input.csv with MX validation")
    print("-" * 80)

    results = process_csv_file(
        csv_path="sample_input.csv",
        validation_method="mx",  # Use MX for faster testing
        output_path="test_results_mx.csv"
    )

    print("\n" + "=" * 80)
    print("Test complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
