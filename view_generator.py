import models
from jinja2 import Environment, FileSystemLoader
from typing import NamedTuple

""" 
Генерация представлений из данных. Необходимо прописать функцию для вызова - зависит от того как будет
                                                                                происходить вызов из API.
"""

env = Environment(
    loader=FileSystemLoader('./templates')
)


def get_data_from_file(path: str) -> models.JSON_Faculties:
    # Удалить отсюда после отладки!!! Тоже почистить после подключения
    with open(path, encoding="utf8") as file:
        data = file.read()
    a = models.JSON_Faculties.parse_raw(data)
    return a


DAYS_OF_WEEK = {
    1: "Пн.",
    2: "Вт.",
    3: "Ср.",
    4: "Чт.",
    5: "Пт.",
    6: "Сб.",
    7: "Вс."
}


class Day(NamedTuple):
    group_name: str
    weekday: str
    date: str
    lessons: list["LessonRow"]

    @property
    def rows(self):
        i = 0
        for lesson in self.lessons:
            i += len(lesson.lessons)
        return i


class LessonRow(NamedTuple):
    time: int
    time_start: str
    time_end: str
    lessons: list["LessonCell"]

    @property
    def rows(self) -> int:
        return len(self.lessons)


class LessonCell(NamedTuple):
    subject: str
    type: str
    subgroup: int
    teachers: str
    auditories: str


def _get_teachers_auditories_from_lesson(lesson: models.Lessons) -> (str, str):
    """Преобразование списков с учителями и аудиториями к строкам. Возможно добавить запятые?"""

    teachers_str = ""
    for teacher in lesson.teachers:
        teachers_str += teacher.teacher_name
    auditories_str = ""
    for auditorie in lesson.auditories:
        auditories_str += auditorie.auditory_name

    return teachers_str, auditories_str


def _get_lessons_from_day(day: models.Days) -> list[LessonRow]:
    """Преобразует данные об уроках из models.Days в класс LessonRow, в котором объединяются пары,
     проходящие в одно время, для создания объединенных (rowspan) ячеек в представлении"""
    lesson_list: list[LessonRow] = []
    for lesson in day.lessons:
        teachers_str, auditories_str = _get_teachers_auditories_from_lesson(lesson)
        cell_lesson = LessonCell(
            subject=lesson.subject,
            type=lesson.type,
            subgroup=lesson.subgroup,
            teachers=teachers_str,
            auditories=auditories_str
        )
        row_lesson = LessonRow(
            time=lesson.time,
            time_start=lesson.time_start,
            time_end=lesson.time_end,
            lessons=[
                cell_lesson
            ]
        )

        if lesson_list:
            processed = False
            for lesson_in_list in lesson_list:
                if lesson.time == lesson_in_list.time and not processed:
                    # lesson_in_list.set_rows(lesson_in_list.rows + 1)
                    lesson_in_list.lessons.append(cell_lesson)
                    processed = True
            if not processed:
                lesson_list.append(row_lesson)
        else:
            lesson_list.append(row_lesson)
    return lesson_list


def convert_group_to_lessons(group: models.Groups) -> list[Day]:
    """Форматирует данные группы в список дней с занятиями этой группы для отображения в представлении
    Тут же подствляется сокращение дня недели вместо номера.
    """

    group_name = group.group_name
    day_lessons_list = []
    for day in group.days:
        weekday = day.weekday
        date = day.lessons[0].date
        new_day = Day(
            group_name=group_name,
            weekday=DAYS_OF_WEEK.get(weekday),
            date=date,
            lessons=_get_lessons_from_day(day)
        )
        day_lessons_list.append(new_day)
    return day_lessons_list


if __name__ == "__main__":
    data = get_data_from_file("rasp2.json")
    week_lessons = convert_group_to_lessons(data.faculties[0].groups[0])
    for day in week_lessons:
        print(day)
        for row in day.lessons:
            print("\t", row)

    template = env.get_template('table_template.html')
    print(template.render(week_lessons=week_lessons))
    f = open("out.html", 'w')
    f.write(template.render(week_lessons=week_lessons))
    f.close()
