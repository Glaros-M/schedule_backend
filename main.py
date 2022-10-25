import json
import models
from jinja2 import Template


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


def get_data_list_for_view(group: models.Groups) -> Template:
    """
    На вход получаем структуру данных группы.


    на выходе таблица:

    | Дата, день | Время_начала | Время_конца | Название предмета| Подгруппа | Тип пары | Аудитория | Преподаватель |

     Дата, день
        Время начала, время конца
        Название предмета
        Подгруппа | None
        Тип пары
        Аудитория
        Преподаватель


    """

    group.group_name
    for day in group.days:
        day.weekday
        date = day.lessons[0].date
        for lesson in day.lessons:
            lesson.time
            lesson.time_start
            lesson.time_end
            lesson.subject
            lesson.type
            lesson.subgroup
            for teacher in lesson.teachers:
                teacher.teacher_name
            for auditorie in lesson.auditories:
                auditorie.auditory_name


    return [""]


if __name__=="__main__":
    #data = get_data_from_file("rasp.json")
    #search_by_group_name('АС2-221-ОБ', [data])
    temp = Template("""
    {% if name %}
    <p>{{name}}</p>
    {% else %}
    <p> not {{name}}</p>
    {% endif %}
    """)
    print(temp.render(name=True))
    #for name in get_group_names_list([data]):
    #    print(name)
    #print(get_group_names_list([data]))