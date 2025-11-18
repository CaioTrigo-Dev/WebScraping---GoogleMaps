import sys
from pathlib import Path

from src.utils.logger import setup_logger

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapers.google_maps_scraper import GoogleMapsScraper

def main():
    query = input('Qual estabelecimento quer Buscar?  ')
    logger = setup_logger('Start', 'INFO')
    logger.info(f'Buscando  {query}')

    with GoogleMapsScraper(headless=False) as scraper:
        scraper.search(query)
        scraper.scroll_browser()
        data = scraper.data_companys
        scraper.pull_csv()


    logger.info(f'Concluido, {len(data)} de Empresas Extraidas')

if __name__ == '__main__':
    main()