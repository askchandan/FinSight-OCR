from src.ingestion.loaders.image_loader import KaggleLoader


loader = KaggleLoader(
        dataset = 'mehaksingal/personal-financial-dataset-for-india',
        extract_path = './data/extracted/'
)

loader.download()
data_path = loader.extract()