import sys
import var

def glti(error, message):
    print(f'ERROR::bhai glti hogyi cstring me:{error}\n{message}')
    sys.exit()

def inqoutes(fcode, cstring: str, onlybool: bool = False) -> bool:
    fqr = None
    if cstring[0] in ['"', "'"]:
        if cstring[0] == '\'':
            qtyp = 's'
            index = 0
            for l in cstring[1:]:
                if l == '\'':
                    fqr = True
                    break
                else:
                    index+=1
        elif cstring[0] == '"':
            qtyp = 'd'
            index = 0
            for l in cstring[1:]:
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
    {fcode}\n{'    '+' '*(fcode.find(cstring))+'^'}
                    '''
            glti(er, f'Glti: aap shayad quote band krna bhul gye... (line 1)')
    elif cstring[-1] in ['"', "'"]:
        er = f'''
    {fcode}\n{'    '+' '*(len(cstring)+1)+'^'}
                        '''
        glti(er, f'GalatSyntax: bhai galat h yaar ye ese nhi hota (line 1)')
    else:
        if not onlybool:
            if cstring in var.vars:
                return
            else:
                er = f'''
    {fcode}\n{' '*4+' '*(fcode.find(cstring))+'^'*len(cstring)}
                        '''
                glti(er, f'NhiMilrha: bhai \'{cstring}\' kya h? mil nhi rha (line 1)')
        else:
            return False
    return True