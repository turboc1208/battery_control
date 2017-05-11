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
#  Setup the self.batteries JSON string below as follows All non-numeric values must be in double quotes
#  self.batteries={"<HA Sensor name for battery state>":{"attribute":"<Attribute name>",
#                                                        "low":<low level>,
#                                                        "mid":<medium level>,
#                                                        "notify":"<HA Notification Component>"},
#                  "<repeat for next sensor>":{"attribute":"<Attribute name>",
#                                                        "low":<low level>,
#                                                        "mid":<medium level>,
#                                                        "notify":"<HA Notification Component>"}
#                  }
#       
#######################################################
import appdaemon.appapi as appapi
import datetime
import time
import json
               
class battery_control(appapi.AppDaemon):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("battery_control App")
    if "full_img" in self.args:
      self.full=self.args["full_img"]
    else:
      self.log("error full_img must be specified in appdaemon.cfg")
    if "mid_img" in self.args:
      self.mid=self.args["mid_img"]
    else:
      self.log("error mid_img must be specified in appdaemon.cfg")
    if "low_img" in self.args:
      self.low=self.args["low_img"]
    else:
      self.log("error low_img must be specified in appdaemon.cfg")
    self.batteries={"empty":"list"}
    if "batteries" in self.args:
      battery_data=""
      battery_data=self.args["batteries"]
      self.batteries=json.loads(battery_data)
    else:
      self.log("error batteries must be specified in appdaemon.cfg")
    self.log("batteries={}".format(self.batteries))
    for s in self.batteries:
      self.listen_state(self.state_handler,s,attribute=self.batteries[s]["attribute"])
    self.check_battery_state()
     
  def state_handler(self,entity,attribute,old,new,kwargs):
    currentpic=self.get_state(entity,attribute="entity_picture")
    if currentpic==None:
      self.check_battery_state()
   
  def check_battery_state(self,**kwargs):
    for b in self.batteries:
      s=self.batteries[b]["attribute"]
      result=self.get_state(b,s)
      self.log("Battery {} is at {}%".format(b,result))
      if int(float(result))>int(self.batteries[b]["mid"]):
        # set green picture      
        self.set_state(b,attributes={"entity_picture":self.full})
      elif int(float(result))>int(self.batteries[b]["low"]):
        # set yellow picture
        self.set_state(b,attributes={"entity_picture":self.mid})
      else:
        # set red picture
        self.set_state(b,attributes={"entity_picture":self.low})
        msg="{} battery is at {}%.  Please replace/recharge the batteries".format(b,result)
        if not "last_notification" in self.batteries[b]:
          self.batteries[b]["last_notification"]=self.date()-datetime.timedelta(days=1)
        if self.batteries[b]["last_notification"]<self.date():
          self.batteries[b]["last_notification"]=self.date()
          try:
            self.log("Sending low battery alert for {} to {}".format(b,self.batteries[b]["notify"]))
            self.notify(msg,name=self.batteries[b]["notify"],title="low battery warning")
          except:
            self.log("{} notify failed {}".format(b,self.batteries[b]["notify"]))
            pass
      self.log("batteries={}".format(self.batteries[b]))
