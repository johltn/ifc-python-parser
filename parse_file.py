
from lark import Lark

# import pdb; pdb.set_trace()

ifc_parser = Lark(r"""

file: iso header data iso_end
iso: "ISO-10303-21;"
iso_end:"END-ISO-10303-21;"
header: "HEADER" ";" (IDENTIFIER |CHAR |SPECIAL| string )* "ENDSEC" ";"
//data: "DATA" ";" (IDENTIFIER |CHAR |SPECIAL| string )* "ENDSEC" ";"
data: "DATA" ";" record* "ENDSEC" ";"

record: id "=" ifcclass attributes ";"
id: "#" (DIGIT)*
ifcclass:"IFC" IDENTIFIER

attributes: "(" attribute ("," attribute)* ")" 

attribute:  INT | REAL| string | SPECIAL | attributes

string    : "\"" ( WORD | ESCAPE | expansion ) * "\""
expansion : "$" IDENTIFIER




SPECIAL : "!"  
		| "'"
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
IDENTIFIER: ("A" .. "Z" | "a" .. "z") ("A" .. "Z" | "a" .. "z" | "0" .. "9") *
ESCAPE    : "\\" ( "$" | "\"" | CHAR )
CHAR      : /[^$"\n]/
WORD      : CHAR +
HASHTAG : "#"

%ignore "\n"

""", start='record')

f = open("Duplex_A_20110505.ifc", "r")

text = f.read() 
text = """
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('0001','2011-05-05T12:10:27',(''),(''),'Autodesk Revit Architecture 2011 - 1.0','20100326_1700','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCORGANIZATION($,'Autodesk Revit Architecture 2011',$,$,$);
#2=IFCAPPLICATION(#1,'2011','Autodesk Revit Architecture 2011','Revit');
#4=IFCCARTESIANPOINT((0.,0.));
#5=IFCDIRECTION((1.,0.,0.));
ENDSEC;
END-ISO-10303-21;
"""
text= "#74=IFCCARTESIANPOINT((-0.,3.582999999999995), "a");"
# text = "3.582999999999995"

tree = ifc_parser.parse(text)

print(dir(tree))
print(tree.pretty())

# record = ifc_parser.parse(text)



