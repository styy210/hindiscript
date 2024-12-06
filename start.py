import re
import os
import sys
import var
import OPS
import time
import conditions

def glti(error, message):
    print(f'ERROR::bhai glti hogyi code me:{error}\n{message}')
    sys.exit()
def runner(scode, line):
    if scode.startswith('sabar') or scode.startswith('sabarkar') or scode.startswith('soja') or scode.startswith('intezaar'):
        if scode.startswith('sabar'):
            token1 = scode[5:]
        elif scode.startswith('sabarkar'):
            token1 = scode[8:]
        elif scode.startswith('soja'):
            token1 = scode[4:]
        elif scode.startswith('intezaar'):
            token1 = scode[8:]
        try:
            waitToken = float(token1.strip())
        except:
            er = f'''
    {scode}\n{'    '+' '*(scode.find(token1))+'^'*len(token1)}
                        '''
            glti(er, f'SyntaxWaliGlti: bhai galat h ye time should be an integer (line {line})')
        time.sleep(waitToken)
    elif scode.strip() in ['rukja', 'khatam']:
        try:
            var.rloops.pop()
        except:
            pass
    elif scode.startswith('string'):
        var.typecon(scode, str)
    elif scode.startswith('int'):
        var.typecon(scode, int)
    elif scode.startswith('likh') or scode.startswith('chhap'): 
        fq = None
        if scode.startswith('chhap'):
            code = scode[5:].strip()
        else:
            code = scode[4:].strip()
        if '+' in code or '*' in code:          
            result = OPS.OPs(code, line)
            print(result)
            return
        if '>' in code or '<' in code:
            result = conditions.conditionVarify(code, scode, True)
            if result:
                print('Sahi')
            elif result == False:
                print('Nahi')
            return
        elif code[0] in ['"', "'"]:
            if code[0] == '\'':
                qtyp = 's'
                index = 0
                for l in code[1:]:
                    if l == '\'':
                        fq = True
                        break
                    else:
                        index+=1
            elif code[0] == '"':
                qtyp = 'd'
                index = 0
                for l in code[1:]:
                    if l == '"':
                        fq = True
                        break
                    else:
                        index+=1 
            if fq != True:
                if qtyp == 's':
                    qoute = '\''
                elif qtyp == 'd':
                    qoute = '"'
                er = f'''
    {scode}\n{'    '+' '*(scode.find(qoute))+'^'}
                        '''
                glti(er, f'Glti: aap shayad quote band krna bhul gye... (line {line})')
            else:
                if fq:
                    if qtyp == 's':
                        qoute = '\''
                    elif qtyp == 'd':
                        qoute = '"'
                    try:
                        if code[index+2] != '':
                            er = f'''
    {scode}\n{'    '+' '*scode.find(qoute)+'^'*len(code)}
                            '''
                            glti(er, f'GalatSyntax: bhai ese thodi hota h (line {line})')
                    except IndexError:
                        pass
        elif code.isnumeric():
            print(code)
            return
        elif code[-1] in ['"', "'"]:
            er = f'''
    {scode}\n{'    '+' '*(len(code)+1)+'^'}
                            '''
            glti(er, f'GalatSyntax: bhai galat h yaar ye ese nhi hota (line {line})')
        elif len(code.split()) > 1:
            er = f'''
    {scode}\n{'    '*2+' '*(len(code.split()[0])+2)+'^'*len(code.split()[1])}
                            '''
            glti(er, f'GalatSyntax: bhai galat h yaar ye ese nhi hota (line {line})')        
        else:
            if code in var.vars:
                print(var.vars[code])
                return
            else:
                er = f'''
    {scode}\n{' '*4+' '*(scode.find(code))+'^'*len(code)}
                        '''
                glti(er, f'NhiMilrha: bhai ye \'{code}\' kya h? mil nhi rha (line {line})')                  
        print(code[1:index+1])
    elif 'hai' in scode:
        var.definer(scode, line)
    elif scode.startswith('puchh'):
        var.inputdefiner(scode)