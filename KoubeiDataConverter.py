def convertData(dir):
    ofile = open("%s.csv" % dir, 'w')
    for i in range(325):
        ifile = open("./%s/%d.csv" % (dir, i), 'r')
        lines = ifile.readlines()

        # 转换第一列 #
        time = lines[0].strip('\n').split(',')[2]
        ofile.write("%s" % time)

        # 转换其余列 #
        for j in range(1, len(lines)):
            time = lines[j].strip('\n').split(',')[2]
            ofile.write("\t%s" % time)
        ofile.write('\n')
        ifile.close()
    ofile.close()


if __name__ == '__main__':
    convertData("RawCorrect")
    convertData("RawCentralized")
    convertData("RawEqualized")

    convertData("SynCorrect")
    convertData("SynCentralized")
    convertData("SynCentralized(1.1)")
    convertData("SynCentralized(1.2)")
    convertData("SynCentralized(1.3)")
    convertData("SynCentralized(1.4)")
    convertData("SynCentralized(1.5)")
    convertData("SynCentralized(1.6)")
    convertData("SynCentralized(1.7)")
    convertData("SynCentralized(1.8)")
    convertData("SynCentralized(1.9)")
    convertData("SynCentralized(3x)")
    convertData("SynEqualized")
