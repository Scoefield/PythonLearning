import difflib
from pprint import pprint

file1 = 'test1.txt'
file2 = 'test2.txt'

with open(file1, 'r') as f1:
    a = f1.read()

with open(file2, 'r') as f2:
    b = f2.read()

# a = 'pythonclub.org is wonderful'
# b = 'Pythonclub.org also wonderful'
s = difflib.SequenceMatcher(None, a, b)

# print("s.get_matching_blocks():")
# pprint(s.get_matching_blocks())

print()
print("s.get_opcodes():")
bstr = ""
for tag, i1, i2, j1, j2 in s.get_opcodes():
    print("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %  (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2]))
    if tag == 'insert':
        listsa = a[i1:i2].split(' ')
        listsb = b[j1:j2].split(' ')
        bstr += '<' + b[j1:j2] + '>'

    elif tag == 'replace':
        listsa = a[i1:i2].split(' ')
        listsb = b[j1:j2].split(' ')
        # print("standar:", listsa)
        # print("recognize:", listsb)
        # print()
        if len(listsb) < 4:
            bstr += '<' + b[j1:j2] + '>'
                   
        else:
            # if len(listsa) == 1:
            #     for lb in listsb:
            #         strlistsb.append('<' + lb + '>') 
            # else:
            bcount = 0
            print(listsa, listsb)
            strlistsb = []
            for lb in listsb:
                bcount += 1
                bindex = listsb.index(lb)
                # print(bindex)
                if lb not in listsa:
                    print(lb)
                    strlistsb.append('<' + lb + '>')
                    print(strlistsb)
                else:
                    aindex = listsa.index(lb) 
                    # print(aindex, bcount)                     
                    if abs(bcount-aindex-1) > 2:
                        # print(aindex)
                        strlistsb.append('<' + lb + '>')
                    else:
                        strlistsb.append(lb)
            bstr += " ".join(strlistsb)
    else:
        bstr += b[j1:j2]
    
print()
print(bstr)
