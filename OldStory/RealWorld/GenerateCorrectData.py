import csv
import os

input_dir = "Old"
output_dir = "Correct"

if not os.path.exists(os.path.abspath(output_dir)):
    os.makedirs(os.path.abspath(output_dir))

for i in range(325):
    ifile = open("%s/%d.csv" % (input_dir, i), 'r')
    ofile = open("%s/%d.csv" % (output_dir, i), 'w')
    reader = csv.reader(ifile)
    for row in reader:
        hour = int(row[2].split(" ")[1].split(":")[0])
        ofile.write("%s,%s,%d\n" % (row[0], row[1], hour))
    ifile.close()
    ofile.close()
    