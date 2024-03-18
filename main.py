from flask import Flask,send_from_directory, render_template, Response, request, make_response, redirect, abort, session, url_for, flash, jsonify
import unittest
from flask_login import fresh_login_required, login_required, current_user, login_fresh, login_manager, login_user
from app import create_app
from deteccionEnVivo import deteccion_en_vivo
import os
from capturaPosturas import CapturePosture, count_exist_file, count_files_by_extension
from deteccionEnVivo import deteccion_en_vivo, tiempo
from app.config import Config
from app.forms import DeleteUserForm, UpdateUserForm, ImageForm, Signup_AdminForm, ExperimentForm, Restart_Form
from app.firestore_service import  get_users, delete_user_by_id, update_user_by_id, get_type, get_user_by_id, user_put_data, update_password
from modelo import exist_model, val_image, entrenamiento
from werkzeug.security import generate_password_hash
from app.models import UserData
from modeloExperimentacion import entrenamiento as modeloRGB
from modeloGrayExperimentacion import entrenamiento as modeloGREY
import yagmail
from random import shuffle, choice
import string
import multiprocessing 
from keras.callbacks import Callback
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle

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
    ALLOWED_EXTENSIONS = {'jpg'}
    ''' Funcion para subir imagenes y visualizar el archivo '''
    images_form = ImageForm()
    username = current_user.id
    # Lista de los archivos que estan en las carpetas
    
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'app/static/Data')):
        CapturePosture(0,'')
    else:
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
        if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
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
            
        else:
                flash('El archivo no cumple con la extension de imagen del dataset, favor de subir otra imagen con extension jpg', category="error")
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
    flash('Imagenes creadas exitosamente, procediendo a generar modelo.')
    if not exist_model():
        flash('Procederan a crearse los modelos, favor de esperar sin salirse de esta pagina.')
        training_process = multiprocessing.Process(target = entrenamiento())
        training_process.start()
        if training_process.is_alive == False:
            flash('Modelo creado exitosamente')
    else: 
        flash("El modelo ha sido creado exitosamente y esta listo para su uso")
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
    
    contador = 0

    if exist_model() and count_files_by_extension(good, 'jpg') == 500 and count_files_by_extension(regular, 'jpg') == 500 and count_files_by_extension(bad, 'jpg') == 500:
        
        if experiment_form.validate_on_submit():
            epocas = experiment_form.epochs.data
            pasos = experiment_form.steps.data
            modelo = experiment_form.model.data
            
            
            if (modelo == 1):
                flash('Entrenando el modelo RGB...')
                modeloRGB(epocas, pasos)
            elif (modelo == 2):
                flash('Entrenando el modelo GREY...')
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

@app.route('/restart_password', methods=['GET', 'POST'])
def restart_password():
    restart_form = Restart_Form()
    context = {
        'restart_form':restart_form,
    }
    username = restart_form.username.data
    if restart_form.validate_on_submit() and (get_user_by_id(username)):
        
        email_send = 'salgadolunae2@gmail.com'
        cont = 'jrnl pmhv gkmj jtja'
        email = restart_form.email.data
        
        new_password = generate_password()   
        
        yag = yagmail.SMTP(user = email_send, password = cont)
        destinatarios = [email]
        asunto = 'Restablecimiento de contraseña Sistema Correctivo de Postura'
        mensaje = f'Su nueva contraseña es: {new_password}'
        
        #html = '<h1><center><center><h1>'
        #archivo = ''
        #yag.send(destinatarios, asunto, [mensaje,html], attachments = [archivo])
        
        yag.send(destinatarios, asunto, mensaje)
        update_password(username, generate_password_hash(new_password))
        flash('Su contraseña ha sido restablecida correctamente, se ha enviado un correo')
        return redirect('hello')
    
    else:
        flash("El usuario ingresado no existe o los datos ingresados son incorrectos", category = 'error')
        
            
        return render_template('restart_password.html', **context)

@app.route('/detener_monitorizacion')
def detener_monitorizacion():


    print(tiempo.get_times())
    good, regular, bad = tiempo.get_times()
    create_pdf(good, regular, bad)

    return redirect(url_for('reportes'))




# def enviar_correo_reporte(email):
#     email_send = 'salgadolunae2@gmail.com'
#     cont = 'jrnl pmhv gkmj jtja'
#     email = email
    
#     new_password = generate_password()   
    
#     yag = yagmail.SMTP(user = email_send, password = cont)
#     destinatarios = [email]
#     asunto = 'Reporte diario sobre su Postura'
#     mensaje = 'Este es su reporte de posturas durante el periodo de tiempo que utilizo la monitorizacion'
    
#     #html = '<h1><center><center><h1>'
#     #archivo = ''
#     #yag.send(destinatarios, asunto, [mensaje,html], attachments = [archivo])
    
#     archivo = os.path.join(os.path.dirname(__file__), 'documento.pdf')
     
#     yag.send(destinatarios, asunto, mensaje, attachments=[archivo])
#     #update_password(username, generate_password_hash(new_password))
    
@app.route('/reportes', methods = ['GET'])
def reportes():
    username = current_user.id
    context = {
        'user_type': get_type(username),
        'username': username,
    }




    return render_template('reportes.html', **context)

def create_pdf (tiempo_buena, tiempo_regular, tiempo_mala):
    
    matplotlib.use('Agg')
    # Crear un objeto BytesIO para almacenar el contenido del PDF
    buffer = BytesIO()

    # Crear un documento PDF con reportlab
    doc = SimpleDocTemplate(buffer, pagesize=letter)
 

    elements= []

    # Generar tabla de tiempos
    data = [
        ["Postura", "Tiempo Total"],
        ["Buena", f"{tiempo_buena:.2f} s"],
        ["Regular", f"{tiempo_regular:.2f} s"],
        ["Mala", f"{tiempo_mala:.2f} s"]
    ]
    tabla = Table(data, colWidths=150, rowHeights=30)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(tabla)

    # Generar gráfico
    plt.figure(figsize=(6, 4))
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    plt.plot(x, y)
    plt.title('Gráfico de ejemplo')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')

    # Guardar el gráfico en un objeto BytesIO
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()

    # Crear un objeto Image con el contenido del gráfico
    image = Image(image_buffer)
    elements.append(image)

    # Agregar los elementos al documento
    doc.build(elements)

    # Mover el cursor del objeto BytesIO al principio del archivo
    buffer.seek(0)


    # Guardar el contenido del PDF en un archivo
    with open('documento.pdf', 'wb') as f:
        f.write(buffer.read())


def generate_password():
    all  = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits)
    shuffle(all)
    new_password = ''
    for _ in range(10):
        new_password += choice(all)
    return new_password

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)