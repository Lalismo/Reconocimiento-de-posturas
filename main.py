from flask import Flask,send_from_directory, render_template, Response, request, make_response, redirect, abort, session, url_for, flash
import unittest
from flask_login import fresh_login_required, login_required, current_user, login_fresh, login_manager, login_user
from app import create_app
from deteccionEnVivo import deteccion_en_vivo
import os
from capturaPosturas import CapturePosture, count_exist_file, count_files_by_extension
#from deteccionEnVivo import deteccion_en_vivo
from app.config import Config
from app.forms import DeleteUserForm, UpdateUserForm, ImageForm, Signup_AdminForm, ExperimentForm
from app.firestore_service import  get_users, delete_user_by_id, update_user_by_id, get_type,get_user_by_id,user_put_data
from modelo import exist_model, val_image
from werkzeug.security import generate_password_hash
from app.models import UserData
from modeloExperimentacion import entrenamiento as modeloRGB
from modeloGrayExperimentacion import entrenamiento as modeloGREY



#Iniciamos la llamada de nuestro app mandando a llamar nuestro create_app
app = create_app()

app.config['DATA'] = (r".\app\static\Data")
app.config['IMAGE_VALIDATION'] = (r".\app\static\Data\Validation")
app.config['IMAGE_GOOD_POSTURE'] = (r".\app\static\Data\Training\Good_Posture")
app.config['IMAGE_REGULAR_POSTURE'] = (r".\app\static\Data\Training\Regular_Posture")
app.config['IMAGE_BAD_POSTURE']=(r".\app\static\Data\Training\Bad_Posture")

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

