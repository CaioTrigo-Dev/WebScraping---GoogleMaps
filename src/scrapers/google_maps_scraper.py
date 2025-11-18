import pyperclip
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict
import time
from ..utils.formatters import format_phone, format_andress
from ..utils.formatters import format_andress
from ..config.settings import WAIT_TIME, XPATH_BUTTON_PHONE, XPATH_BUTTON_ADDRESS,XPATH_CHECK_FIM_LIST
from scripts.AuthGoogleSheets import add_google_sheets
from ..utils.validatorys import check_name_sheets
from ..utils.logger import setup_logger

class GoogleMapsScraper:
    def __init__(self, headless: bool = False):
        self.browser = self._init_browser(headless)
        self.wait_time = WAIT_TIME
        self.data_companys = []
        self.logger = setup_logger('Executando Scraper', 'INFO')

    def _init_browser(self, headless: bool = False) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    def search(self, query: str) -> None:
        url = f'https://www.google.com/maps/search/{query}'
        self.browser.get(url)
        self.browser.maximize_window()
        time.sleep(2)

    def scroll_browser(self):
        while True:
            self.browser.execute_script(
                """
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                """,
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                )
            )
            time.sleep(WAIT_TIME)
            if self.check_end_list():
                break
        self.extract_company()
    def check_end_list(self):
        try:
            element = self.browser.find_element(By.XPATH, XPATH_CHECK_FIM_LIST)
            return True
        except NoSuchElementException:
            return False

    def extract_company(self):
        contents_company = self.browser.find_elements(By.XPATH, "//a[contains(@href , '/place/')]")
        for i, company in enumerate(contents_company):
            self.logger.info(f'Processando {i + 1}/{len(contents_company)}')
            try:
                data = self.extract_data_company(company)
                if data == None:
                    continue
                else:
                    self.data_companys.append(data)
                    self.logger.info(f'Adicionado a Lista Foram {len(self.data_companys)}/{len(contents_company)}')
            except Exception as e:
                self.logger.error(e)
    def extract_data_company(self, data: Dict) -> dict[str, str | None] | None:
        self.click_company(data)
        name = self.extract_name(data)
        check_name = check_name_sheets(name)
        if check_name:
            number_phone = self.extract_phone()
            andress = self.extract_andress()
            return {
                'name': name,
                'number_phone': number_phone,
                'andress': andress
            }
        return None

    def click_company(self, data: Dict) -> None:
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", data)
        time.sleep(1)
        self.browser.execute_script("arguments[0].click();", data)
        time.sleep(2)

    def extract_name(self, data) -> str:
        try:
            return data.get_attribute('aria-label')
        except:
            return 'Não encontrado'

    def extract_phone(self) -> str | None:
        try:
            number = self.browser.find_element(By.XPATH, XPATH_BUTTON_PHONE)
            number.click()
            time.sleep(0.5)
            number_company = pyperclip.paste()
            time.sleep(0.5)
            return format_phone(number_company)
        except:
            return 'Não encontrado'

    def extract_andress(self) -> str:
        try:
            andress = self.browser.find_element(By.XPATH, XPATH_BUTTON_ADDRESS)
            andress.click()
            time.sleep(0.5)
            andress_company = pyperclip.paste()
            time.sleep(0.5)
            return format_andress(andress_company)
        except:
            return 'Não Encontrado'

    def pull_csv(self) -> None:
        add_google_sheets(self.data_companys)
        self.logger.info(f'Adicionado no Google Sheets!')

    def close(self):
        if hasattr(self, 'browser') and self.browser:
            self.logger.info(f'Fechando navegador...')
            self.browser.quit()
            self.logger.info(f'Fechando navegador...')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False



