[![build status](https://travis-ci.org/mrabbitt/grouping.svg?branch=master)](https://travis-ci.org/mrabbitt/grouping/)

## Instructions

### Prerequisites
* Make sure Python v2.7.x is installed.
* No third party libraries are required to run the solution in `grouping.py`.
* *(optional)* To run the tests in `test_grouping.py`, [pytest](http://pytest.org) must be installed.

### Running
* For usage, run:  `python grouping.py -h`
* To match records by email:  `python grouping same_email /path/to/input.csv`
* To match records by phone number:  `python grouping same_phones /path/to/input.csv`
* To match records by phone number or email:  `python grouping same_email_or_phone /path/to/input.csv`
* Output is written to standard output.

## Assumptions
* The unique identifier is an integer assigned by the application code.
* All input files are in CSV format, without quotes or escapes.
* Columns whose name starts with "email" (case insensitive) are expected to contain email addresses.
* Columns whose name starts with "phone" (case insensitive) are expected to contain phone addresses.
* Phone numbers are considered if a match if they have the same digits (discarding punctuation) after adding an explicit "1" prefix for 10-digit phone numbers.
* Email addresses are matched case-insensitively.
* An empty phone or email field is not considered a match with other fields.
