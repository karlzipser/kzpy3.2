#,a
from kzpy3.vis3 import *
import kzpy3.Array.fit3d as fit3d
from kzpy3.Array.Array import Array

def test_Array():

    n = 4000
    A = Array(n,2)
    B = Array(n,2)
    w = 200
    A['setup_plot'](
        height_in_pixels=w,
        width_in_pixels=w,
        pixels_per_unit=w/10,
    )

    for x in arange(-0.0,10,1):
        for y in arange(0,10,.1):
            A['append'](na([x,y]))
    for x in arange(-10,0,.1):
        for y in arange(0,10,1):
            A['append'](na([x,y]))

    A['show'](
        color=(255,255,255),
    )

    B['setup_plot'](
        height_in_pixels=94,
        width_in_pixels=168,
        x_origin_in_pixels=0,
        y_origin_in_pixels=94,
    )
    
    B['to_3D'](A)

    q = B['show'](
        use_CV2_circles=False,
        color=(255,255,255),
        background_image=z55(0.*rnd((94,168,3)))
    )
    


if __name__ == '__main__':
    test_Array()
#,b
    raw_enter()


#EOF
