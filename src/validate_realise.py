import os
import re
import argparse

parser = argparse.ArgumentParser(description='Generate new data file with the highest ITO')
parser.add_argument('-f', '--files', nargs="+", help='path of file')
parser.add_argument('-d', '--directory', help="path of direcory")
parser.add_argument('-o', '--output', help='path of new data file', required=True)

args = parser.parse_args()
if args.files is None and args.directory is None:
    parser.error("-[-f]iles or -[-d]irectory option is mandatory")
elif args.files and args.directory:
    parser.error("-[-f]iles or -[-d]irectory options are mutually exclusive")

if args.files:
    for fn in args.files:
        if not os.path.isfile(fn):
            print("Insert valid files")
            quit()

if not os.path.isdir(args.directory) and args.directory:
    print("Insert valid directory")
    quit()

chop_percentage = 0.02
out_file = open(args.output[0], "w")
out_file.close()


def optimize_data():
    reg_exp = re.compile(r"((.+\/\w+.* IOU):\s*(\d+[\.\d+]\d+))")
    new_data = {}
    new_data1 = {}

    if args.files:
        for in_file in args.files:
            for in_file1 in args.files:
                sum = 0
                sum1 = 0
                if in_file != in_file1:
                    fn1 = open(in_file, "r")
                    lines1 = fn1.readlines()
                    for line in lines1:
                        if reg_exp.search(line):
                            key, value = line.split(':', 2)
                            new_data[key] = value

                    fn = open(in_file1, "r")
                    lines = fn.readlines()
                    for line in lines:
                        if reg_exp.search(line):
                            key, value = line.split(':', 2)
                            new_data1[key] = value
                            matched = reg_exp.search(line).group(2)
                            if matched in new_data and matched in new_data1:
                                if abs(float(new_data[matched]) - float(new_data1[matched])) < chop_percentage:
                                    del new_data[matched]
                                    del new_data1[matched]
                    for key, value in new_data.items():
                        sum = sum + float(new_data[key])
                        sum1 = sum1 + float(new_data1[key])
                    aver_rel = sum / len(new_data)
                    aver_mod = sum1 / len(new_data1)
                    diff = aver_rel - aver_mod
                    out_file = open(args.output[0], "a")
                    fname = os.path.splitext(os.path.basename(in_file))[0] + '_' + \
                            os.path.splitext(os.path.basename(in_file1))[0]
                    out_file.writelines(fname + '\t' + "difference is" + '\t' + str(diff) + '\n')
    elif args.directory:
        for in_file in os.listdir(args.directory):
            for in_file1 in os.listdir(args.directory):
                sum = 0
                sum1 = 0
                if in_file != in_file1:
                    fn1 = open(args.directory + '\\' + in_file, "r")
                    lines1 = fn1.readlines()
                    for line in lines1:
                        if reg_exp.search(line):
                            key, value = line.split(':', 2)
                            new_data[key] = value

                    fn = open(args.directory + '\\' + in_file1, "r")
                    lines = fn.readlines()
                    for line in lines:
                        if reg_exp.search(line):
                            key, value = line.split(':', 2)
                            new_data1[key] = value
                            matched = reg_exp.search(line).group(2)
                            if matched in new_data and matched in new_data1:
                                if abs(float(new_data[matched]) - float(new_data1[matched])) < chop_percentage:
                                    del new_data[matched]
                                    del new_data1[matched]
                    for key, value in new_data.items():
                        sum = sum + float(new_data[key])
                        sum1 = sum1 + float(new_data1[key])
                    aver_rel = sum / len(new_data)
                    aver_mod = sum1 / len(new_data1)
                    diff = aver_rel - aver_mod
                    out_file = open(args.output[0], "a")
                    fname = os.path.splitext(os.path.basename(in_file))[0] + '_' + \
                            os.path.splitext(os.path.basename(in_file1))[0]
                    out_file.writelines(fname + '\t' + "difference is" + '\t' + str(diff) + '\n')


def analyze_result():
    data_dict = {}
    fn = open(args.output[0], "r+")
    lines = fn.readlines()
    reg_exp1 = re.compile(r"(\w+.*)_.*_.*\s*difference is\s*(.+)")
    for line in lines:
        if reg_exp1.search(line):
            if reg_exp1.search(line).group(1) not in data_dict:
                data_dict[reg_exp1.search(line).group(1)] = reg_exp1.search(line).group(2)

            else:
                data_dict[reg_exp1.search(line).group(1)] = float(data_dict[reg_exp1.search(line).group(1)]) + float(
                    reg_exp1.search(line).group(2))
    sorted_values = sorted(data_dict.values())
    sorted_dict = {}
    for i in sorted_values:
        for k in data_dict.keys():
            if data_dict[k] == i:
                sorted_dict[k] = data_dict[k]

    for key, value in sorted_dict.items():
        fn.write('\n' + '\n')
        fn.write('Average IOU  ' + '%s:%s' % (key, value))

    fn.write('\n' + '\n' + "The best version for realise is " + list(sorted_dict)[-1])


if __name__ == '__main__':
    optimize_data()
    analyze_result()
