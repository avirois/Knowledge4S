from flask import Blueprint, render_template
from modules.search import search
from datetime import datetime
import sqlite3

DB_NAME = "database.db"
limit_by_days = 30

last_updates_blueprint = Blueprint("last_updates_blueprint", __name__, template_folder="templates")


def parse_file_time(string):
    tmp = string.split(" ")
    date = tmp[0]
    time = tmp[1]
    date = date.split("-")
    time = time.split(":")
    return "{}/{}/{} - {}:{}".format(date[2],date[1],date[0],time[0],time[1])


@last_updates_blueprint.route('/last_updates', methods = ['GET', 'POST'])
def last_updates():
    search_res = search(DB_NAME,'all','all','all','all','all','all','all')
    now  = datetime.now().date()
    print(now)
 

    as_list = []
    for line in search_res:
        as_list.append(list(line))

    for line in as_list:
        for index_in_line in range(len(line)):
            if index_in_line == 1 or index_in_line == 2:
                date = datetime.strptime(line[index_in_line], '%Y-%m-%d %H:%M:%S.%f').date()
                age = now - date
                if age.days<=limit_by_days:
                    show = 1
                else:
                    show = 0

                tmp = (parse_file_time(line[index_in_line]),show)
                line[index_in_line] = tmp
    return render_template('last_updates.html',search_res=as_list)