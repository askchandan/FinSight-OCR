from ollama import Client
from src.utils.logger import Logger


class LLMModel:

    def __init__(self, model_name: str):
        self.model_name = model_name
        
        
        self.logger = Logger("LLM_MODEL", "./logs/llm.log").get_logger()
        self.logger.info(f"Initializing LLMModel with: {model_name}")

        
        self.client = Client()


    def generate(self, prompt: str, image_path: str = None):

        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            }

            
            if image_path:
                payload["images"] = [image_path]
                self.logger.info(f"Sending image to model: {image_path}")

            self.logger.debug(f"Prompt sent to LLM:\n{prompt[:300]}...\n")

           
            response = self.client.generate(**payload)

            
            output = response.get("response", "")

            self.logger.debug(f"Raw LLM Output: {output[:300]}...")
            return output

        except Exception as e:
            self.logger.error(f"LLM Generation Error: {str(e)}")
            return ""
