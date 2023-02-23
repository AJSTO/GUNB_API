import os
from datetime import datetime
from typing import Optional, Union

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path, Query, Response
import pandas_gbq
from google.cloud import bigquery
from google.oauth2 import service_account
from unidecode import unidecode


api = FastAPI()

load_dotenv()  # load environment variables from .env file

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_NAME = os.getenv("DATASET_NAME")
TABLE_AGG = os.getenv("TABLE_AGG")
TABLE_UNIT_INFO = os.getenv("TABLE_UNIT_INFO")
JSON_KEY_BQ = os.getenv("JSON_KEY_BQ")
CURRENT_Y_M = datetime.date.today().strftime("%Y-%m")
KEY_PATH = f"./{JSON_KEY_BQ}"
CREDENTIALS = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
CLIENT = bigquery.Client(credentials=CREDENTIALS, project=CREDENTIALS.project_id)


@api.get("/")
def home():
    """
    Returns the contents of the 'home.html' file as an HTTP response.

    Parameters:
        None.

    Returns:
        An HTTP response containing the contents of the 'home.html' file.
        Return type is `fastapi.responses.Response`.
    """
    with open('home.html') as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")


@api.get("/info")
def units_info():
    """
    Returns a JSON response containing information about unit types.

    Parameters:
        None.

    Returns:
        A JSON response containing unit type information.
    """

    query = f"""
            SELECT 
                *
            FROM
                `{PROJECT_ID}.{DATASET_NAME}.{TABLE_UNIT_INFO}`
            """
    df_types = pandas_gbq.read_gbq(query, credentials=CREDENTIALS, progress_bar_type=None)
    df_types.set_index(['unit_type'], drop=True, inplace=True)
    df_types = df_types.applymap(lambda x: unidecode(x))
    df_types['full_unit_info'] = df_types['unit_name'] + ': ' + df_types['unit_number']
    df_types = df_types.groupby('unit_type')['full_unit_info'].apply(list).to_json(orient='index')
    return Response(content=df_types, media_type="application/json")


@api.get("/aggregates/{unit_id}")
def get_aggregates(
        unit_id: Union[str, None] = Path(
            None,
            regex=r'\d{2}$|\d{4}$|\d{6}_\d$',
            description="Type valid unit id, to get all unit's id type /info",
            example='2 digits | 4 digits | 6 digits + "_" + 1 digit'
        ),
        date: Optional[str] = Query(
            CURRENT_Y_M,
            description=f"Available dates from 2023-01 to {datetime.date.today().strftime('%Y-%m')}",
        )
):
    """
    Returns a JSON response containing the aggregates for a specific unit ID and date.

    Parameters:
        - unit_id (Union[str, None]): A string containing the unit ID to retrieve aggregates for.
          Must be a string of 2 digits, 4 digits, or 6 digits followed by an underscore and 1 digit.
          Defaults to `None`.
        - date (Optional[str]): A string containing the date in "YYYY-MM" format to retrieve aggregates for.
          Defaults to the current year and month.

    Returns:
        A JSON response containing the aggregates for the specified unit ID and date.
        If no data is found for the specified unit ID and date, raises an HTTPException with a 404 status code.
    """
    query = f"""
                SELECT 
                    *
                FROM
                    `{PROJECT_ID}.{DATASET_NAME}.{TABLE_AGG}`
                WHERE 
                    unit_id = '{unit_id}'
                AND
                    STRING(injection_date) LIKE '{date}%' ;
                """
    df = pandas_gbq.read_gbq(query, credentials=CREDENTIALS, progress_bar_type=None)
    if not len(df):
        raise HTTPException(
            status_code=404,
            detail=f" Data not valid. Available dates from 2023-01 to {datetime.date.today().strftime('%Y-%m')}."
                   f" To get available units id please type /info.",
        )
    df['injection_date'] = df['injection_date'].apply(lambda x: x.strftime("%Y-%m"))
    # Df.loc[0] in case of doubled aggregates for chosen month.
    df = df.loc[0].to_json(orient='index')
    return Response(content=df, media_type="application/json")
