Battery_Control.py

  Set image on battery sensors to show state.

  Install:

  Download the pictures you want.  Green, Yellow and Red battery images 
  are available in this repository.  
  Place them in the .homeassistant/www directory.  Create the www directory if its not there.
  Put the Battery_control.py app in your appdaemon code storage directory.
  Add the app to your appdaemon.cfg file as follows
<pre>
[battery_control]
module=battery_control
class=battery_control

  Setup the self.batteries JSON string below as follows All non-numeric values must be in double quotes
  batteries={"sensor.upstairs_sensor_battery":{"attribute":"state",
                                               "levels":{"1":{"value":25,"img":"/local/battery1.jpg"},
                                                     "2":{"value":50,"img":"/local/battery2.jpg"},
                                                     "3":{"value":75,"img":"/local/battery3.jpg"},
                                                     "4":{"value":100,"img":"/local/battery4.jpg"}},
                                               "notify":"EmailChip"},
           "sensor.office_sensor_battery":{"attribute":"state",
                                               "levels":{"1":{"value":33,"img":"/local/battery1.jpg"},
                                                     "2":{"value":66,"img":"/local/battery2.jpg"},
                                                     "3":{"value":100,"img":"/local/battery4.jpg"}},
                                             "notify":"EmailChip"}}
#</pre>
<ul>
</ul><p>
  Setup the self.batteries JSON string below as follows, remember to use double quotes.
  <pre>
  self.batteries={"&LTHA Sensor name for battery state&GT":
                        {"attribute":"&LTAttribute name&GT",
                         "levels":{"1":{"value":%LTMax value for this level%GT,"img":"%LTImageFile%GT"},
                                   "2":{"value":%LTMax value for this level%GT,"img":"%LTImageFile%GT"},
                                   "3":{"value":75,"img":"/local/battery3.jpg"},
                                   "4":{"value":100,"img":"/local/battery4.jpg"}},
                         "notify":"&LTHA Notify Component&GT"},
                  "&LTrepeat for next sensor&GT":
                        {"attribute":"&LTAttribute name&GT",
                         "levels":{"1":{"value":25,"img":"/local/battery1.jpg"},
                                   "2":{"value":50,"img":"/local/battery2.jpg"},
                                   "3":{"value":75,"img":"/local/battery3.jpg"}},
                         "notify":"&LTHA Notify Component&GT"},
                  }
                  </pre>
<ul>                  
<li>HA Sensor name : The full sensor name : sensor.den_sensor_battery
<li>attribute : the attribute that holds the battery level (state, battery_level, etc)
<li>high : Values above mid are considered high<br>
high battery level > mid
<li>mid : Values less than or equal to mid but above low are considered mid <br>
mid >= mid battery level > low
<li>low : Values less than or equal to low are considered Low<br>
low >= low battery level
<li>notify : HA notify component to send message.  Only one notify method is allowed per
sensor but different sensors can use different notify methods.  Sensor A can send a page
sensor b can send an email.  Just set up notify components in you HA configuration.yaml file.
</ul>
