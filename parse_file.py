from lark import Lark, Transformer
import time

# import pdb; pdb.set_trace()
ifc_parser = Lark(r"""

file: "ISO-10303-21;" header data "END-ISO-10303-21;"

header: "HEADER" ";" filerecord* "ENDSEC" ";"
data: "DATA" ";" record* "ENDSEC" ";"
filerecord: filedecl attributes ";"
record: id "=" ifcclass attributes ";"
id: "#" (DIGIT)*
ifcclass:"IFC" IDENTIFIER
filedecl : "FILE_" IDENTIFIER

tup: "(" attribute ("," attribute)* ")" | "()"

attributes: "(" attribute ("," attribute)* ")" | "()" 

attribute:  STAR| NONE | INT | REAL | enumeration |id|ifcclass attributes|string |tup 

enumeration: "." (IDENTIFIER|"_")* "."

string: "'" (SPECIAL|DIGIT|LCASE_LETTER|UCASE_LETTER)* "'"


WO:(LCASE_LETTER)*
STAR: "*"
NONE: "$"
expansion : "$" IDENTIFIER

SPECIAL : "!"  
        | "*" 
        | "$" 
        | "%" 
        | "&" 
        | "." 
        | "#" 
        | "+" 
        | "," 
        | "-" 
        | "(" 
        | ")" 
        | "?" 
        | "/" 
        | ":" 
        | ";" 
        | "<" 
        | "=" 
        | ">" 
        | "@" 
        | "[" 
        | "]" 
        | "{" 
        | "|" 
        | "}" 
        | "^" 
        | "`" 
        | "~"
        | "_"

real: REAL
REAL: SIGN?  DIGIT  (DIGIT)* "." (DIGIT)* ("E"  SIGN  DIGIT (DIGIT)* )?
INT: SIGN? DIGIT  (DIGIT)* 
DIGIT: "0".."9"
SIGN: "+"|"-"

LCASE_LETTER: "a".."z"
UCASE_LETTER: "A".."Z"

IDENTIFIER: ("A" .. "Z" | "a" .. "z") ("A" .. "Z" | "a" .. "z" | "0" .. "9")*
ESCAPE    : "\\" ( "$" | "\"" | CHAR )
CHAR      : /[^$"\n]/
WORD      : CHAR+
HASHTAG : "#"

WS: /[ \t\f\r\n]/+
%ignore WS

%ignore "\n"

""", parser='lalr', start='file')

f = open("files/Duplex_A_20110505.ifc", "r")


text = f.read() 

start_time = time.time()
tree = ifc_parser.parse(text)

print(len(tree.children))

for c in tree.children:
        print(c.data)

print("--- %s seconds ---" % (time.time() - start_time))




