from kzpy3.utils.common import *

def intr(n):
    return np.int(np.round(n))
    
def zeroToOneRange(m):
    min_n = 1.0*np.min(m)
    return (1.0*m-min_n)/(1.0*np.max(m)-min_n)
z2o = zeroToOneRange

def z2_255(m):
    return (255*z2o(na(m))).astype(np.uint8)

z55 = z2_255

def z2_255_by_channel(m):
    for i in range(3):
        m[:,:,i] = z2_255(m[:,:,i])




def rebin(a, shape):
    '''
    from http://stackoverflow.com/questions/8090229/resize-with-averaging-or-rebin-a-numpy-2d-array
    '''
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)


def zscore(m,thresh=np.nan,all_values=False):
    m_mean = np.mean(m)
    z = m - m_mean
    m_std = np.std(m)
    z /= m_std
    if not np.isnan(thresh):
        z[z < -thresh] = -thresh
        z[z > thresh] = thresh
    if all_values:
        return z,m_mean,m_std
    else:
        return z


def sequential_means(data,nn):
    a = array(data)
    d = []
    x = []
    n = min(len(a),nn)
    for i in range(0,len(a),n):
        d.append(a[i:i+n].mean())
        x.append(i+n/2.)
    return x,d




try:
    import numbers
    def is_number(n):
        if type(n) == bool:
            return False
        if type(n) == type(None):
            return False
        return isinstance(n,numbers.Number)
except:
    print("Don't have numbers module")



def mean_of_upper_range(data,min_proportion,max_proportion):
    return array(sorted(data))[int(len(data)*min_proportion):int(len(data)*max_proportion)].mean()


def mean_exclude_outliers(data,n,min_proportion,max_proportion):
    """
    e.g.,

    L=lo('/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta/direct_rewrite_test_11May17_16h16m49s_Mr_Blue/left_image_bound_to_data.pkl' )
    k,d = get_key_sorted_elements_of_dic(L,'encoder')
    d2=mean_of_upper_range_apply_to_list(d,30,0.33,0.66)
    CA();plot(k,d);plot(k,d2)
    
    """
    n2 = int(n/2)
    rdata = []
    len_data = len(data)
    for i in range(len_data):
        if i < n2:
            rdata.append(mean_of_upper_range(data[i:i-n2+n],min_proportion,max_proportion))
        elif i < len_data + n2:
            rdata.append(mean_of_upper_range(data[i-n2:i-n2+n],min_proportion,max_proportion))
        else:
            rdata.append(mean_of_upper_range(data[i-n2:i],min_proportion,max_proportion))
    return rdata

def meo(data,n):
    return mean_exclude_outliers(data,n,1/3.0,2/3.0)





def find_index_of_closest(val,lst):
    d = []
    for i in range(len(lst)):
        d.append(abs(lst[i]-val))
    return d.index(min(d))











def find_nearest(array,value):
    """
    https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    """
    idx = (np.abs(array-value)).argmin()
    return array[idx]





def bound_value(the_value,the_min,the_max):
    if the_value > the_max:
        return the_max
    elif the_value < the_min:
        return the_min
    else:
        return the_value



def sort_by_column(a,col,reverse=False):
    a = na(a)
    if reverse:
        a *= -1
    a = a[a[:,col].argsort()]
    if reverse:
        a *= -1
    return a

#exec(identify_file_str)

#EOF
