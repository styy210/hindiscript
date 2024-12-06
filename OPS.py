from strrch import inqoutes
import var
import sys

plus, mul, equal = '+', '*', '='

def glti(error, message):
    print(f'ERROR::bhai glti hogyi code me:{error}\n{message}')
    sys.exit()

def OPs(code, eline):
    if plus in code:
        toadd = []
        alpha, num = None, None
        for tokens in code.split(plus):
            tokens = tokens.strip()
            if tokens.isnumeric():
                toadd.append(int(tokens))
                num = True
            elif inqoutes(code, tokens):
                toadd.append(tokens)
                alpha = True
            else: 
                if tokens in var.vars:
                    if type(var.vars[tokens]) == str:
                        toadd.append(f'"{var.vars[tokens]}"')
                    elif type(var.vars[tokens]) == int:
                         toadd.append(var.vars[tokens])
                         num=True
        if num == None:
                return ''.join(adding[1:-1] for adding in toadd)
        elif num and alpha:
            er = f'''
    {code}\n{'    '+'~'*(len(code))}
                            '''
            glti(er, f'GalatExp: bhai string ke sath integer to plus nhi kr skte yarr smjha kr (line {eline})')
        elif alpha==None:
            try:
               result = eval(code)
            except:
                result = sum(toadd)
            return result
    elif mul in code:
        alpha, num = None, None
        texts, nums, text, numb = 0, 0, None, []
        for tokens in code.split(mul):
            tokens = tokens.strip() 
            if tokens.isnumeric():
                nums+=1
                numb = tokens
                num = True
            elif inqoutes(code, tokens):
                texts+=1
                text = tokens
                alpha = True
            else:
                if tokens in var.vars:
                    if type(var.vars[tokens]) == str:
                        alpha=True
                        text='"'+var.vars[tokens]+'"'
                        texts=1
                    elif type(var.vars[tokens]) == int:
                        nums+=1
                        numb.append(var.vars[tokens])
                        num = True
        if texts+nums > 2:
                er = f'''
    {code}\n{'    '+'~'*(len(code))}
                            '''
                glti(er, f'oops: bhai me 1 se jyada operations nhi kr skta maths kamzor h meri (line {eline})')
        elif alpha and num:
                return text[1:-1]*int(numb[0])
        elif num:
             try:
                  return eval(code)
             except:
                return numb[0]*numb[1]
        else:
            er = f'''
    {code}\n{'    '+'~'*(len(code))}
                            '''
            glti(er, f'SyntaxWaliGalat: bhai yha kuchh gadbad lag rhi h (line {eline})')
    else:
         return None
                
