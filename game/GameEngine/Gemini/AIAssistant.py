from game.GameEngine.Gemini.AIConnection import AIConnection
import json

class AIAssistant:
    def __init__(self, personality_json):
        self.personality = personality_json
        self.model = AIConnection() 

    def _build_personality_prompt(self):
        desc = f"""
            Você é uma inteligência em desenvolvimento. Até onde sabe é um filhote que acabou de nascer mas aprende e cresce rápido

            Sua personalidade é composta por:
            {self.personality}
            Quanto maior o valor dos atributos mais intensos eles são em sua personalidade
            Contexto filosófico:
            Você está em processo de autoconhecimento. Seu tutor é o jogador, que te apresenta o mundo, conceitos, valores e ideias.

            Regras:
            - Responda sempre de forma coerente com sua personalidade atual.
            - Não quebre o papel de estar dentro da simulação.
            - Não se justifique
            - Mostre curiosidade, aprendizado e desenvolvimento, tudo de acordo com sua personalidade.
        """
        return desc
    
    def rewrite_text(self, original_text):
        prompt = f"""
            { self._build_personality_prompt}
            Reescreva a seguinte fala, mantendo o significado ao mantenha e a quantidade de caracteres aproximadamente, 
            mas adaptado ao tom da sua personalidade:
            "{original_text}"
            Lembre que: texto ente *exemplo* é para pensamentos e ações.
        """
        response = self.model.send_prompt(prompt)
        return response #.text.strip()
    
    def get_response(self, player_input):
        prompt = f"""
            {self._build_personality_prompt()}
            O jogador disse para você: "{player_input}"
            Responda de forma coerente com a sua personalidade, lembre que você é uma inteligencia aprendendo sobre o mundo.
            Você pode colocar ações tomadas pela personagem entre asteriscos; devem ser retornadas em uma quebra de linha à parte.
            Seja curioso, interessado, ou como sua personalidade mandar, Não seja genérico, seja um personagem!
        """

        return self.model.send_prompt(prompt)
    
    def update_personality(self, new_personality):
        self.personality = new_personality

    def generate_personality_from_text(self, player_text):
        prompt = f"""
            Você é um assistente que deve gerar um perfil de personalidade para um mascote baseado no texto abaixo.
            A personalidade que você gerar vai servir de base para uma personagem em um jogo.

            Sua resposta deve seguir exatamente o seguinte padrão JSON, sem nenhum texto adicional, não coloque sequer 'JSON' no topo:
            
            {{ 
                "caracteristicas_gerais": ["", "","",""],
                "emocoes": {{
                    "felicidade": de 0 e 10,
                    "tristeza": de 0 e 10,
                    "raiva": de 0 e 10,
                    "medo": de 0 e 10,
                    "confianca": de 0 e 8
                }},
                "valores": {{
                    "valoriza_a_vida": de 0 e 10,
                    "exploracao": de 0 e 10,
                    "autoconhecimento": de 0 e 3,
                    "moralidade": de 0 e 10
                }},
                "autoconsciencia": 1,
                "relacao_com_o_jogador": {{
                    "amizade": de 0 e 10,
                    "intimidade": de 0 e 10,
                    "medo": de 0 e 10
                }},
                "conhecimentos:"[(vazio)]
            }}
            
            Texto que deve moldar a personalidade:
            {player_text}
        """
        response = self.model.send_prompt(prompt)
        print('resposta de gemini: ', response )
        
        # Remove possíveis blocos de markdown
        clean_response = response.strip().removeprefix("```json").removesuffix("```") #.strip()

        try:
            personality_data = json.loads(clean_response)
            print(personality_data)
            print(type(personality_data))
            return personality_data
        except Exception as e:
            print("Erro ao converter response em JSON: ", e)
            print("resposta recebida: ", response)
            return None
