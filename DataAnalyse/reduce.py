import sys

prev_key = False
sum = 0
for line in sys.stdin:
    line = line.strip()
    data = line.split('\t')
    str_city = data[0]
    curr_key = str_city
    num = data[1]
    if prev_key and curr_key != prev_key:
        print >> sys.stdout, "%s has %d confirmation in total" % (prev_key, sum)
        prev_key = curr_key
        sum = 0
        sum += num
    else:
        prev_key = curr_key
        sum += num
if prev_key:
    print >> sys.stdout, "%s has %d confirmation in total" % (prev_key, sum)
