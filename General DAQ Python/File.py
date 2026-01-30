import numpy
import csv

class FileSaving:
    def __int__(self):
        self.var_dict = {}
        self.file = ''
        self.writer = ''

    def create_file(self, file_location):
        
        self.file = open(file_location, 'w', newline='')
        self.writer_ref = csv.writer(self.file)

    def write_infor(self,chl_infor,sample_rate):
        # write sample rate, scale and offset
        chl_name=['']*(len(chl_infor)+1)
        idx=['']*(len(chl_infor)+1)
        self.writer_ref.writerow(['Sample Rate'])
        self.writer_ref.writerow([str(sample_rate)])
        self.writer_ref.writerow(['Channel Index','Channel Name','Scale','Offset'])
        chl_name[0]='Time(s)'
        i=1
        for element in chl_infor:

            self.writer_ref.writerow([element["Index"],element["Chl Name"], str(element["Scale"]),str(element["Offset"])])
            
            idx[i]=element["Index"]
            chl_name[i]="Chl "+str(element["Index"])+": "+element["Chl Name"]
            i=i+1
        
        
        self.delta_t = 1/float(sample_rate)
        
        self.writer_ref.writerow(chl_name)
        self.var_dict = {item: [] for item in chl_name} # define the key for var_dict
        self.var_dict['Time(s)'] = []
        # length of keys corresponding to number of column
        #self.writer_ref.writerow(self.var_dict.keys())


    def write_data(self, time_col, saving_data):
        # if data_list_no == 1:  # only one channel of data
        #     key_name = list(self.var_dict.keys())
        #     self.var_dict[key_name[0]].extend(saving_data)
        # else:  # more than one channel of data
        
        for key_name in self.var_dict.keys():
            self.var_dict[key_name] = []
        i = 0
        for key_name in self.var_dict.keys():
            if key_name == 'Time(s)':  # save time
                self.var_dict[key_name].extend(time_col)
            else:  # save data
                if len(time_col) == len(saving_data):  # only one channel of data
                    self.var_dict[key_name].extend(saving_data)
                else:   # more than one channel of data
                    self.var_dict[key_name].extend(saving_data[i])
                    i = i + 1
        self.writer_ref.writerows(zip(*self.var_dict.values()))
        return time_col

    def close_file(self):

        self.file.close()
