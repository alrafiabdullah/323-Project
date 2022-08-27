
import sqlite3
import sys
import Adafruit_DHT

def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/home/abdullah/323-Project/roomAppF.db')  
	
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()
	return

def add_record():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

	if humidity is not None and temperature is not None:
		log_values("1", temperature, humidity)	
	else:
		log_values("1", -999, -999)
	return
