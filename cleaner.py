import re

def load_setting(filename):
    ptn = re.compile("(\d+)\s+(\d+)\s+(\d+)")
    settings = []
    dups = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            m = ptn.match(line)
            if m:
                #print(line)
                ID  = int(m.group(1))
                reg = int(m.group(2))
                val = int(m.group(3))

                #print(ID, reg, val)
                if ID not in dups:
                    dups[ID] = {}

                dup = dups[ID]

                dup[reg] = i

                settings.append((ID, reg, val, lines[i].rstrip()))
            else:
                settings.append((-1, -1, -1, lines[i].rstrip()))

    return settings, dups

def clean_settings(settings, dups, output):
    for i in range(len(settings)):
        line = settings[i]
        ID  = line[0]
        reg = line[1]
        if ID < 0:
            print(line[3], file=output)
            continue

        if i < dups[ID][reg]:
            print(';'+line[3], file=output)
        else:
            print(line[3], file=output)

def print_info(settings, dups):
    reginfo = {}
    for i in range(len(settings)):
        line = settings[i]
        ID  = line[0]
        reg = line[1]
        val = line[2]
        if ID < 0:
            continue

        if reg not in reginfo:
            reginfo[reg] = []

        reginfo[reg].append((line[2], i))

    for reg in reginfo:
        print("Register %d:" % reg)
        for i in reginfo[reg]:
            print("\t @line%4d: %d" % (i[1], i[0]))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-input",   help='input settings')
    parser.add_argument("-show",    help='show', action='store_true', default=False)
    parser.add_argument("-clean",   help='clean to output')
    args = parser.parse_args()
    settings, dups = load_setting(args.input)

    if args.show:
        print_info(settings, dups)

    if args.clean:
        with open(args.clean, 'w') as output:
            clean_settings(settings, dups, output)
