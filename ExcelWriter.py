import pandas as pd
import os

__datafolder__ = "stored_data"


class InvalidDirectory(Exception):
    pass


def dir() -> str:
    ''' generated the current working directory '''

    working_dir = "/".join(__file__.split("/")[:-1])
    if __datafolder__ not in os.listdir(working_dir):
        raise InvalidDirectory("No data folder file found")
    return working_dir


def read_files(category: str, working_dir: str = dir()) -> dict[pd.DataFrame]:
    ''' reads the csv files from a passed category '''

    tables = dict()
    files = os.listdir(f"{working_dir}/{__datafolder__}/{category}")

    for file in files:
        file_name, type = file.split(".")
        if not type == "csv":
            continue
        try:
            tables[file_name] = pd.read_csv(f"{working_dir}/{__datafolder__}/{category}/{file}")
        except Exception as exc:
            print(exc, "occured in:", file)
        else:
            tables[file_name] = tables[file_name].fillna(0)

    return tables


def get_categories(working_dir: str = dir()) -> list[str]:
    f''' lists all the category folders in __datafolder__={__datafolder__}'''

    path = f"{working_dir}/{__datafolder__}"
    return [category for category in os.listdir(path) if os.path.isdir(f"{path}/{category}")]


def compile_sheets(working_dir: str = dir(), update_sheet=False):
    '''
    Convert all the dataframe files to an excel file
        Dataframes are from csv files generated by read_files
        Table names/CSV file names are sheets
        Excel sheet name is its respective category
    '''
    categories = get_categories()

    if update_sheet:

        for category in categories:
            file_path = f"{working_dir}/{__datafolder__}/{category}"
            if os.path.isfile(file_path):
                os.remove(file_path)

    for category in categories:
        excel_name = f"{working_dir}/{__datafolder__}/{category}.xlsx"
        writer = pd.ExcelWriter(excel_name, engine="xlsxwriter")

        for sheet_name, table in read_files(category).items():
            table.to_excel(writer, sheet_name=sheet_name)
        writer.save()


if __name__ == '__main__':
    print(read_files("Dark Elixer"))
