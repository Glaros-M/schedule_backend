import datetime
from typing import NamedTuple


class Faculties(NamedTuple):
    id: int | None
    faculty_name: str
    date_start: str | datetime.date
    date_end: str | datetime.date
    groups: list["Groups"] | None

    def __repr__(self):
        return f"{self.id=}, {self.faculty_name=}, {self.date_start=}, {self.date_end=}, {self.groups=}"


class Groups(NamedTuple):
    id: int
    group_name: str
    course: int
    days: list["Days"]


class Days(NamedTuple):
    id: int
    weekday: int
    lessons: list["Lessons"]


class Lessons(NamedTuple):
    id: int
    subject: str #Название предмета
    type: str   #Тип занятия. "лек.", "лаб.", "прак."
    subgroup: int #Подгруппа 0-вся группа, 1 - первая, 2 - вторая
    time_start: str | datetime.time    #Вот тут возможно словарь с соотношением номера пары и времени
    time_end: str | datetime.time
    time: int   #Порядковый номер пары
    week: int    #Номер недели от начала года, вродебы (?)
    date: str      #Дата занятия
    teachers: list["Teachers"]
    auditories: list["Auditories"]


class Teachers(NamedTuple):
    id: int
    teacher_name: str # "Вакансия" или "Фамилия И.О."


class Auditories(NamedTuple):
    id: int
    auditory_name: str # "201к/7к" или "Спортзал Гл.к."
