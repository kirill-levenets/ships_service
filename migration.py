"""

for test

sudo docker ps -a
sudo docker rm some-postgres
sudo docker run --name some-postgres -e POSTGRES_PASSWORD=123456 -d -p 54320:5432 postgres

sudo docker stop some-postgres
sudo docker start some-postgres


upsert example:
https://www.postgresqltutorial.com/postgresql-upsert/

...

sudo docker run -d --hostname my-rabbit --name some-rabbit -p 56720:5672 -p 8080:15672 rabbitmq:3-management

"""

import psycopg2
import csv

from settings import DB_URL

dsn = DB_URL
con = psycopg2.connect(dsn)
cur = con.cursor()

################ create countries table #############
# data from https://www.worldometers.info/geography/alphabetical-list-of-countries/

cur.execute("DROP TABLE IF EXISTS countries CASCADE")

cur.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id serial PRIMARY KEY, 
        name varchar UNIQUE,
        population integer,
        area integer,
        density integer 
    );'''
)
con.commit()


data = []
rows_count = 0
with open('static/countries.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in spamreader:
        if rows_count > 0:
            data.extend(row)  # !!!
        rows_count += 1

pls = ["(%s, %s, %s, %s, %s)"] * (rows_count - 1)
query = f'''INSERT INTO countries (id, name, population, area, density) 
        VALUES {", ".join(pls)}
        ON CONFLICT (name) DO NOTHING
'''

cur.execute(query, data)
con.commit()


## !!!!
alter_serial = f"ALTER SEQUENCE countries_id_seq RESTART WITH {rows_count}"
cur.execute(alter_serial)
con.commit()

############# create ships table ####################

cur.execute("DROP TABLE IF EXISTS ships")
con.commit()

cur.execute('''
    CREATE TABLE IF NOT EXISTS ships (
        id serial PRIMARY KEY,
        country_id integer REFERENCES countries(id) NOT NULL,
        name varchar UNIQUE NOT NULL,
        ship_description varchar DEFAULT '--',
        built_year integer NOT NULL,
        length integer DEFAULT 134,
        width integer DEFAULT 100,
        gt integer DEFAULT 300,
        dwt integer DEFAULT 700
    );'''
)

# cur.execute("CREATE UNIQUE INDEX ships_name_idx ON public.ships (name);")

con.commit()

insert_ship = '''
INSERT INTO ships (name, country_id, ship_description, built_year) 
VALUES (%s, (SELECT id from countries WHERE name=%s), %s, %s);
'''

for i in range(50):
    print(i)
    cur.execute(
        insert_ship, (f'ship #{i}', 'Ukraine', f'ship with flag', 2000 + i))
    con.commit()

cur.execute('''
    SELECT ships.*, countries.name 
    FROM ships inner join countries on ships.country_id = countries.id
    WHERE ships.name LIKE %(pattern)s
    LIMIT 1000''',
    {'pattern': '%' + '9' + '%'}
)

for v in cur:
    print('row: ', v)


# result = cur.fetchall()

# print(
#     len(result),
#     '\n'.join([str(r) for r in result])
# )



# Close communication with the database
cur.close()
con.close()

# TODO: create rabbit queues before start

