INPUT OFF
VERBOFF
INPUT ON
LAYOUT INPUT "tmp:LABEL1"
PP104,41:AN7
DIR4
NASC 8
FT "Univers",18,0,99
PT "~{friendlyname}"
PP166,41:FT "Univers"
FONTSIZE 10
FONTSLANT 15
PT "~{scientificname}"
FONTSLANT 0
PP74,41:PT "Produktnavn / Product name / ~{productinthirdlanguage}"
PP237,1200:AN1
DIR2
PL1181,6
PP200,41:AN7
DIR4
PT "Production method:"
PP24,41:PT "GTIN: ~{gtin}"
PP256,41:PT "Size:"
PP348,214:PT "~{processingmethod}"
PP460,41:PT "Catch date:"
PP501,41:PT "Prod date:"

PP556,41:FONTSIZE 12
PT "Net weight:"
PP606,122:FONTSIZE 19
PT "~{weight} kg"
PP680,41:FONTSIZE 19
PT "~{customer}"
PP259,462:BARSET "CODE128C",2,1,4,112
PB CHR$(128);"0~{gtin}10~{batchno}"
PP369,571:FONTSIZE 11
PT "(01) 0~{gtin} (10) ~{batchno}"

PP436,594:BARSET "CODE128C",2,1,4,112
PB CHR$(128); "11~{proddate}3102~{weightflat}"
PP546,700:PT "(11) ~{proddate} (3102) ~{weightflat}"

PP612,550:BARSET "CODE128C",2,1,4,112
PB CHR$(128);"00370333500011222549"
PP723,667:PT "(00) 3 7033350 001122254 9"

PP256,214:FONTSIZE 10
PT "~{grade}"
PP348,41:PT "Treatment:"
PP395,41:PT "Preservation:"
PP395,214:PT "Alive"
PP460,214:PT "~{catchdate}"
PP501,214:PT "~{productiondatetime}"
PP200,328:PT "Handpicked"
PP200,578:PT "Origin:"
PP200,712:PT "FAO 27 IIa, Norwegian Sea"
PP166,578:PT "Batch no:"
PP166,712:PT "~{batchno}"
PP25,578:PT "Exp.:"
PP25,649:PT "Statsnail AS"
PP60,649:PT "7165 Oksvoll, NORWAY"
PP300,41:PT "pcs/kg:"
PP300,214:PT "~{pcskg}"

PRPOS 0,985
PRIMAGE "SNAIL150X125.PCX"

PRPOS 125,990
PRIMAGE "EFTA150X81.PCX"
LAYOUT END
VERBOFF