from game.Terminal.message_type import MessageType

class StoryManager:
    def __init__(self, story_json, terminal_controller, session, ai_assitant, input_manager):
        self.story = story_json
        self.terminal = terminal_controller
        self.session = session
        self.ai = ai_assitant
        self.input_manager = input_manager
        self.current_node =  "Tutorial-1" #"Confirmacao"

        self.terminal.on_sent_message = self.handler_input
        self.show_current_node()

    def show_current_node(self):
        node = self.story.get(self.current_node)

        if not node:
            self.terminal.send_message("Fim da história ou erro - isso não faz parte do jogo é erro real.", MessageType.SIMULACAO)
            return 
        
        for item in node["text_body"]:
            if item["type"] == "MASCOTE":
                text = self.ai.rewrite_text(item["text"])
                self.terminal.send_message_slowly(text, MessageType.MASCOTE, on_finish=lambda:self.call_terminal_options(node))
            else:
                self.terminal.send_message(item["text"], MessageType[item["type"]])
        
        if not item["type"] == "MASCOTE":
            self.call_terminal_options(node)

    def call_terminal_options(self, node):
        # Mostra escolhas ou libera input livre
        if node.get("choices"):
            options = [choice["text"] for choice in node["choices"]]
            self.terminal.show_options(options)
        else:
            # deveria ter algo pra indicar que o input é livre ?
            pass
        
    
    def handler_input(self, user_input):
        node = self.story.get(self.current_node)

        result = self.input_manager.process_input(user_input,node,self.current_node)

        if result["type"] == "choice":
            self.current_node = result["target"]

            if result.get("flag"):
                self.session.set_flag(result["flag"], True)

            if result.get("knoledge"):
                self.session.mascot.personality_manager.add_knoledge(result["knoledge"])

            personality_changes = result.get("personality")
            if result.get("personality"):
                for key, value in personality_changes.items():
                    if key == "auto_consciencia":
                        self.session.mascot.personality_manager.update_autoconsciencia(value)
                    elif key in ["felicidade", "tristeza", "raiva", "medo", "confiança"]:
                        self.session.mascot.personality_manager.update_emotion(key, value)
                    elif key in ["amizade", "medo", "confiança"]:
                        self.session.mascot.personality_manager.update_relation(key, value)
                    elif key in ["valoriza_a_vida", "exploracao", "autoconhecimento", "moralidade"]:
                        self.session.mascot.personality_manager.update_value(key, value)

            self.show_current_node()
        
        elif result["type"] == "free":
            self.terminal.send_message(result["response"], MessageType.MASCOTE)

        elif result["type"] == "personality":
            self.session.mascot.personality_manager.update_personality(result["response"])
            self.terminal.send_message("Consciência alimentada: pronto para iniciar", MessageType.SIMULACAO)
            self.current_node = "Confirmacao"
            self.show_current_node()

        else:
            self.terminal.send_message(">>> Input inválido.", MessageType.SIMULACAO)

