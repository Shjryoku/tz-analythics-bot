import json
import requests
import re

from llm.prompt import PROMPT_LLM
from config import Config
from requests.exceptions import RequestException

def extract_json(text: str) -> dict:
    # извлекаем json из текста llm
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("JSON не найден")
    return json.loads(match.group())

def parse_query(user_txt: str) -> dict:
    # формируем промпт для llm
    prompt = f"""
    {PROMPT_LLM}
    
    Запрос пользователя:
    {user_txt}
    
    Ответ(JSON):
    """
    
    try:
        # конфигурация llm
        response = requests.post(
            Config.OLLAMA_URL,
            json={
                "model": Config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            }
        )
        response.raise_for_status()
        
        # ответ от llm
        raw = response.json().get("response", "").strip()
        print("LLM raw response:", raw)
        return extract_json(raw)
    
    except json.JSONDecodeError:
        return {
            "error": "invalid_json_from_llm",
            "raw_response": "raw",
        }
    
    except requests.RequestException as jsE:
        print("Request exception:", repr(jsE))
        return {
            "error": "ollama_request_failed",
            "detailed": str(jsE),
        }
        
    except Exception as e:
        print("LLM exception:", repr(e))
        return {
            "error": "llm_error",
            "details": str(e),
        }