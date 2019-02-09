from __future__ import division
from kzpy3.vis3 import *
assert(1/2 == 0.5)
import kzpy3.scratch.image as image

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L,O,___ = open_run("Mr_Black_25Jul18_14h44m55s_local_lrc",
                opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py"),want_list=['L','O'])

topics = [
    u'acc_x',
    

    #u'acc_x_meo',
    u'acc_y',

    #u'acc_y_meo',
    u'acc_z',
    

    #u'acc_z_meo',
    #u'behavioral_mode',
    u'button_number',
    #u'cmd_motor',
    #u'cmd_steer',
    u'drive_mode',
    u'encoder',
    #u'encoder_meo',
    u'gyro_heading_x',
    #u'gyro_heading_x_meo',
    #u'gyro_heading_y',
    #u'gyro_heading_y_meo',
    #u'gyro_heading_z',
    #u'gyro_heading_z_meo',
    u'gyro_x',
    #u'gyro_x_meo',
    u'gyro_y',
    #u'gyro_y_meo',
    u'gyro_z',
    #u'gyro_z_meo',
    #u'human_agent',
    u'left_ts_deltas',
    u'motor',
    #u'place_choice',
    #u'right_ts',
    u'steer',
    #u'ts',
]

max_steps = 500
P = {}

P['index'] = 15000
for t in topics:
    P[opj(t,'data')] = None#zeros((1,2))
    P[opj(t,'min')] = -0.1#2**16
    P[opj(t,'max')] = 0.1#-2**16

window_seconds_width = 10

cat = zeros((1,2))
def update(P):
    index = P['index']
    P['ts'] = L['ts'][index]
    for t in topics:
        value = L[t][index]
        if value > P[opj(t,'max')]:
            P[opj(t,'max')] = value
        if value < P[opj(t,'min')]:
            P[opj(t,'min')] = value

        MN,MX = P[opj(t,'min')],P[opj(t,'max')]
        s = 0.9999
        MX = s*MX + (1-s)*(MX-MN)/2.0
        MN = s*MN + (1-s)*(MX-MN)/2.0
        P[opj(t,'min')],P[opj(t,'max')] = MN,MX


        cat[0,0] = P['ts']
        cat[0,1] = value
        if P[opj(t,'data')] == None:
            P[opj(t,'data')] = cat
        else:
            P[opj(t,'data')] = np.concatenate((P[opj(t,'data')],cat),0)
        for i in rlen(P[opj(t,'data')]):
            if P[opj(t,'data')][i,0] >= P['ts'] - window_seconds_width:
                break
        P[opj(t,'data')] = P[opj(t,'data')][i:]
        #if len(P[opj(t,'data')]) > max_steps:
        #    P[opj(t,'data')] = P[opj(t,'data')][-max_steps:,:]
    P['index'] += 1
    Hz.freq()

img = image.get_blank_image(500,500) #########

#cs = z55(np.random.randn(len(P[opj(t,'data')]),3))
#cs *= 0
#for i in range(3):
#    cs[:,i] = 255
plot_timer = Tr(2/30)
message = Tr(3)
tr = Tr(500)
Hz=Tr(3)


while not tr.c():

    #message.message(d2s(P['acc_x/min'],P['acc_x/max']))
    
    if True:#:try:
        for i in range(1):
            update(P)
        if True:#plot_timer.c():
            plot_timer.reset()
            ctr = 0
            image.place_image_in_image2(img,O['left_image']['vals'][P['index']],row=(2,3),col=(2,3)) #########
            image.place_image_in_image2(img,O['right_image']['vals'][P['index']],row=(2,3),col=(3,3)) #########

            for t in topics:
                cs = na((255,255,255))
                if '_x' in t:
                    cs = na((255,0,0))
                if '_y' in t:
                    cs = na((0,255,0))
                    
                if '_z' in t:
                    cs = na((0,0,255))
                    
                if 'motor' in t:
                    cs = na((0,0,255))
                if 'steer' in t:
                    cs = na((255,0,0))
                if 'encoder' in t:
                    cs = na((0,255,255))

                    
                ctr += 1

                r = len(topics)-ctr+1
                xys = image.get_float_pixels( #########
                    xys=na(P[opj(t,'data')]),
                    img_shape=shape(img),
                    col=(1.1,2),
                    row=(r+0.5,1+len(topics)),
                    box=((P['ts'] - window_seconds_width,P['ts']),(0.8*P[opj(t,'min')],0.8*P[opj(t,'max')]))
                    #box=((0,len(P[opj(t,'data')])),(0.8*P[opj(t,'min')],0.8*P[opj(t,'max')]))
                )
                image.img_pts_plot(img,xys,cs) #########
            
            mci(img)
            img *= 0

    else:#except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            




/////////////////////// LIGHTS ///////////////////////////////
//

int RIGHT_YELLOW = 9;
int LEFT_YELLOW = 12;
int BLUE = 5;
int WHITE = 7;
int PURPLE = 118;
int GREEN = 6;
int LEFT_RED = 11;
int RIGHT_RED = 10;
int LEFT_GREEN = 13;
int RIGHT_GREEN = 8;
int LIGHTS_OUT = 22;
int LIGHTS_ENABLED = 21;
int HUMAN_DRIVER = 100;
int NOT_HUMAN_DRIVER = 101;
int WHITE_OUT = 117;
int GREEN_OUT = 116;
int BLUE_OUT = 115;
int PURPLE_OUT = 119;
int LEFT_GREEN_OFF = 121;
int RIGHT_GREEN_OFF = 123;
int PURPLE_PIN = 4;
//
//////////////////////////////////////////////////////

int button = 0;
int mode = 0;
int lights_out = 0;
int human_driver = 1;


void begin_serial()
{
  Serial.begin(115200);
  Serial.setTimeout(5);
  for (int i = 0; i < 10; i++)
   {
     while (Serial.available() > 0)
     {
       char k = Serial.read();
       delay(1);
     }
     delay(1);
   }
}

void setup()
{
    for (int i=4; i<14;++i){
      pinMode(i, OUTPUT);digitalWrite(i, LOW);
    }
    begin_serial();
    Serial.println("lights_and_tones__led_master.ino setup()");    
}

int toggle(int t) {
  if (t==0) t=1;
  else t = 0;
  return t;
}

int ___tic___ = 1;

long unsigned int ___prev_time___ = millis();

int tic_toc(int delay_time)
{
  if (delay_time < 0) return 1;
  long unsigned int now = millis();
  if (now - ___prev_time___ > delay_time){
    ___prev_time___ = now;
    ___tic___ = toggle(___tic___);
  }
  return ___tic___;
}


long unsigned int __start_time__;
int __duration__;
int start_stopwatch(int t)
{
  __start_time__ = millis();
  __duration__ = t;
}
int check_stopwatch()
{
  if (millis() - __start_time__ > __duration__) return 1;
  return 0;
}

long unsigned int now_sound = millis();

int red_delay = -1;

void loop() {
  
  int A;

  if (millis()-now_sound > 5000) {
    now_sound = millis();
    Serial.println("('sound',0,0,0)");
  }

  A = Serial.parseInt();

  int level = tic_toc(250);

  
  
  int red_level = 1;
  /*
  if (A >=-100&&A<-90) red_delay = 10*(-A-90);
  int red_level = tic_toc(red_delay);
  Serial.println(red_delay);
  Serial.println(red_level);
  */
  if (A == LIGHTS_OUT) {
    lights_out = 1;
  }
  else if (A == LIGHTS_ENABLED) {
    lights_out = 0;
  }

  if (lights_out == 1) {
    for (int i = 0; i< 14;++i){
        pinMode(i,OUTPUT);digitalWrite(i,LOW);
    }
    delay(100);
    return;
  }

  if (A == HUMAN_DRIVER) {
    human_driver = 1;
  }
  else if (A == NOT_HUMAN_DRIVER) {
    human_driver = 0;
  }
  else if (A == BLUE) {
    digitalWrite(BLUE, HIGH);
  }
  else if (A == BLUE_OUT) {
    digitalWrite(BLUE, LOW);
  }
  else if (A == PURPLE) {
    digitalWrite(PURPLE_PIN, HIGH);
  }
  else if (A == PURPLE_OUT) {
    digitalWrite(PURPLE_PIN, LOW);
  }
  else if (A == WHITE) {
    digitalWrite(WHITE, HIGH);
  }
  else if (A == WHITE_OUT) {
    digitalWrite(WHITE, LOW);
  }
  else if (A == GREEN) {
    digitalWrite(GREEN, HIGH);
  }
  else if (A == GREEN_OUT) {
    digitalWrite(GREEN, LOW);
  }
  else if (A == LEFT_GREEN) {
    digitalWrite(LEFT_GREEN, HIGH);
  }
  else if (A == LEFT_GREEN_OFF) {
    digitalWrite(LEFT_GREEN, LOW);
  }
  else if (A == RIGHT_GREEN) {
    digitalWrite(RIGHT_GREEN, HIGH);
  }
  else if (A == RIGHT_GREEN_OFF) {
    digitalWrite(RIGHT_GREEN, LOW);
  }
  else if (A < 5 && A > 0) { 
    button = A;
  }
  else if (A < 65 && A > 60) { 
    mode = A;
  }
  if (mode == 62) {      
      digitalWrite(LEFT_RED, HIGH);
      digitalWrite(RIGHT_RED, HIGH);
      digitalWrite(LEFT_YELLOW, LOW);
      digitalWrite(RIGHT_YELLOW, LOW);
  }

  if (mode == 61) {
    digitalWrite(LEFT_YELLOW, level);
    digitalWrite(RIGHT_RED, HIGH);
    digitalWrite(RIGHT_YELLOW, LOW);
    digitalWrite(LEFT_RED, level);
  }

  if (mode == 63) {
    digitalWrite(RIGHT_YELLOW, level);
    digitalWrite(LEFT_RED, HIGH);
    digitalWrite(LEFT_YELLOW, LOW);
    digitalWrite(RIGHT_RED, level);
  }   


  if (button == 2) {      
      digitalWrite(LEFT_GREEN, HIGH);
      digitalWrite(RIGHT_GREEN, HIGH);
  }

  if (button == 1) {
    digitalWrite(RIGHT_GREEN, LOW);
    digitalWrite(LEFT_GREEN, HIGH);
  }

  if (button == 3) {
    digitalWrite(LEFT_GREEN, LOW);
    digitalWrite(RIGHT_GREEN, HIGH);
  }   

  if (button == 4) {
    digitalWrite(LEFT_YELLOW, level);
    digitalWrite(RIGHT_YELLOW, level);
    digitalWrite(LEFT_RED, LOW);
    digitalWrite(RIGHT_RED, LOW);
    digitalWrite(LEFT_GREEN, LOW);
    digitalWrite(RIGHT_GREEN, LOW);
  }
  
}

//EOF


#EOF
