# ICAI CA Scraper

A Python package to fetch CA member details from the ICAI (Institute of Chartered Accountants of India) website.

## Installation

```bash
pip install icai-ca-scraper
```

## Usage

### Basic Usage

```python
from icai_ca_scraper import CAScraper

# Initialize the scraper
scraper = CAScraper()

# Get details for a single CA member
member_details = scraper.get_member_details(100000)
if member_details:
    print(member_details)

# Get details for multiple CA members
member_numbers = [100001, 100002, 100003]
results = scraper.get_multiple_members(member_numbers)
print(results)
```

### Example with Custom Delay

```python
# Initialize with custom delay between requests (in seconds)
scraper = CAScraper(delay_between_requests=2.0)

# Get member details
details = scraper.get_member_details(100000)
```

### Save Results to JSON

```python
import json

# Get multiple member details
results = scraper.get_multiple_members([100001, 100002, 100003])

# Save to file
with open("ca_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
```

## Features

- Fetch CA member details by membership number
- Support for both single and multiple member lookups
- Built-in rate limiting to prevent server overload
- Clean and standardized data output
- Proper error handling
- SSL verification handling
- Session management

## Data Fields

The package retrieves the following information (when available):

- Name
- Gender
- Qualification
- Address
- COP Status (Certificate of Practice)
- Associate Year
- Fellow Year
- Membership Number
- Date of Birth
- Email
- Mobile
- Phone

## Example Response

```json
{
  "100000": {
    "name": "JOHN DOE",
    "gender": "M",
    "qualification": "B.Com",
    "address": "123 MAIN ST, CITY, STATE 123456",
    "cop_status": "FULL TIME",
    "associate_year": "A1995",
    "fellow_year": "F2013",
    "membership_no": "100000",
    "date_of_birth": "01-01-1970",
    "email": "john@example.com",
    "mobile": "9999999999",
    "last_updated": "2024-04-07 10:30:00"
  }
}
```

## Requirements

- Python 3.7+
- requests>=2.25.0
- beautifulsoup4>=4.9.0
- urllib3>=1.26.0

## License

This project is licensed under the MIT License - see the LICENSE file for details. 