from kzpy3.utils3 import *

flex_names = [
    'FL0',
    'FL1',
    'FL2',
    'FL3',
    'FR0',
    'FR1',
    'FR2',
    'FR3',
    'FC0',
    'FC1',
    'FC2',
    'FC3',
]
imu_names = ['acc','gyro','head']



class Mock_Arduino:

    def __init__(self,P,atype):
        self.P = P
        self.atype = atype

    def write(self,write_str):
        pass

    def readline(self):
        a = np.sin(time.time()/5.)*400+1200
        b = np.sin(time.time()/15.)*400+1200
        c = np.sin(time.time()/30.)*1.0+3.0
        d = np.sin(time.time()*2)
        if self.atype == 'MSE':
            rstr = d2c("('mse'",1700,a,b,c,")")
        elif self.atype == 'FLEX':
            rstr = "('"+d2c(np.random.choice(flex_names)+"'",b+500)+')'
        elif self.atype == 'IMU':
            rstr = "('"+d2c(np.random.choice(imu_names)+"'",d,d,d)+')'
        print rstr
        return rstr

    def flushInput(self):
        pass

    def flushOutput(self):
        pass


def put_mock_Arduinos_into_P(P):
    P['Arduinos'] = {}

    for a in ['MSE','FLEX','IMU','SOUND']:
        P['Arduinos'][a] = Mock_Arduino(P,a)





#EOF


