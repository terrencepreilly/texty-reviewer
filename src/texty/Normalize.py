"""
Utility for normalizing a file to using tabs instead of spaces.
"""

import argparse

def normalize(filename):
    """Convert spaces to tabs"""
    lines = []
    try:
        fin = open(filename, 'r')
        lines = [a.split() for a in fin.readlines()]
        fin.close()
    except FileNotFoundError:
        print('Could not find file.')

    if len(lines) > 0:
        try:
            fout = open(filename, 'w')
            for line in lines:
                fout.write('\t'.join([a.strip() for a in line]) + '\n')
            fout.close()
        except FileNotFoundError:
            print('Could not find file.')

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Normalize File Spacing')

    PARSER.add_argument('-f', nargs='?', help="""The filename for the file
        to be normalized""")

    ARGS = PARSER.parse_args()

    if ARGS.f:
        normalize(ARGS.f)
