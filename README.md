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
</pre>
  Setup the self.batteries dictionary below as follows
  <pre>
  self.batteries={"&LTHA Sensor name for battery state&GT":{"attribute":"&LTAttribute name (None if it's the default state for the sensor&GT",
                                                        "low":&LTlow level&GT,
                                                        "med":&LTmedium level&GT,
                                                        "notify":"&LTemail address to notify on low level&GT"},
                  "&LTrepeat for next sensor&GT":{"attribute":&LTAttribute name (None if it's the default state for the sensor&GT",
                                                        "low":&LTlow level&GT,
                                                        "med":&LTmedium level&GT,
                                                        "notify":"&LTemail address to notify on low level&GT"}
                  }
                  </pre>

