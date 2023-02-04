import time

from grow.moisture import Moisture

import sqlite3
connection = sqlite3.connect("grow.db")

print(connection.total_changes)

print("""moisture.py - Print out sensor reading in Hz

Press Ctrl+C to exit!

""")

m1 = Moisture(1)
m2 = Moisture(2)
m3 = Moisture(3)


cursor = connection.cursor()

insert = cursor.execute("INSERT INTO grow (sensor1, sensor2, sensor3) VALUES (m1, m2, m3)", (m1, m2, m3))


rows = cursor.execute("SELECT * FROM grow").fetchall()
print(rows)

# Print out the sensor reading every 15 mins.
# while True:
    # print(f"""1: {m1.moisture}
        # 2: {m2.moisture}
        # 3: {m3.moisture}
        # """)
