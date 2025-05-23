import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from core.config import SHEET_KEY

# TODO вынести в отдельный файл
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = SHEET_KEY

rename_dct = {
    "ФИО" : "party_rk",
    "Дата заявки" : "open_dt",
    "Страна поездки" : "Страна",
    "Город поездки" : "Город_text",
    "Месяц отправления" : "Месяц отправления",
    "Звездность отеля" : "Звездность",
    "Большая территория": "Большая территория",
    "Наличие аквапарка": "Наличие аквапарка",
    "Все включено": "Все включено",
    "Активная анимация": "Активная анимация",
    "Песчаный пляж": "Пляж песчаный",
    "Много зелени": "Много зелени",
    "Красивая природа": "Красивая природа",
    "Первая линия": "Первая линия",
    "Рядом большой город": "Рядом большой город",
    "Размещение с животными": "Размещение с животными",
    "Хорошая транспортная доступность": "Хорошая транспортная доступность",
}


def get_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"])
    httpAuth = credentials.authorize(httplib2.Http())
    return apiclient.discovery.build("sheets", "v4", http=httpAuth)

def create_json(keys: list, values: list):
    features_json = {}
    result_json = {}
    for i in range(len(keys)):
        val = values[i]
        if keys[i] in ("ФИО", "Дата заявки"):
            result_json[rename_dct[keys[i]]] = val
        else:
            if isinstance(val, str) and val.lower() in ('false', 'true'):
                val = 0 if val.lower() == 'false' else 1
            elif isinstance(val, str) and keys[i] == "Месяц отправления":
                val = int(val.split()[0])
            features_json[rename_dct[keys[i]]] = val

    result_json['features'] = features_json
    return result_json

def read_sheet(row_num: int, major_dimension: str = "COLUMNS"):
    service = get_service()
    column_names = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="A1:Q1",
        majorDimension=major_dimension
    ).execute()
    column_names = [item[0] for item in column_names["values"]]
    print(column_names)

    range_ = f"A{row_num}:Q{row_num}"
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_,
        majorDimension=major_dimension
    ).execute()

    values = [item[0] if item else 0 for item in values["values"]]
    print(values)

    return create_json(column_names, values)