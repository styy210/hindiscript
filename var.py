import re
import sys
import string
import OPS
import strrch
vars = {}
rloops = []
def glti(error, message):
    print(f'ERROR::bhai glti hogyi code me:{error}\n{message}')
    sys.exit()

def declaretionChecker(scode, fscode, eline):
    if scode[0][0].isnumeric():
        er = f'''
    {fscode}\n{'    '+'^'}
                        '''
        glti(er, f'GalatSyntax: bhai variable declaration me kuchh gadbad h (line {eline})')
    elif not scode[0].replace('_', '').isalnum():
            for char in scode[0]:
                if char not in (string.ascii_letters+string.digits+'_'):
                    break
            er = f'''
    {fscode}\n{'    '+' '*fscode.find(char)+'^'}
                        '''
            glti(er, f'GalatSyntax: bhai variable declaration me kuchh gadbad h (line {eline})')
    elif bool(re.match(r'^["\'][^"\']*["\']$', scode[0])):
        er = f'''
    {fscode}\n{'    '+'^'*len(scode[0])}
                        '''
        glti(er, f'GalatSyntax: bhai ese nhi hota yarr ye kya h (line {eline})')
    elif scode[0][0] in ['"', "'"]:
        er = f'''
    {fscode}\n{'    '+'^'}
                        '''
        glti(er, f'GalatSyntax: bhai ese nhi hota yarr ye kya h (line {eline})')
def DtypeCheck(scode, fscode, eline, opt:bool=False):
    fqr = None
    lcode = scode[1]
    if not opt:
        if lcode.isnumeric():
            return int(lcode)
    if '+' in scode or '*' in scode:
        result = OPS.OPs(scode, eline)
        return result
    elif lcode[0] in ['"', "'"]:
        if lcode[0] == '\'':
            qtyp = 's'
            index = 0
            for l in lcode[1:]:
                if l == '\'':
                    fqr = True
                    break
                else:
                    index+=1
        elif lcode[0] == '"':
            qtyp = 'd'
            index = 0
            for l in lcode[1:]:
                if l == '"':
                    fqr = True
                    break
                else:
                    index+=1
        if fqr != True:
            if qtyp == 's':
                qoute = '\''
            elif qtyp == 'd':
                qoute = '"'
            er = f'''
    {fscode}\n{'    '+' '*(fscode.find(qoute))+'^'}
                    '''
            glti(er, f'Glti: aap shayad quote band krna bhul gye... (line {eline})')
        else:
            if fqr:
                if qtyp == 's':
                    qoute = '\''
                elif qtyp == 'd':
                    qoute = '"'
                try:
                    if fscode[fscode.find(lcode)+len(lcode)] not in ['', ' ']:
                        er = f'''
    {fscode}\n{'    '+' '*fscode.find(qoute)+'^'*len(lcode)}
                        '''
                        glti(er, f'GalatSyntax: bhai ese thodi hota h (line {eline})')
                except IndexError:
                    pass
    elif lcode[-1] in ['"', "'"]:
        er = f'''
    {fscode}\n{'    '+' '*(len(lcode)+1)+'^'}
                        '''
        glti(er, f'GalatSyntax: bhai galat h yaar ye ese nhi hota (line {eline})')
    else:
        if lcode in vars:
            return vars[lcode]
        else:
            er = f'''
    {fscode}\n{'    '+' '*(fscode.find(lcode))+'^'*len(lcode)}
                    '''
            glti(er, f'NhiMilrha: bhai ye \'{lcode}\' kya h? mil nhi rha (line {eline})')
    return lcode[1:index+1]
    
