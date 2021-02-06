from lark import Lark
import time

# import pdb; pdb.set_trace()
ifc_parser = Lark(r"""

file: iso header data iso_end
iso: "ISO-10303-21;"
iso_end:"END-ISO-10303-21;"
header: "HEADER" ";" filerecord* "ENDSEC" ";"
data: "DATA" ";" record* "ENDSEC" ";"
filerecord: filedecl attributes ";"
record: id "=" ifcclass attributes ";"
id: "#" (DIGIT)*
ifcclass:"IFC" IDENTIFIER
filedecl : "FILE_" IDENTIFIER

attributes: "(" attribute ("," attribute)* ")" | "()" 

attribute:  STAR| NONE | INT | REAL | enumeration |id|ifcclass attributes|string |attributes 

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

f = open("Duplex_A_20110505.ifc", "r")


text = f.read() 
# text = """
# ISO-10303-21;
# HEADER;
# FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
# FILE_NAME('0001','2011-05-05T12:10:27',(''),(''),'Autodesk Revit Architecture 2011 - 1.0','20100326_1700','');
# FILE_SCHEMA(('IFC2X3'));
# ENDSEC;
# DATA;
# #1=IFCORGANIZATION($,'Autodesk Revit Architecture 2011',$,$,$);
# #2=IFCAPPLICATION(#1,'2011','Autodesk Revit Architecture 2011','Revit');
# #4=IFCCARTESIANPOINT((0.,0.));
# #5=IFCDIRECTION((1.,0.,0.));
# ENDSEC;
# END-ISO-10303-21;
# """
# text= "#229=IFCSHAPEREPRESENTATION(#27,'Body','SweptSolid',(#226));"
# text = "3.582999999999995"
# text = "#15=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);"

start_time = time.time()

tree = ifc_parser.parse(text)

print("--- %s seconds ---" % (time.time() - start_time))


print(len(tree.children))
print(dir(tree))
print(tree.data)

for c in tree.children:
        print(c.data)
        if c.data == 'header':
                header = c
        if c.data == 'data':
                data = c


for c in header.children:
        print(c.data)

record = data.children[45]


