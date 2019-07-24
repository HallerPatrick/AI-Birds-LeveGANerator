#!/usr/bin/env python3

file = open("parabolaEval-RedBird.csv", "r")
c = file.readlines()
for l in c:
    item = l.strip().split(";")
    if float(item[4]) != 0:
        # launch angle to velocity
        print(("%1.7f %1.7f %1.7f" % (float(item[1]) + float(item[2]),
              -float(item[2]), float(item[3]))).replace('.', ','))
        # Reverse actual angle to launch angle:
        # print(("%1.7f %1.7f" % (float(item[1]),
        #       float(item[1]) + float(item[2]))).replace('.', ','))
