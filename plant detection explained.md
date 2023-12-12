The Plant Cam is a Raspberry Pi based long distance plant monitor. It has a built in camera that can rotate 180 degrees to visualize the environment, along with built-in temperature sensor and soil moisture reader to give you constant updates on your beloved plants.

Wiring:
required materials:
9 gram SG90 servo,
pi-camera v2
Keyes Studio Temperature Sensor
Analog to Digital Converter-MCP-3008
Keyes Studio Soil Moisture Sensor
assorted male to male wires
assorted male to female wires

to setup the ADC, connect it to the breadboard and wire it to the corresponding wires based off of this diagram
![[Pasted image 20231212133230.png]]
next connect the sg90 to the respective 5.0v, GPIO pin, and Ground
do the same to the soil moisture sensor,
make sure to write down what input/output pins you used

alter your code to work with the correct GPIO pins and your cuircuit is wired.


Code with Comments:
you will need to setup a few files,
one named eric.py, one named Main.py and one named camera.py
to code main:



from flask import Flask, render_template, Response, request, send_from_directory
import eric
from camera import VideoCamera

pi_camera = VideoCamera(flip=False)

app = Flask(__name__)
Data = {
    "temp": 0,
    "water": 0,
}
#sets up data from other files as well as libraries
@app.route('/')
def index():
    return render_template('index.html')
#sets up html website
def gen(camera):#sets up our camera with the camera python file
        while True:
            frame = pi_camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():#handles video feed
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
   
@app.route("/Dy_update")
def Dy_update():#handles updating the data from the eric.py folder
     global Data
     Data = {
        "temp": eric.temps(),
        "water": eric.callback(), 
     }
     return Data

if __name__ == '__main__': #runs main
    app.run(host='0.0.0.0', debug=False)


to code eric,
from ast import Global
import time
import numpy as np
from gpiozero import MCP3008
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
#designates what pins to gather data from
chtemp = MCP3008(channel=0, clock_pin=11, mosi_pin=10,miso_pin=9, select_pin=8)
#setting parameters
tsample = 0.5 #how often to get data
tdisp = 1 #how often to display data
tstop = 20 #how long data should be gathered
vref = 3.3 #voltage used
ktemp = 23 #adjusts the temperature
tprev = 0
tcurr = 0
tstart = time.perf_counter() #starts a timer

def temps():
    
    global tsample, tdisp, tstop, vref, ktemp, tprev, tcurr, tstart #This code operates the temperature sensor and outputs the temperature data
    tcurr = time.perf_counter() - tstart #the current time is set to the timer
    valuecurr = chtemp.value #puts the temperature sensor value into a new variable
    tempcurr = vref*ktemp*valuecurr*(9/5)+32 #calculates the temperature
    return int(np.round(tempcurr)) #returns the temperature vlaue
    tprev = tcurr #updates the current amount of time passed
       
#GPIO SETUP

GPIO.setup(5, GPIO.IN)
def callback():
    return GPIO.input(5) # will return input of soil moisture sensor






to code camera,




#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np
#
class VideoCamera(object): #this code starts the camera stream
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start() (removed code)
        self.vs = PiVideoStream().start()
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.photo_string = photo_string # Name to save the photo
        time.sleep(2.0)

    def __del__(self): #will stop the camera if needed
        self.vs.stop()

    def flip_if_needed(self, frame): #will flip the camera if oriented wrong
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self): #this code is unused but it will get our current frame
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()

    # Take a photo, called by camera button, currently unused but left in code
    def take_picture(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, image = cv.imencode(self.file_type, frame)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") # get current time
        cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)




now you will need to make a folder labeled "templates"
and within it make an html file labeled "index"
to code index,





<!DOCTYPE html>
<html>
<head>
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.Left {
  position: fixed;
  left: 15px;
  bottom: 53px;
  width: 50px;
  height: 40px; 
  background-color: Transparent;
}

.Down {
  position: fixed;
  left: 52.5px;
  bottom: 15.5px;
  width: 50px;
  height: 40px; 
  background-color: Transparent;
}

.Up {
  position: fixed;
  left: 52.5px;
  bottom: 90.5px;
  width: 50px;
  height: 40px; 
  background-color: Transparent;
}

.Right {
  position: fixed;
  left: 90px;
  bottom: 53px;
  width: 50px;
  height: 40px; 
  background-color: Transparent;
}
.camera-movement{
  float: none;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.lights-button{
	float: right;
}


img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    height: 100%;
}

button {
    background-color: Transparent;
    background-repeat:no-repeat;
    border: none;
    cursor:pointer;
    overflow: hidden;
    outline:none;
    width: 100%;
    height: 100%;
}

.camera-bg {
  position: fixed;
  top: 0;
  left: 0;

  /* Preserve aspet ratio */
  min-width: 100%;
  min-height: 100%;

    /* Full height */
  height: 100%;


  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;

}


.TempText {
  position: absolute;
  top: 2%;
  left: 2%;
  font-size: 25px;
  color: white;
  opacity: 0.5;
}

.WaterText {
  position: absolute;
  top: 15%;
  left: 2%;
  font-size: 25px;
  color: white;
  opacity: 0.5;
}


body {
    margin: 0;
    padding: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background-color: black;
}


</style>
</head>

<title>Pant-Cam</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<body>



<div class="main" id="newpost">
  <img  class="camera-bg" style="width: 100%; height:100%; background-attachment: fixed;" id="bg" class="center" src="{{ url_for('video_feed') }}">
</div>

<div class="TempText">
  <a id="Temp"></a></a>
</div>
<div class="WaterText">
  <a id="Water"></a></a>
</div>



  <div class="Left">
        <button id="move-button" onclick="L(1)" >
          <img src="https://drive.google.com/uc?id=1fgnmoAhRBwOK2V5RG5MnAoSaniwKFs9U">
      </button>
  </div>
  <div class="Down">
        <button id="move-button" onclick="D(1)" >
          <img src="https://drive.google.com/uc?id=11wuafkh5yxm7yNQPY-yp0LzMy2YpG7mZ">
      </button>
  </div>
  <div class="Up">
        <button id="move-button" onclick="U(1)">
          <img src="https://drive.google.com/uc?id=1L5MfLavzaOSbT7pct052JU2ItXMuYYEL">
      </button>
  </div>
  <div class="Right">
        <button id="move-button" onclick="R(1)" >
          <img src="https://drive.google.com/uc?id=1sic3-WKPxFJ_8GCF_4f4LreGnZ9afAFy">
      </button>
  </div>

  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

  <script>
    var LH,DH,UH,RH;
    function L(Arg) {
        $.getJSON("/L");
    }
    function R(Arg) {
        $.getJSON("/R");
    }
    function D(Arg) {
        $.getJSON("/D");
    }
    function U(Arg) {
        $.getJSON("/U");
    }
    </script>

  <script>
    setInterval(function(){
        $.getJSON("/Dy_update",function(data){
            document.getElementById("Temp").innerHTML = "Room Tempature: "+data.temp;
            document.getElementById("Water").innerHTML = "Water Level: "+data.water;
        });
    },.1)
  </script>

</body>
</html>

and your code is done. make sure to change code according to your used gpio pins.

to run the code go to temrinal and type the following

sudo python3 Main.py

Final Assembly Display![[image_50458881.jpg]]