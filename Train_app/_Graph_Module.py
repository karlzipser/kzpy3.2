from Parameters_Module import *
from vis2 import *
exec(identify_file_str)

_ = dictionary_access

def Image2(*args):
    Args = args_to_dictionary(args)
    D = {}
    D[xmin] = Args[xmin] 
    D[xmax] = Args[xmax]
    D[ymin] = Args[ymin]
    D[ymax] = Args[ymax]
    D[xsize] = Args[xsize]
    D[ysize] = Args[ysize]
    if data_type in Args:
        D[data_type] = Args[data_type]
    else:
        D[data_type] = np.uint8
    if Img in Args:
        D[img] = Args[Img][img]
    else:
        D[img] = zeros((D[ysize],D[xsize],3),D[data_type]) #!!!
    True
    D[dic_type] = inspect.stack()[0][3]
    D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates.')
    D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
    D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
    
    def _function_floats_to_pixels(*args):
        Args = args_to_dictionary(args)
        xv = array(Args[x])
        yv = array(Args[y])
        xintv = ((xv-D[xmin])*D[xscale]).astype(np.int64)
        yintv = ((yv-D[ymin])*D[yscale]).astype(np.int64)
        return D[ysize]-yintv,xintv #!!!
    D[floats_to_pixels] = _function_floats_to_pixels
    def _function_pixel_to_float(*args):
        Args = args_to_dictionary(args)
        xintv = Args[xint]
        yintv = Args[yint]
        xv = xintv / (1.0*D[xsize]) * (D[xmax]-D[xmin]) + D[xmin]
        yv = (D[ysize]-yintv) / (1.0*D[ysize]) * (D[ymax]-D[ymin]) + D[ymin]

        return xv,yv
    D[pixel_to_float] = _function_pixel_to_float
    def _function_pts_plot(*args):
        Args = args_to_dictionary(args)
        xv,yv,colorv = Args[x],Args[y],Args[color]
        True
        D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
        D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
        xv,yv = D[floats_to_pixels](x,xv,y,yv)
        indiciesv = np.where(np.logical_and(yv>=0, yv<D[xsize]))
        xv = xv[indiciesv]
        yv = yv[indiciesv]        
        indiciesv = np.where(np.logical_and(xv>=0, xv<D[ysize]))
        # Note confusing reversals of x and y above and in this module
        xv = xv[indiciesv]
        yv = yv[indiciesv]    
        D[img][xv,yv,:] = colorv
    D[ptsplot] = _function_pts_plot
    return D





def mouse_event(event, xv, yv, buttons, user_param):
    P[MOUSE_X] = xv
    P[MOUSE_Y] = yv
    if event == cv2.EVENT_MOUSEMOVE:
        P[MOUSE_MOVE_TIME] = time.time()
    elif event == cv2.EVENT_LBUTTONDOWN:
        #if yv < P[Y_MOUSE_RANGE_PROPORTION] * P[Y_PIXEL_SIZE]:
        _do_center_time('center_time',_(P,IMAGE3,pixel_to_float)(xint,xv, yint,0)[0])
        for nv in P[ICONS].keys():
            P[ICONS][nv][check](x,xv, y,yv)


def _do_center_time(*args):
    Args = args_to_dictionary(args)
    center_timev = Args['center_time']
    True
    time_widthv = P[END_TIME] - P[START_TIME]
    P[START_TIME] = center_timev - time_widthv/2
    P[END_TIME] = center_timev + time_widthv/2







def Icon(*args):
    Args = args_to_dictionary(args)
    D = {}
    D[x] = int(Args[x])
    D[y] = int(Args[y])
    D[img] = Args[img]
    D[path] = Args[path]
    D[Img] = Args[Img]
    D[name] = Args[name]
    True
    D[width] = shape(D[img])[0]
    D[height] = shape(D[img])[1]
    D[click_time] = False
    D[clicked] = False
    def _function_check(*args):
        Args = args_to_dictionary(args)
        xv = Args[y]
        yv = Args[x]
        #pd2s('checking',D[name],(xv,yv),'vs',(D[x],D[y]))
        True
        if xv >= D[x]:
            if xv <= D[x]+D[width]:
                if yv >= D[y]:
                    if yv <= D[y]+D[height]:
                        D[click_time] = time.time()
                        D[clicked] = True
                        print(D[name]+ ' clicked')
    def _function_show():
        True
        D[Img][img][D[x]:D[x]+D[width],D[y]:D[y]+D[height],:] = D[img]
    D[check] = _function_check
    D[show] = _function_show
    return D



#EOF
