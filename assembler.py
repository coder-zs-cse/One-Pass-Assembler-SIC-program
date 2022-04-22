import opcode
from tracemalloc import start


OPTAB = {'ADD': '18', 'COMP': '28', 'DIV': '24', 'J': '30',
         'JEQ':'30', 'JGT': '34', 'JLT': '38', 'JSUB': '48', 
         'LDA': '00', 'LDCH': '50', 'LDL': '08', 'LDX': '04',
         'MUL': '20', 'OR': '44', 'RD': 'D8', 'RSUB': '4C', 
         'STA': '0C', 'STCH': '54', 'STL': '14', 'STSW': 'E8',
         'STX': '10', 'SUB': '1C', 'TD': 'E0', 'TIX': '2C', 'WD': 'DC'}

with open('input.txt', 'r') as file:
    data = file.readlines()

loc = data[0].split()[-1]
starting_address = loc
program_name = data[0].split()[0]
while len(program_name)<6:
    program_name += " "
print(loc)
objCode = {}
labels = {}
backRef = {}
obj_prog = []
program_length = ""
for line in data:
    current = line.split()
    if current[0]=='.':
        continue
    if len(current)==3:
        labels[current[0]] = loc

    if len(current)==1: # handling edge case for RSUB
        objCode[loc] = OPTAB[current[0]] + "0000"
        loc = str(hex(int(loc,16) + 3)[2:]).upper()
    elif current[-2] == "RESB":
        loc = str(hex(int(loc,16) + int(current[2]))[2:])
    elif current[-2] == "RESW":
        loc = str(hex(int(loc,16) + 3*int(current[2]))[2:])
    elif current[-2] == "BYTE":
        if current[-1][0] == 'C':
            objCode[loc] =  ''.join(map(lambda c : str(hex(ord(c))[2:]).upper(), current[-1][2:-1]))
            loc = str(hex(int(loc,16)+ 3)[2:])
        elif current[-1][0] == 'X':
            objCode[loc] = current[-1][2:-1]
            loc = str(hex(int(loc,16)+ 1)[2:])
    elif current[-2]=="START" or current[-2]=="END":
        if current[-2] == "END":
            program_length = str(hex(int(loc,16) - int(starting_address,16))[2:].upper())
    elif current[-2]=="WORD":
        objCode[loc] = hex(int(current[-1]))[2:].zfill(6)
        loc = str(hex(int(loc,16) + 3)[2:])
    else:
        operand = ""
        if ",X" in current[-1]:
            operand = current[-1][:-2]
        else:
            operand = current[-1]

        if operand in labels.keys():
            objCode[loc] = OPTAB[current[-2]] + labels[operand]
        else:
            if operand in backRef.keys():
                backRef[operand].append(hex(int(loc,16)+1)[2:].upper())
            else:
                backRef[operand] = [hex(int(loc,16)+1)[2:].upper()]
            objCode[loc] = OPTAB[current[-2]] + "0000"

        if ',X' in current[-1]:
            objCode[loc]= objCode[loc][:2] + str(int(objCode[loc][2]) | 8) + objCode[loc][3:]
        else:
            objCode[loc]= objCode[loc][:2] + str(int(objCode[loc][2]) & 7) + objCode[loc][3:]
            
        loc = str(hex(int(loc,16) + 3)[2:])
    

for key, value in labels.items():
    print(value.upper(), key.upper())
print()
for key, value in objCode.items():
    print(key.upper(),value.upper())
print()
for key, value in backRef.items():
    print(key.upper(),value)

print(program_length)


            