import re

def search_brackets(text: str, start: int):
    stack = []
    for i in range(start, len(text)):
        if text[i] == '(':
            stack.append(i)
        if text[i] == ')':
            stack.pop()
            if len(stack) == 0:
                return i
    return -1

def convert(text: str):
    replacing_patterns = [
        (r'{.*\n', '\\begin{cases}\n'),
        (r'}', '\\end{cases} \\\\ \n'),
        (r'\[', '\\left[ \n\\begin{gathered}'),
        (r'\]', '\\end{gathered} \n\\right.'),
        (r'\n', '\\\\\n'),
        (r'\^\(', '^{', '}'),
        (r'_\(', '_{', '}'),
        (r'sqrt\(', 'sqrt{', '}')
    ]
    for pattern in replacing_patterns:
        pairsDiaps = [(m.start(0), m.end(0)) for m in re.finditer(pattern[0], text)]
        if len(pairsDiaps) > 0:
            res = ""
            linDiaps = [0]
            for el in pairsDiaps:
                linDiaps += el
           
            closures = []         
            if len(pattern) > 2:
                prestarts = [m[0] for m in pairsDiaps]
                inds = [search_brackets(text, m) for m in prestarts]
                closures = inds
                for el in inds:
                    linDiaps += (el, el+1)
            linDiaps.sort()
            linDiaps.append(-1)
                        
            for i in range(len(linDiaps)-1):
                if i % 2 == 0:
                    ttc = text[linDiaps[i]:linDiaps[i+1]]
                    if len(ttc) > 0:
                        res += convert(ttc)                    
                else:
                    if linDiaps[i] not in closures:
                        res += pattern[1] 
                    else:                      
                        res += pattern[2]
                    
            return res            
            
    else:
        return text
    
exText = '''[
{
x_(1)^2 + y^2 = 3 
x^(2 + 3^x) = 5 
}{
x+2 = y
y-5 = x^2
}
] 
'''
print(convert(exText))