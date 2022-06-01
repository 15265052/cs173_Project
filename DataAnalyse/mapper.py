import sys
from pyspark import SparkContext
if __name__ == "__main__":
    sc = SparkContext(appName="mapper")
    for line in sys.stdin:
        line = line.strip()
        data = line.split(',')
        city = data[2]
        area = data[3]
        str_city = data[2] + data[3]
        print >> sys.stdout, "%s\t%d" % (str_city, 1)
