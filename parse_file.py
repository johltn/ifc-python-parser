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

#f = open("files/acad2010_walls.ifc", "r")

text = f.read() 

start_time = time.time()
tree = ifc_parser.parse(text)

print("--- %s seconds ---" % (time.time() - start_time))

header = tree.children[0]

for filerecord in header.children:
        if filerecord.children[0].children[0] == 'SCHEMA':
                schema_tree = filerecord.children[1]
                schema_string = schema_tree.children[0].children[0].children[0].children[0]
                char_list = [c[0] for c in schema_string.children ]
                schema = "".join(char_list)     

data = tree.children[1]

test_record = data.children[42]

entities = {}

def process_attributes(attributes_tree):
        attributes = []
        for a in attributes_tree.children:
                if a.children[0].data == 'tup':
                        attributes.append(process_attributes(a.children[0]))
                elif a.children[0].data == 'string' :
                        attributes.append(a)
                elif a.children[0].data == 'id' :
                        attributes.append(a)
                else:
                        attributes.append(a)

        return attributes

class T(Transformer):
        def id(self, s):
                num_list = [str(n) for n in s ]
                word = int("".join(num_list))
                return word

def create_entity(record):
        id_tree = record.children[0]
        file_id = T(visit_tokens=True).transform(id_tree)
        
        ifc_type = "IFC" + record.children[1].children[0]
       
        attributes_tree = record.children[2]
        attributes = process_attributes(attributes_tree)

      
create_entity(test_record)

