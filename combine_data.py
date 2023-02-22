with open("input/sample_dhoopbahuthai_1.txt", "r") as f:
    data1 = f.read()

with open("input/sample_naaraz_81.txt", "r") as f:
    data2 = f.read()

with open("input/sample_pukhraaj_1.txt", "r") as f:
    data3 = f.read()

with open("input/combined.txt", "w") as f:
    f.write(data1 + "\n" + data2 + "\n" + data3)