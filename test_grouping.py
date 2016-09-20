#!/usr/bin/env python
import grouping
import os.path
from cStringIO import StringIO

# `pip install pytest` to install.
import pytest


TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')


@pytest.mark.parametrize('test_input,expected', [
    ('(555) 123-4567', '15551234567'),
    ('555-123-4567', '15551234567'),
    ('555.123.4567', '15551234567'),
    ('5551234567', '15551234567'),
    ('15551234567', '15551234567'),
    ('', None),
    ('no digits', None),
])
def test_normalize_phone(test_input, expected):
    assert grouping.normalize_phone(test_input) == expected


@pytest.mark.parametrize('test_input,expected', [
    ('john.smith@domain.com', 'john.smith@domain.com'),
    ('JOHN.SMITH@DOMAIN.COM', 'john.smith@domain.com'),
    ('John.Smith@Domain.com', 'john.smith@domain.com'),
    ('', None),
])
def test_normalize_email(test_input, expected):
    assert grouping.normalize_email(test_input) == expected


@pytest.mark.parametrize('header_line,matching_type,expected_phone_indices,expected_email_indices', [
    ('FirstName,LastName,Phone,Email,Zip', 'same_email', [], [3]),
    ('FirstName,LastName,Phone,Email,Zip', 'same_phone', [2], []),
    ('FirstName,LastName,Phone,Email,Zip', 'same_email_or_phone', [2], [3]),
    ('FirstName,LastName,Phone1,Phone2,Email1,Email2,Zip', 'same_email', [], [4, 5]),
    ('FirstName,LastName,Phone1,Phone2,Email1,Email2,Zip', 'same_phone', [2, 3], []),
    ('FirstName,LastName,Phone1,Phone2,Email1,Email2,Zip', 'same_email_or_phone', [2, 3], [4, 5]),
])
def test_person_grouper_parse_headers(header_line, matching_type, expected_phone_indices,
                                      expected_email_indices):
    grouper = grouping.PersonGrouper(matching_type, None)
    grouper.parse_headers(header_line)
    assert grouper.email_column_indices == expected_email_indices and \
           grouper.phone_column_indices == expected_phone_indices


@pytest.mark.parametrize('matching_type,input_file,expected_output_file', [
    ('same_email', 'input1.csv', 'output1-same_email.csv'),
    ('same_phone', 'input1.csv', 'output1-same_phone.csv'),
    ('same_email_or_phone', 'input1.csv', 'output1-same_email_or_phone.csv'),
    ('same_email', 'input2.csv', 'output2-same_email.csv'),
    ('same_phone', 'input2.csv', 'output2-same_phone.csv'),
    # ('same_email_or_phone', 'input2.csv', 'output2-same_email_or_phone.csv'),
])
def test_end_to_end(matching_type, input_file, expected_output_file):
    output = StringIO()
    input_path = os.path.join(TEST_DATA_DIR, input_file)
    expected_output_path = os.path.join(TEST_DATA_DIR, expected_output_file)
    with open(expected_output_path, 'rU') as expected_output_stream:
        expected_output = expected_output_stream.read()

    grouper = grouping.PersonGrouper(matching_type, input_path, output_stream=output)
    grouper.process_file()

    assert output.getvalue() == expected_output

if __name__ == '__main__':
    pytest.main([__file__])
