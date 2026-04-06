#!/usr/bin/env python3
"""
Batch Email Finder - Process multiple leads from CSV
"""

import csv
import os
import sys
from typing import List, Dict
from email_finder import find_valid_email, validate_email_hunter


def process_leads_batch(
    input_csv: str,
    output_csv: str,
    hunter_api_key: str = None,
    use_hunter_fallback: bool = True,
    validation_method: str = 'smtp'
):
    """
    Process a batch of leads from CSV and find their email addresses.

    Args:
        input_csv: Path to input CSV with columns: first_name, last_name, title, company, domain
        output_csv: Path to output CSV with results
        hunter_api_key: Hunter.io API key (optional, uses env var if not provided)
        use_hunter_fallback: Whether to use Hunter.io fallback
        validation_method: Initial validation method ('smtp', 'mx', 'syntax')
    """
    # Read leads from CSV
    leads = []
    try:
        with open(input_csv, 'r') as f:
            reader = csv.DictReader(f)
            leads = list(reader)
    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_csv}")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    if not leads:
        print("❌ No leads found in CSV")
        return

    print("=" * 70)
    print(f"Batch Email Finder - Processing {len(leads)} leads")
    print("=" * 70)
    print(f"Input: {input_csv}")
    print(f"Output: {output_csv}")
    print(f"Validation: {validation_method}" + (" → Hunter.io fallback" if use_hunter_fallback else ""))
    print("=" * 70)
    print()

    # Process each lead
    results = []
    success_count = 0
    failed_count = 0

    for i, lead in enumerate(leads, 1):
        first_name = lead.get('first_name', '').strip()
        last_name = lead.get('last_name', '').strip()
        title = lead.get('title', '').strip()
        company = lead.get('company', '').strip()
        domain = lead.get('domain', '').strip()

        print(f"\n[{i}/{len(leads)}] {first_name} {last_name} - {company}")
        print("-" * 70)

        # Skip if missing required fields
        if not first_name or not last_name or not domain or domain == 'unknown.com':
            print("⚠️  Skipped: Missing required information (name or domain)")
            results.append({
                'first_name': first_name,
                'last_name': last_name,
                'title': title,
                'company': company,
                'domain': domain,
                'email': '',
                'status': 'SKIPPED',
                'method': 'N/A',
                'notes': 'Missing required fields'
            })
            failed_count += 1
            continue

        # Find email
        email = find_valid_email(
            first_name,
            last_name,
            domain,
            validation_method=validation_method,
            hunter_api_key=hunter_api_key,
            use_hunter_fallback=use_hunter_fallback
        )

        if email:
            print(f"\n✅ SUCCESS: {email}")
            results.append({
                'first_name': first_name,
                'last_name': last_name,
                'title': title,
                'company': company,
                'domain': domain,
                'email': email,
                'status': 'FOUND',
                'method': validation_method + (' + Hunter.io' if use_hunter_fallback else ''),
                'notes': ''
            })
            success_count += 1
        else:
            print(f"\n❌ FAILED: No valid email found")
            results.append({
                'first_name': first_name,
                'last_name': last_name,
                'title': title,
                'company': company,
                'domain': domain,
                'email': '',
                'status': 'NOT_FOUND',
                'method': validation_method,
                'notes': 'No valid email found after all attempts'
            })
            failed_count += 1

    # Write results to output CSV
    print("\n" + "=" * 70)
    print("Writing results to CSV...")
    print("=" * 70)

    try:
        with open(output_csv, 'w', newline='') as f:
            fieldnames = ['first_name', 'last_name', 'title', 'company', 'domain', 'email', 'status', 'method', 'notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"✅ Results written to: {output_csv}")
    except Exception as e:
        print(f"❌ Error writing results: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total leads processed: {len(leads)}")
    print(f"✅ Emails found: {success_count}")
    print(f"❌ Failed/Skipped: {failed_count}")
    print(f"Success rate: {(success_count / len(leads) * 100):.1f}%")
    print("=" * 70)


def main():
    """Main function for batch processing."""
    import argparse

    parser = argparse.ArgumentParser(description='Batch Email Finder - Find emails for multiple leads')
    parser.add_argument('input_csv', help='Input CSV file with leads')
    parser.add_argument('-o', '--output', default='results.csv', help='Output CSV file (default: results.csv)')
    parser.add_argument('-k', '--api-key', help='Hunter.io API key (or set HUNTER_API_KEY env var)')
    parser.add_argument('--no-hunter', action='store_true', help='Disable Hunter.io fallback')
    parser.add_argument('-m', '--method', choices=['smtp', 'mx', 'syntax'], default='smtp',
                        help='Initial validation method (default: smtp)')

    args = parser.parse_args()

    # Get API key from args or environment
    api_key = args.api_key or os.getenv('HUNTER_API_KEY')

    if not args.no_hunter and not api_key:
        print("⚠️  WARNING: No Hunter.io API key provided. Hunter.io fallback will be disabled.")
        print("   Set HUNTER_API_KEY environment variable or use --api-key argument")
        print()

    # Process leads
    process_leads_batch(
        input_csv=args.input_csv,
        output_csv=args.output,
        hunter_api_key=api_key,
        use_hunter_fallback=not args.no_hunter,
        validation_method=args.method
    )


if __name__ == "__main__":
    main()
