#!/usr/bin/env python3
"""
Show all permutations that would be generated
"""

from email_finder import generate_email_permutations

permutations = generate_email_permutations("Aliyah", "Wimbish", "ngc.com")

print("All email permutations that will be tested (in order):")
print("=" * 60)
for i, email in enumerate(permutations, 1):
    print(f"{i:2d}. {email}")
print("=" * 60)
print(f"Total: {len(permutations)} permutations")
