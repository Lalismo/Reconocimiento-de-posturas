from flask import Flask, render_template, Response,request,make_response,redirect,abort,session,url_foor
from camera import VideoCamera


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        results = camera.get_frame()
        frame = results[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        if  0xFF == ord('q'):
            break

@app.route('/camara')
def camara():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

#Codigos para inicio de sesión

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)