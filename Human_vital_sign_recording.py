import numpy as np
import time
import board
import matplotlib.pyplot as plt
from smbus import SMBus
import adafruit_mlx90640
import busio
from matplotlib.animation import FuncAnimation
import serial
import cv2
temp=0.0
distance=0
heart_rate=0
breath_rate=0
high=0.0
ser= serial.Serial("/dev/ttyACM1",115200)
ser1= serial.Serial("/dev/ttyACM0",9600)
print("logging")
#values=[]
#values1=[]
i2c= busio.I2C(board.SCL,board.SDA,frequency=400000)
mlx= adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate=adafruit_mlx90640.RefreshRate.REFRESH_4_HZ
frame=[0]*768
fig,ax=plt.subplots(figsize=(8,6))
thermal_img=ax.imshow(np.zeros((240,320)),cmap="inferno",vmin=20,vmax=40)
plt.colorbar(thermal_img)
dis_txt=ax.text(0.02,0.95,f"{distance}breath per min",fontsize=15,color="black",transform=ax.transAxes)
heart_txt=ax.text(0.02,0.90,f"{heart_rate}cm",fontsize=15,color="black",transform=ax.transAxes)
breath_txt=ax.text(0.02,0.85,f"{breath_rate}bpm",fontsize=15,color="black",transform=ax.transAxes)
temp_txt=ax.text(0.02,0.80,f"temperature:{temp}C",fontsize=15,color="black",transform=ax.transAxes)
height_txt=ax.text(0.02,0.75,f"height:{(high):.1f}cm",fontsize=15,color="black",transform=ax.transAxes)
def update(frame_num):
    for i in range(3):
        global distance,breath_rate,heart_rate,temp,high
        if ser.in_waiting:
            data=ser.readline().decode().strip()
            print(data)
            #values.append(data)
            if i==0: distance=data
            if i==1: breath_rate=data
            if i==2: heart_rate=data
    if ser1.in_waiting:
        data1=ser1.readline().decode().strip()
        data1= float(data1)
        high= 205-data1
        if high<70: high=0
        print(f"height:{(high):.1f}")
        #values1.append(high)
    try:
        mlx.getFrame(frame)
        data2=np.reshape(frame,(24,32))
        data2_resized = cv2.resize(data2, (240, 320), interpolation=cv2.INTER_CUBIC)
        thermal_img.set_data(data2_resized)
        dis_txt.set_text(f"{distance}breath per min")
        heart_txt.set_text(f"{heart_rate}cm")
        breath_txt.set_text(f"{breath_rate}bpm")
        temp_txt.set_text(f"temperature:{np.max(data2):.1f}C")
        height_txt.set_text(f"height:{(high):.1f}cm")
        return[thermal_img,dis_txt,heart_txt,breath_txt,height_txt]
    except ValueError:
        print("dropped frame")
        return[]
plt.subplots_adjust(left=0.05,right=0.95,top=0.95,bottom=0.05)
ani=FuncAnimation(fig,update,interval:=250)

plt.title("thermal image")
plt.show()