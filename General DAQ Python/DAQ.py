from nidaqmx.constants import TerminalConfiguration
import nidaqmx
#import os

class VoltageInput:
        
    def start_task(self,physicalChannel,sampleRate):
        # Create and start task
        self.task = nidaqmx.Task()
        self.task.ai_channels.add_ai_voltage_chan(physicalChannel, min_val=-10, max_val=10,
                                                  terminal_config=TerminalConfiguration.RSE)
        self.numberOfSamples = int(sampleRate)
        self.task.timing.cfg_samp_clk_timing(sampleRate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                             samps_per_chan=self.numberOfSamples)
        self.task.start()
           
    def runTask(self):
        #print("here")
        
        while True:
            # Check if task needs to update the graph
            samples_available = self.task._in_stream.avail_samp_per_chan
            if samples_available >= self.numberOfSamples:
                vals = self.task.read(self.numberOfSamples)
                #print(vals)
                return vals
            
            else:
                #print()
                continue
        
    def stopTask(self):
        # call back for the "stop task" button
        self.task.stop()
        self.task.close()
        
        
        