'''
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
@fresh_login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    delete_form = DeleteUserForm()   
    
    context = {
        'user_ip': user_ip,
        'username': username,
        'users': get_users(),
        'delete_form': delete_form,
        'user_type': get_type(username)
    }
    return render_template('hello.html', **context)

@app.route('/users/delete/<user_id>', methods=['POST'])
@login_required
@fresh_login_required
def delete(user_id):
    delete_user_by_id(user_id=user_id)
    return redirect(url_for('hello'))

@app.route('/update', methods=['GET'])
@login_required
@fresh_login_required
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


@app.route('/signup_admin', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def signup_admin():
    signup_adminform = Signup_AdminForm()
    username = current_user.id
    context = {
        'signup_admin_form': signup_adminform,
        'user_type': get_type(username),
        'username': username,
    }
    
    if signup_adminform.validate_on_submit():
        username = signup_adminform.username.data
        password = signup_adminform.password.data
        email = signup_adminform.email.data
        typeuser = signup_adminform.type_user.data
        
        user_doc = get_user_by_id(username)
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash, email, typeuser)
            user_put_data(user_data)
            
            flash(f'Usuario {username} creado correctamente!')
            return redirect(url_for('signup_admin'))
        else:
            flash('El usuario ya existe!')
    
    return render_template('signup_admin.html', **context)



@app.route('/users/<user_id>', methods=['GET' ,'POST'])
@login_required
@fresh_login_required
def update_user(user_id):
    if request.method == 'POST':
        email = request.form.get('email')
        update_user_by_id(user_id=user_id, email=email )
    return redirect(url_for('hello'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def upload():
    ''' Funcion para subir imagenes y visualizar el archivo '''
    images_form = ImageForm()
    username = current_user.id
    # Lista de los archivos que estan en las carpetas
    
    list_of_good_posture = os.listdir(app.config['IMAGE_GOOD_POSTURE']) 
    list_of_regular_posture = os.listdir(app.config['IMAGE_REGULAR_POSTURE']) 
    list_of_bad_posture =os.listdir(app.config['IMAGE_BAD_POSTURE'])
    
    # Variables que se enlazan al html que llama la funcion
    context = {
        'list_of_good_posture': list_of_good_posture,
        'list_of_regular_posture' : list_of_regular_posture,
        'list_of_bad_posture': list_of_bad_posture,
        'images_form' : images_form,
        'user_type': get_type(username),
        'username': username
    }
    
    # Condicion para validar los datos ingresados en el formulario
    if images_form.validate_on_submit():
        file = images_form.file.data # Información del nombre
        filename = (file.filename) # Nombre del archivo
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['IMAGE_VALIDATION'], filename) # Ruta donde se guardara el archivo            
        file.save(file_path) # Guardado de la imagen en la ruta que contiene la variable file_path
        
            # Validacion de clasificacion de imagen
        if val_image(file_path) == 0:#Si la imagen coincide con el modelo se mete al primer if
            new_filename = count_exist_file(app.config['IMAGE_GOOD_POSTURE'], 0) # Obtencion del nombre del archivo conforme el archivo faltante en caso contrario se omite
            print(new_filename)
            if (new_filename != 3 ):#Si el contador de imagenes esta incompleto en la carpeta hace el cambio de nombre por la imagen que falta
                os.rename(os.path.join(app.config['IMAGE_VALIDATION'], filename), os.path.join(app.config['IMAGE_GOOD_POSTURE'], new_filename))
            else:
                #Si no manda mensaje para mostrar al usuario que la carpeta esta llena
                flash('Ya existe el valor maximo de imagenes permitido de esta categoria')
        elif val_image(file_path) == 1:
            new_filename = count_exist_file(app.config['IMAGE_BAD_POSTURE'], 1)
            print(new_filename)
            if (new_filename != 3):
                os.rename(os.path.join(app.config['IMAGE_VALIDATION'], filename), os.path.join(app.config['IMAGE_BAD_POSTURE'], new_filename))
            else:
                flash('Ya existe el valor maximo de imagenes permitido de esta categoria')
        elif val_image(file_path) == 2:
            new_filename = count_exist_file(app.config['IMAGE_REGULAR_POSTURE'], 2)
            print(new_filename)
            if (new_filename != 3):    
                os.rename(os.path.join(app.config['IMAGE_VALIDATION'], filename), os.path.join(app.config['IMAGE_REGULAR_POSTURE'], new_filename))
            else:
                flash('Ya existe el valor maximo de imagenes permitido de esta categoria')
        elif val_image(file_path) == 3:
            flash('La imagen no presenta ninguna similitud entre las 3 posturas, favor de subir otra foto')
        else:
            flash("Los modelos necesitan ser creados para poder validar el tipo de postura de la imagen, vuelva a intentarlo despues de crear los modelos.")
            
        if os.path.exists(file_path):
            os.remove(file_path)
            return redirect(url_for('upload'))
        
    return render_template('images.html', **context)


@app.route('/update_image/<filename>/<category>')
@login_required
@fresh_login_required
def update_images(filename, category):
    file_path = os.path.join(app.config['IMAGE_GOOD_POSTURE'], filename)
  
    if (category == '1'):   
        file_path = os.path.join(app.config['IMAGE_GOOD_POSTURE'], filename)
       
    elif(category == '2'):
        file_path = os.path.join(app.config['IMAGE_REGULAR_POSTURE'], filename)
  
    elif(category == '3'):
        file_path = os.path.join(app.config['IMAGE_BAD_POSTURE'], filename)

    else:
        flash("Archivo no encontrado porfavor, no juegue con la URL chifladito")
        redirect(url_for('upload'))
    
    if os.path.exists(file_path):
        int(category)
        os.remove(file_path)
        CapturePosture(category, filename)
        flash('Imagen actualizada exitosamente')
        return redirect(url_for('upload'))
    return redirect(url_for('upload'))
        
@app.route('/create_images')
@login_required
@fresh_login_required
def create_images():
    CapturePosture(0, '')
    flash('Imagenes creadas exitosamente')
    return redirect(url_for('upload'))

@app.route('/delete_good/<filename>')
@login_required
@fresh_login_required
def delete_good_image(filename):
    file_path = os.path.join(app.config['IMAGE_GOOD_POSTURE'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Imagen eliminada exitosamente')
        return redirect(url_for('upload'))
    else:
        flash('Imagen no encontrada')
        return redirect(url_for('upload'))

@app.route('/delete_regular/<filename>')
@login_required
@fresh_login_required
def delete_regular_image(filename):
    file_path = os.path.join(app.config['IMAGE_REGULAR_POSTURE'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Imagen eliminada exitosamente')
        return redirect(url_for('upload'))
    else:
        flash('Imagen no encontrada')
        return redirect(url_for('upload'))

@app.route('/delete_bad/<filename>')
@login_required
@fresh_login_required
def delete_bad_image(filename):
    file_path = os.path.join(app.config['IMAGE_BAD_POSTURE'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Imagen eliminada exitosamente')
        return redirect(url_for('upload'))
    else:
        flash('Imagen no encontrada')
        return redirect(url_for('upload'))

@app.route('/experimentation', methods=["GET", "POST"])
@login_required
@fresh_login_required
def experimentacion():
    experiment_form = ExperimentForm()
    username = current_user.id
    good = app.config['IMAGE_GOOD_POSTURE']
    regular = app.config['IMAGE_REGULAR_POSTURE']
    bad = app.config['IMAGE_BAD_POSTURE']
    
    context = {
            'experiment_form' : experiment_form,
            'user_type': get_type(username),
            'username': username,
        }
    
    if exist_model() and count_files_by_extension(good, 'jpg') == 500 and count_files_by_extension(regular, 'jpg') == 500 and count_files_by_extension(bad, 'jpg') == 500:
        
        if experiment_form.validate_on_submit():
            epocas = experiment_form.epochs.data
            pasos = experiment_form.steps.data
            modelo = experiment_form.model.data

            if (modelo == 1):
                modeloRGB(epocas, pasos)
            elif (modelo == 2):
                modeloGREY(epocas, pasos)
            else:
                flash('Ocurrio un error inesperado..')
                return redirect(url_for('experimentacion'))

            return redirect(url_for('experimentacion'))
    else:
        flash('No se puede usar el modulo de experimentación debido a la falta de imagenes o inexistencia en las categorías', category='error')
    
    return render_template('experimentacion.html', **context)

@app.route('/camara')
@login_required
@fresh_login_required
def camara():
    username = current_user.id
    context = {
        'user_type': get_type(username),
        'username': username,
    }
    return render_template('monitorización.html', **context)

@app.route('/video_feed')
@login_required
@fresh_login_required
def video_feed():
    return Response(deteccion_en_vivo(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)