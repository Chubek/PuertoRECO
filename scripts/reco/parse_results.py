import pandas as pd
from dotenv import dotenv_values

temp = dotenv_values(".env")


def parse_results(df):
    argmin_cs = df[temp["SELECTED_MODEL_COL"]].argmin()

    selected_img = df.loc[argmin_cs, "identity"]

    person_name = selected_img.replace("\\", "/").split("/")[-2]

    person_name_split = person_name.split("_")

    id = person_name_split[1]
    name = person_name_split[0]
    hash = person_name_split[2]

    return id, name, hash
