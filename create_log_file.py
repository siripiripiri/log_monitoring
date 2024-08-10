f = open("logfile.txt", "x")

nums = [x for x in range(1,101)]
for i in nums:
    f.write(str(i))
    if i<100:
        f.write("\n")


f.close()
