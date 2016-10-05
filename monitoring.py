import psutil
import socket
import time
import matplotlib.pyplot as plt
import numpy as np
import pylab
import matplotlib
import matplotlib.dates
import datetime
import subprocess
import platform
import os
from datetime import timedelta
import requests
import socket
import logging

logger = logging.getLogger('performance')
hdlr = logging.FileHandler('performance.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

def _cpu_perf(plo):
 
 objects = ('CPU 1', 'CPU 2', 'CPU 3', 'CPU 4', 'CPU 5', 'CPU 6', 'CPU 7', 'CPU 8')
 performance = psutil.cpu_percent(interval=1, percpu=True)
 y_pos = np.arange(len(performance))
 logger.info('CPU per core: '+str(performance))
 if plo==1:
  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects)
  plt.ylabel('Usage')
  plt.title('CPU usage')
  plt.savefig('cpu.test.png')
  plt.close()

def _get_time():
 print (time.strftime("%H:%M:%S"),time.strftime("%d/%m/%Y"))

def _monitor_bandwith():
    fig = pylab.figure()
    ax = fig.gca()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('Bandwith')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Bandwith in Mbps')
    ax.xaxis.set_major_formatter(
    matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S')
    )
    plt.ion()
    plt.setp(ax.get_xticklabels(), size=8)
    plt.grid(True)
    old_value = 0
    while True:
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        if old_value:
            send_stat(new_value - old_value)
        old_value = new_value
        time.sleep(1)
def convert_to_gbit(value):
    return value/1024./1024./1024.*8
def convert_to_mbit(value):
    return value/1024./1024.*8
def send_stat(value):
    _get_time()
    print ("%0.3f" % convert_to_gbit(value))
    now = datetime.datetime.now()
    now.isoformat()
    x = [now]
    xs = matplotlib.dates.date2num(x)
    plt.ylim(-20, 1000)
    plt.scatter(xs, convert_to_mbit(value))
    plt.savefig('net.test.png')
    logger.info(str(convert_to_mbit(value))+' Gbps')
    plt.pause(5.0)

def _get_name(pid):
    p = psutil.Process(pid)
    p_name = p.name
    print ("p_name:", p.name)

def _name_proc(pid):
 for proc in psutil.process_iter():
   if proc.pid == pid:
        msg = 'name {}'
        msg = msg.format(str(proc.name))
        print (msg)

def _get_mem(plo):
 virtual = psutil.virtual_memory().percent
 swap = psutil.swap_memory().percent
 objects = ('VIRTUAL', 'SWAP')
 performance = [virtual,swap]
 logger.info('Memory : '+str(virtual)+' : Virtual | '+str(virtual)+' : SWAP')
 if plo==1:
  y_pos = np.arange(len(performance))
  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects)
  plt.ylabel('Usage')
  plt.title('Memory usage')
  plt.savefig('mem.test.png')
  plt.close()
  plt.pause(5.0)

def _get_disk(plo):
 if  platform.system().lower()=="windows":
  disk_c =  psutil.disk_usage('C:')
  disk_d =  psutil.disk_usage('D:')
  objects = ('Disk C','Disk D')
  performance = [disk_c.percent,disk_d.percent]
  logger.info('Disk Usage C: '+str(disk_c.percent))
  logger.info('Disk Usage D: '+str(disk_d.percent))
  
 else:
  root_disk =  psutil.disk_usage('/')
  logs =  psutil.disk_usage('/var/log/')
  objects = ('/','/var/log/')
  performance = [root_disk.percent,logs.percent]
  logger.info('Disk Usage / '+str(root_disk.percent))
  logger.info('Disk Usage /var/log '+str(logs.percent))
 if plo==1:
  y_pos = np.arange(len(performance))
  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects)
  plt.ylabel('Usage')
  plt.title('Disk usage')
  plt.savefig('disk.test.png')
  plt.close()
  plt.pause(5.0)
 
def _http_request(host):
 r = requests.get(host)
 str_elapsed = str(r.elapsed.total_seconds())+' delay to ' + host
 print(str_elapsed)
 logger.info(str_elapsed)

def _ping(host):
    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    # Ping
    #ping = os.system("ping " + ping_str + " " + host)
    print (ping)

#_monitor_bandwith()
while True:
 #_ping('8.8.8.8')
 _http_request("http://google.com")
 #_get_time()
 #Switch on (1)/off (0) plotting
 #_get_mem(0)
 #_cpu_perf(0)
 #_get_disk(0)
