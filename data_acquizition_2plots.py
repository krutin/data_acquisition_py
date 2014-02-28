import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt
 
# class that holds analog data for N samples
class AnalogData:
  # constr
  def __init__(self, maxLen):
    self.ax = deque([0.0]*maxLen)
    self.ay = deque([0.0]*maxLen)
    self.maxLen = maxLen
 
  # ring buffer
  def addToBuf(self, buf, val):
    if len(buf) < self.maxLen:
      buf.append(val)
    else:
      buf.pop()
      buf.appendleft(val)
 
  # add data
  def add(self, data):
    assert(len(data) == 2)
    self.addToBuf(self.ax, data[0])
    self.addToBuf(self.ay, data[1])
    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, analogData):
    # set plot to animated
    fig = plt.figure(1)
    plt.ion()
    fig = plt.figure(1)
    temp_plot = fig.add_subplot(211)
    temp_plot.set_title('Temperature (Celcius)')
    temp_plot.set_autoscaley_on(False)
    temp_plot.set_ylim([0,50])
    #temp_plot.xlabel('Samples')
    #temp_plot.ylabel('Celcius')
    self.axline, = temp_plot.plot(analogData.ax)
    
    ldr_plot = fig.add_subplot(212)
    ldr_plot.set_title('LDR (Volts) ')
    ldr_plot.set_autoscaley_on(False)
    ldr_plot.set_ylim([0,5])
    #ldr_plot.xlabel('Samples')
    #ldr_plot.ylabel('Volts')
    self.ayline, = ldr_plot.plot(analogData.ay)
    
 
  # update plot
  def update(self, analogData):
    self.axline.set_ydata(analogData.ax)
    self.ayline.set_ydata(analogData.ay)
    plt.draw()
 
# main() function
def main():
  # expects 1 arg - serial port string
  """if(len(sys.argv) != 2):
    print 'Example usage: python showdata.py "/dev/tty.usbmodem411"'
    exit(1)"""
  figure = 0
 #strPort = '/dev/tty.usbserial-A7006Yqh' ## Example for Linux/OSX Platform
  #strPort = 'COM9' ## Example for Windows platform
  strPort = raw_input("Which Serial port is your device connected to >> ")
 
  # plot parameters
  analogData = AnalogData(500)
  analogPlot = AnalogPlot(analogData)
  
  print 'plotting data...'
 
  # open serial port
  ser = serial.Serial(strPort, 9600)
  ser.write('s')
  print "Seems like serial port is open..."
  
  while True:
    try:
      print "Getting new data..."
      line = ser.readline()
      print "Data :: "
      print line
      print "\n"
      data = [float(val) for val in line.split()]
      #print data
      if(len(data) == 2):
        analogData.add(data)
        analogPlot.update(analogData)
        
    except KeyboardInterrupt:
      print 'exiting'
      break
  # close serial
  ser.flush()
  ser.close()
 
# call main
if __name__ == '__main__':
  main()
