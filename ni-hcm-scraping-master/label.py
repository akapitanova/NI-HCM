#!/usr/bin/env python3

import csv
import os
import sys

class bold_color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    start = None
    if len(sys.argv) == 2:
        start = int(sys.argv[1])

    with open('./data/houbelec.csv', 'r', encoding='utf8') as input_file,\
         open('./data/labeled.csv', 'a', encoding='utf8') as output_file:
        reader = csv.reader(input_file, delimiter=',')

        cnt = 0
        for title, first_par, _pos, _neg in reader:
            cnt += 1

            if start and cnt < start:
                continue

            clear()

            print(f'#{cnt}')
            print(f'{bold_color.BOLD}{title}{bold_color.END}')
            print(first_par)

            print()

            pos = None
            while pos not in (1, 2, 3, 4):
                pos = int(input('Positive sentiment [1,2,3,4]: '))

            print()

            neg = None
            while neg not in (1, 2, 3, 4):
                neg = int(input('Negative sentiment [1,2,3,4]: '))


            output_file.write(f'{title};{first_par};{pos};{neg}\n')
            output_file.flush()

if __name__ == '__main__':
    main()
