from flask import Flask, render_template, Response, request, send_from_directory
import eric
from camera import VideoCamera

pi_camera = VideoCamera(flip=False) # Sets up Pi Camera

app = Flask(__name__) # Create a new Flask data set


@app.route('/')
def index():
    return render_template('index.html') # Renders a HTML file 


def gen(): # When Called Yeilds out a Byte Array of the Current Frame from the Pi Camera
        while True:
            frame = pi_camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed') # Rerouts any http:/localhost:5000/video_feed to this file
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame') # AnyThing from gen will update the info on http:/localhost:5000/video_feed
   
@app.route("/Dy_update") # Rerouts any http:/localhost:5000/Dy_update to this file
def Dy_update():
     return {
        "temp": eric.temps(), # Call eric.py temps for the current Temtature 
        "water": eric.callback(), # Calls the callback for water level from eric.py
     } #sends it back so the website gets updated

if __name__ == '__main__': #runs main
    app.run(host='0.0.0.0', debug=False) #Hosts the Site and gives out 1 - 2 Ip Addresses 
