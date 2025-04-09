# zimvalidator

A Python package for validating Zimbabwean phone numbers.

## Features

- Validates Zimbabwean mobile numbers from:
  - Econet
  - NetOne
  - Telecel
  - Africom
  - TelOne VoIP

## Usage

```python
from zimvalidator.phone import PhoneNumberValidator

validator = PhoneNumberValidator()
result = validator.validate("0771234567")
print(result)
