"""Count failed logins by IP address in a fictional CSV login log."""

import argparse
import csv
from datetime import datetime
from ipaddress import ip_address


def analyse(path):
    failures = {}
    total = 0
    with open(path, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        required = {'timestamp', 'ip', 'status'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('CSV must contain timestamp, ip and status columns.')
        for line, row in enumerate(reader, start=2):
            try:
                datetime.fromisoformat(row['timestamp'])
                address = str(ip_address(row['ip'].strip()))
                status = row['status'].strip().lower()
                if status not in {'success', 'failure'}:
                    raise ValueError
            except (ValueError, TypeError, AttributeError):
                raise ValueError(f'Invalid login on CSV line {line}.') from None
            total += 1
            if status == 'failure':
                failures[address] = failures.get(address, 0) + 1
    return total, failures


def positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('Threshold must be at least 1.')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='CSV log to read')
    parser.add_argument('--threshold', type=positive_integer, default=3)
    args = parser.parse_args()
    try:
        total, failures = analyse(args.file)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Login events: {total}')
    print(f'Failed logins: {sum(failures.values())}')
    print(f'IPs with at least {args.threshold} failures across the whole file:')
    flagged = sorted(address for address in failures if failures[address] >= args.threshold)
    for address in flagged:
        print(f'{address}: {failures[address]} failures')
    if not flagged:
        print('None')


if __name__ == '__main__':
    main()
