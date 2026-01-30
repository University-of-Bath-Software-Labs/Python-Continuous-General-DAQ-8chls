# Python Continuous General DAQ (8 channels)

A Python alternative to our LabVIEW general-purpose data acquisition (DAQ) program.  
It reads **analog voltage** data from an NI DAQ device, displays it on a **real-time graph**, and records acquired data to a **CSV file**.

Suitable for most general-purpose DAQ needs.

---

## Related project (LabVIEW version)

If you prefer LabVIEW (or need the 16‑channel LabVIEW variant), see:  
https://github.com/University-of-Bath-Software-Labs/LabVIEW-Continuous-General-DAQ-16chls

---

## What the program does

- Reads analog voltage data continuously from an NI DAQ device
- Displays the acquired data on a real-time graph 
- Lets you initialise/configure channels (including scale and offset)
- Records data to a CSV file when you press **Record**  
- Saves results into a **Results** folder 

---

## Requirements

- Windows PC
- A compatible NI DAQ device (e.g., NI USB‑6009 / similar)
- NI software installed:
  - NI‑DAQmx  
  - NI MAX (Measurement & Automation Explorer)

---

## How to run (Python source)

1. Download or clone this repository. 
2. Open the project in your IDE:
   - Either open the repo root, **or**
   - Open the folder: `General DAQ Python` 
3. Open and run:
   - `General DAQ Python/DAQ_Main.py` 

---

## How to use (typical workflow)

### 1) Launch the program
Run `DAQ_Main.py` from your IDE (see “How to run” above). 

### 2) File name (optional)
If you want to define your own output name, enter it in **File Name** and press **OK**.  
If you don’t define one, a default file name is used (including date & time).

<img alt="image" src="https://github.com/user-attachments/assets/b44e4992-6482-4832-bf7c-53bf5de16081" />

### 3) Confirm your NI device name (first-time setup)
If your PC connects to the NI device for the first time, the device name is often `Dev1`.

To confirm the device name:
- Open **NI MAX**
- Go to **Devices and Interfaces**
- Find your connected NI device and note the device name (e.g., `Dev1`)

<img alt="image" src="https://github.com/user-attachments/assets/5004a4cc-7d9d-42aa-a749-7884377d96ec" />

### 4) Choose sample rate and configure channels
- Select your **Sample Rate**  
- Click **Initialise New Channels** (a new window will open)  
- For each channel:
  - Enter **Channel Name**, **Scale**, and **Offset**
  - Tick **Select Channel**
  - Click **OK** when finished 

<img alt="image" src="https://github.com/user-attachments/assets/2b454fff-f242-4166-bc8e-7c4c142b29f9" />

### 5) Start acquisition
Click **Start** to begin acquiring and displaying live data.  

<img alt="image" src="https://github.com/user-attachments/assets/ae67c1be-c17c-4114-a74b-604a2889cc15" />

### 6) Recording data (two modes)
You can press **Record** at any point while acquisition is running.

**Mode A — Record until you stop**
- Leave **Use Record Time** unticked
- Press **Record**
- Data will be saved until you press **Stop**

**Mode B — Record for a fixed duration**
- Enter a value in **Record Time (s)**
- Tick **Use Record Time**
- Press **Record**
- Data will be recorded for the specified number of seconds 

Recorded files are saved as CSV in the **Results** folder.  

<img src="https://github.com/user-attachments/assets/7e657287-2e91-4ad0-8192-13fadc43450f" />

### 7) Stop
Press **Stop** to stop acquisition.

If you want to run again, you can start from the sample rate step again.  
You can also skip channel setup by selecting **Use Previous Configured Channels** instead of **Initialise New Channels**.

<img alt="image" src="https://github.com/user-attachments/assets/5faf1bd2-9c53-44dd-8cc8-aca2a158400c" />

---

## Output files

- Output format: CSV  
- Location: Results folder 
- File name: your defined name + date/time, or a default name + date/time

---

## Support / contact

If you need help setting this up or adapting it for a specific experiment, contact the **Electronics & Software Labs** team.
