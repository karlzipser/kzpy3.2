from kzpy3.vis3 import *
exec(identify_file_str)
CA()
velocity = arange(-3,3,0.001)

gain = -5*velocity+5
gain[gain<0] = 0
gain[gain>4] = 4
figure(1)
plot(velocity,gain,'.')
plt.title('camera gain direct')
xylim(-3,3,0,4.1)
spause()

gain = -2.5*velocity+4.25
gain[gain<1.5] = 1.5
gain[gain>4] = 4
figure(2)
plot(velocity,gain,'.')
plt.title('steer gain direct')
xylim(-3,3,0,4.1)
spause()
#raw_enter()