try:
    from ctransformers import AutoModelForCausalLM
except ImportError:
    AutoModelForCausalLM = None

from config import MODEL_PATH
import asyncio

class LocalAI:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path
        self.model = None

    async def load(self):
        if AutoModelForCausalLM is None:
            self.model = None
            return
        loop = asyncio.get_event_loop()
        self.model = await loop.run_in_executor(None, lambda: AutoModelForCausalLM.from_pretrained(self.model_path, model_type="mistral", gpu_layers=0, context_length=2048, quantized=True) if AutoModelForCausalLM else None)

    async def ask(self, prompt: str, max_new_tokens=128, temperature=0.7) -> str:
        if self.model is None:
            await self.load()
        if self.model is None:
            return "Ошибка: модель не загружена."
        loop = asyncio.get_event_loop()
        if callable(self.model):
            return await loop.run_in_executor(None, lambda: self.model(prompt, max_new_tokens=max_new_tokens, temperature=temperature))
        else:
            return "Ошибка: модель не поддерживает вызов."

ai_instance = LocalAI() 