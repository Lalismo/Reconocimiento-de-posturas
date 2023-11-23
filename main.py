from flask import Flask, render_template, Response, request, make_response, redirect, abort, session, url_for, flash
from camera import VideoCamera
import unittest
from flask_login import login_required, current_user
from app import create_app
from werkzeug.utils import secure_filename
import os
from app.config import Config
from app.forms import DeleteUserForm, UpdateUserForm, ImageForm, DeleteImageForm
from app.firestore_service import  get_users, delete_user_by_id,update_user_by_id
#Iniciamos la llamada de nuestro app mandando a llamar nuestro create_app
app = create_app()
# app.config['UPLOAD_FOLDER'] = ("/app/static/files")

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    context = {
        'error':error,
        'texto':"Lo sentimos no encontramos lo que buscas",
        'status':404
    }
    return render_template('error.html', **context)

@app.route('/error')
def error_500():
    abort(500)
    
@app.errorhandler(500)
def server_error(error):
    context = {
        'error':error,
        'texto':"Algo salio mal",
        'status':500
    }
    return render_template('error.html', **context)

#Indicación para poner la ruta,
@app.route('/')
#Declaramos función para el inicio de nuestra pagina
def index():
    #Inicializamos la variable user_ip para mandar un request donde extrae la ip
    user_ip = request.remote_addr
    #creamos la variable response para poder crear la respuesta redireccionando a la ruta
    #Donde tenemos el mensaje de hello world
    response = make_response(redirect(url_for('hello', _external=True)))
    #Almacenamos la ip en la session que tenemos
    session['user_ip'] = user_ip
    #Retonamos la respuesta
    return response

'''''
def gen(camera):
    while True:
        results = camera.get_frame()
        frame = results[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
      
        if  0xFF == ord('q'):
            break@app.route('/camara')
def camara():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')odigos para inicio de sesión
'''
    
 #Creamos la ruta de hello y definimos su función

@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    delete_form = DeleteUserForm()

    context = {
        'user_ip': user_ip,
        'username': username,
        'users': get_users(),
        'delete_form': delete_form,
    }
    return render_template('hello.html', **context)

@app.route('/users/delete/<user_id>', methods=['POST'])
def delete(user_id):
    delete_user_by_id(user_id=user_id)
    return redirect(url_for('hello'))

@app.route('/update', methods=['GET'])
def update_redirect():
    users = get_users() # Obtain all the users 
    user_ip = session.get('user_ip') # Obtain the Ip from the cookies
    update_form = UpdateUserForm()
    context = {
        'users': users,
        'user_ip': user_ip,
        'update_form': update_form,
    }
    return render_template('update.html', **context)


@app.route('/users/<user_id>', methods=['GET' ,'POST'])
def update_user(user_id):
    if request.method == 'POST':
        email = request.form.get('email')
        phone = int(request.form.get('phone'))
        update_user_by_id(user_id=user_id, email=email, phone=phone)
    return redirect(url_for('hello'))


'''
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    images_form = ImageForm()
    context = {
        'images_form': images_form
    }
    if images_form.validate_on_submit():
        file = images_form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename))
        return('Succesfull upload')
        
    return render_template('images.html', **context)
'''

def listaArchivos():
    urlFiles = 'app/static/files'
    return (os.listdir(urlFiles))

@app.route('/images', methods=['GET', 'POST'])
def image():
    
    images_form = ImageForm()
    delete_form = DeleteImageForm()
    context = {
        'images_form': images_form,
        'delete_image_form': delete_form
    }
    print(listaArchivos())
    return render_template('images.html', list_Photos = listaArchivos(), **context)

@app.route('/guardar-foto', methods=['GET', 'POST'])
def registarArchivo():
  
    if request.method == 'POST':
            if(request.files['archivo']):
                #Script para archivo
                file     = request.files['archivo']
                basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
                filename = secure_filename(file.filename) #Nombre original del archivo
                
                #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
                extension = os.path.splitext(filename)[1]
                upload_path = os.path.join (basepath, 'app/static/files', extension) 
                file.save(upload_path)

    return render_template('images.html', list_Photos = listaArchivos())

@app.route('/<string:nombreFoto>', methods=['GET','POST'])
def EliminarFoto(nombreFoto):
    print(nombreFoto)
    if request.method == 'GET':
        #print(nombreFoto) #Nombre del archivo subido
        basepath = os.path.dirname (__file__) #C:\xampp\htdocs\elmininar-archivos-con-Python-y-Flask\app
        url_File = os.path.join (basepath, 'app/static/files', nombreFoto)
        #print(url_File)
        
        #verifcando si existe el archivo, con la funcion (path.exists) antes de de llamar remove 
        # para eliminarlo, con el fin de evitar un error si no existe.
        if os.path.exists(url_File):
            os.remove(url_File) #Borrar foto desde la carpeta
            #os.unlink(url_File) #Otra forma de borrar archivos en una carpeta
    return render_template('images.html', list_Photos = listaArchivos())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)