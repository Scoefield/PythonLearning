import difflib

def main():
    file1 = "test1.txt"
    file2 = "test2.txt"

    with open(file1, 'r') as f1:
        lines1 = f1.read().split(' ')
    print(lines1)

    with open(file2, 'r') as f2:
        lines2 = f2.read().split(' ')
    print(lines2)

    hd = difflib.ndiff(lines1, lines2)
    cplists = list(hd)
    print(cplists)

    print() # 換行

    templine1 = []
    templine2 = []
    count = 0
    for cpline in cplists:
        count += 1
        if cpline[0] == ' ':
            templine1.append(cpline[2:])
            templine2.append(cpline[2:])
        elif cpline[0] == '-':
            # lines1.remove(cpline[2:])
            templine1.append('<' + cpline[2:] + '>')
        else:
            # lines2.remove(cpline[2:])
            templine2.append('<' + cpline[2:] + '>')
    print(templine1)
    print(templine2)

if __name__ == "__main__":
    main()