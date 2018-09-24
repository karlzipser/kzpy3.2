### #!/bin/bash
/usr/local/Cellar/sox/14.4.2_1/bin/play -n synth 60 brownnoise gain $1 &
time.sleep(1)
killall sox
/usr/local/Cellar/sox/14.4.2_1/bin/play -n synth 60 brownnoise gain $2 &
time.sleep(1)
/usr/local/Cellar/sox/14.4.2_1/bin/play -n synth 60 brownnoise gain $1 &
time.sleep(1)
killall sox