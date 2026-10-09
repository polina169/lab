words = {'0':'ноль','1':'один','2':'два','3':'три','4':'четыре','5':'пять','6':'шесть','7':'семь','8':'восемь','9':'девять'}
f = open('input.txt', 'r')
for i in f:
    for z in i.split():
        if all(c in '01' for c in z) and (n := int(z,2)) % 2 == 0 and n <= 8191 and z.count('000') == 1:
            pos = z.find('000') + 1
            no_zeros = ''.join(d for d in z if d != '0')
            pos_str = ' '.join(words[d] for d in str(pos))
            print(f"{z} = {no_zeros}, позиция: {pos_str}")
