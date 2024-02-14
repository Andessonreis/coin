from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import os
import traceback
import logging

def get_currency_quote(browser: webdriver, currency: str) -> str:
    """
    Get the currency quote for the given currency.

    Parameters:
    - browser (webdriver): The Selenium WebDriver instance.
    - currency (str): The currency to get the quote for.

    Returns:
    - str: The currency quote or None if an error occurred.
    """
    try:
        browser.get('https://google.com')

        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.NAME, 'q')))
        search_box = browser.find_element(By.NAME, 'q')
        search_box.send_keys(f'{currency} today')
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')))
        currency_quote = browser.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text
        return currency_quote
    except Exception as e:
        traceback.print_exc()
        logging.exception('Error message: ', e)
        return None

def save_txt_file(file_name: str, data_time: str, usd_quote: str, euro_quote: str) -> None:
    """
    Save data to a TXT file.

    Parameters:
    - file_name (str): The name of the file.
    - data_time (str): The date and time.
    - usd_quote (str): The USD quote.
    - euro_quote (str): The Euro quote.
    """
    if not file_name:
        file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_quotes.txt'

    with open(file_name, 'a', encoding='UTF-8') as file:
        file.write(f'{data_time} | USD: {usd_quote}  Euro: {euro_quote}\n')
        print(f'File {file_name} saved successfully!')

def save_xlsx_file(file_path: str, data_time: str, usd_quote: str, euro_quote: str) -> None:
    """
    Save data to an XLSX file.

    Parameters:
    - file_path (str): The path of the file.
    - data_time (str): The date and time.
    - usd_quote (str): The USD quote.
    - euro_quote (str): The Euro quote.
    """
    try:
        if file_path.lower().endswith(('.xls', '.xlsx', '.csv')):
            file_path = os.path.abspath(file_path)
            df = pd.DataFrame(columns=['DATE/TIME', 'CURRENCY', 'VALUE'])

            if os.path.exists(file_path):
                df = pd.read_excel(file_path)

            df.loc[len(df.index)] = data_time, 'USD', usd_quote
            df.loc[len(df.index)] = data_time, 'Euro', euro_quote

            df.to_excel(file_path, index=False)

            print(f'File saved successfully at {file_path}')
            os.startfile(file_path)
        else:
            print('Invalid file extension. Exiting the program...')
    except FileNotFoundError as e:
        print(f'Invalid path: {e}')

def main() -> None:
    try:
        # Configurar o geckodriver 0.32.0 explicitamente
        browser = webdriver.Firefox(executable_path='/snap/bin/geckodriver')
        print('Collecting data... Please wait')

        usd_quote = get_currency_quote(browser, 'usd')
        euro_quote = get_currency_quote(browser, 'euro')

        browser.close()

        print(f'USD: {usd_quote}')
        print(f'Euro: {euro_quote}')

        save_file = input('Do you want to save the file? (Y/N) ').upper()
        if save_file == 'Y':
            file_format = input('Which file format do you want to save?\n[1] - .txt\n[2] - .xlsx\n ').lower()
            if file_format == '1':
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_txt_file(None, current_time, usd_quote, euro_quote)
            elif file_format == '2':
                file_path = input('Enter the file path: ').strip('"')
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_xlsx_file(file_path, current_time, usd_quote, euro_quote)
            else:
                print('Invalid option. Choose 1 (.TXT) or 2 (.XLSX)')
        else:
            print('Exiting the program...')
    except Exception as e:
        print('An error occurred: ', e)

if __name__ == "__main__":
    main()
