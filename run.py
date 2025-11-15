from src.ingestion.loaders.image_loader import KaggleLoader
from src.ingestion.preprocess.ocr import BankStatementOCR


parser = BankStatementOCR(input_dir='./data/extracted/images', output_dir='./data/output')
parser.process_all_images()



# loader = KaggleLoader()

# loader.download()
# data_path = loader.extract()