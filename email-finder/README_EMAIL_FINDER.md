# Email Finder

A Python application that finds valid email addresses by testing common permutations of a person's name and company domain.

## Features

- Generates 40+ common email permutations from first name, last name, and domain
- Three validation methods:
  - **Syntax**: Fast format validation only
  - **MX Record**: Checks if domain has mail servers
  - **SMTP**: Attempts to verify email existence (most thorough)
- Stops at first valid email found
- Caps at 100 permutation attempts
- Progress tracking for each attempt

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the script and follow the prompts:

```bash
python email_finder.py
```

Example:
```
Enter first name: Aliyah
Enter last name: Wimbish
Enter company domain (e.g., ngc.com): ngc.com
Choose validation method (1/2/3) [default: 3]: 3
```

### Programmatic Usage

```python
from email_finder import find_valid_email

# Find valid email with SMTP validation (recommended)
email = find_valid_email("Aliyah", "Wimbish", "ngc.com", validation_method="smtp")

if email:
    print(f"Found: {email}")
else:
    print("No valid email found")
```

## Email Permutations Generated

The tool generates permutations including:

1. `firstname.lastname@domain`
2. `firstnamelastname@domain`
3. `lastname.firstname@domain`
4. `firstname_lastname@domain`
5. `f.lastname@domain` (first initial)
6. `flastname@domain`
7. `fi.lastname@domain` (first two letters)
8. `lastname.f@domain`
9. `lastnamef@domain`
10. `firstname-lastname@domain`
11. `firstname@domain`
12. `lastname@domain`
13. Plus many more variations...

## Validation Methods

### 1. Syntax Validation (Fast)
- Only checks if the email format is valid
- Doesn't verify if the email actually exists
- Use for quick testing or when you just need format validation

### 2. MX Record Validation (Medium)
- Checks if the domain has mail exchange (MX) records
- Verifies the domain can receive emails
- Faster than SMTP but less thorough

### 3. SMTP Validation (Thorough) - Recommended
- Connects to the mail server and attempts to verify the email
- Most accurate method
- Some servers may block or limit verification attempts
- Falls back to MX validation if SMTP verification is blocked

## Important Notes

- **Rate Limiting**: Some mail servers may rate-limit or block verification attempts. Use responsibly.
- **False Positives**: Some servers accept all emails during SMTP verification to prevent enumeration. The tool accounts for this where possible.
- **Privacy**: Email verification may be logged by mail servers. Only use for legitimate purposes.
- **Firewall**: SMTP validation requires outbound connections on port 25. Ensure your firewall allows this.

## Example Output

```
==============================================================
Email Address Finder
==============================================================

Enter first name: Aliyah
Enter last name: Wimbish
Enter company domain (e.g., ngc.com): ngc.com

Validation methods:
1. syntax - Fast, only checks format (no actual validation)
2. mx     - Medium, checks if domain has mail servers
3. smtp   - Thorough, attempts to verify email existence (recommended)

Choose validation method (1/2/3) [default: 3]: 3

==============================================================
Starting email search...
==============================================================

Generated 45 email permutations to test...
Validation method: smtp

[1/45] Testing: aliyah.wimbish@ngc.com ... VALID!

==============================================================
SUCCESS! Valid email found: aliyah.wimbish@ngc.com
==============================================================
```

## Troubleshooting

**Issue**: SMTP validation always fails
- Check if your network allows outbound connections on port 25
- Try using MX validation instead
- Some corporate networks block SMTP

**Issue**: All emails show as valid
- The mail server might be accepting all addresses during verification
- Try with a known invalid email to test
- Consider using MX validation instead

**Issue**: DNS resolution errors
- Check your internet connection
- Verify the domain is spelled correctly
- Some domains might not have MX records configured

## License

MIT License - Use at your own risk and responsibility.
