#!/usr/bin/env python3
"""
Test script for Hunter.io fallback validation
"""

import os
from email_finder import find_valid_email

print("=" * 60)
print("Testing Email Finder with Hunter.io Fallback")
print("=" * 60)
print()
print("This test will:")
print("1. Try SMTP validation first (likely to fail for saronic.com)")
print("2. Fall back to Hunter.io if SMTP finds nothing")
print()

# Check for API key
api_key = os.getenv('HUNTER_API_KEY')
if not api_key:
    print("⚠️  WARNING: HUNTER_API_KEY environment variable not set!")
    print("   Set it with: export HUNTER_API_KEY='your_api_key_here'")
    print("   Or pass it as a parameter to find_valid_email()")
    print()
    api_key_input = input("Enter your Hunter.io API key now (or press Enter to skip): ").strip()
    if api_key_input:
        api_key = api_key_input
    else:
        print("\n⚠️  Skipping test - no API key provided")
        exit(0)

print("Input:")
print("  First name: Anuj")
print("  Last name: Patel")
print("  Domain: saronic.com")
print("  Validation: SMTP → Hunter.io fallback")
print()
print("=" * 60)
print("Starting search...")
print("=" * 60)
print()

# Run the email finder with Hunter.io fallback
valid_email = find_valid_email(
    "Anuj",
    "Patel",
    "saronic.com",
    validation_method="smtp",
    hunter_api_key=api_key,
    use_hunter_fallback=True
)

print()
print("=" * 60)
if valid_email:
    print(f"✓ SUCCESS! Valid email found: {valid_email}")
else:
    print("✗ No valid email found after testing all permutations.")
print("=" * 60)
