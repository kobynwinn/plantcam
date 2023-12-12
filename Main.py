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
