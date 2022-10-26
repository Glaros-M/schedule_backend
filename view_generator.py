import models
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from typing import NamedTuple

env = Environment(
    loader=FileSystemLoader('./templates')#,
    #autoescape=select_autoescape(['html', 'xml'])
)




def get_data_from_file(path: str) -> models.JSON_Faculties:
    # Удалить отсюда после отладки!!!
    with open(path, encoding="utf8") as file:
        data = file.read()
    a = models.JSON_Faculties.parse_raw(data)
    return a


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


def convert_group_to_lessons(group: models.Groups) -> list[list[LessonRow]]:
    group_name = group.group_name
    days_lessons_list = []
    for day in group.days:
        weekday = day.weekday
        date = day.lessons[0].date
        days_lessons_list.append(_get_lessons_from_day(day))

    return days_lessons_list


if __name__ == "__main__":
    data = get_data_from_file("rasp2.json")
    week_lessons = convert_group_to_lessons(data.faculties[0].groups[0])
    """for day in week_lessons:
        print(day)
        for row in day:
            print("\t", row.time, row.rows)
            for lesson_row in row.lessons:
                print("\t\t", lesson_row)"""
    # print(week_lessons[0][1].lessons)
    #print(week_lessons[0][1].time, week_lessons[0][1].time_start, week_lessons[0][1].time_end, week_lessons[0][1].rows)
    #for l in week_lessons[0][1].lessons:
    #    print(l)



    template = env.get_template('table_template.html')
    print(template.render(week_lessons=week_lessons))
    f = open("out.html", 'w')
    f.write(template.render(week_lessons=week_lessons))
    f.close()
