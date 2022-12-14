import datetime
from typing import NamedTuple
from pydantic import BaseModel


class JsonFaculties(BaseModel):
    faculties: list["Faculties"]

    def __repr__(self):
        s = ""
        for faq in self.faculties:
            s+= str(faq)
        return s

    def __str__(self):
        return self.__repr__()


class Faculties(BaseModel):

    faculty_name: str | None
    date_start: str | None #| datetime.date
    date_end: str | None #| datetime.date
    groups: list["Groups"] #| None
    id: int | None = None

    def __repr__(self):
        s = f" {self.faculty_name=}\n"
        for group in self.groups:
            s += '\t' + str(group) + "\n"
        return s 

    def __str__(self):
        return self.__repr__()


class Groups(BaseModel):
    #id: int
    group_name: str
    course: int
    days: list["Days"]
    
    def __repr__(self):
        s = f"{self.group_name}\n"
        for day in self.days:
            s += "\t\t" + str(day) + "\n"
        return s

    def __str__(self):
        return self.__repr__()


class Days(BaseModel):
    #id: int
    weekday: int
    lessons: list["Lessons"] | None = None
    
    def __repr__(self):

        s = f"{self.weekday}\n"
        if self.lessons:
            for lesson in self.lessons:
                s += "\t\t\t" + str(lesson) + "\n"
        else:
            s += "\t\t\tNo lessons"
        return s


    def __str__(self):
        return self.__repr__()


class Lessons(BaseModel):
    #id: int
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
    
    def __repr__(self):
        s = f"{self.time}-{self.subject}\n"
        for teach in self.teachers:
            s += "\t\t\t\t" + str(teach) + "\n"
        for aud in self.auditories:
            s += "\t\t\t\t" + str(aud) + "\n"
        return s

    def __str__(self):
        return self.__repr__()


class Teachers(BaseModel):
    #id: int
    teacher_name: str # "Вакансия" или "Фамилия И.О."
    
    def __repr__(self):
        return f"{self.teacher_name}"

    def __str__(self):
        return self.__repr__()


class Auditories(BaseModel):
    #id: int
    auditory_name: str # "201к/7к" или "Спортзал Гл.к."
    
    def __repr__(self):
        return f"{self.auditory_name}"

    def __str__(self):
        return self.__repr__()



Lessons.update_forward_refs()
Days.update_forward_refs()
Groups.update_forward_refs()
Faculties.update_forward_refs()
JsonFaculties.update_forward_refs()


"""Блок функций. Не уверен что ему место тут, но пока пускай лежит"""


def get_data_from_file(path: str) -> JsonFaculties:
    with open(path, encoding="utf8") as file:
        data = file.read()
    facultie = JsonFaculties.parse_raw(data)
    return facultie


def search_by_group_name(group_name: str, all_files: list[JsonFaculties]) -> Groups | None:
    finded = None
    for faculties in all_files:
        for facultie in faculties.faculties:
            for group in facultie.groups:
                if group.group_name == group_name:
                    finded = group
    return finded


def get_group_names_list(all_files: list[JsonFaculties]) -> list[str]:
    groups = []
    for faculties in all_files:
        for facultie in faculties.faculties:
            for group in facultie.groups:
                groups.append(group.group_name)
    return groups



if __name__ == "__main__":
    data = get_data_from_file("rasp.json")
    print(search_by_group_name("ИС2-222-ОБ", [data]))