import re
w = {'0':'ноль', '1':'один', '2':'два', '3':'три', '4':'четыре', '5':'пять', '6':'шесть', '7':'семь', '8':'восемь', '9':'девять'}
with open('input.txt') as f:
    file = f.read()
    for n in re.findall(r'\b[01]{1,12}0', file):
        if n.count('000', 0) < 2:
            print(n)
