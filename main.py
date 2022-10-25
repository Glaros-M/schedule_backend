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
    result = []
    for faculties in all_files:
        for facultie in faculties.faculties:
            for group in facultie.groups:
                result.append(group.group_name)
    return result


class DataForView(NamedTuple):
    # TODO: Перенести класс и функцию куданадо (придумать куда)
    rows: int
    time: int
    time_start: str
    time_end: str
    subject: str
    type: str
    subgroup: int
    teachers: str
    auditories: str


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

    group_name = group.group_name
    for day in group.days:
        weekday = day.weekday
        date = day.lessons[0].date

        # TODO: Нада сделать както сортировку массива lessons. По параметру time наверное

        def _get_list_from_lesson(lesson: models.Lessons) -> DataForView:
            teachers_str = ""
            for teacher in lesson.teachers:
                teachers_str += teacher.teacher_name
            auditories_str = ""
            for auditorie in lesson.auditories:
                auditories_str += auditorie.auditory_name

            data = DataForView(
                rows=0,
                time=lesson.time,
                time_start=lesson.time_start,
                time_end=lesson.time_end,
                subject=lesson.subject,
                type=lesson.type,
                subgroup=lesson.subgroup,
                teachers=teachers_str,
                auditories=auditories_str)

            return data

        for i in range(len(day.lessons) - 1):
            lesson = day.lessons[i]
            view_data = _get_list_from_lesson(lesson)
            #TODO: Ну и как тут блин решать вопрос с обьединением строк? Либо считать по каунт, добавлять словарь, либо еще как то. я хз

            

    return [""]


if __name__ == "__main__":
    # data = get_data_from_file("rasp.json")
    # search_by_group_name('АС2-221-ОБ', [data])
    temp = Template("""
    {% if name %}
    <p>{{name}}</p>
    {% else %}
    <p> not {{name}}</p>
    {% endif %}
    """)
    print(temp.render(name=True))
    # for name in get_group_names_list([data]):
    #    print(name)
    # print(get_group_names_list([data]))
