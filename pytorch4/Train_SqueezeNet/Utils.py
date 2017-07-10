from Parameters import args
from kzpy3.utils2 import *
import matplotlib.pyplot as plt


class Rate_Counter:
    """Calculate rate of process in Hz"""

    def __init__(self):
        self.rate_ctr = 0
        self.rate_timer_interval = 10.0
        self.rate_timer = Timer(self.rate_timer_interval)

    def step(self):
        self.rate_ctr += 1
        if self.rate_timer.check():
            print('rate = ' + str(args.batch_size * self.rate_ctr /
                  self.rate_timer_interval) + 'Hz')
            self.rate_timer.reset()
            self.rate_ctr = 0


def save_net(net, loss_record, weights_folder_path):
    weights_file_name = 'save_file' + time_str()
    torch.save(net.state_dict(),
               opjh(weights_folder_path, weights_file_name+'.weights'))

    # Next, save for inference (creates ['net'] and moves net to GPU #0)
    weights = {'net': net.state_dict().copy()}
    for key in weights['net']:
        weights['net'][key] = weights['net'][key].cuda(device=0)
    torch.save(weights,
               opjh(weights_folder_path, weights_file_name+'.infer'))


class Loss_Record:
    def __init__(self):
        self.t0 = time.time()
        self.loss_list = []
        self.timestamp_list = []
        self.loss_sum = 0
        self.loss_ctr = 0
        self.loss_timer = Timer(30)

    def add(self, loss):
        self.loss_sum += loss
        self.loss_ctr += 1
        if self.loss_timer.check():
            self.loss_list.append(self.loss_sum / float(self.loss_ctr))
            self.loss_sum = 0
            self.loss_ctr = 0
            self.timestamp_list.append(time.time())
            self.loss_timer.reset()

    def plot(self, c):
        plt.plot((np.array(self.timestamp_list) - self.t0) / 3600.0,
                 self.loss_list, c + '.')
