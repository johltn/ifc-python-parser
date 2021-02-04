
from lark import Lark

# import pdb; pdb.set_trace()

ifc_parser = Lark(r"""

file: iso header
iso: "ISO-10303-21;"
header: "HEADER" ";" (IDENTIFIER |CHAR | string )* "ENDSEC" ";"
string    : "\"" ( WORD | ESCAPE | expansion ) * "\""
expansion : "$" IDENTIFIER

IDENTIFIER: ("A" .. "Z" | "a" .. "z") ("A" .. "Z" | "a" .. "z" | "0" .. "9") *
ESCAPE    : "\\" ( "$" | "\"" | CHAR )
CHAR      : /[^$"\n]/
WORD      : CHAR +

%ignore "\n"

""", start='file')

f = open("Duplex_A_20110505.ifc", "r")

text = f.read() 
text = """
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('0001','2011-05-05T12:10:27',(''),(''),'Autodesk Revit Architecture 2011 - 1.0','20100326_1700','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
"""
tree = ifc_parser.parse(text)

