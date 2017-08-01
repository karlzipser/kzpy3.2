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
    True
    D[dic_type] = inspect.stack()[0][3]
    D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates.')
    D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
    D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
    D[img] = zeros((D[ysize],D[xsize],3),D[data_type]) #!!!
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
        indiciesv = np.where(np.logical_and(xv>=0, xv<D[ysize])) # Note confusing reversals of x and y
        xv = xv[indiciesv]
        yv = yv[indiciesv]          #indiciesv = np.where(np.logical_and(yv>=0, yv<D[ysize]))
        #xv = xv[indiciesv]
        #yv = yv[indiciesv]        
        D[img][xv,yv,:] = colorv
    D[ptsplot] = _function_pts_plot
    return D




def Image3(*args):
    Args = args_to_dictionary(args)
    D = {}
    D[xmin] = Args[xmin] 
    D[xmax] = Args[xmax]
    D[ymin] = Args[ymin]
    D[ymax] = Args[ymax]
    D[xsize] = Args[Image_source][xsize]
    D[ysize] = Args[Image_source][ysize]
    D[img] = Args[Image_source][img]
    D[xscale] = Args[Image_source][xscale]
    D[yscale] = Args[Image_source][yscale]
    True
    D[dic_type] = inspect.stack()[0][3]
    D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates, using source Image2.')
    D[floats_to_pixels] = Args[Image_source][floats_to_pixels]
    D[pixel_to_float] = Args[Image_source][pixel_to_float]
    D[ptsplot] = Args[Image_source][ptsplot]
    return D





#EOF
