#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'GPIO处理'
__author__ = 'kakake'

from GPIO import GPIO
from httphandle import httphandle
	
#命令解析
#1.cmdname:setgpio	设置指定GPIO，包括setup和loop两部分
#{"cmdname":"setgpio","setup":{"1":"out","4":"out"},"loop":[{"pinval":[1,0]},{"sleep":1},{"pinval":[1,1]}]}
#2.cmdname:replygpio	设置指定GPIO并返回IN
#{"cmdname":"replygpio","setup":{"1":"out","4":"out"},"loop":[{"pinval":[1,0]},{"sleep":1},{"pinval":[1,1]}],"reply":[1,4]}
#3.cmdname:getgpio	获取指定GPIO
#{"cmdname":"getgpio","pins":[0,1]}
#4.cmdname:getgpios 	请求所有GPIO的状态
#{"cmdname":"getgpios"}
class gpiohandle(httphandle):
    def __init__(self,name='gpio',interval=0.1,hostname=""):
        httphandle.__init__(self,name,interval,hostname)
        self.gpio=GPIO()
    def execute(self):#重写
        self.gpio.stop()#停止之前的命令
        cmd= self.gethttpdata(self.name)
        if cmd<>None:
		    cmdname=cmd['cmdname']
		
		    if cmdname=='setgpio':
			    self.setgpio(cmd)
		    elif cmdname=='replygpio':
			    self.replygpio(cmd)
		    elif cmdname=='getgpio':
			    self.getgpio(cmd)
		    elif cmdname=='getgpios':
			    self.getgpios()
			
    def checkGPIO(self, gpio):
        i = int(gpio)
        if not self.gpio.isAvailable(i):
            print "GPIO " + gpio + " Not Available"
            return False
        if not self.gpio.isEnabled(i):
            print "GPIO " + gpio + " Disabled"
            return False
        return True
			
    def getgpios(self):
		data=self.gpio.writeJSON()
		self.posthttpdata(self.name,data)
		
		
    def getgpio(self,cmd):
		pins=cmd["pins"]
		self.gpio.reply(pins)
		
    def setgpio(self,cmd):
		setup=cmd['setup']
		loop=cmd['loop']
		self.gpio.setdata(setup,loop)
		self.gpio.setDaemon(True)#守护线程
		self.gpio.start()#开始执行命令
		
    def replygpio(self,cmd):
		setup=cmd['setup']
		loop=cmd['loop']
		reply=cmd['reply']
		self.gpio.setdata(setup,loop,reply,self.posthttpdata)
		self.gpio.setDaemon(True)#守护线程
		self.gpio.start()#开始执行命令
