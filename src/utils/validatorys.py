from scripts.AuthGoogleSheets import get_table_data

data_table_google_sheets = get_table_data()

def check_name_sheets(name: str) -> bool:
    not_exist = True
    for value in data_table_google_sheets['name']:
        if name in value:
            not_exist = False
    return not_exist