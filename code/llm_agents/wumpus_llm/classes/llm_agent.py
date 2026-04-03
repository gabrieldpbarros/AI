import yaml
import json
from pathlib import Path
from langchain_groq import ChatGroq

CURRENT_PATH = Path(__file__).resolve()
ROOT = CURRENT_PATH.parent.parent

class LLMAgent:
    def __init__(self, user_prompt: str):
        self.user_text = user_prompt
        self.assistant_text = None
        self.system_text = self._get_sys_prompt()
        self.llm = self._init_llm()

    def _init_llm(self):
        llm = ChatGroq(
            model="qwen/qwen3-32b",
            api_key=self._get_keys(),
            temperature=0.0,
            reasoning_format="parsed" # facilita a remoção do print do raciocínio
        )
        return llm
    
    def _get_keys(self) -> str:
        yaml_path = ROOT / "info" / "keys.yaml"

        with open(yaml_path, "r") as arquivo:
            yaml_arc = yaml.safe_load(arquivo)
        
        return yaml_arc["GROQ_API_KEY"]
    
    def _get_sys_prompt(self) -> str:
        prompt = ""
        info_path = ROOT / "info"

        prompt_p1_path = info_path / "system_prompt1.txt"
        tools_path = info_path / "tools.json"
        prompt_p2_path = info_path / "system_prompt2.txt"

        # Primeira parte do prompt
        with open(prompt_p1_path, "r") as arquivo:
            prompt += arquivo.read()
            prompt += "\n"

        # Ferramentas (segunda parte)
        with open(tools_path, "r") as arquivo:
            tools_dict = json.load(arquivo)
            prompt += json.dumps(tools_dict, indent=4, ensure_ascii=False)
            prompt += "\n\n"

        # Terceira parte do prompt
        with open(prompt_p2_path, "r") as arquivo:
            prompt += arquivo.read()

        return prompt

    def _andar(self, direcao: str):
        pass

    def _atirar(self, direcao: str):
        pass

    def _pegar_ouro(self):
        pass

    def _escalar_saida(self):
        pass

    def _call_tool(self, response: str) -> str:
        tool_call = json.loads(response.split("Action:")[1])
        kwargs = tool_call["action_input"]
        match tool_call["action"]:
            case "andar":
                return self._andar(**kwargs)
            case "atirar":
                return self._atirar()
            case "pegar_ouro":
                return self._pegar_ouro(**kwargs)
            case "escalar_saida":
                return self._escalar_saida(**kwargs)
            case _:
                return f'A ferramenta "{tool_call["action"]}" não existe. Confirme as funções disponíveis.'