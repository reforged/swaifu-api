from BDD.Database import Database
import json
import pprintpp

class RequetesFormatTxt(Database):

    def __init__(self):
        pass

    def reqSelect(self, f):
        if(self.select == ["*"]):
            return f
        returned_list = []
        for i in f:
            temporary_dic = {}
            for j in self.select:
                temporary_dic[j[0]+"."+j[1]] = i[j[0]+"."+j[1]]
            returned_list.append(temporary_dic)
        return(returned_list)
    
    
    def reqWhere(self, f):
        returned_list = []
        for i in f:
            possible = True
            for j in self.where:
                if( i[j[0]+"."+j[1]] != j[2]):
                    possible = False
            if possible:
                returned_list.append(i)
        return(returned_list)
    
    def fusion(self, d1, d2, cond):
        """
        fusionne deux dictionnaires sans dupliquer la valeur dans la condition et en renommant tout
        """
        returned_dic = {}
        if(len(d2.keys()) > 0):
            for i in d1.keys():
                returned_dic[i] = d1[i]
            for i in d2.keys():
                if i != cond[1][1]:
                    returned_dic[i] = d2[i]
        return returned_dic   

    def detect(self, d, cond, value): 
        """
        regarde dans un dictionnaire si la clé de valeur cond a pour valeur value
        """
        return d[cond] == value

    def modifNomsFile(self, f, name):
        """
        modifie les noms de tout les attributs dans une table en y rajoutant name +"." avant
        """
        returned_list = []
        for i in range(len(f)):
            returned_list.append({})
            for j in f[i].keys():
                returned_list[i][name+"."+j] = f[i][j]
        return returned_list    

    def modifAllFiles(self, fs):
        """
        modifie les noms de tout les attributs dans un fichier avec plusieurs tables en y rajoutant name +"." avant
        """
        for i in fs.keys():
            fs[i] = self.modifNomsFile(fs[i], i)
        return fs


    def reqFrom(self, f):
        old_f = f[self.from_req["cond"][0][0][0]]
        new_f = []
        returned_list = []
        for condition in self.from_req["cond"]:
            for table in old_f:
                for table2 in f[condition[1][0]]:
                    if self.detect(table2, condition[1][0]+"."+condition[1][1], table[condition[0][0]+"."+condition[0][1]]):
                        new_f.append(self.fusion(table, table2, condition))
            old_f = new_f
            new_f = []
        return old_f

    

    def query(self, request):
        self.file = {}
        for i in request["from"]["tables"]:
            f = open("BDD/BDD_Fichiers/Donnees/"+i+".json")
            self.file[i] = json.load(f)
            f.close()


        self.select = request.get("select", ["*"])
        self.where = request.get("where", [])
        self.from_req = request.get("from", {})

        self.inner_table = self.reqSelect(self.reqWhere(self.reqFrom(self.modifAllFiles(self.file))))
        return(self.inner_table)
        
    def execute(self, request):
        f = open("BDD/BDD_Fichiers/Donnees/"+request["table"]+".json")
        self.file = json.load(f)
        f.close()
        self.dic = {}
        for i in request["valeurs"]:
            self.dic[i[0]] = i[1]
        self.file.append(self.dic)
        f = open("donnees/"+request["table"]+".json", "w")
        #f.write(json.dumps(self.file))
        f.write(json.dumps(self.file, indent=4))
    


b = {
	"select" : [
        ["Ex_Donnee", "name"],
        ["Ex_Donnee", "email"], 
        ["Ex_Donnee3", "label"],
        ["Ex_Donnee2", "id"],
        ["Ex_Donnee4", "id"]
    ],
	"from": {
		"tables": ["Ex_Donnee", "Ex_Donnee2", "Ex_Donnee3", "Ex_Donnee4"],
        "cond" : [
            [
                ["Ex_Donnee", "id"],
                ["Ex_Donnee2", "user_id"]
            ],
            [
                ["Ex_Donnee2", "permission_id"],
                ["Ex_Donnee3", "id"]
            ],
            [
                ["Ex_Donnee2", "id"],
                ["Ex_Donnee4", "id_autre"]
            ]
        ]
	},
    "where": [
        ["Ex_Donnee", "name" , "fabriceleplubo"]
    ]

}

c = {
	"table": "Ex_Donnee",

	"valeurs": [
		["id", "1246"],
		["email", "encoreunmail@mail.mail"],
		["name", "Mr.Man"],
		["password", "thebestmotdepasse"]

	]
}
a = RequetesFormatTxt()
pprintpp.pprint(a.query(b))
a.execute(c)