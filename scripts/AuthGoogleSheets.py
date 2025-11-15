import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame

file_name ='../src/config/botprospeccao-e8ae21050d17.json' ## Colocar seu Client do Google Sheets

scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

creds = ServiceAccountCredentials.from_json_keyfile_name(filename=file_name, scopes=scopes)
client = gspread.authorize(creds)
sheets_complete = client.open(title='Estabelecimentos', folder_id='1P_UmdQkvMnuHG0d3J8fDmPmZuSKGn3j6',) ## Colocar Titulo da sua planilha e o ID da pasta que está Arquivo
sheets = sheets_complete.worksheet('Estabelecimentos') # nome da página
data_sheets = pd.DataFrame(sheets.get_all_records())
list = []

def get_table_data()-> DataFrame:
    return data_sheets


def add_google_sheets(values: dict) -> dict:
    for value in values:
        if value['number_phone'] == None:
            value['number_phone'] = None
        list.append([
            value['name'],
            value['number_phone'],
            value['andress']
        ])
    print('Adicionando a Google Sheets!')
    sheets.append_rows(list, value_input_option='RAW')
    print(f'Foram adicionadas {len(list)} Empresas no Google Sheets!')


