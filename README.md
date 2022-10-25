# schedule_backend


# Структура данных:

## Faculties
    faculty_name : str,
    date_start : str | datetime,
    date_end : str | datetime,
    groups : list[Groups]

## Groups
    group_name : str,
    course : int,
    days: list[Days]

## Days
    weekday : int,
    lessons : list[Lessons]

## Lessons
    subject : str //Название предмета
    type : str,   //Тип занятия. "лек.", "лаб.", "прак."
    subgroup : int, //Подгруппа 0-вся группа, 1 - первая, 2 - вторая
    time_start : str | datetime.time,     //Вот тут возможно словарь с соотношением номера пары и времени
    time_end : str | datetime.time,
    time : int,   //Порядковый номер пары
    week : 7,     //Номер недели от начала года, вродебы (?)
    date : str,      //Дата занятия
    teachers : list[Teachers]
    auditories : list[Auditories]

## Teachers
    teacher_name : str // "Вакансия" или "Фамилия И.О."


## Auditories
    auditory_name : str // "201к/7к" или "Спортзал Гл.к."


| Дата, день | Время_начала | Время_конца | Название предмета | Тип пары | Аудитория | Преподаватель |
|------------|------------|------------|------------|------------|------------|------------|
|1|2|3|4|5|6|7|

