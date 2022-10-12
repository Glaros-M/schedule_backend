import json
import models


with open("rasp.json") as file:
    datas: dict = json.load(file)


def get_faculties(data: dict) -> list[models.Faculties]:
    faculties = []
    for i in range(len(data["faculties"])):
        faculties.append(models.Faculties(id=i,
                                faculty_name=data["faculties"][i]["faculty_name"],
                                date_start=data["faculties"][i]["date_start"],
                                date_end=data["faculties"][i]["date_end"],
                                groups=None
                                ))
    return faculties


def get_groups(data: dict) -> list[models.Groups]:
    groups: list[models.Groups]
    return groups