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
  self.batteries={"<HA Sensor name for battery state>":{"attribute":"<Attribute name (None if it's the default state for the sensor>",
                                                        "low":<low level>,
                                                        "med":<medium level>,
                                                        "notify":"<email address to notify on low level>"},
                  "<repeat for next sensor>":{"attribute":"<Attribute name (None if it's the default state for the sensor>",
                                                        "low":<low level>,
                                                        "med":<medium level>,
                                                        "notify":"<email address to notify on low level>"}
                  }
                  </pre>

