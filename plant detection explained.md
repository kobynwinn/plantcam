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

to setup the ADC, connect it to the breadboard and wire it to the corresponding wires based off of this diagram (labelled wiring.png)

https://drive.google.com/drive/folders/1d5sZ45J1pqAGjh2wdIwn_g3h6gzKXOKV?usp=sharing

next connect the sg90 to the respective 5.0v, GPIO pin, and Ground
do the same to the soil moisture sensor,
make sure to write down what input/output pins you used

alter your code to work with the correct GPIO pins and your circuit is wired.


Code with Comments:
you will need to setup a few files,
one named eric.py, one named Main.py and one named camera.py
to code main:



````python
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

````

````python
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





````

to code camera,
``
````python
#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np
#importing libraries
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

````

---------------------------------------------------

now all is left for you is to set up the Website, But you need a HTML file to show everything else.

First you need to create a folder called **templates** and within that folder a file called **index.html**. Now all you need is the code to display all of the information. Lets start with all of the metadata which is stored in the head for every website

You Copy and Past this to start
````html
<head>
<!DOCTYPE html>
<html>
<head>
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">

<style>
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

/* Left Button Placement */
.Left { 
  position: fixed;
  right:50%;
  bottom: 15px;
  width: 80px;
  height: 70px; 
  background-color: Transparent;
}

/* Right Button Placement */
.Right {
  position: fixed;
  left: 50%;
  bottom: 15px;
  width: 80px;
  height: 70px; 
  background-color: Transparent;
}

/* Tempature Text Placement */
.TempText {
  white-space: pre-line;
  position: absolute;
  bottom: 25px;
  right: 52.25%;
  font-size: 20px;
  opacity: 1;
  text-align: center;
  transform: translate(-50%, 0);
}

/* Is Soil Wet Text Placement */
.WaterText {
  white-space: pre-line;
  position: absolute;
  bottom: 25px;
  left: 60%;
  font-size: 20px;
  opacity: 1;
  text-align: center;
  transform: translate(-50%, 0);
}

/* How the Button Is going to show */
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

/* Camera Display */
.camera-bg {
  top: 0;
  left: 0;
  background-position: center;
  background-repeat: no-repeat;
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

<title>Plant-Cam</title> 
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
````
Now you have Added all the Metadata for the site if you set anything to one of the things in the meta data it will copy all of that Infomation or you can do it manually. 

Now Lets move on to the Body of the site the Most inmport part of this to display all of the documents on the site. This Is Basiclly the Core of the site without it you site would just now show anything to the users connecting to it.

You Copy and Past this
````html
<body>

<!-- Adding The Camera As Images while the Main.py is Sending bits to http://losthost:5000/video_feed -->
<img  class="camera-bg" style="width: 100%; height: 85%;" id="bg" class="center" src="{{ url_for('video_feed') }}">


<!-- Text Displaying -->
<div class="TempText">
  <a  id="Temp" style="color: hwb(234 0% 1%);">Tempature\n"+data.temp+"°F | "+parseFloat((data.temp - 32) * 5/9).toFixed(2)+ "°C</a>
</div>
<div class="WaterText">
  <a id="Water" style="color: green;">Is Soil Wet\n"+(data.water == 1)</a>
</div>


<!-- Button Crestion and one clicked to Call a function also crweates a image of a arrow -->
  <div class="Left">
        <button id="move-button" onclick="L(1)" >
          <img src="https://drive.google.com/uc?id=1fgnmoAhRBwOK2V5RG5MnAoSaniwKFs9U">
      </button>
  </div>
  <div class="Right">
        <button id="move-button" onclick="R(1)" >
          <img src="https://drive.google.com/uc?id=1sic3-WKPxFJ_8GCF_4f4LreGnZ9afAFy">
      </button>
  </div>

  </body>
  </html>
````

  Now you Site will now have a functioning display but you site has zero code to it and will not have any functionality So now Lets add in the lines for the Scrips of the site.

First lets start with like the core of the site. If this isn't apart of the Code the Whole site would look weird and proceed not to function as intended.
````html
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script> <!-- This is the True Core of the site or it will break -->
````
Now Lets do The Button Functions. If Anything from anywhere in the body calls for a L() or a R() Theses Functions will be called and send a Request to http://localhost:5000/(L or R) for Information the Main.py will send back "None" so it doesn't break.
````html

  <!-- The Left and Right function for the Servor that Main.py calls fom http://localhost:5000/(L/R) -->
  <script>
    function L() {
        $.getJSON("/L");
    }
    function R() {
        $.getJSON("/R");
    }
    </script>
````

For the Most part your site fully works but there is one thing. The Temperature and Is Soil Wet Text Objects Won't Update ever that is a bad thing. So finally lets add a Dynamically updating part to this whole site. 
````html
<!-- Same as Above but at http://localhost:5000/Dy_update and gets data back to update Tempature and Is Soil Wet -->
  <script>
    setInterval(function(){
        $.getJSON("/Dy_update",function(data){

          //Tempature Changing  propertys
          var TempateureVal = document.getElementById("Temp")
          TempateureVal.innerHTML = "Tempature\n"+data.temp+"°F | "+parseFloat((data.temp - 32) * 5/9).toFixed(2)+ "°C"; // Text Displaying
          TempateureVal.style= "color: hwb("+(260-parseFloat((data.temp - 32) * 5/9).toFixed(2)*6.5)+" 0% 0%);"; // Color Changeing


          // Is Soil Wet Changeing Propertys of Text and Color
          document.getElementById("Water").innerHTML = "Is Soil Wet\n"+(data.water == 1);
          if (data.water == 1)
            document.getElementById("Water").style= "color: rgb(0,255,0);";
          else
            document.getElementById("Water").style= "color: rgb(255,0,0);";
        });
    },.1)
  </script>
````
This Whole Function will send a Request to http://localhost:5000/Dy_update for information And the Main.py Redirects that do a function within that will send back a table of data that this will Receive. With this data the was Received this will update the Information on the Temperature Text and also the Is Soil Wet Text. 

Now all is left is for you to run the code go to terminal and type the following **sudo python3 Main.py**. And now you are finished with this whole Plant Camera, We Hope you Enjoy to pretend to care about your plants!

Final Assembly Display (labeled final.jpg)
https://drive.google.com/drive/folders/1d5sZ45J1pqAGjh2wdIwn_g3h6gzKXOKV?usp=sharing