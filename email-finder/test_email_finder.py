#!/usr/bin/env python3
"""
Test script for email finder
"""

from email_finder import find_valid_email

# Test with the example data
print("=" * 60)
print("Testing Email Finder")
print("=" * 60)
print()
print("Input:")
print("  First name: Aliyah")
print("  Last name: Wimbish")
print("  Domain: ngc.com")
print()
print("=" * 60)
print("Starting search with SMTP validation...")
print("=" * 60)
print()

# Run the email finder
valid_email = find_valid_email("Aliyah", "Wimbish", "ngc.com", validation_method="smtp")

print()
print("=" * 60)
if valid_email:
    print(f"✓ SUCCESS! Valid email found: {valid_email}")
else:
    print("✗ No valid email found after testing all permutations.")
print("=" * 60)
