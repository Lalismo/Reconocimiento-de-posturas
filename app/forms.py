from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Correo de usuario', validators=[DataRequired()])
    phone = IntegerField('Numero de telefono', validators = [DataRequired()])
    submit = SubmitField('Enviar')
    
# class TodoForm(FlaskForm):
#     description = StringField('Descripcion', validators=[DataRequired()])
#     submit = SubmitField('Crear')

class ImageForm(FlaskForm):
    image = FileField('Imagen', validators=[DataRequired()])
    
class DeleteUserForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateUserForm(FlaskForm):
    email = StringField('Correo de usuario', validators=[DataRequired()])
    phone = IntegerField('Numero de telefono', validators = [DataRequired()])
    submit = SubmitField('Actualizar')


    