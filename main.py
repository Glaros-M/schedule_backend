from flask import Flask
from view_generator import get_table_by_group_name
from models import get_data_from_file, get_group_names_list
from flask import request



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# TODO: Переписать тут код, для подгрузки в оперативу данных о всех факультетах. (зависит от предоставляемых данных)
INPUT_FILE = "rasp.json"
ALL_FACULTIES = [get_data_from_file(INPUT_FILE)]


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.get("/groups")
def get_all_groups() -> dict:
    """Пока что тестовые значения"""
    group_name = request.args.get('group_name')
    if not group_name:
        group_name = ""
    grops_list = get_group_names_list(ALL_FACULTIES)
    grops_list = list(filter(lambda x: group_name.upper() in x, grops_list))
    out = {"groups": grops_list, "query": group_name}
    return out


@app.get("/schedule")
def get_schedule_by_group_name() -> str:  # Возвращается шаблон
    """Пока что тестовые значения"""
    group_name = request.args.get('group_name')
    if not group_name:
        group_name = "ОП2-221-ОБ"
    out = get_table_by_group_name(group_name=group_name, list_faculties=ALL_FACULTIES)
    return out


if __name__ == "__main__":
    print(get_all_groups(""))
