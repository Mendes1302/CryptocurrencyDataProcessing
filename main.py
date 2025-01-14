from dotenv import load_dotenv
from datetime import datetime
import os, sys, json
sys.path.insert(1, os.getcwd())
from libs.request.crypto_info import CoinCapAPI 
from libs.sql.sqlite_manager import Sqlite
from libs.request.news import News 

load_dotenv()
DATABASE_PATH = os.getenv('DATABASE_PATH')
API_KEY = os.getenv('API_KEY')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

sql = Sqlite(database=DATABASE_PATH)
coin = CoinCapAPI(api_key=API_KEY)
news = News(path_chromedriver=CHROMEDRIVER_PATH)

def __set_query(data:dict, col_name:str, remove_col:str=None) -> str:
    try:
        if remove_col: data.pop(remove_col)
        __columns = tuple(data.keys())
        __values = tuple(data.values())
        __query = f"""INSERT INTO {col_name} {__columns} VALUES {__values};"""
        return __query.replace("None", "NULL")
    except Exception as e:
        print(f"Error set query for {col_name}: {e}")
     

def __save_crypto_details(crypto_name: str) -> None:
    try:
        __data = coin.get_crypto_by_id(crypto_name)
        __query = __set_query(__data, "details", "id")
        sql.insert(__query)
    except Exception as e:
        print(f"Error saving details for {crypto_name}: {e}")


def __save_crypto_historic(crypto_name: str) -> None:
    try:
        __args = {"crypto_id": crypto_name,
                  "start_date": datetime(2024, 1, 1),
                  "end_date": datetime(2024, 12, 31)
        }
        __values = coin.get_price_history(**__args)
        __id_crypto = 0 if crypto_name == "bitcoin" else 1
        for value in  __values:
            __value = {'cryptoId': __id_crypto, **value}
            __query = __set_query(__value, "historic_prices", "time")
            sql.insert(__query)
    except Exception as e:
        print(f"Error saving historic_prices history for {crypto_name}: {e}")


def __save_crypto_markets(crypto_name: str) -> None:
    try:
        __values = coin.get_market_details(crypto_name)
        __id_crypto = 0 if crypto_name == "bitcoin" else 1
        for value in  __values:
            __value = {'cryptoId': __id_crypto, **value}
            __query = __set_query(__value, "Markets", "baseId")
            sql.insert(__query)
    except Exception as e:
        print(f"Error saving markets history for {crypto_name}: {e}")


def __save_crypto_news(crypto_name: str) -> None:
    try:
        __date = {"01/01/2024": "06/30/2024",
                  "07/01/2024": "12/31/2024"
        }
        for from_date, to_date in __date.items():
            __args = {"query": crypto_name,
                    "from_date": from_date,
                    "to_date": to_date 
            }
            __values = news.search(**__args)
            __values = __values.to_json(orient="records")
            __values = json.loads(__values)
            __id_crypto = 0 if crypto_name == "bitcoin" else 1
            for value in  __values:
                __value = {'cryptoId': __id_crypto, **value}
                __query = __set_query(__value, "news")
                sql.insert(__query)
    except Exception as e:
        print(f"Error saving news history for {crypto_name}: {e}")


def main() -> None:
    cryptos = ["bitcoin", "ethereum"]
    for crypto in cryptos:
        __save_crypto_details(crypto)
        __save_crypto_historic(crypto)
        __save_crypto_markets(crypto)
        __save_crypto_news(crypto)


if __name__ == "__main__": main()