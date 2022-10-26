import models
from jinja2 import Template
from typing import NamedTuple



def get_data_from_file(path: str) -> models.JSON_Faculties:
    #Удалить отсюда после отладки!!!
    with open(path, encoding="utf8") as file:
        data = file.read()
    a = models.JSON_Faculties.parse_raw(data)
    return a



class LessonRow(NamedTuple):
    time: int
    time_start: str
    time_end: str
    lessons: list["LessonToCell"]

    @property
    def rows(self) -> int:
        return len(self.lessons)


class LessonToCell(NamedTuple):
    subject: str
    type: str
    subgroup: int
    teachers: str
    auditories: str


def _get_teachers_auditories_from_lesson(lesson: models.Lessons) -> (str, str):
    teachers_str = ""
    for teacher in lesson.teachers:
        teachers_str += teacher.teacher_name
    auditories_str = ""
    for auditorie in lesson.auditories:
        auditories_str += auditorie.auditory_name

    return teachers_str, auditories_str


def _get_lessons_from_day(day: models.Days) -> list[LessonRow]:
    lesson_list: list[LessonRow] = []
    for lesson in day.lessons:
        if lesson_list:
            processed = False
            for lesson_in_list in lesson_list:

                if lesson.time == lesson_in_list.time and not processed:
                    #lesson_in_list.set_rows(lesson_in_list.rows + 1)

                    teachers_str, auditories_str = _get_teachers_auditories_from_lesson(lesson)

                    lesson_in_list.lessons.append(
                        LessonToCell(
                            subject=lesson.subject,
                            type=lesson.type,
                            subgroup=lesson.subgroup,
                            teachers=teachers_str,
                            auditories=auditories_str
                        )
                    )
                    processed = True
            if not processed:
                #TODO: refractor this one to function?
                teachers_str, auditories_str = _get_teachers_auditories_from_lesson(lesson)

                lesson_list.append(
                    LessonRow(
                        time=lesson.time,
                        time_start=lesson.time_start,
                        time_end=lesson.time_end,
                        lessons=[
                            LessonToCell(
                                subject=lesson.subject,
                                type=lesson.type,
                                subgroup=lesson.subgroup,
                                teachers=teachers_str,
                                auditories=auditories_str
                            )
                        ]
                    )
                )
        else:
            teachers_str, auditories_str = _get_teachers_auditories_from_lesson(lesson)

            lesson_list.append(
                LessonRow(
                    time=lesson.time,
                    time_start=lesson.time_start,
                    time_end=lesson.time_end,
                    lessons=[
                        LessonToCell(
                            subject=lesson.subject,
                            type=lesson.type,
                            subgroup=lesson.subgroup,
                            teachers=teachers_str,
                            auditories=auditories_str
                        )
                    ]
                )
            )
    return lesson_list


def convert_group_to_lessons(group: models.Groups) -> list[list[LessonRow]]:
    group_name = group.group_name
    days_lessons_list = []
    for day in group.days:
        weekday = day.weekday
        date = day.lessons[0].date
        days_lessons_list.append(_get_lessons_from_day(day))

    return days_lessons_list
