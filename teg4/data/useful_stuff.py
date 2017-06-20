                self.timestamps = sorted(self.img_dic['left'].keys())
                self.binned_timestamp_nums = [[],[]]
                for i in range(len(self.timestamps)-num_data_steps):
                    t = self.timestamps[i+num_data_steps]
                    if left_image_bound_to_data[t]['state_one_steps'] > num_data_steps:
                        steer = left_image_bound_to_data[t]['steer']
                        if steer < 43 or steer > 55:
                            self.binned_timestamp_nums[0].append(i)
                        else:
                            self.binned_timestamp_nums[1].append(i)
            #print((len(self.binned_timestamp_nums[0]),len(self.binned_timestamp_nums[1])))
            if len(self.binned_timestamp_nums[0]) > 0 and len(self.binned_timestamp_nums[1]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[np.random.randint(len(self.binned_timestamp_nums))])
            elif len(self.binned_timestamp_nums[0]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[0])
            elif len(self.binned_timestamp_nums[1]) > 0:
                timestamp_num = random.choice(self.binned_timestamp_nums[1])
            else:
                return None
            t = self.timestamps[timestamp_num]