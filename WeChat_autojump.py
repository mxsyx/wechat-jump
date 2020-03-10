import numpy as np
import os,math,time
from PIL import Image

def screencap(i):
	os.system('adb shell screencap -p /sdcard/%d.png'%i)
	os.system('adb pull /sdcard/%d.png ./screencap'%i)

def jump(distance):
	press_time=(distance*2.04)
	command='adb shell input swipe 500 500 500 500 %d'%(press_time)
	os.system(command)

def find_now(image):
	im=np.array(image)
	points=[]
	for row in range(image.size[0]):
		total=0
		for column in range(image.size[1]):
			now=im[column][row].tolist()
			isme=abs(now[0]-54)<10 and abs(now[1]-52)<10 and abs(now[2]-92)<10
			if isme:
				total+=1
			else:
				if total>30:
					points.append([row+10,column-10,total])
					total=0
	maxPoint=[0,0,0]
	for point in points:
		if point[2]>maxPoint[2]:
			maxPoint=point
	return maxPoint[0],maxPoint[1]

def	find_target_top(image,x_now,y_now):
	im=np.array(image)
	if(x_now>=360):
		for column in range(300,y_now):
			for row in range(0,360):
				isme=im[0][row].sum()-im[column][row].sum()
				if isme>100:
					return row,column
	else:
		for column in range(300,y_now):
			for row in range(719,360,-1):
				isme=im[0][row].sum()-im[column][row].sum()
				if isme>100:
					return row,column

def	find_target_lar(image,x_now,y_now):
	im=np.array(image)
	x_top,y_top=find_target_top(image,x_now,y_now)
	if(x_now>=360):
		for row in range(0,x_top):
			for column in range(y_top,y_now):
				isme=(im[y_top][x_top].sum()-im[column][row].sum() if im[y_top][x_top].sum()>im[column][row].sum() else im[column][row].sum()-im[y_top][x_top].sum())
				if isme<70 and column<y_now:
					return x_top,column

	else:
		for row in range(719,x_top,-1):
			for column in range(y_top,y_top+200):
				isme=(im[y_top][x_top].sum()-im[column][row].sum() if im[y_top][x_top].sum()>im[column][row].sum() else im[column][row].sum()-im[y_top][x_top].sum())
				if isme<50 and column<y_now:
					return x_top,column

def manage():
	print('运行日志：\n')
	try:	
		os.system('adb connect 10.132.4.50:5555')
	except Exception:
		print('连接手机失败')
		return 1
	try:
		for i in range(1,200):
			print('\n============正在进行第%d次跳跃============'%i)
			print('正在采集图片...')
			screencap(i)
			print('图片采集完毕...')
			image=Image.open('./screencap/%d.png'%i)
			print('正在计算棋子坐标...')
			x_now,y_now=find_now(image)
			print('棋子坐标计算完成，棋子坐标为（%d,%d）'%(x_now,y_now))
			print('正在计算目标块中心坐标...')
			x_center,y_center=find_target_lar(image,x_now,y_now)
			print('目标块中心坐标计算完成，目标块中心坐标为（%d,%d）'%(x_center,y_center))
			distance=math.hypot(x_center-x_now,y_center-y_now)
			print('跃点距离：%d'%(distance))
			print('正在尝试跳跃.....')
			jump(distance)
			time.sleep(1)
			print('============第%d次跳跃完成============'%i)
	except Exception:
		print('跳跃失败，退出')
		return 1

if __name__ == '__main__':
	manage()
