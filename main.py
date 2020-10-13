import pandas as pd
import datetime
from datetime import datetime, timedelta
import requests
import csv
import psycopg2


def init_db():
    con = psycopg2.connect(database="postgres", user="user", password="tes123", host="127.0.0.1", port="5432")
    print("Database opened successfully")
    con.autocommit = True
    cur = con.cursor()
    return cur


def update_tracking(site):
    cur.execute("""select * from request_tracking where website_name = {} order by 
    last_req_ts desc limit 1""".format(site))
    data = cur.fetchall()
    df_req = pd.DataFrame(data, columns=[x[0] for x in cur.description])
    now = datetime.now()
    if datetime.now() - timedelta(minutes=30) > df_req['last_req_ts']:
        values = (site, now.strftime("%m/%d/%Y %H:%M:%S"))
        cur.execute("INSERT INTO request_tracking (website_name, last_req_ts) VALUES {}".format(values))
        return 'not fresh'
    else:
        return 'fresh'


def request(site):
    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    params = {'apikey': '3840c426fa25fa993dd9d5dd8a59230a748114c7f7c7049ecc48ffc468f13d55', 'resource': site,
              'allinfo': True}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(response.status_code))
    response_json = response.json()
    site_grouped_by_type = pd.DataFrame.from_dict({(i, j): response_json['scans'][i][j]
                                                   for i in response_json['scans'].keys()
                                                   for j in response_json['scans'][i].keys()},
                                                  orient='index', columns=['type']).groupby('type').size()
    site_risk = 'safe' if response_json['positives'] == 0 else 'risk'
    clean = site_grouped_by_type['clean site']
    unrated = site_grouped_by_type['unrated site']
    values = (site, site_risk, clean, unrated)
    return values


def insert_data(data):
    if exsits in db: # not fully written , checks if sites already in table tracking if yes makes update not insert 
        cur.execute("""UPDATE websites
        SET site_risk = {}, clean={}, unrated ={}
        WHERE website_name = {}}
        RETURNING *;""".format(data[1], data[2], data[3], data[0]))
    else:
        cur.execute("INSERT INTO websites (website_name, site_risk, clean, unrated) VALUES {}".format(values))


if __name__ == "__main__":
    cur = init_db()
    with open('sites/request1.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            site = row[0]
            last_update_status = update_tracking(site)
            if last_update_status != 'fresh':
                request(site)
            insert_data()
