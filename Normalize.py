import argparse

def normalize(filename):
    """Convert spaces to tabs"""
    lines = []
    try:
        fin = open(filename, 'r')
        lines = [a.split() for a in fin.readlines()]
        fin.close()
    except:
        print('Problem reading file.')

    if len(lines) > 0:
        try:
            fout = open(filename, 'w')
            for line in lines:
                fout.write('\t'.join([a.strip() for a in line]) + '\n')
            fout.close()
        except:
            print('Problem writing file.')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Normalize File Spacing')

    parser.add_argument('-f', nargs='?', help="""The filename for the file 
        to be normalized""")

    args = parser.parse_args()

    if args.f:
        normalize(args.f)
