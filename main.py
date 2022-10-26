import json
import models
from jinja2 import Template
from typing import NamedTuple


def get_data_from_file(path: str) -> models.JSON_Faculties:
    with open(path, encoding="utf8") as file:
        data = file.read()
    a = models.JSON_Faculties.parse_raw(data)
    return a


def search_by_group_name(group_name: str, all_files: list[models.JSON_Faculties]) -> models.Groups | None:
    for faculties in all_files:
        for facultie in faculties.faculties:
            for group in facultie.groups:
                if group.group_name == group_name:
                    print(group)
                    return group
                else:
                    # raise Exception
                    print("404 Not Found")
                    return None


def get_group_names_list(all_files: list[models.JSON_Faculties]) -> list[str]:
    groups = []
    for faculties in all_files:
        for facultie in faculties.faculties:
            for group in facultie.groups:
                groups.append(group.group_name)
    return groups



if __name__ == "__main__":
    data = get_data_from_file("rasp2.json")
    week_lessons = convert_group_to_lessons(data.faculties[0].groups[0])
    #for day in week_lessons:
        #print(day)
    #print(week_lessons[0][1].lessons)
    print(week_lessons[0][1].time, week_lessons[0][1].time_start, week_lessons[0][1].time_end, week_lessons[0][1].rows)
    for l in week_lessons[0][1].lessons:
        print(l)