from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, FileField, EmailField, SelectField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Correo de usuario', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class Signup_AdminForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Correo de usuario', validators=[DataRequired()])
    type_user = IntegerField('Tipo de usuario', validators= [DataRequired(), NumberRange(1,2)])
    submit = SubmitField('Enviar')

class ImageForm(FlaskForm):
    file = FileField('Imagen', validators=[InputRequired()])
    submit = SubmitField('Upload')
    
class DeleteImageForm(FlaskForm):
    submit = SubmitField('Borrar')    

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateUserForm(FlaskForm):
    email = EmailField('Correo de usuario', validators=[DataRequired()])
    phone = IntegerField('Numero de telefono', validators = [DataRequired(),NumberRange(0000000000,9999999999)])
    submit = SubmitField('Actualizar')

class ExperimentForm(FlaskForm):
    steps = IntegerField('Pasos de la red neuronal', validators=[DataRequired(), NumberRange(1, 10000)])
    epochs = IntegerField('Epocas de la red neuronal',  validators=[DataRequired(), NumberRange(1, 10000)])
    model = SelectField('Tipo de modelo', choices={('1', 'Modelo de color'), ('2', 'Modelo de escala de grises')}, coerce=int, validators={DataRequired()})
    submit = SubmitField("Iniciar Experimentación")

class Restart_Form(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = EmailField('Correo de usuario', validators=[DataRequired()])
    