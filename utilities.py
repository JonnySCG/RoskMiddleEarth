def estrapola(testo,divisore,posizione):
	stringhetta=testo.split(divisore)
	print(stringhetta)

	return stringhetta[posizione]

def responseHTTP(risposta,codice):
	
	return "HTTP/1.1 {} \r\n\r\n {}".format(codice,risposta)

def debug(out,LEVEL):
	LEVEL_OUT = 6

	if LEVEL> LEVEL_OUT:
		print(out)

def parser(oggetto,json,match):
	
	oggetti=[]

	for o in json:

		oggetti.append(oggetto(o,match))
		
	return oggetti
