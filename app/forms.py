from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, FileField, EmailField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Correo de usuario', validators=[DataRequired()])
    phone = IntegerField('Numero de telefono', validators = [DataRequired(),NumberRange(0000000000,9999999999)])
    submit = SubmitField('Enviar')
    
# class TodoForm(FlaskForm):
#     description = StringField('Descripcion', validators=[DataRequired()])
#     submit = SubmitField('Crear')

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


    