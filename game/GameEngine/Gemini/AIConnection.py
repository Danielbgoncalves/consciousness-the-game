import os
import json
from dotenv import load_dotenv

try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False


class AIConnection:
    """Conexão com a API GenAI (Gemini).
    Tenta selecionar dinamicamente um modelo a partir de preferências
    e fornece um fallback em JSON lendo o `story_map.json` local se a
    API não estiver acessível.
    """

    DEFAULT_MODELS = [
        'gemini-1.5-mini',
        'gemini-1.5-small',
        'gemini-1.0',
    ]

    def __init__(self, models=None, enable_fallback=True):
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'secrets', '.env'))
        load_dotenv(env_path)

        api_key = os.getenv('GENAI_API_KEY')
        pref = os.getenv('GENAI_MODEL_PREFERENCES')
        if pref:
            models_env = [m.strip() for m in pref.split(',') if m.strip()]
        else:
            models_env = None

        self.enable_fallback = enable_fallback
        self.models = models or models_env or self.DEFAULT_MODELS
        self.model_name = None
        self.model_chat = None

        if api_key and HAS_GENAI:
            genai.configure(api_key=api_key)
            last_exc = None
            for m in self.models:
                try:
                    model = genai.GenerativeModel(m)
                    self.model_chat = model.start_chat()
                    self.model_name = m
                    break
                except Exception as e:
                    last_exc = e
            if self.model_chat is None and not self.enable_fallback:
                raise RuntimeError(f'Não foi possível inicializar nenhum modelo: {last_exc}')
        else:
            # Sem chave ou sem biblioteca `google.generativeai` — apenas fallback
            if not self.enable_fallback:
                if not api_key:
                    raise RuntimeError('Chave da API não encontrada. Defina GENAI_API_KEY em secrets/.env ou no ambiente.')
                if not HAS_GENAI:
                    raise RuntimeError('google.generativeai não está instalado no ambiente.')

    def send_prompt(self, prompt, raw_json_on_error=True):
        """Envia `prompt` ao modelo configurado.

        - Se um modelo estiver ativo, retorna a string de texto da resposta.
        - Em caso de erro de rede/API e `raw_json_on_error=True`, retorna um dicionário JSON-like de fallback.
        """
        if self.model_chat is None:
            return json.dumps(self._fallback_response(prompt, reason='no_model_configured'), ensure_ascii=False)

        try:
            response = self.model_chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            if raw_json_on_error:
                return json.dumps(self._fallback_response(prompt, reason=str(e)), ensure_ascii=False)
            raise

    def _fallback_response(self, prompt, reason=None):
        """Gera uma resposta de fallback em formato JSON-like.

        Tenta carregar `story_map.json` que está em `game/GameEngine/story_map.json`
        e retorna uma pré-visualização útil junto com o `prompt` e o motivo do fallback.
        """
        gm = {
            'ok': False,
            'reason': reason,
            'source': None,
            'prompt': prompt,
        }

        story_map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'story_map.json'))
        try:
            with open(story_map_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Monta preview e tenta extrair um texto de resposta "padrão".
            preview = None
            response_text = None
            if isinstance(data, dict):
                preview = {'top_keys': list(data.keys())[:10]}

                # Prioriza nó `Carga-inicial` quando disponível
                if 'Carga-inicial' in data and isinstance(data['Carga-inicial'].get('text_body'), list):
                    first = data['Carga-inicial']['text_body'][0]
                    response_text = first.get('text') if isinstance(first, dict) else None
                else:
                    # fallback: pega o primeiro nó e seu primeiro texto
                    for k, v in data.items():
                        if isinstance(v.get('text_body'), list) and v['text_body']:
                            first = v['text_body'][0]
                            response_text = first.get('text') if isinstance(first, dict) else None
                            break
            elif isinstance(data, list):
                preview = {'first_items': data[:3]}
                if data:
                    item = data[0]
                    if isinstance(item, dict) and 'text' in item:
                        response_text = item.get('text')
            else:
                preview = {'type': type(data).__name__}

            gm.update({'source': 'local_story_map', 'preview': preview, 'response': response_text})
        except Exception as e2:
            gm.update({'source': 'none', 'preview': None, 'response': None, 'load_error': str(e2)})

        return gm

'''def create_personalite(base_of_knoledge):
    prompt = ( 
        f"Você é vai gerar a personalidade de um filhote com base em uam entrada de texto."       
        "Sinta cada letra, cada poesia e significados dos texto base e gere uma string de caracteristicas"
        f"Text:  "
        ""
        "Responda apenas com o texto reescrito, sem explicações de "
        "qualquer tipo. Se achar que ocorreu algo de errado e não puder "
        "responder de acordo, responda apenas o texto base de entrada."
   )
        
    response = model.generate_content(prompt)

    return response.text.strip() #.replace('\n', ' ')


def rewrite(base_text, personality):
    prompt = ( 
        f"Você é um filhote {personality}."       
        "Reescreva o seguinte texto de a cordo com sua personalidade, mantenha o mesmo significado"
        f"Text: '{base_text}' "
        ""
        "Responda apenas com o texto reescrito, sem explicações de "
        "qualquer tipo. Se achar que ocorreu algo de errado e não puder "
        "responder de acordo, responda apenas o texto base de entrada."
   )
        
    response = model.generate_content(prompt)

    return response.text.strip() #.replace('\n', ' ')

resposta = rewrite("Onde eu estou ? Que cheiro é esse ? Quem é voce ?", "medrosa, autoconfiante em sí, preocupada com o mundo")
print(resposta)'''