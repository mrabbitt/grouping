#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
import re


SAME_EMAIL = 'same_email'
SAME_PHONE = 'same_phone'
SAME_EMAIL_OR_PHONE = 'same_email_or_phone'


def normalize_email(email):
    return email.lower() if email != '' else None


def normalize_phone(phone_number):
    # Strip all non-digit characters
    normalized_phone = re.sub(r'\D+', '', phone_number)

    if normalized_phone == '':
        return None

    if len(normalized_phone) == 10:
        # Assume US phone number without country prefix "1"
        normalized_phone = ('1' + normalized_phone)

    return normalized_phone


class PersonGrouper(object):
    def __init__(self, matching_type, input_path, output_stream=sys.stdout):
        self.matching_type = matching_type
        self.input_path = input_path
        self.output_stream = output_stream

        self.email_column_indices = []
        self.phone_column_indices = []
        self.ids_by_key = {}
        self.next_id = 1

    def process_file(self):
        with open(self.input_path, 'rU') as csvfile:
            # Parse input file header
            header_line = next(csvfile)
            self.parse_headers(header_line)

            # Write headers to output.
            print("UniqueID,%s" % header_line, file=self.output_stream, end='')

            # Process each line in file.
            for line in csvfile:
                self.process_line(line)

    def parse_headers(self, header_line):
        # Parse column headers
        headers = header_line.strip().split(',')
        for i in xrange(0, len(headers)):
            if self.matching_type == SAME_EMAIL or self.matching_type == SAME_EMAIL_OR_PHONE:
                if headers[i].lower().startswith('email'):
                    self.email_column_indices.append(i)
            if self.matching_type == SAME_PHONE or self.matching_type == SAME_EMAIL_OR_PHONE:
                if headers[i].lower().startswith('phone'):
                    self.phone_column_indices.append(i)

    def process_line(self, line):
        '''Process a single line from a CSV input file.'''
        fields = line.strip().split(',')
        unique_id = None

        # Search for a matching phone
        for i in self.phone_column_indices:
            key = normalize_phone(fields[i])
            if key is not None and key in self.ids_by_key:
                unique_id = self.ids_by_key[key]
                break

        # Search for a matching email if match not already found
        if unique_id is None:
            for i in self.email_column_indices:
                key = normalize_email(fields[i])
                if key is not None and key in self.ids_by_key:
                    unique_id = self.ids_by_key[key]
                    break

        # Assign a new unique ID if no matches found
        if unique_id is None:
            unique_id = self.next_id
            self.next_id += 1

        # Set unique ID for all normalized keys
        for i in self.phone_column_indices:
            key = normalize_phone(fields[i])
            if key is not None:
                self.ids_by_key[key] = unique_id
        for i in self.email_column_indices:
            key = normalize_email(fields[i])
            if key is not None:
                self.ids_by_key[key] = unique_id

        print('%i,%s' % (unique_id, line), file=self.output_stream, end='')


def parse_args(raw_args):
    parser = argparse.ArgumentParser(description='MightyHive Programing Exercise - Grouping')
    parser.add_argument('matching_type', help='matching type to identify same people',
                        choices=(SAME_EMAIL, SAME_PHONE, SAME_EMAIL_OR_PHONE))
    parser.add_argument('input_file', help='path to input file in CSV format')

    return parser.parse_args(raw_args)


def main(raw_args):
    args = parse_args(raw_args)

    grouper = PersonGrouper(args.matching_type, args.input_file)
    grouper.process_file()


if __name__ == '__main__':
    main(sys.argv[1:])
