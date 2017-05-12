def parser(oggetto,json):
	oggetti=[]

	for o in json:
		oggetti.append(oggetto())
		
		for prop in o:
			oggetti[len(oggetti)-1][prop]=json[prop]

	return oggetti
