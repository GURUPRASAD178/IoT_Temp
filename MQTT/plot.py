import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

db=sqlite3.connect("sensor_data.db")

fig,(ax1,ax2)=plt.subplots(2,1,figsize=(10,8))

def update(i):

    cursor=db.cursor()

    cursor.execute("""
    SELECT timestamp,temperature,humidity
    FROM sensor_data
    ORDER BY id DESC
    LIMIT 20
    """)

    rows=cursor.fetchall()

    rows=rows[::-1]

    time=[]
    temp=[]
    hum=[]

    for r in rows:
        time.append(r[0][-8:])
        temp.append(r[1])
        hum.append(r[2])

    ax1.clear()
    ax2.clear()

    ax1.plot(time,temp,marker='o')
    ax1.set_title("Temperature")
    ax1.set_ylabel("°C")
    ax1.grid(True)

    ax2.plot(time,hum,marker='o')
    ax2.set_title("Humidity")
    ax2.set_ylabel("%")
    ax2.set_xlabel("Time")
    ax2.grid(True)

    plt.setp(ax1.get_xticklabels(), rotation=45)
    plt.setp(ax2.get_xticklabels(), rotation=45)

ani=FuncAnimation(fig,update,interval=2000)

plt.tight_layout()

plt.show()