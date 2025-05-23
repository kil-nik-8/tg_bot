import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from core.config import SHEET_KEY

CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = SHEET_KEY



rename_dct = {
    "Дата заявки": "open_dt",
    "Страна поездки": "Страна",
    "ФИО": "party_rk",
    "Месяц отправления": "Месяц отправления",
    "Тип клиента": "Тип клиента",
    "Звезды отеля": "stars",
    "Близость к аэропорту": "proximity_to_airport",
    "Близость к крупному городу": "close_to_major_city",
    "Транспортная доступность": "good_transport_accessibility",
    "Первая береговая линия": "first_coastline",
    "Вторая береговая линия": "second_coastline",
    "Трансфер к пляжу": "shuttle_service_to_beach",
    "Близость к пляжу": "remote_from_beach",
    "Крупный отель": "large_hotel",
    "Аквапарк": "water_park",
    "Открытые бассейны": "outdoor_pools",
    "Крытые бассейны": "indoor_pools",
    "Подогреваемые бассейны": "heated_pools",
    "Спа-центр": "spa_center",
    "Тренажерный зал": "gym",
    "Система 'Все включено'": "all_inclusive_system",
    "Полный пансион": "full_board",
    "Полупансион": "half_board",
    "Завтрак включен": "breakfast_included",
    "Бесплатные рестораны": "free_restaurants",
    "Платные рестораны": "paid_restaurants",
    "Круглосуточный бар": "twenty_four_hour_bar",
    "Детский аквапарк": "kids_water_park",
    "Отель для взрослых": "adults_only_hotel",
    "Бесплатный Wi-Fi": "free_wifi",
    "Мини-бар": "mini_bar",
    "Частный пляж": "private_beach",
    "Бесплатные шезлонги": "free_sunbeds_umbrellas",
    "Песчаный пляж": "sandy_beach",
    "Галечный пляж": "pebble_beach",
    "Бесплатная парковка": "free_parking",
    "Развлечения для взрослых": "adult_entertainment",
    "Детские развлечения": "kids_entertainment",
    "Озелененная территория": "abundant_greenery",
    "Размещение с животными": "pet_friendly_accommodation",
    "Кондиционер": "air_conditioning"
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
