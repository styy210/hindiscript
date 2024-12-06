import start
from conditions import paraChecker, conditionVarify
import sys
import textwrap
from loops import whileInnit, looplen

def NoErrors(exctype, excvalue, exectraback):
    if exctype == KeyboardInterrupt:
        print('\nThike bhai, bye bhai.')
        sys.exit(1)
    print("Bhai bhai !! an unexpected error has occured in source.")
    sys.exit(1)
class Compiler:
    def __init__(self, scode):
        self.scode = scode
        self.readedLines = 0
        self.ulength = 1
    def compiler(self):
        for index, lines in enumerate(self.scode.splitlines()):
            if (self.ulength+self.readedLines)-1 > index:
                continue
            if lines.strip().startswith('jab tak') or lines.strip().startswith('jabtak'):
                length, con, ctx,  nxtcode = whileInnit('\n'.join(line for line in self.scode.splitlines()[self.readedLines:]))
                nxtcode = self.indRemover(nxtcode)
                self.ulength += length
                break_ = None      
                if nxtcode.strip() != '':
                    while True:
                        if conditionVarify(con, ctx):
                            pass
                        else:
                            break
                        if break_:
                            break
                        rlen1 =  looplen()
                        Compiler(nxtcode).compiler()
                        rlen2=looplen()
                        if rlen1 > rlen2:
                            break
            elif lines.strip().startswith('agar'):
                length, nxtcode = paraChecker('\n'.join(line for line in self.scode.splitlines()[self.readedLines:]))
                self.ulength += length           
                if nxtcode.strip() != '':
                    nxtcode = self.indRemover(nxtcode)
                    Compiler(nxtcode).compiler()
            else:
                self.readedLines += 1
                if lines.strip() == '':
                    continue
                if len(line:=lines.strip().split()) == 1:
                    if not any(line[0].startswith(prefix) for prefix in ['likh', 'chhap', '{', '}', '}nhitoh{', '}nhi', 'rukja', 'soja', 'sabar', 'intezaar', 'khatam', 'puchh', 'int', 'string']):
                        self.undefined(line[0])
                start.runner(lines.strip(), index)
                
    def indRemover(self, code):
        code = textwrap.dedent(code.replace('\t', ' '*4))
        return code
    def undefined(self, line):
        print(f'ERROR::bhai glti hogyi code me:\n    {line}\nbhai ye \'{line}\' kya hai? mujhe nhi pta.')
        sys.exit()

def main(argv):
    if len(argv) > 1:
        try:
            with open(argv[1], 'r') as file:
                scode = file.read()
        except FileNotFoundError:
            print("No such file: bhai ye wali file nhi mil rhi: 'scode.txt'")
        except:
            print('Unkown Error')
        compiler = Compiler(scode)
        compiler.compiler()
    else:
        print(f'''Usage: {sys.argv[0]} file.bks
INFO:    
    Written in: Python3.12
    Dynamically Typed
    So many bugs and unsupported features.         
              ''')
        
if __name__ == '__main__':
    #sys.excepthook = NoErrors
    main(sys.argv)

