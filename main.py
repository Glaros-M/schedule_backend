import json
import models


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
                    #raise Exception
                    print("404 Not Found")
                    return None


def get_group_names_list(all_files: list[models.JSON_Faculties]) -> list[str]:
    result = []
    for faculties in all_files:
        for facultie in faculties.faculties:
            for group in facultie.groups:
                result.append(group.group_name)
    return result

if __name__=="__main__":
    data = get_data_from_file("rasp.json")
    search_by_group_name('', [data])
    #for name in get_group_names_list([data]):
    #    print(name)
    #print(get_group_names_list([data]))