import os
import mysql.connector
import pandas as pd
import count_per_day_graph
import day_of_the_week_graph
import count_per_week_graph
import post_per_tag_graph
import upvotes_hour_of_day
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

day_of_week = pd.read_sql(
    'select count(*) as count, WEEKDAY(created_at) as day from comments group by WEEKDAY(created_at);', con=gambero_db)
fig_3 = day_of_the_week_graph.plot(day_of_week["day"], day_of_week["count"],
                                   "Commenti per giorno della settimana")

most_used_tags = pd.read_sql(
"""select tag as tag, count(*) as count from taggings as ts join tags as t on t.id=ts.tag_id join stories as s on s.id=ts.story_id 
group by tag order by count(*) desc limit 30;""",
con=gambero_db)

fig_4 = post_per_tag_graph.plot(most_used_tags["tag"][::-1], most_used_tags["count"][::-1],
                                   "Tag più usate")

least_used_tags = pd.read_sql(
    """select tag as tag, count(*) as count from taggings as ts join tags as t on t.id=ts.tag_id join stories as s on s.id=ts.story_id 
    group by tag order by count(*) asc limit 20;""",
    con=gambero_db)

fig_5 = post_per_tag_graph.plot(least_used_tags["tag"], least_used_tags["count"],
                                "Tag meno usate")

stories_upvotes_by_hour = pd.read_sql(
    'select count(vote)/count(distinct(v.story_id)) as count, HOUR(s.created_at) as hour from stories as s join votes as v on s.id=story_id group by HOUR(s.created_at);', con=gambero_db)
fig_6 = upvotes_hour_of_day.plot(stories_upvotes_by_hour["hour"], stories_upvotes_by_hour["count"],
                                   "Performance storie per ora di creazione")


save(column(row(fig_1, fig_2), row(fig_3,fig_6), fig_4, fig_5), filename="/tmp/graph.html", title="Gambe.ro grafici")
