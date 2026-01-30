from PyQt5 import QtCore, QtWidgets
from DAQ_Dialog import Ui_Dialog
from DAQ_UIv2 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QDialog,QTableWidgetItem
import sys
from datetime import datetime
import os
from File import FileSaving
from DAQ import VoltageInput
from Diagram import Diagram
import numpy as np


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        
        self.ChlSelectArray=[0,0,0,0,0,0,0,0]; 
        self.ChlNameArray=["","","","","","","",""]
        self.ScaleArray=[0,0,0,0,0,0,0,0]
        self.OffsetArray=[0,0,0,0,0,0,0,0]
        self.IdxArray=[0,1,2,3,4,5,6,7]
        self.OkCancel=0

        self.setupUi(self)
        self.buttonBox.accepted.connect(self.close)
        self.Select0.clicked.connect(lambda:self.selectChlClicked(self.Select0.isChecked(),0))
        self.Select1.clicked.connect(lambda:self.selectChlClicked(self.Select1.isChecked(),1))
        self.Select2.clicked.connect(lambda:self.selectChlClicked(self.Select2.isChecked(),2))
        self.Select3.clicked.connect(lambda:self.selectChlClicked(self.Select3.isChecked(),3))
        self.Select4.clicked.connect(lambda:self.selectChlClicked(self.Select4.isChecked(),4))
        self.Select5.clicked.connect(lambda:self.selectChlClicked(self.Select5.isChecked(),5))
        self.Select6.clicked.connect(lambda:self.selectChlClicked(self.Select6.isChecked(),6))
        self.Select7.clicked.connect(lambda:self.selectChlClicked(self.Select7.isChecked(),7))
        

    def selectChlClicked(self,checked,idx):
        if checked ==1: 
            self.ChlSelectArray[idx]=1
            
        else:
            self.ChlSelectArray[idx]=0
    
    
    def okClicked(self):
        
        self.IdxArray=[self.Idx0.text(),self.Idx1.text(),self.Idx2.text(),self.Idx3.text(),self.Idx4.text(),self.Idx5.text(),self.Idx6.text(),self.Idx7.text()]
        self.ChlNameArray=[self.ChlName0.text(),self.ChlName1.text(),self.ChlName2.text(),self.ChlName3.text(),self.ChlName4.text(),self.ChlName5.text(),self.ChlName6.text(),self.ChlName7.text()]
        self.ScaleArray=[self.Scale0.value(),self.Scale1.value(),self.Scale2.value(),self.Scale3.value(),self.Scale4.value(),self.Scale5.value(),self.Scale6.value(),self.Scale7.value()]
        self.OffsetArray=[self.Offset0.value(),self.Offset1.value(),self.Offset2.value(),self.Offset3.value(),self.Offset4.value(),self.Offset5.value(),self.Offset6.value(),self.Offset7.value()]
        factor=0
        for i in range(len(self.ChlSelectArray)):
            
            if self.ChlSelectArray[i]==0:
                del self.ChlNameArray[i-factor]
                del self.ScaleArray[i-factor]
                del self.OffsetArray[i-factor]
                del self.IdxArray[i-factor]
                factor=factor+1
            
        self.OkCancel=1

    def CancelClicked(self,Dialog):
        self.ChlNameArray=[]
        print("Cancel")
        self.OkCancel=0
    
    
    

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.InitialButton.clicked.connect(self.openDialog) # Initial Channel clicked, Open dialog
        self.PreConfigButton.clicked.connect(self.previousSetting)
        self.FileOk.clicked.connect(self.createFile) # Okay Clicked, create file
        self.StartButton.clicked.connect(self.startDAQ) # Start Clicked, Start DAQ and save channel infor
        self.RecordButton.clicked.connect(self.writeData) # Record is clicked, write voltage data into file, and display data on the chart
        self.StopButton.clicked.connect(self.stopDAQ) # Stop Clicked, Stop DAQ and close file
        self.ExitButton.clicked.connect(self.appExit) # Exit is clicked, exit app
        self.file=FileSaving()
        self.voltRead=VoltageInput()
        self.Chart=Diagram()
        self.horizontalLayout_13.addWidget(self.Chart)
        
        self.continueRunning = False
        self.timer=QtCore.QTimer()
        self.FileOk.setEnabled(True)
        self.InitialButton.setEnabled(False)
        self.PreConfigButton.setEnabled(False)
        self.StartButton.setEnabled(False)
        self.StopButton.setEnabled(False)
        self.RecordButton.setEnabled(False)
        self.saveData=False
        self.ChlInfor=[]
    # when Initial Channel clicked, this function will be called    
    def openDialog(self):
        #openDialog
        updateDialog = Dialog()
        updateDialog.exec_()
        if updateDialog.OkCancel==1:
            # Ok is pressed
            arrayLen=len(updateDialog.IdxArray)
            # reset ChlInfor len
            self.ChlInfor=[{}]*arrayLen
            self.StartButton.setEnabled(True)
            for i in range(arrayLen):
                self.ChlInfor[i]={'Index': updateDialog.IdxArray[i],'Chl Name': updateDialog.ChlNameArray[i], 'Scale': updateDialog.ScaleArray[i],'Offset':updateDialog.OffsetArray[i]}
            
            #Sort the Channel Information with Index in ascending order
            self.ChlInfor=sorted(self.ChlInfor,key=lambda x:x['Index'])
            print(self.ChlInfor)
            print("\n")
            #self.PreConfigButton.setEnabled(True)
    
    # PreConfigButton clicked
    def previousSetting(self):
        self.StartButton.setEnabled(True)
        print(self.ChlInfor)

    # FileOk clicked
    def createFile(self):
        
        if self.FileName.text()=="":
            # file name is 'Experiment Result 08Dec2022_14h02m17s.csv'
            FName= 'Experiment Result' + datetime.today().strftime(' %d%b%Y_%Hh%Mm%Ss') + '.csv'
        else:
            # file name is 'user select file name 08Dec2022_14h02m17s.csv'
            FName=self.FileName.text() + datetime.today().strftime(' %d%b%Y_%Hh%Mm%Ss') + '.csv'
        pyfilePath=os.getcwd()
        file_location =os.path.join(pyfilePath,'Results\\'+FName)
        # print out the file path with result file name in FilePath
        self.FilePath.setText("File Path:"+str(file_location))
        # create csv file 
        
        self.file.create_file(file_location)
        self.FileOk.setEnabled(False)
        self.InitialButton.setEnabled(True)
       
        if self.ChlInfor:
            self.PreConfigButton.setEnabled(True)

    # Start clicked
    def startDAQ(self):
        self.StartButton.setEnabled(False)
        self.InitialButton.setEnabled(False)
        self.StopButton.setEnabled(True)
        self.RecordButton.setEnabled(True)
        # Write Channel Information in the file
        self.file.write_infor(self.ChlInfor,self.SampleRate.text())
        physicalChannel=""
        for element in self.ChlInfor:
            physicalChannel=physicalChannel+self.DevicName.text()+'/ai'+element["Index"]+','
        #print(physicalChannel)
        #print("\n")
        physicalChannel=physicalChannel[:-1]
        print("DAQ Channels are: "+physicalChannel+"\nSample Rate: " + self.SampleRate.text())
        self.sRate=float(self.SampleRate.text())
        
        self.voltRead.start_task(physicalChannel,self.sRate)
        self.timer.timeout.connect(self.startPressed) 
        self.timer.start() # timer for timeout event after user pressed Start
        self.timer.setInterval(500)
        self.Chart.define_xy_array(len(self.ChlInfor))
        self.startTime=0
        self.writeTime=0
        self.chlNo=len(self.ChlInfor)
        self.sumTotal=[0.0]*self.chlNo
        
        #print("{:<10} {:<10} {:<10}".format('Chl Index', 'Chl Name', 'Scale','Offset'))
        #newLabel="{:<10} {:<20} {:} {:}".format('Index', 'Name', 'Scale','Offset')
        headers=['Index','Scale','Offset']
        newLabel=f'{headers[0]:<20}{headers[1]:<20}{headers[2]}'
        for item in self.ChlInfor:
            idx=item['Index']
            scale=item['Scale']
            offset=item['Offset']
            #newLabel+='\n'+"{:<10} {:<20} {:} {:}".format(idx,name,scale,offset)
            newLabel+='\n'+ f'{idx:<25}{scale:<20}{offset}'
        #newLabel= oldLabel + '\n' + '\n'+'Channel Information:' + '\n' + newLabel
        
        self.chlInfor.setText(newLabel)    
        self.chlInfor.setWordWrap(True)
        self.PreConfigButton.setEnabled(False)
    # After Start clicked, and before Stop Clicked
    def startPressed(self):
        self.voltTime=np.arange(self.startTime,self.startTime+1,1/self.sRate) #start,stop,step
        self.startTime = self.startTime + 1
        self.voltVal=self.voltRead.runTask()
        self.meanCalculation()
        self.Chart._update_canvas(self.voltTime,self.voltVal,self.ChlInfor)
        if self.saveData == True: # start recording data
            self.file.write_data(self.voltTime,self.voltVal)
            self.writeTime=self.writeTime+1 # count the record time

        if self.UseRTCheckBox.isChecked(): # use record time
           if self.writeTime>=int(self.RecordTime.text()): # if time is equal or long than defined record time
                self.RecordLED.setStyleSheet("background-color: rgb(3, 65, 0);") # stop recording
                self.saveData=False
                self.writeTime=0 # reset the record time
                self.RecordButton.setEnabled(True)
    
    # Calculate the mean of raw voltage for each channel
    def meanCalculation(self):
        
        if self.chlNo==1:
            
            meanSec=round(sum(self.voltVal)/float(len(self.voltVal)),3) # voltVal/number of samples per second
            self.sumTotal[0]=sum(self.voltVal)+self.sumTotal[0]
            meanTotal=round(self.sumTotal[0]/float(len(self.voltVal)*self.startTime),3)
            self.MeanPerSec.setItem(0,0,QTableWidgetItem(str(meanSec)))
            self.MeanOverall.setItem(0,0,QTableWidgetItem(str(meanTotal)))
        else:
            # initialize meanSec and meanTotal
            meanSec=[0]*self.chlNo
            meanTotal=[0]*self.chlNo
            
            for i in range(self.chlNo): 
                meanSec[i]=round(sum(self.voltVal[i])/float(len(self.voltVal[i])),3)
                self.sumTotal[i]=sum(self.voltVal[i])+self.sumTotal[i]
                meanTotal[i]=round(self.sumTotal[i]/float(len(self.voltVal[i])*self.startTime),3)
                self.MeanPerSec.setItem(i,0,QTableWidgetItem(str(meanSec[i])))
                self.MeanOverall.setItem(i,0,QTableWidgetItem(str(meanTotal[i])))  
        
    # Record is clicked
    def writeData(self):
        self.RecordLED.setStyleSheet("background-color: red")
        self.saveData=True
        self.RecordButton.setEnabled(False)
            
        #self.file.write_data(self.voltTime,self.voltVal)
        
    # Stop is clicked
    def stopDAQ(self):
        self.StopButton.setEnabled(False)
        self.RecordButton.setEnabled(False)
        self.FileOk.setEnabled(True)
        self.voltRead.stopTask()
        self.file.close_file()
        self.timer.stop()
        self.RecordLED.setStyleSheet("background-color: rgb(3, 65, 0);")
        self.timer.timeout.disconnect(self.startPressed) # Disconnect the connection
        #self.PreConfigButton.setEnabled(True)

    # Exit is clicked
    def appExit(self):
        sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())