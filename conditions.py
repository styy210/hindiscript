import re
import sys
import var
import OPS
from strrch import inqoutes

def glti(error, message):
    print(f'ERROR::bhai glti hogyi code me:{error}\n{message}')
    sys.exit()

def CharInQts(text, char, start=0):
    in_single_quotes = False
    in_double_quotes = False
    for i in range(start, len(text)):
        if text[i] == "'" and not in_double_quotes:
            in_single_quotes = not in_single_quotes
        elif text[i] == '"' and not in_single_quotes:
            in_double_quotes = not in_double_quotes
        if text[i] == char and (in_single_quotes or in_double_quotes):
            return True
    return False


def simpVerify(con):
    if con.lower() == 'sahi':
        return True
    elif con.lower() == 'nahi':
        return False
    else:
        return 99
def conditionVarify(condition, sfcode, c:bool=False):
    if c:
        col = condition.strip()
    else:
        col = condition[1:-1].strip()
    if lrarg22:=simpVerify(col) != 99:
        return lrarg22
    if col.isnumeric():
        return True
    elif '=' in col:
        colparts = col.split('=')
        parts = []
        for part in colparts:
            part = part.strip()
            if simpVerify(part) != 99:
                parts.append(simpVerify(part))
            elif '*' in part or '+' in part:
                parts.append(OPS.OPs(part, 1))
            if part.isnumeric():
                parts.append(int(part))
            elif inqoutes(sfcode, part, True):
                parts.append(part)
        return all(i==parts[0] for i in parts)
    elif '<' in col:
        colpart = col.split('<')
        colparts = []
        for char in colpart:
            if not inqoutes(sfcode, char, True):
                if char in var.vars:
                    colparts.append(var.vars[char])
                elif char.isnumeric():
                    colparts.append(int(char))
            else:
                colparts.append(char)
        if len(colparts) > 2:
            return 'inalid'
        return colparts[0] < colparts[1]
    elif '>' in col:
        colpart = col.split('>')
        colparts = []
        for char in colpart:
            if not inqoutes(sfcode, char, True):
                if char in var.vars:
                    colparts.append(var.vars[char])
                elif char.isnumeric():
                    colparts.append(int(char))
            else:
                colparts.append(char)
        if len(colparts) > 2:
            return 'inalid'
        return colparts[0] > colparts[1]
    return True


def agarComp(scode):
        ctx = scode.strip().splitlines()[0]
        if ctx.startswith('agar ') or ctx.startswith('agar('):
            qtxt = re.search(r'\((.*)\)', ctx)
            if qtxt == None:
                if bool(re.search(r'([\(])(.*?)', ctx)) or  bool(re.search(r'(.*?)([\)])', ctx)):

                    er = f'''
    {ctx}\n{'    '+'~'*(len(ctx.strip()))}'''
                    glti(er, f'GalatSyntax: bhai yha kuchh gadbad h dhyan se dekh (line 1)')
                else:
                    er = f'''
    {ctx}\n{'    '*2+'~'*(len(ctx.strip())-4)}'''
                    glti(er, f'GalatSyntax: bhai yarr (condition) (...) ke andar hona chhaiye (line 1)')
            qtxt = qtxt.group()
            mctx = ctx[:ctx.find(qtxt)+1]+ctx[ctx.find(qtxt)+1+len(qtxt[1:-1]):]
            rarg1 = re.search(r'agar(.*?)([\(])', mctx)
            if bool(rarg1) and not (rarg1.group()[4:-1].strip() == ''):
                rarg1 = rarg1.group()
                er = f'''
    {ctx}\n{'    '+' '*ctx.find(rarg1[4:-1].strip())+'^'*(len(rarg1[4:-1].strip()))}'''
                glti(er, f'GalatSyntax: bhai ye galat h ese nhi hota (line 1)')
            rarg2 = re.search(r'([\)])(.*?)([{])', mctx)
            if bool(rarg2) and not (rarg2.group()[1:-1].strip() in ['', 'hai toh', 'toh', 'hai']):
                rarg2 = rarg2.group()
                er = f'''
    {ctx}\n{'    '+' '*ctx.find(rarg2[1:-1].strip(), len(qtxt)+4)+'^'*(len(rarg2[1:-1].strip()))}'''
                glti(er, f'GalatSyntax: bhai yha sirf \'hai toh\' element use kr skte h (line 1)')
            result = conditionVarify(qtxt, ctx)
            return result
        