def definer(scode, eline):
    if 'hai' in scode:
        scode = scode.strip()
        code=scode.strip().split()
        try:
            qtxt = re.search(r'([\'"])(.*?)([\'"])', scode).group()
            code = [code[0], qtxt]+scode[scode.find(qtxt)+len(qtxt):].split()
        except:
            pass
        declaretionChecker(code, scode, eline)
        if len(code) > 3 and not ('*' in scode or '+' in scode):
            for args in code:
                if args == code[3]:
                    llen = len(args)
                    break
            er = f'''
    {scode}\n{'    '+'^'*len(scode)}
                        '''
            glti(er, f'GalatSyntax: bhai ese nhi hota yarr ye kya h (line {eline})')
        elif len(code) < 2:

            lenm = len(code[0])+len(code[1])
            er = f'''
    {scode}\n{'    '+' '*(len(code))+' '*(lenm)+'^'}
                        '''
            glti(er, f'GalatSyntax: bhai galat h ye value to define kr (line {eline})')
        try:
            code.remove('hai')
        except:
            pass
        if '+' in scode or '*' in scode:
            alcode = scode.strip().split()
            alcode.remove('hai')
            alcode.remove(code[0])
            if len(alcode) > 1:
                er = f'''
    {scode}\n{'    '+' '*(len(code[0])+len(alcode[0])+2)+'^'*len(alcode[1])}
                        '''
                glti(er, f'GalatSyntax: bhai galat likha h ye (line {eline})')
            typ = DtypeCheck(alcode[0], scode, eline, opt=True)
        else:
            typ = DtypeCheck(code, scode, eline)
        vars[code[0]] = typ

def inputdefiner(scode):
    kcode = scode[5:]
    if kcode.strip() =='':
        qwertyuio=input();return
    code = kcode.strip().split()    
    declaretionChecker(code[0], scode, 'not detected')
    if len(code) == 1:
        rarg = input()
        vars[code[0]] = rarg
        return
    token = code[0]
    code = code[1:]
    qtxt = re.search(r'([\'"])(.*?)([\'"])', kcode)
    token1 = (' '.join(c for c in code)).strip()
    if not strrch.inqoutes(scode, token1):
        if token1 in vars:
            token1 = vars[token1]
        elif len(token1.strip().split()) == 1:
            er = f'''
    {scode}\n{'    '+' '*(len(scode.find(token1)))+'^'}
                        '''
            glti(er, f'GalatSyntax: bhai ye \'{token1}\' kya h?')
        else:
            er = f'''
    {scode}\n{'    '+' '*(scode.find(token1))+'^'*len(scode.find(token1))}
                        '''
            glti(er, f'GalatSyntax: bhai galat h ye')
    lcode = token1.replace(qtxt.group(), '')
    if not lcode.strip() == '':
        er = f'''
    {scode}\n{'    '+' '*(scode.find(token1))+'^'*len(scode[scode.find(token1):])}
                        '''
        glti(er, f'GalatSyntax: bhai galat h ye')
    rarg12 = input(token1[1:-1])
    vars[token] = rarg12

def typecon(code, typ: int|str):
    kcode = code.strip().split()
    if typ == str and kcode[0] != 'string':
        er = f'''
    {code}\n{'    '+'^'*len(kcode[0])}
                        '''
        glti(er, f'GalatSyntax: bhai galat h ye')
    if typ == int and kcode[0] != 'int':
        er = f'''
    {code}\n{'    '+'^'*len(kcode[0])}
                        '''
        glti(er, f'GalatSyntax: bhai galat h ye')
    if len(kcode) > 2:
        er = f'''
    {code}\n{'    '+'^'*len(code)}
                        '''
        glti(er, f'GalatSyntax: bhai yha bs ek argument allowed h')
    if typ == str:
        if kcode[1] not in vars:
            er = f'''
    {code}\n{'    '+' '*(code.find(kcode[1]))+'^'*len(kcode[1])}
                        '''
            glti(er, f'GalatSyntax: bhai ye \'{kcode[1]}\' kya h?')
        else:
            vars[vars[kcode[1]]] = str(vars[kcode[1]])
    elif typ == int:
        if kcode[1] not in vars:
            er = f'''
    {code}\n{'    '+' '*(code.find(kcode[1]))+'^'*len(kcode[1])}
                        '''
            glti(er, f'GalatSyntax: bhai ye \'{kcode[1]}\' kya h?')
        else:
            if not vars[kcode[1]].isnumeric():
                er = f'''
    {code}\n{'    '+' '*(code.find(kcode[1]))+'^'*len(kcode[1])}
                        '''
                glti(er, f'GalatSyntax: bhai ye numeric nhi h: {vars[kcode[1]]}')
            vars[kcode[1]] = int(vars[kcode[1]])

