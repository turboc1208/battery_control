#####################################################
#
#  Battery_Control.py
#
#  Set image on battery sensors to show state.
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
#  Setup the self.batteries dictionary below as follows
#  self.batteries={"<HA Sensor name for battery state>":{"attribute":"<Attribute name (None if it's the default state for the sensor>",
#                                                        "low":<low level>,
#                                                        "med":<medium level>,
#                                                        "notify":"<email address to notify on low level>"},
#                  "<repeat for next sensor>":{"attribute":"<Attribute name (None if it's the default state for the sensor>",
#                                                        "low":<low level>,
#                                                        "med":<medium level>,
#                                                        "notify":"<email address to notify on low level>"}
#                  }
#
#######################################################
import my_appapi as appapi
import datetime
import time
               
class battery_control(appapi.my_appapi):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("battery_control App")
  
    self.batteries={"sensor.den_sensor_battery":{"attribute":None,"low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "sensor.office_sensor_battery":{"attribute":None,"low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "sensor.ring_front_door_battery":{"attribute":None,"low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "zwave.aeotec_zw074_multisensor_gen5_14":{"attribute":"battery_level","low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "zwave.office_door_4":{"attribute":"battery_level","low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "zwave.toolcabinetleft_6":{"attribute":"battery_level","low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "sensor.ring_front_door_battery":{"attribute":None,"low":10,"med":60,"notify":"chip.cox@coxdogs.com"},
                    "zwave.toolcabinetright_7":{"attribute":"battery_level","low":10,"med":60,"notify":"chip.cox@coxdogs.com"}}
    for s in self.batteries:
      self.listen_state(self.state_handler,s,attribute=self.batteries[s]["attribute"])
    self.log("about to set time")
    time=self.datetime()
    self.log("time={}".format(time))
    #self.run_every(self.timer_handler,time,3*60)
    self.log("event scheduled")
    self.check_battery_state()
    self.log("back from check battery state")
     
  def timer_handler(self,**kwargs):
    self.check_battery_state()

  def state_handler(self,entity,attribute,old,new,kwargs):
    self.check_battery_state()

  def check_battery_state(self,**kwargs):
    for b in self.batteries:
      s=self.batteries[b]["attribute"]
      result=self.get_state(b,s)
      self.log("{},{}={}".format(b,s,result))
      if int(float(result))>int(float(self.batteries[b]["med"])):
        # set green picture      
        self.set_state(b,attributes={"entity_picture":"/local/full_battery_icon.jpg"})
      elif int(float(result))>int(float(self.batteries[b]["low"])):
        # set yellow picture
        self.set_state(b,attributes={"entity_picture":"/local/mid_battery_icon.jpg"})
      else:
        # set red picture
        self.set_state(b,attributes={"entity_picture":"/local/low_battery_icon.jpg"})

