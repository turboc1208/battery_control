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
full_img=/local/full_battery_icon.jpg
mid_img=/local/mid_battery_icon.jpg
low_img=/local/low_battery_icon.jpg
batteries={"sensor.den_sensor_battery":{"attribute":"state","low":10,"mid":60,"notify":"EmailChip"},
           "sensor.office_sensor_battery":{"attribute":"state","low":10,"mid":60,"notify":"EmailSusan"},
           "sensor.ring_front_door_battery":{"attribute":"state","low":10,"mid":60,"notify":"EmailCharlie"},
           "zwave.aeotec_zw074_multisensor_gen5_14":{"attribute":"battery_level","low":10,"mid":60,"notify":"TextSam"},
           "zwave.office_door_4":{"attribute":"battery_level","low":10,"mid":60,"notify":"EmailChip"},
           "zwave.toolcabinetleft_6":{"attribute":"battery_level","low":10,"mid":60,"notify":"EmailChip"},
           "sensor.ring_front_door_battery":{"attribute":None,"low":10,"mid":60,"notify":"EmailChip"},
           "zwave.toolcabinetright_7":{"attribute":"battery_level","low":10,"mid":60,"notify":"EmailChip"}}
</pre>
<ul>
<li>full_img : image to display for high or full battery levels
<li>mid_img : image to display for mid battery levels
<li>low_img : image to display for low battery levels
</ul><p>
  Setup the self.batteries JSON string below as follows, remember to use double quotes.
  <pre>
  self.batteries={"&LTHA Sensor name for battery state&GT":
                        {"attribute":"&LTAttribute name&GT",
                         "low":&LTlow level&GT,
                         "med":&LTmedium level&GT,
                         "notify":"&LTHA Notify Component&GT"},
                  "&LTrepeat for next sensor&GT":
                        {"attribute":"&LTAttribute name&GT",
                         "low":&LTlow level&GT,
                         "med":&LTmedium level&GT,
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