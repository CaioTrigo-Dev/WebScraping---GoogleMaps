import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
projeto_root = Path(__file__).parent.parent

from src.scrapers.google_maps_scraper import GoogleMapsScraper

def main():
    query = 'Hamburgueria'
    output = projeto_root / 'data' / 'processed' / 'hamburgueria.csv'
    input = projeto_root / 'data' / 'Row' / 'establishment.csv'

    print(f'Buscando {query}')

    with GoogleMapsScraper(headless=False) as scraper:
        scraper.search(query)
        scraper.scroll_browser()
        data = scraper.data_companys
        scraper.save_csv(output)


    print(f'Concluido, {len(data)} de Empresas Extraidas')

if __name__ == '__main__':
    main()