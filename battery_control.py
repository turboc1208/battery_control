#####################################################
#
#  Battery_Control.py
#
#  Set image on battery sensors to show state.
#
#  Version  Date       Person      Description
#   0.2     24JUL2017  CC          First push from new server        
#
#  Install:
#
#  Download the pictures you want.  Green, Yellow and Red battery images 
#  are available in this repository.  
#  Place them in the .homeassistant/www directory.  Create the www directory if its not there.
#  Put the Battery_control.py app in your appdaemon code storage directory.
#  Add the app to your appdaemon.cfg file as follows
#
#  [battery_control]
#  module=battery_control
#  class=battery_control
#
#  Setup the self.sensors JSON string below as follows All non-numeric values must be in double quotes
#  sensors={"sensor.upstairs_sensor_battery":{"attribute":"state",
#                                               "levels":{"1":{"value":25,"img":"/local/battery1.jpg"},
#                                                     "2":{"value":50,"img":"/local/battery2.jpg"},
#                                                     "3":{"value":75,"img":"/local/battery3.jpg"},
#                                                     "4":{"value":100,"img":"/local/battery4.jpg"}},
#                                               "notify":"EmailChip"},
#           "sensor.office_sensor_battery":{"attribute":"state",
#                                               "levels":{"1":{"value":33,"img":"/local/battery1.jpg"},
#                                                     "2":{"value":66,"img":"/local/battery2.jpg"},
#                                                     "3":{"value":100,"img":"/local/battery4.jpg"}},
#                                             "notify":"EmailChip"}}
#       
#######################################################
import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
import json
               
class battery_control(hass.Hass):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("battery_control App")
    self.sensors={}
    if "sensors" in self.args:
      sensor_data=""
      sensor_data=self.args["sensors"]
      self.sensors=json.loads(sensor_data)
    else:
      self.log("error sensors must be specified in appdaemon.cfg")
    #self.log("sensors={}".format(self.sensors))
    for s in self.sensors:
      for v in self.sensors[s]:
        #self.log("v={}-{}".format(v,self.sensors[s][v]["attribute"]))  
        lookup="{}.attributes.battery_level".format(s)
        cstate=self.get_state(s,attribute=self.sensors[s][v]["attribute"])
        #self.log("lookup={}, cstate={}".format(lookup,cstate))
        self.listen_state(self.state_handler,s,attribute=self.sensors[s][v]["attribute"])
    self.run_every(self.timer_handler,self.datetime(),60)
    self.log("sensor_control initialization complete")
    
  def timer_handler(self,kwargs):
    self.log("timer Check")
    for ts in self.sensors:
      for tv in self.sensors[ts]:
        self.check_sensor_state(ts,self.sensors[ts][tv]["attribute"],"timer")
    self.log("Timer check completed")
     
  def state_handler(self,entity,attribute,old,new,kwargs):
    self.check_sensor_state(entity,attribute,"state")
   
  def check_sensor_state(self,sensor,attribute,source):
    cstate=self.get_state(sensor,attribute=attribute)
    #self.log("check_sensor_state({},{},{})".format(sensor,attribute,source))
    vtyp,vsensor=self.split_entity(sensor)
    #self.log("vtyp={}, vsensor={}, sensor={},self.sensors[sensor]={}".format(vtyp,vsensor,sensor,self.sensors[sensor]))
    for ct in self.sensors[sensor]:
      #self.log("ct={}".format(ct))
      newsensor="sensor.{}_{}".format(vsensor,self.sensors[sensor][ct]["postfix"])
      #self.log("newsensor={}".format(newsensor))
      if ct=="value":
        self.log("setting state for {} to {}".format(newsensor,cstate))
        self.set_state(newsensor,state=cstate)
      elif ct=="text":
        for ev in sorted(self.sensors[sensor]["text"]["values"],key=self.my_key):
          #self.log("{} - ev={}-{}".format(sensor,ev,self.sensors[sensor]["text"]["values"][ev]))
          if float(cstate) <= float(ev):
            self.set_state(newsensor,state=self.sensors[sensor]["text"]["values"][ev])
            self.log("set state of {} to {}".format(newsensor,self.sensors[sensor]["text"]["values"][ev]))
            break
      else:
        self.log("type={} - unknown",format(ct))

  def my_key(self,dict_key):
    try:
      return float(dict_key)
    except ValueError:
      return dict_key
