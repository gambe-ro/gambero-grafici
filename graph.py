import os
import mysql.connector
import pandas as pd
import count_per_day_graph
import day_of_the_week_graph
import count_per_week_graph
from bokeh.plotting import save
from bokeh.layouts import row, column

username = os.environ.get("MYSQL_USERNAME", "root")
password = os.environ.get("MYSQL_PASSWORD", "sss")
hostname = os.environ.get("MYSQL_HOSTNAME", "172.20.0.3")
port = os.environ.get("MYSQL_PORT", "3306")
database = os.environ.get("MYSQL_DATABASE", "test")

gambero_db = mysql.connector.connect(
    host=hostname,
    user=username,
    passwd=password,
    database=database
)
post_per_day = pd.read_sql(
    'select count(*) as count, DATE(created_at) as date from comments group by DATE(created_at);', con=gambero_db)
fig_1 = count_per_day_graph.plot(post_per_day["date"], post_per_day["count"], "Commenti per giorno")

post_per_week = pd.read_sql(
    """select count(*) as count, CONCAT(YEAR(created_at), \'-\', WEEK(created_at)) as week from comments 
    group by CONCAT(YEAR(created_at), \'-\', WEEK(created_at));""",
    con=gambero_db)
fig_2 = count_per_week_graph.plot(pd.to_datetime(post_per_week["week"].add('-0'), format='%Y-%W-%w'),
                                  post_per_week["count"], "Commenti per settimana")

post_per_day_of_week = pd.read_sql(
    'select count(*) as count, WEEKDAY(created_at) as day from comments group by WEEKDAY(created_at);', con=gambero_db)
fig_3 = day_of_the_week_graph.plot(post_per_day_of_week["day"], post_per_day_of_week["count"],
                                   "Commenti per giorno della settimana")

save(column(row(fig_1, fig_2), fig_3), filename="/tmp/graph.html", title="Gambe.ro grafici")