def paraChecker(scode):
    pos = 0
    code = scode.strip().splitlines()[0]
    f = None
    ef = None
    ign = (None, 0)
    ifs = 0
    answer = agarComp(scode)
    tLines, eLines = 0, 0
    if code.startswith('agar'):
        for token in code.split():
            if token in ['{:', '{ :'] or (token[-3:] == '{ :' or token[-2:] == '{:'):
                f = True
            elif f==True and token.rstrip() not in [' ', '']:
                er = f'''
    {code}\n{'    '+' '*(code.find(token, pos))+'^'}
                    '''
                glti(er, 'GalatHaibhai: bhai ye kya h ese nhi hota')
            else:
                pos+=len(token)+1
        if f == None:
            er = f'''
    {code}\n{'    '+' '*len(code[:-1])+'^'}'''
            glti(er, 'GalatSyntax: bhai ese nhi hota yarr missing (\'{:\') (line 1)')
        for linm, tokenlines in enumerate(scode.strip().splitlines()[1:]):
            if ign[0]:
                break
            tLines += 1
            if tokenlines.strip() == '':
                continue
            if re.match(r'[(})]\s*nhi\s*toh\s*[({)]', tokenlines):
                ef = True
                ign = (True, linm+2)
                break
            elif tokenlines[0] not in [' ', '\t', '}']:
                if tokenlines == scode.strip().splitlines()[1]:
                    er = f'''
    {tokenlines}\n{'    '+'^'}
                    '''
                    glti(er, 'GalatIndentation: bhai indentation galat h space daal waha pe, ese nhi chalta yrr fir me confuse hojata hu')
                else:
                    el = False
                    rarg08 = False
                    for dex, token in enumerate(reversed(tokenlines)):
                            if token == '}' and not CharInQts(tokenlines, token, dex):
                                if ifs == 0:
                                    er = f'''
    {tokenlines}\n{'    '+'^'}'''
                                    glti(er, 'GalatHaibhai: bhai ese nhi hota indentation galat ha ya to tu uper koi \'{:\' band krna bhul gya')
                                el = True
                                rarg08 = True
                            else:
                                if rarg08:
                                    er = f'''
    {tokenlines}\n{'    '+'^'}'''
                                    glti(er, 'GalatIndentation: bhai indentation galat h space daal waha pe, ese nhi chalta yrr fir me confuse hojata hu')
                    if not el:
                        er = f'''
    {scode.strip().splitlines()[0]}\n{'    '+' '*(scode.strip().splitlines()[0].find('{:')+1)+'^'}'''
                        glti(er, 'GalatHaibhai: bhai \'{:\' ko \'}\' se close bhi krna hota h (line)')
            elif tokenlines[0] == " " or tokenlines[0] == '\t':
                if (tokenlines.strip().startswith('agar') and '{' in tokenlines[-4:]) or ('{' in tokenlines[-4:]):
                    ifs += 1
                elif bool(re.search(r'[(})]\s*nhi\s*toh\s*[({)]', tokenlines)):
                    ifs+= 1
                if tokenlines.strip()=='}' or bool(re.search(r'[(})]\s*nhi\s*toh\s*[({)]', tokenlines.strip())):
                    if ifs == 0:
                            er = f'''
    {tokenlines}\n{'    '+'^'}'''
                            glti(er, 'GalatHaibhai: bhai ese nhi hota indentation galat ha ya to ye hona hi nhi chhaiye')
                    else:
                        ifs -= 1
                        continue
                    ef = True
                    break
                elif tokenlines.rstrip()[-1] == '}':
                    er = f'''
    {tokenlines}\n{'    '+' '*(len(tokenlines))+'^'}'''
                    glti(er, 'GalatHaibhai: bhai ese nhi hota isko niche kr')           
            else:
                if tokenlines.strip() == '}':
                    ef = True
                    break
                else:
                    rarg09 = False
                    rarg99 = None
                    for tokn in reversed(scode.strip().splitlines()[1:linm+2]):
                        if rarg99: break
                        for dex, token in enumerate(tokn):
                            if token == '}' and not CharInQts(tokn, token, dex):
                                ef = True
                                rarg09 = True
                            else:
                                if rarg09 and token != ' ':
                                    if 'nhitoh' or 'nhi toh' in tokn:
                                        if bool(re.search(r'[(})]\s*nhi\s*toh\s*[({)]', tokn)) and not bool(re.search(r'[(\'")].*?[(})]\s*nhi\s*toh\s*[({)].*?[(\'")]', tokn)):
                                            rarg99 = True
                                            break
                                    er = f'''
    {tokn}\n{'    '+' '*(tokn.find(token))+'^'}'''
                                    glti(er, 'GalatHaibhai: bhai ye kya h ese nhi hota')                      
        if ef == None:
                er = f'''
    {scode.strip().splitlines()[0]}\n{'    '+' '*(scode.strip().splitlines()[0].find('{:')+1)+'^'}
                    '''
                glti(er, 'GalatHaibhai: bhai \'{:\' ko \'}\' se close bhi krna hota h (line)')
        elif ef and ign[0]:
            ign = (ign[0], ign[1])
            el = False
            rarg08 = False
            for ender, tokenn in enumerate(scode.splitlines()[ign[1]:]):
                eLines += 1
                if tokenn.strip() == '':
                    continue
                if tokenn[0] not in [' ', '\t', '}']:
                    if tokenn == scode.strip().splitlines()[ign[1]:][1]:
                        er = f'''
    {tokenn}\n{'    '+'^'}'''
                        glti(er, 'GalatIndentation: bhai indentation galat h space daal waha pe, ese nhi chalta yrr fir me confuse hojata hu')
                    else:
                        for dex, token in enumerate(reversed(tokenn)):
                                if token == '}' and not CharInQts(tokenn, token, dex):
                                    el = True
                                    rarg08 = True
                                else:
                                    if rarg08:
                                        er = f'''
    {tokenn}\n{'    '+'^'}'''
                                        glti(er, 'GalatIndentation: bhai indentation galat h space daal waha pe, ese nhi chalta yrr fir me confuse hojata hu')
                        if not el:
                            er = f'''
    {scode.strip().splitlines()[ign[1]:][0]}\n{'    '+' '*len(scode.strip().splitlines()[ign[1]:][0])+'^'}'''
                            glti(er, 'GalatHaibhai: bhai nhitoh statement ke baad \'{\' ko \'}\' se close bhi krna hota h (line)')
                elif tokenn[0] == " " or tokenn[0] == '\t':
                    if tokenn.strip().startswith('agar') and ('{' in tokenn):
                        ifs += 1
                    if (tokenn.strip().startswith('jabtak') or tokenn.strip().startswith('jab tak')) and ('{' in tokenn):
                        ifs += 1
                    if bool(re.search(r'\bnhi\s*toh\s*\b(?=(?:(?:[^\"]*\"[^\"]*\")*[^\"]*$)(?:(?:[^\']*\'[^\']*\')*[^\']*$))', tokenn)):
                        ifs+= 1
                    if tokenn.strip()=='}':
                        if ifs == 0:
                                er = f'''
    {tokenn}\n{'    '+'^'}'''
                                glti(er, 'GalatHaibhai: bhai ese nhi hota indentation galat ha ya to ye hona hi nhi chhaiye')
                        else:
                            ifs -= 1
                            continue
                        el = True
                        break
                    elif tokenn.rstrip()[-1] == '}':
                        er = f'''
    {tokenn}\n{'    '+' '*(len(tokenn))+'^'}'''
                        glti(er, 'GalatHaibhai: bhai ese nhi hota isko niche kr')           
                else:
                    if tokenn.strip() == '}':
                        el = True
                        break
                    else:
                        rarg09 = False
                        rarg99 = None
                        for tokn in reversed(scode.strip().splitlines()[ign[1]:]):
                            if rarg99: break
                            for dex, token in enumerate(tokn):
                                if token == '}' and not CharInQts(tokn, token, dex):
                                    el = True
                                    rarg09 = True
                                else:
                                    if rarg09 and token != ' ':
                                        er = f'''
    {tokn}\n{'    '+' '*(tokn.find(token))+'^'}'''
                                        glti(er, 'GalatHaibhai: bhai ye kya h ese nhi hota')
            if el != True:
                er = f'''
    {scode.strip().splitlines()[ign[1]-1:][0]}\n{'    '+' '*len(scode.strip().splitlines()[ign[1]-1:][0])+'^'}'''
                glti(er, 'GalatHaibhai: bhai nhitoh statement ke baad \'{\' ko \'}\' se close bhi krna hota h (line)')                             
        if not answer:
            if ign[0]:
                outp = scode.splitlines()[ign[1]:ign[1]+ender]
        elif answer:
            outp = scode.splitlines()[1:linm+1]
        try:
            return tLines+eLines, '\n'.join(lines for lines in outp)
        except UnboundLocalError:
            return tLines+eLines, '' 