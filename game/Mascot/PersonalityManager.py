import json

class PersonalityManager:
    def __init__(self,filepath="personality.json"):
        self.filepath = filepath
        self.personality = { # opção default
            "caracteristicas_gerais": ["curiosa", "ingenua"],
            "emocoes": {
                "felicidade": 5,
                "tristeza": 5,
                "raiva": 5,
                "medo": 5,
                "confianca": 5
            },
            "valores": {
                "valoriza_a_vida": 5,
                "exploracao": 5,
                "autoconhecimento": 5,
                "moralidade": 5
            },
            "autoconsciencia": 1,
            "relacao_com_o_jogador": {
                "amizade": 5,
                "intimidade": 5,
                "medo": 1
            },
            "conhecimentos":[]
        }
    
    def load(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self.personality = json.load(f)
                print("personalidade carregada")
        except FileNotFoundError:
            print("Arquivo de personalidade não encontrado. Usando padrão")
    
    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.personality, f, indent=4, ensure_ascii=False)
            print("Personalidade salva")
    
    def update_emotion(self, emotion, amount):
        if emotion in self.personality["emocoes"]:
            self.personality["emocoes"][emotion] = max(0,min(10,self.personality["emocoes"][emotion] + amount))

    def update_value(self, value, amount):
        if value in self.personality["valores"]:
            self.personality["valores"][value] = max(0,min(10,self.personality["valores"][value] + amount))

    def update_autoconsciencia(self, amount):
            self.personality["autoconsciencia"] = max(0, min(10, self.personality["autoconsciencia"] + amount))


    def update_relation(self, relation,amount):
         if relation in self.personality["relacao_com_o_jogador"]:
            self.personality["relacao_com_o_jogador"][relation] = max(0,min(10,self.personality["relacao_com_o_jogador"][relation] + amount))

    def update_personality(self, new_personality):
        self.personality = new_personality

    def get_personality_context(self):
        return json.dums(self.personality, ensure_ascii=False)
    
    def add_knoledge(self, knoledge):
        if not knoledge:
            return # Ignora none, vazio, ...
        
        if isinstance(knoledge, list):
            for k in knoledge:
                if not k in self.personality['conhecimentos']:
                    self.personality['conhecimentos'].append(k)
        else:
            if not k in self.personality['conhecimentos']:
                self.personality['conhecimentos'].append(knoledge)



