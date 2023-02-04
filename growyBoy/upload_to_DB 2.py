import time

from grow.moisture import Moisture
from grow.pump import Pump

import sqlite3

connection = sqlite3.connect("grow.db")

print(connection.total_changes)

print("""moisture.py - Print out sensor reading in Hz

Press Ctrl+C to exit!

""")

m1 = Moisture(1)
m2 = Moisture(2)
m3 = Moisture(3)

while m1.moisture < 0.0001:
    time.sleep(5)

cursor = connection.cursor()

insert = cursor.execute("INSERT INTO grow (sensor1, sensor2, sensor3, uploaded) VALUES (?, ?, ?, ?)",
                        (m1.moisture, m2.moisture, m3.moisture, 0))
try:
    connection.commit()
except:
    connection.rollback()
    raise

rows = cursor.execute("SELECT * FROM grow").fetchall()
print(rows)

# get the settings from the API to change these
auto_water = False
dry_point = 27
enabled = True
pump_speed = 0.5
pump_time = 0.5
warn_level = 0.2
watering_delay = 60
wet_point = 3

last_water_row = cursor.execute("SELECT * FROM water_freq ORDER BY id DESC LIMIT 1;").fetchall()
last_dose = last_water_row[1]
time = time.datetime.now()


def water(channel, dose_speed, dose_time, last_dose):
    if time.time() - last_dose > DOSE_FREQUENCY:
        p = Pump(channel)
        p.dose(dose_speed, dose_time)
        p.off()
        insert_water = cursor.execute("INSERT INTO water_freq (timedate) VALUES (?)", (time.datetime.now()))
        try:
            connection.commit()
        except:
            connection.rollback()
            raise

