#!/usr/bin/python3
import sys
import csv
from datetime import datetime

def get_commands():
    """validate user commands, if command is valid, open csv file"""
    if len(sys.argv) != 4 or sys.argv[2] != '-d' or not validate_date_format(sys.argv[3]):
        print(f"The valid format is {sys.argv[0]} <csv_file_name.csv> -d yyyy-mm-dd")
        exit(1)
    
    csv_file, input_date = sys.argv[1], sys.argv[3]
    open_file(csv_file, input_date)


def validate_date_format(date: str) -> bool:
    """validate input date, return boolean"""
    try:
        return bool(datetime.strptime(date, '%Y-%m-%d'))
    except ValueError:
        raise ValueError("Incorrect date format, valid format should be YYYY-MM-DD")


def open_file(csv_file: str, input_date: str) -> None:
    """open csv file and create cookie frequency table"""
    cookies_frequency = {}
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as cookie_log_csv_file:
            csv_reader = csv.reader(cookie_log_csv_file)
            for row in csv_reader:
                if not row[0]: # filter empty row
                    continue
                cookie, timestamp = row[0], row[1]
                if timestamp[:10] == input_date[:10] and validate_date_format(timestamp[:10]):
                    cookies_frequency[cookie] = cookies_frequency.get(cookie, 0) + 1
    except FileNotFoundError:
        print(f"Error: CSV file {csv_file} not found.")
        exit(1)
    except IOError:
        print(f"Error: IO error occurred trying to open CSV file {csv_file}")
        exit(1)
    except Exception as err:
        print(f"Unexpected error happens when we open CSV file {csv_file}, it is {err}")
        exit(1)

    if cookies_frequency:
        print_most_active_cookie(cookies_frequency)
    else:
        print("There is no active cookie in the given date")


def print_most_active_cookie(cookies_frequency: dict) -> None:
    """
    print most active cookie if only one cookie is most active
    print multuple active cookies if multuple cookies meet the criteria
    """
    max_frequency = max(cookies_frequency.values())
    most_active_cookie_cnt = 1
    most_active_cookie = []

    for frequency in cookies_frequency.values():
        if max_frequency == frequency:
            most_active_cookie_cnt += 1
    
    if most_active_cookie_cnt > 1:
        for cookie, frequency in cookies_frequency.items():
            if frequency == max_frequency:
                most_active_cookie.append(cookie)

        for cookie in most_active_cookie:
            print(cookie)

    if most_active_cookie_cnt == 1:
        for cookie, frequency in cookies_frequency.items():
            if frequency == max_frequency:
                print(cookie)
    

if __name__ == '__main__':
    get_commands()
