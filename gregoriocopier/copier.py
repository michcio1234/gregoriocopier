from __future__ import print_function
import re
import sys

# CONSTANTS
to_join_with_previous_note = ['(,)', '(::)']

# CHECK INPUT ARGS
usage = """
Usage:
gcopier input_file.txt output_file.txt
"""
input_file = 'input.txt'
output_file = 'output.txt'
if len(sys.argv)<2:
    print("Input file not given. Using default: input.txt")
elif len(sys.argv)<3:
    input_file = sys.argv[1]
    print("Output file not given. Using default: output.txt" + usage)
else:
    output_file = sys.argv[2]



# DO IT
with open(input_file, 'r') as f:
    lines = f.readlines()
sin = lines[0]
if sin[-1]=='\n': sin = sin[0:-1]
s = []
for line in lines[1:]:
    # print(line)
    if line != '\n':
        s.append(line)

notes = re.findall("\([^)]*\)", sin)
for i, n in enumerate(notes):
    if n in to_join_with_previous_note:
        notes[i-1] += n
        notes.remove(n)

code = ''
for s2 in s:
    s2 = s2.replace(' ', '- ')
    if s2[-1]=='\n': s2 = s2[0:-1]
    syls2 = re.split(r'-', s2)
    # print(syls2)

    if len(syls2)!=len(notes):
        raise IOError("Number of syllables in verse {} does not match number of notes.".format(s2[0:10]))

    for i, syl in enumerate(syls2):
        code += "{s}{n}".format(s=syl, n=notes[i])

    code += '\n\n'

print(code)
if output_file is not None:
    with open(output_file, 'w') as f:
        f.write(sin+'\n\n')
        f.write(code)