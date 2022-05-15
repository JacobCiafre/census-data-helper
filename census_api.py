from dotenv import load_dotenv
import os
import pandas as pd
import re
import requests
import time


def New_CSV_File(api_endpoint: str, file_name: str, save_path: str) -> str:
    '''Fetches data from the census api and stores it in a csv file\n
    Do not call this function unless you know the exact structure of the census api\n
    See Search_Census function'''

    if not os.path.isdir(save_path):
        raise ValueError('Target Directory does not exist.')

    nl = len(file_name)
    if nl == 0:
        raise ValueError('Inappropriate file name.')

    nc = re.compile(r'[a-zA-Z0-9_]\w*')
    acceptedChars = len(nc.match(file_name).group(0))
    if acceptedChars != len(file_name):
        raise ValueError(
            'The file name you are trying to save is incorrectly formatted.')

    file_path = f'{save_path}/{file_name}.csv'

    response = requests.get(api_endpoint)

    if response.status_code != 200:
        raise ConnectionError(
            'Bad api endpoint, check documentation for Search_Census')

    data = response.json()

    try:
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_csv(file_path, index=None)
    except:
        return "Failed to load data into pandas dataframe"

    return "Success"


def Search_Census(year: int, namesetAcr: str, * variables: str, file_name='autogen', save_path='./data') -> str:
    '''This helper file simplifies the endpoint creation process for querying census data.\n
    A csv file will be create in specified location\n
    Use Get_Options function if you are unsure of what excepted values for namesetAcr'''

    assert year < time.gmtime().tm_year, 'Search year must be less than current year.'

    acros = namesetAcr.split('/')

    assert len(variables) > 0, 'You must have atleast one selection variable'

    if file_name == 'autogen':
        searchTime = time.localtime()
        fmtime = f'{searchTime.tm_mday}_{searchTime.tm_hour}_{searchTime.tm_min}'
        file_name = f'data_{year}_{acros[-1]}_{fmtime}'

    load_dotenv()
    CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY")
    vars = ''
    for index, val in enumerate(variables):
        vars += val.upper()
        if index != len(variables)-1:
            vars += ','

    api_url = f'https://api.census.gov/data/{year}/{namesetAcr}?get={vars}&for=state:*&key={CENSUS_API_KEY}'

    message = New_CSV_File(api_url, file_name, save_path)

    return message


def Get_Options(year: int) -> dict:
    '''Returns a nested dictionary with keys of valid namesetAcr associated with a link to the api requst for the list of variables for a given year. Avoid calling this function multiply times in a script, it is O(N^2)'''

    assert year < time.gmtime().tm_year, 'Search year must be less than current year.'

    response = requests.get(f'https://api.census.gov/data/{year}.json')

    if response.status_code != 200:
        raise ConnectionError(
            'Bad connection, it is likely the year you entered is not available')

    df = pd.read_json(response.content)

    extensions = {year: dict()}
    for i in df['dataset']:
        tempStr = ''
        for index, val in enumerate(i['c_dataset']):
            tempStr += val
            if index != len(i['c_dataset'])-1:
                tempStr += '/'
        extensions[year].update({tempStr: i['c_variablesLink']})

    return extensions
