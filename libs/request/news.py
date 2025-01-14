from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome
from datetime import datetime, timedelta
from urllib.parse import quote
from bs4 import BeautifulSoup
from re import compile
from time import sleep
import pandas as pd



class News():
    def __init__(self, path_chromedriver:str) -> None:
        """
        Initializes the NewsScraper object.
        ------

        Parameters:
            path_chromedriver (str): Path to the ChromeDriver executable.
        """
        self.__chrome_service = Service(path_chromedriver)
        self.__options = ChromeOptions()
        self.__options.add_argument('--ignore-certificate-errors')
        self.__options.add_argument('--incognito')
        self.__options.add_argument('--headless')
        self.driver = None


    def __to_datetime(self, date:str) -> str:
        """
        Converts a Portuguese date string to a standard 'YYYY-MM-DD' format.
        ------

        Parameters:
            date (str): The Portuguese date string to be converted.

        Returns:
            str: The date converted to 'YYYY-MM-DD' format.
            
        Raises:
            ValueError: If the input string does not match the expected date format.
        """
        try:
            abbreviated_months = {
                'jan.': 'January',
                'fev.': 'February',
                'mar.': 'March',
                'abr.': 'April',
                'mai.': 'May',
                'jun.': 'June',
                'jul.': 'July',
                'ago.': 'August',
                'set.': 'September',
                'out.': 'October',
                'nov.': 'November',
                'dez.': 'December'
            }

            for abbreviation, full_name in abbreviated_months.items():
                date = date.replace(abbreviation, full_name)
            date_obj = datetime.strptime(date, "%d de %B de %Y")
            return date_obj.strftime('%d/%m/%Y')
        except Exception as error:
            print(error)


    def __extract_difference(self, date:str) -> str:
        """
        Extracts the time difference from a string containing relative time information (e.g., '2 dias atrás').
        ------

        Parameters:
            date (str): The string containing relative time information.

        Returns:
            str: The calculated date in 'YYYY-MM-DD' format based on the provided relative time.
            
        Raises:
            ValueError: If the input string does not match the expected format.
        """
        try:
            pattern = compile(r'(\d+)\s+(\w+)\s+atrás')
            match = pattern.match(date)

            if match:
                amount = int(match.group(1))
                unit = match.group(2)

                if 'dia' in unit:
                    delta = timedelta(days=amount)
                elif 'semana' in unit:
                    delta = timedelta(weeks=amount)
                elif 'hora' in unit:
                    delta = timedelta(hours=amount)
                elif 'mês' in unit or 'meses' in unit:
                    delta = timedelta(days=30 * amount)  

                current_date = datetime.now()
                previous_date = current_date - delta
                return previous_date.strftime('%d/%m/%Y')

            else:
                raise ValueError('Invalid text format')
        except Exception as error:
            print(error)



    def _convert_date(self, dataframe:pd.DataFrame, column:str) -> pd.DataFrame:
        """
        Converts date strings in a DataFrame column to 'YYYY-MM-DD' format.
        ------

        Parameters:
            dataframe (pd.DataFrame): The DataFrame containing date strings to be converted.
            column (str): The name of the column containing date strings.

        Returns:
            pd.DataFrame: The DataFrame with the specified date column converted to 'YYYY-MM-DD' format.
        """
        try:
            for i in range(dataframe.shape[0]):
                date = dataframe[column][i].strip()
                date = self.__extract_difference(date) if 'atrás' in date else self.__to_datetime(date)
                dataframe.at[i, column] = date

            return dataframe
        except Exception as error:
            print(error)


    def _parse_html(self, html_content:str, query:str) -> list:
        """
        Parses HTML content from Google News search results, extracting relevant information.
        ------

        Parameters:
            html_content (str): HTML content of the Google News search results page.
            query (str): The search query for news articles.

        Returns:
            list: A list of dictionaries, each containing details of a news article including title, media, date, and link.
        """
        try:
            content = BeautifulSoup(html_content, "html.parser")
            content = content.find('div', {'id': 'search'})
            results = content.find_all('div', {'class': 'SoaBEf'})

            values = list()

            for item in results:
                media = item.find('span').text
                date = item.find('div', {'class': 'OSrXXb'}).text
                link = item.find('a')['href']
                title = item.find('div', {'role': 'heading'}).text
                description = item.find('div', class_='GI74Re nDgy9d').text

                print(f"Search: {query}")
                print(f"Title: {title}")
                print(f"Source: {media}")
                print(f"Date: {date}")
                print(f"Link: {link}")
                print(f"Description: {description}")
                print()
            
                values.append({'title': title, 'media': media,'news_date': date, 'description':description,'link': link})

            sleep(2)
            return values
        except Exception as error:
            print(error)


    def search(self, query:str, from_date:str, to_date:str) -> pd.DataFrame:
        """
        Searches Google News for articles based on the provided query, from_date, and to_date.
        ------

        Parameters:
            query (str): The search query for news articles.
            from_date (str): The start date for the search in 'YYYY-MM-DD' format.
            to_date (str): The end date for the search in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: A DataFrame containing details of the scraped news articles.
        """
        try:
            df = 0
            self.driver = Chrome(service=self.__chrome_service, options=self.__options)
            for i in range(100):

                page,  encoded_search_query =  i * 10, quote(query, safe='')
                url = f"https://www.google.com/search?q={encoded_search_query}&tbs=cdr:1,cd_min:{from_date},cd_max:{to_date},sbd:1&tbm=nws&start={page}"
                self.driver.get(url)
                html_content = self.driver.page_source
                values = self._parse_html(html_content, query)
                if not values: break 
                df = pd.DataFrame(values) if i == 0 else pd.concat([df, pd.DataFrame(values)])
                        
            sleep(15)
            self.driver.quit()

            if type(df) == int: return None
            df.index = range(df.shape[0])
            return self._convert_date(df, 'news_date')
                
        except Exception as error:
            print(error)
            return None