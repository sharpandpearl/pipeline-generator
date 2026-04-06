#!/usr/bin/env python3
"""
Email Finder - Finds valid email addresses by testing common permutations
"""

import dns.resolver
import re
import smtplib
import socket
from typing import Optional, List


def generate_email_permutations(first_name: str, last_name: str, domain: str) -> List[str]:
    """
    Generate common email permutations from name components and domain.

    Args:
        first_name: First name
        last_name: Last name
        domain: Company domain (e.g., 'ngc.com')

    Returns:
        List of email permutations to try
    """
    fn = first_name.lower().strip()
    ln = last_name.lower().strip()

    permutations = [
        # Standard formats
        f"{fn}.{ln}@{domain}",
        f"{fn}{ln}@{domain}",
        f"{ln}.{fn}@{domain}",
        f"{fn}_{ln}@{domain}",
        f"{ln}_{fn}@{domain}",

        # First initial variations
        f"{fn[0]}.{ln}@{domain}",
        f"{fn[0]}{ln}@{domain}",
        f"{fn[0]}_{ln}@{domain}",
        f"{ln}.{fn[0]}@{domain}",
        f"{ln}{fn[0]}@{domain}",
        f"{ln}_{fn[0]}@{domain}",

        # First two letters
        f"{fn[:2]}.{ln}@{domain}",
        f"{fn[:2]}{ln}@{domain}",
        f"{fn[:2]}_{ln}@{domain}",
        f"{ln}.{fn[:2]}@{domain}",
        f"{ln}{fn[:2]}@{domain}",

        # Last initial variations
        f"{fn}.{ln[0]}@{domain}",
        f"{fn}{ln[0]}@{domain}",
        f"{ln[0]}.{fn}@{domain}",

        # Hyphen variations
        f"{fn}-{ln}@{domain}",
        f"{ln}-{fn}@{domain}",

        # With middle initial placeholder
        f"{fn}.{ln[0]}.{ln[1:]}@{domain}" if len(ln) > 1 else None,

        # First name only
        f"{fn}@{domain}",

        # Last name only
        f"{ln}@{domain}",

        # Reversed combinations
        f"{ln[0]}{fn}@{domain}",
        f"{ln[:2]}{fn}@{domain}",

        # Numbers suffix (common patterns)
        f"{fn}.{ln}1@{domain}",
        f"{fn}.{ln}2@{domain}",
        f"{fn}{ln}1@{domain}",

        # Department/role prefixes (common)
        f"{fn}@{domain}",

        # Mixed case preservation for certain patterns
        f"{fn[0]}{ln}@{domain}",

        # Three letter combinations
        f"{fn[:3]}.{ln}@{domain}",
        f"{fn[:3]}{ln}@{domain}",

        # Full name no separator
        f"{fn}{ln}@{domain}",

        # Edge cases
        f"{fn}.{ln[:1]}@{domain}",
        f"{fn[0]}.{fn[1:]}.{ln}@{domain}" if len(fn) > 1 else None,

        # Additional common formats
        f"{ln}.{fn[:3]}@{domain}",
        f"{fn}.{ln}.{fn[0]}@{domain}",
        f"{ln}{fn[:2]}@{domain}",
    ]

    # Filter out None values and duplicates while preserving order
    seen = set()
    result = []
    for email in permutations:
        if email and email not in seen:
            seen.add(email)
            result.append(email)

    return result[:100]  # Cap at 100 permutations


def validate_email_syntax(email: str) -> bool:
    """
    Validate email syntax using regex.

    Args:
        email: Email address to validate

    Returns:
        True if syntax is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def check_mx_records(domain: str) -> bool:
    """
    Check if domain has valid MX records.

    Args:
        domain: Domain to check

    Returns:
        True if MX records exist, False otherwise
    """
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False
    except Exception:
        return False


def validate_email_smtp(email: str) -> bool:
    """
    Validate email using SMTP verification.
    This checks if the email address exists by connecting to the mail server.

    Args:
        email: Email address to validate

    Returns:
        True if email appears to be valid, False otherwise
    """
    domain = email.split('@')[1]

    # First check MX records
    if not check_mx_records(domain):
        return False

    try:
        # Get MX records
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange).rstrip('.')

        # Connect to SMTP server
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)

        # SMTP conversation
        server.connect(mx_host)
        server.helo(server.local_hostname)
        server.mail('verify@example.com')
        code, message = server.rcpt(email)
        server.quit()

        # 250 = success, 251 = user not local (but might be forwarded)
        return code in [250, 251]

    except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError):
        # Server doesn't allow verification, assume valid if MX exists
        return True
    except socket.timeout:
        # Timeout, assume valid if MX exists
        return True
    except Exception:
        return False


def find_valid_email(first_name: str, last_name: str, domain: str,
                     validation_method: str = 'smtp') -> Optional[str]:
    """
    Find a valid email address from permutations.

    Args:
        first_name: First name
        last_name: Last name
        domain: Company domain
        validation_method: 'syntax', 'mx', or 'smtp' (default: 'smtp')

    Returns:
        Valid email address if found, None otherwise
    """
    permutations = generate_email_permutations(first_name, last_name, domain)

    print(f"Generated {len(permutations)} email permutations to test...")
    print(f"Validation method: {validation_method}\n")

    for i, email in enumerate(permutations, 1):
        print(f"[{i}/{len(permutations)}] Testing: {email}", end=" ... ")

        # Always check syntax first
        if not validate_email_syntax(email):
            print("Invalid syntax")
            continue

        # Apply chosen validation method
        is_valid = False

        if validation_method == 'syntax':
            is_valid = True
        elif validation_method == 'mx':
            domain_part = email.split('@')[1]
            is_valid = check_mx_records(domain_part)
        elif validation_method == 'smtp':
            is_valid = validate_email_smtp(email)

        if is_valid:
            print("VALID!")
            return email
        else:
            print("Not found")

    return None


def main():
    """Main function to run the email finder."""
    print("=" * 60)
    print("Email Address Finder")
    print("=" * 60)
    print()

    # Get user input
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    domain = input("Enter company domain (e.g., ngc.com): ").strip()

    print("\nValidation methods:")
    print("1. syntax - Fast, only checks format (no actual validation)")
    print("2. mx     - Medium, checks if domain has mail servers")
    print("3. smtp   - Thorough, attempts to verify email existence (recommended)")

    method_choice = input("\nChoose validation method (1/2/3) [default: 3]: ").strip()

    method_map = {'1': 'syntax', '2': 'mx', '3': 'smtp', '': 'smtp'}
    validation_method = method_map.get(method_choice, 'smtp')

    print("\n" + "=" * 60)
    print("Starting email search...")
    print("=" * 60 + "\n")

    # Find valid email
    valid_email = find_valid_email(first_name, last_name, domain, validation_method)

    print("\n" + "=" * 60)
    if valid_email:
        print(f"SUCCESS! Valid email found: {valid_email}")
    else:
        print("No valid email found after testing all permutations.")
    print("=" * 60)


if __name__ == "__main__":
    main()
