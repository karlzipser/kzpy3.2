from kzpy3.vis3 import *
import fit3d
from Array import Array


def test_Array():

    n = 4000
    A = Array(n,2)
    B = Array(n,2)

    A['setup_plot'](
        height_in_pixels=500,
        width_in_pixels=500,
        pixels_per_unit=50,
    )

    for x in arange(-0.0,10,1):
        for y in arange(0,10,.1):
            A['append'](na([x,y]))
    for x in arange(-10,0,.1):
        for y in arange(0,10,1):
            A['append'](na([x,y]))

    A['show'](
        do_print=False,
        use_maplotlib=False,
        color=(255,255,255),
    )


    height_in_pixels=94
    width_in_pixels=168
    x_origin_in_pixels=0
    y_origin_in_pixels=height_in_pixels
    pixels_per_unit=1

    B['setup_plot'](
        height_in_pixels=height_in_pixels,
        width_in_pixels=width_in_pixels,
        x_origin_in_pixels=x_origin_in_pixels,
        y_origin_in_pixels=y_origin_in_pixels,
        pixels_per_unit=pixels_per_unit,
    )
    
    B['to_3D'](A)

    B['show'](
        do_print=False,
        use_maplotlib=False,
        use_CV2_circles=True,
        grid=False,
        scale=1.0,
        color=(0,127,255),
    )
    


if __name__ == '__main__':
    test_Array()
    raw_enter()

#EOF
