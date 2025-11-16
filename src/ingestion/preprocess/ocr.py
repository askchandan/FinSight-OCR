from ollama import Client
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from src.utils.logger import Logger
import os
import re
import json


load_dotenv()


OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')

class BankStatementOCR:

    def __init__(
            self, 
            input_dir='./data/extracted/images/', 
            output_dir='./data/output/', 
            model=MODEL_NAME
            ):
        
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True,exist_ok=True)
        self.model = model
        self.logger = Logger("OCR", "./logs/ocr.log").get_logger()
        self.logger.info("OCR Class initialized")
    
        self.client = Client()

    
    def parse_llm(self, image_path):

        self.logger.info('LLM : QWEN2.5-vl:7b Parsing Started')

        prompt = """
            Analyze this bank statement image and extract the following information in JSON format.
            If any information is not found, use null for that field.
            
            Required fields to extract:
            1. bank_name: Name of the bank
            2. account_number: Account number (remove all non-digits)
            3. account_holder_name: Name of account holder (if available)
            4. phone_number: Contact phone number (if available)
            5. statement_from_date: Start date of statement period (as string, e.g., "01-01-2024")
            6. statement_to_date: End date of statement period (as string, e.g., "31-01-2024")
            7. opening_balance: Opening balance amount (as number, e.g., 50000.00)
            8. closing_balance: Closing balance amount (as number, e.g., 75000.00)
            9. total_debits: Total debit/withdrawal amount (as number, e.g., 25000.00)
            10. total_credits: Total credit/deposit amount (as number, e.g., 50000.00)
            11. currency: Currency code (e.g., "INR", "USD", "EUR")
            12. statement_date_generated: Date when statement was generated (if available)
            13. branch_name: Branch name (if available)
            14. statement_number: Statement number or ID (if available)
            
            Important:
            - Look for patterns like "from X to Y", "between X and Y", "period from X to Y"
            - Extract numeric values only for balance/amount fields
            - Convert all amounts to plain numbers without currency symbols
            - Return ONLY valid JSON, no other text
            
            Return the extracted data as valid JSON only.
            """
        
        response = self.client.generate(
                model=self.model,
                prompt=prompt,
                images=[image_path],
                stream=False,
        )

        response_text = response['response']
        self.logger.info('LLM Parsing Completed, Sending to JSON Decoder')
        extracted_data = self.parse_json(response_text)

        extracted_data["source_file"] = os.path.basename(image_path)
        extracted_data["processing_timestamp"] = datetime.now().isoformat()
        
        self.logger.info('Completed Everything, going to save file as JSON')
        return extracted_data
    

    def parse_json(self, response_text:str) -> Dict[str, Any]:
        self.logger.info('Started JSON Parsing')
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)

        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                self.logger.error('JSON DECODE ERROR')
                pass
        self.logger.info('JSON Parsing Completed and returned to LLM Parser')
        return {}


    def process_all_images(self):

        
        self.logger.info("Starting OCR...")
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(self.input_dir.glob(f'*{ext}'))
            image_files.extend(self.input_dir.glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"No images found in {self.input_dir}")
            self.logger.info(f'No images found in {self.input_dir}')
            return []
        
        # Remove duplicates
        image_files = list(set(image_files))
        image_files.sort()
        
        print(f"Found {len(image_files)} images to process")
        print("=" * 60)
        self.logger.info(f'Found {len(image_files)} images to process')

        all_results = []
        
        for idx, image_file in enumerate(image_files, 1):
            print(f"[{idx}/{len(image_files)}] Processing: {image_file.name}")
            self.logger.info(f'[{idx}/{len(image_files)}] Processing: {image_file.name}')
            try:
                result = self.parse_llm(str(image_file))
                
                if result:
                    all_results.append(result)
                    
                    # Save individual JSON file
                    output_filename = f"{image_file.stem}_parsed.json"
                    output_path = self.output_dir / output_filename
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=4, ensure_ascii=False)
                    
                    print(f"  → Saved: {output_filename}\n")
                    self.logger.info(f'→ Saved: {output_filename}\n')
                
            
            except Exception as e:
                print(f"  ✗ Error processing {image_file.name}: {str(e)}\n")
                self.logger.error(f'✗ Error processing {image_file.name}: {str(e)}\n')
        
        self.logger.info('OCR Parsing Completed Successfully.')


