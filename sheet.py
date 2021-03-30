import pygsheets
import os
from utils import routine, multi_processing
from loguru import logger
from dotenv import load_dotenv
from pathlib import Path

env_path = Path("./private/.env")
load_dotenv(dotenv_path=env_path)

def config():
    logger.add("./log/{time}.log", rotation="00:00", retention="30 days")
    auth = pygsheets.authorize(service_account_file="./private/credentials.json")
    sheet = auth.open_by_url(os.getenv("sheet_url"))
    return sheet

if __name__ == "__main__":

    sheet = config()
    logger.info("get auth")

    student_page = sheet.worksheet_by_title("student")
    upload_page = sheet.worksheet_by_title("upload")

    routine(upload_page, student_page, os.getenv("upload_root_path"))
    logger.info("routine done")

    #file_manage("P76097612")
    # print(page.get_values("A1", "B100", returnas='range')[0][0])
    # page.update_value("A10", "GG")

    # c1 = page.cell("H1")
    # c1.color = (1, 0, 0, 0)