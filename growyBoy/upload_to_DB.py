import time
from datetime import datetime
from grow.moisture import Moisture
from grow.pump import Pump
import requests
import sqlite3

def check_data_base():
    connection = sqlite3.connect("grow.db")
    cursor = connection.cursor()
    check_rows = cursor.execute("SELECT * FROM grow WHERE uploaded != 1;").fetchall()
    for row in check_rows:
        print(row)
        # send data to api here 
        import requests
        payload = {
        "saturation": 0,
        "moisture": row[1],         
        }
        resp = requests.post('https://63df75c7a76cfd410582cf50.mockapi.io/api/v1/plants/1/sensor_measurements', json=payload)
        print(resp.json())
        # set to the right thing
        change_row = cursor.execute("UPDATE grow SET uploaded = 1 WHERE id = (?)", (row[0],))
        connection.commit()

        

def settings():
    # get the settings from the API to change these
    auto_water = False
    dry_point = 27
    enabled = True
    pump_speed = 0.5
    pump_time = 0.5
    warn_level = 0.2
    watering_delay = 6
    wet_point = 3


def water(channel, dose_speed, dose_time, watering_delay):
    connection = sqlite3.connect("grow.db", detect_types=sqlite3.PARSE_DECLTYPES)
    # | sqlite3.PARSE_COLNAMES
    cursor = connection.cursor()
    
    last_water_freq_row = cursor.execute("SELECT * FROM water_freq ORDER BY id DESC LIMIT 1").fetchone()  # returns
    # DATETIME
    last_dose = last_water_freq_row[1]  # this should be a datetime object
    now = time.mktime(last_dose.timetuple())
    last = time.mktime(datetime.today().timetuple())
    print("now = ", now, "last = ", last)
    if last - now > watering_delay:
        print("here")
        # p = Pump(channel)
        pump1 = Pump(3)
        pump1.set_speed(dose_speed)
        # pump1.dose(0.5, 0.5, blocking=False)
        time.sleep(dose_time)
        pump1.stop()
        # p.dose(dose_speed, dose_time, blocking=False)
        # p.stop()
        now_upload = datetime.today()
        insert_water = cursor.execute("INSERT INTO water_freq (date_time) VALUES (?)", (datetime.now(),))
        try:
            connection.commit()
        except:
            connection.rollback()
            raise
        
        # check if there is data waiting to be uploaded
        check_data_base()
        

def main():
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

    # The above code all works
    water(3, 1, 1, 30)
    
    
if __name__ == "__main__":
    main()
