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

        # Terceia parte do prompt
        with open(prompt_p2_path, "r") as arquivo:
            prompt += arquivo.read()

        return prompt

    def _call_tool(self, response: str) -> str: