
import sqlite3

conn=sqlite3.connect('/home/abdullah/323-Project/roomAppF.db')  

curs=conn.cursor()
curs.execute("""DELETE FROM temperatures""")
curs.execute("""DELETE FROM humidities""")
conn.commit()
conn.close()
