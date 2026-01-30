from PyQt5 import QtWidgets,QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy


class Diagram(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        
        
        
        #dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.fig=Figure(figsize=(5, 3))
        dynamic_canvas = FigureCanvas(self.fig)
        
        #self.ax = self.fig.add_subplot(1, 1, 1)

        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))
        
        #self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax=dynamic_canvas.figure.add_subplot(1,1,1)
        
        self._dynamic_ax.set_xlabel("Time(s)")
        self._dynamic_ax.set_ylabel("Calibrated Data")
        #self._timer = dynamic_canvas.new_timer(
        #    100, [(self._update_canvas, (), {})])
        #self._timer = dynamic_canvas.new_timer(100)
       # self._timer.add_callback(lambda:self._update_canvas(3.0))
       # self._timer.start()
    def define_xy_array(self, array_no):
        
        self.xdata = numpy.array([])  # x axis data buffer
        # y axis data buffer, one channel: []; two channels: [[],[]]; three channels: [[],[],[]]...
        empty_array = []
        if array_no > 1:
            for _ in range(array_no):
                empty_array.append([])
        self.ydata = numpy.array(empty_array)

    def _update_canvas(self,voltTime,voltVal,ChlInfor):
        
        
        self._dynamic_ax.clear()
        self._dynamic_ax.set_xlabel("Time(s)")
        self._dynamic_ax.set_ylabel("Calibrated Data")
        self.extend_data(voltTime,voltVal)
        legendNames=[]
        #print(self.ChlInfor[0]['Chl Name'])

        if len(voltVal)==len(voltTime): # one channel
            #print(voltVal)
            scaledata = self.ydata*ChlInfor[0]['Scale']+ChlInfor[0]['Offset']
            
            #self._dynamic_ax.plot(self.xdata, scaledata,label=ChlInfor[0]['Chl Name'])
            self._dynamic_ax.plot(self.xdata, scaledata)
            legName="Chl "+str(ChlInfor[0]['Index'])+": "+ChlInfor[0]['Chl Name']
            self._dynamic_ax.legend([legName],loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4, fancybox=True, shadow=True)
            #print(ChlInfor[0]['Chl Name']) 
        else: # multiple channels
            i=0
            for volt in self.ydata:
                scaledata = volt*ChlInfor[i]['Scale']+ChlInfor[i]['Offset']
                self._dynamic_ax.plot(self.xdata, scaledata)
                legName="Chl "+str(ChlInfor[i]['Index'])+": "+ChlInfor[i]['Chl Name']
                legendNames.extend([legName])            
                i=i+1
            self._dynamic_ax.legend(legendNames,loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4, fancybox=True, shadow=True)
        # Shift the sinusoid as a function of time.
        
        #print("negNo = "+str(negNo))
        self._dynamic_ax.figure.canvas.draw()

    def extend_data(self,voltTime,voltVal):
        xlimit=20 # number of second display board
        displayNumber=len(voltTime)*xlimit
        if len(self.xdata) < displayNumber:  # buffer is not full, put number into buffer xdata and ydata
            self.xdata = numpy.append(self.xdata, voltTime)
            if len(voltVal)==len(voltTime): # one channel
                self.ydata = numpy.append(self.ydata, voltVal)  # [] append
            else:
                self.ydata = numpy.append(self.ydata, voltVal, axis=1)  # [[],[]]...append data in each list
        else:  # over number of second display limit shift number
            self.xdata = self.shift_number(self.xdata, -len(voltTime), voltTime)
            if len(voltVal)==len(voltTime): # one channel
                self.ydata = self.shift_number(self.ydata, -len(voltTime), voltVal)
            else:
                
                for i in range(len(voltVal)):
                    self.ydata[i] = self.shift_number(self.ydata[i], -len(voltTime), voltVal[i])
        
    # shift data when array holds 10s of data
    def shift_number(self, arr, num, fill_value):
        # arr-it is the array for shifting
        # num-index(e.g. num=-3(arr[3]->arr[0]...), num=3(arr[0]->arr[3]...) )
        # fill_value-after array shifting to desire position, fill the empty position with this value
        result = numpy.empty_like(arr)
        if num > 0:  # move the array to right
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:  # move the array to left
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:  # no moving
            result[:] = arr
        return result