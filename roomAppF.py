
from flask import Flask, request, render_template
import sys
import Adafruit_DHT
import time
import datetime
import sqlite3

app = Flask(__name__)
app.debug = True 

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/")
def room_temp():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	if humidity is not None and temperature is not None:
		return render_template("roomAppF.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")
		
@app.route("/details", methods=['GET'])
def room_env_db():
	temperatures, humidities, from_date_str, to_date_str = get_records()
	#return render_template("room_env_db.html",temp=temperatures,hum=humidities,temp_items= len(temperatures),hum_items= len(humidities))
	return render_template(	"room_env_db.html",
							temp 			= temperatures,
							hum 			= humidities,
							from_date 		= from_date_str, 
							to_date 		= to_date_str,
							temp_items 		= len(temperatures),
							hum_items 		= len(humidities))

def get_records():
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) 
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   
	range_h_form	= request.args.get('range_h','');  

	range_h_int 	= "nan"  

	try: 
		range_h_int	= int(range_h_form)
	except:
		print ("range_h_form not a number")

	if not validate_date(from_date_str):			# Validate date before sending it to the DB
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")		# Validate date before sending it to the DB

	# If range_h is defined, we don't need the from and to times
	if isinstance(range_h_int,int):	
		time_now		= datetime.datetime.now()
		time_from 		= time_now - datetime.timedelta(hours = range_h_int)
		time_to   		= time_now
		from_date_str   = time_from.strftime("%Y-%m-%d %H:%M")
		to_date_str	    = time_to.strftime("%Y-%m-%d %H:%M")

	conn=sqlite3.connect('/home/abdullah/323-Project/roomAppF.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return [temperatures, humidities, from_date_str, to_date_str]
		

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
