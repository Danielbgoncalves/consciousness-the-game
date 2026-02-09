class InputManager:
    def __init__(self,ai_assistant):
        self.ai = ai_assistant

    def process_input(self, user_input, node, node_name):
        
        '''
        Processa o input do usuario com base no nó atual
        Retorna um dicionário:
        {
            type: choise | free | invalid
            target: Node 
            flag: flag (se tiver)
            response: text (se for input livre)
        }
        '''

        user_input = user_input.strip().lower()

        # Se for multipla escolha
        if node.get("choices"):
            # verifica se está por extenso
            for option in node.get("choices"):
                if user_input == option["text"].lower():
                    return {
                        "type": "choice",
                        "target": option["target"],
                        "flag": option.get("flag"),
                        "knoledge": option.get("knoledge"),
                        "personality": option.get("personality")
                    }

            try:
                idx = int(user_input) - 1
                if 0<= idx < len(node["choices"]):
                    chosen = node["choices"][idx]
                    return {
                        "type": "choice",
                        "target": chosen["target"],
                        "flag": option.get("flag"),
                        "knoledge": option.get("knoledge"),
                        "personality": option.get("personality")
                    }
            except ValueError:
                pass # Não era número então
            
            # era multiplaescolha e não teve entrada válida
            return {"type": "invalid"}
        
        # Se não é multiplaescolha -> carga inicial ou input livre
        if node_name == "Carga-inicial":
            response = self.ai.generate_personality_from_text(user_input)

            return {
                "type": "personality",
                "response": response
            }
            
        else:
            response = self.ai.get_response(user_input)

            return {
                "type": "free",
                "response": response
            }
            
