from src.ingestion.loaders.image_loader import KaggleLoader


loader = KaggleLoader()

loader.download()
data_path = loader.extract()