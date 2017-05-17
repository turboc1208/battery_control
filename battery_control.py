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
#  batteries={"sensor.upstairs_sensor_battery":{"attribute":"state",
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
import appdaemon.appapi as appapi
import datetime
import time
import json
               
class battery_control(appapi.AppDaemon):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("battery_control App")
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
    self.run_every(self.timer_handler,self.datetime(),5*60)
    
  def timer_handler(self,kwargs):
    self.log("timer Check")
    self.check_battery_state()
     
  def state_handler(self,entity,attribute,old,new,kwargs):
    currentpic=self.get_state(entity,attribute="entity_picture")
    if currentpic==None:
      self.check_battery_state(battery=entity)
   
  def check_battery_state(self,**kwargs):
    blist=[]
    if "battery" in kwargs:
      blist.append(kwargs["battery"])
    else:   
      for b in self.batteries:
        blist.append(b)
    for b in blist:
      s=self.batteries[b]["attribute"]
      result=self.get_state(b,s)
      self.log("Battery {} is at {}%".format(b,result))
      if (result==None) or (result==""):
        self.log("Battery {} returned None skipping".format(b))
        continue
      #self.log("batteries[{}]['levels']={}".format(b,self.batteries[b]))
      for level in sorted(self.batteries[b]["levels"]):
        #self.log("level={} result={}, level[value]={}".format(level,result,self.batteries[b]["levels"][level]["value"]))
        if int(float(result))<=self.batteries[b]["levels"][level]["value"]:
          self.set_state(b,attributes={"entity_picture":self.batteries[b]["levels"][level]["img"]})
          break
      self.log("level={}".format(level))
      if level==len(self.batteries[b]["levels"]):    
        msg="{} battery is at {}%.  Please replace/recharge the batteries".format(b,result)
        if not "last_notification" in self.batteries[b]:
          self.batteries[b]["last_notification"]=self.date()-datetime.timedelta(days=1)
        if self.batteries[b]["last_notification"]<self.date():
          self.batteries[b]["last_notification"]=self.date()
          if "notify" in self.batteries[b]:
            try:
              self.log("Sending low battery alert for {} to {}".format(b,self.batteries[b]["notify"]))
              self.notify(msg,name=self.batteries[b]["notify"],title="low battery warning")
            except:
              self.log("{} notify failed {}".format(b,self.batteries[b]["notify"]))
              pass
