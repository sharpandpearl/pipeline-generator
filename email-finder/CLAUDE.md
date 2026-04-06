# Email Finder Project

## Project Overview

This is a Python application that discovers valid email addresses by testing common permutations of a person's name and company domain. The tool generates up to 100 email variations and validates them using DNS MX records and SMTP verification.

**Primary Use Case**: Finding professional email addresses when you know someone's name and company domain.

## Project Structure

```
pipeline-generator/
└── email-finder/
    ├── email_finder.py           # Main application (core logic)
    ├── test_email_finder.py      # Test script with example usage
    ├── show_permutations.py      # Utility to preview permutations
    ├── requirements.txt          # Python dependencies
    ├── README_EMAIL_FINDER.md    # User-facing documentation
    └── CLAUDE.md                 # This file - project documentation for Claude Code
```

## Core Components

### email_finder.py

**Key Functions**:
- `generate_email_permutations()` - Creates 34+ unique email patterns from name/domain
- `validate_email_syntax()` - Regex-based format validation
- `check_mx_records()` - DNS validation for mail exchange records
- `validate_email_smtp()` - SMTP-based email existence verification
- `find_valid_email()` - Main orchestration function (stops at first valid email)

**Validation Methods**:
1. **Syntax**: Fast format-only validation
2. **MX**: Checks if domain can receive mail
3. **SMTP**: Attempts to verify email existence (default, most thorough)

## Development Guidelines

### Adding New Permutations

When adding email permutations to `generate_email_permutations()`:
- Add to the `permutations` list in order of likelihood
- More common patterns should appear first
- Remember the 100 permutation cap (currently generates ~34)
- Ensure no duplicates (the function deduplicates automatically)
- Test with various name lengths (short names, long names, single letter)

Example permutation patterns already implemented:
- firstname.lastname@domain
- f.lastname@domain (first initial)
- fi.lastname@domain (first two letters)
- lastname.f@domain
- firstname_lastname@domain
- And 30+ more variations

### Code Conventions

- **Error Handling**: Network operations (DNS, SMTP) should gracefully handle timeouts and connection errors
- **Timeouts**: SMTP connections timeout at 10 seconds to prevent hanging
- **Logging**: Use print statements for user feedback during iterations
- **Return Values**: Functions return `None` when validation fails, specific values on success
- **Type Hints**: Use typing annotations for function signatures

### Testing

**Manual Testing**:
```bash
cd email-finder
python3 test_email_finder.py  # Run with example data
python3 show_permutations.py  # Preview permutations without validation
```

**Interactive Testing**:
```bash
cd email-finder
python3 email_finder.py  # Run in interactive mode
```

**Programmatic Testing**:
```python
from email_finder import find_valid_email
email = find_valid_email("FirstName", "LastName", "domain.com", "smtp")
```

### Performance Considerations

- **SMTP validation is slow**: Each SMTP check can take 1-10 seconds
- **Network failures**: DNS/SMTP failures should timeout gracefully
- **Rate limiting**: Some mail servers may rate-limit or block verification attempts
- **False positives**: Some servers accept all addresses during SMTP handshake to prevent enumeration

### Security & Ethics

**IMPORTANT**: This tool should only be used for:
- ✅ Legitimate business contact discovery
- ✅ Reconnecting with professional contacts
- ✅ Research with proper authorization
- ✅ Educational purposes

**DO NOT use for**:
- ❌ Spam or unsolicited marketing
- ❌ Harassment or stalking
- ❌ Unauthorized enumeration attacks
- ❌ Bypassing privacy controls

**Privacy Considerations**:
- Email verification attempts may be logged by mail servers
- SMTP verification can be considered reconnaissance in security contexts
- Some organizations may have policies against email enumeration
- Always ensure you have legitimate purpose and authorization

### Network Requirements

- **Outbound Port 25**: Required for SMTP validation
- **DNS Resolution**: Required for all validation methods except syntax-only
- **Firewall**: Corporate firewalls may block port 25 (use MX validation instead)
- **VPN/Proxy**: May interfere with SMTP connections

## Dependencies

- **dnspython** (>=2.3.0): DNS resolution for MX record lookups
- **smtplib**: Built-in Python library for SMTP
- **socket**: Built-in Python library for network connections
- **re**: Built-in Python library for regex validation

## Common Issues & Solutions

### Issue: SMTP validation always fails
**Solution**: 
- Check firewall allows outbound port 25
- Try MX validation instead (`validation_method='mx'`)
- Some networks block SMTP entirely

### Issue: All emails appear valid
**Solution**:
- Server may accept all addresses to prevent enumeration
- Test with known-invalid email to verify
- Fall back to MX validation for better accuracy

### Issue: DNS resolution errors
**Solution**:
- Verify internet connection
- Check domain spelling
- Some domains lack MX records

### Issue: Timeouts or slow performance
**Solution**:
- SMTP validation is inherently slow (10s per check)
- Use MX validation for faster results
- Consider syntax validation for format-only checks

## Future Enhancements

Potential improvements to consider:
- [ ] Async/parallel validation to speed up SMTP checks
- [ ] Machine learning to predict most likely permutations
- [ ] Company-specific pattern detection (e.g., tech companies often use first.last)
- [ ] Caching of MX records to avoid repeated DNS lookups
- [ ] Export results to CSV/JSON
- [ ] Batch processing for multiple names
- [ ] Integration with LinkedIn/company directory APIs
- [ ] Custom permutation templates per company

## Examples

### Basic Usage
```python
from email_finder import find_valid_email

# SMTP validation (thorough)
email = find_valid_email("Aliyah", "Wimbish", "ngc.com")
# Output: aliyah.wimbish@ngc.com

# MX validation (faster)
email = find_valid_email("John", "Doe", "example.com", "mx")

# Syntax only (instant)
email = find_valid_email("Jane", "Smith", "company.com", "syntax")
```

### Viewing Permutations
```python
from email_finder import generate_email_permutations

perms = generate_email_permutations("Aliyah", "Wimbish", "ngc.com")
for p in perms:
    print(p)
# Output: aliyah.wimbish@ngc.com, awimbish@ngc.com, ...
```

## Contributing Guidelines

When modifying this project:
1. Test with multiple validation methods (syntax, mx, smtp)
2. Test with edge cases (single letter names, hyphens, apostrophes)
3. Verify permutation order (common patterns first)
4. Ensure error handling for network failures
5. Update README_EMAIL_FINDER.md if adding features
6. Keep ethical use guidelines in mind

## Support

For issues or questions:
- Check [README_EMAIL_FINDER.md](README_EMAIL_FINDER.md) for troubleshooting
- Review permutations with `show_permutations.py`
- Test validation methods with `test_email_finder.py`
