from flask_wtf import FlaskForm
from wtforms import validators, DecimalField, FloatField
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import SubmitField, PasswordField, TextAreaField, TextField
from models import proveedores, productos

lista_art = proveedores.listado_art()
lista_prov = productos.listado_prov()


#################################################################
#####                        USUARIOS              ##############
#################################################################

class Login(FlaskForm):    
    identificacion = StringField('Identif. Usuario:', validators=[validators.required(),validators.length(max=15)])
    contrasena = PasswordField('Contraseña:',validators=[validators.required()]) 	
    iniciar_sesion = SubmitField('Iniciar Sesión')

class FormRegistroUsuarios(FlaskForm):   
    identificacion = StringField('Identif. Usuario:', validators=[validators.required(),validators.length(max=15)])    
    nombre = StringField('Nombre Completo:', validators=[validators.required(), validators.length(max=100)])   
    contrasena = PasswordField('Contraseña:',validators=[validators.required()])
    confirm_contrasena = PasswordField('Confirmar constraseña:',validators=[validators.required()])
    rol=SelectField("Asignar Rol / Perfil:",choices=[("0","Select Perfil"),("1","Superadministrador"),("2","Administrador"),("3","Usuario Final")],validators=[validators.required()])    	
    grabar_registro = SubmitField()

class FormEditarUsuarios(FlaskForm):    
    identificacion = StringField('Identif. Usuario:', validators=[validators.required(),validators.length(max=15)])    
    nombre = StringField('Nombre Completo:', validators=[validators.required(), validators.length(max=100)])   
    contrasena = PasswordField('Contraseña:',validators=[validators.required()])
    confirm_contrasena = PasswordField('Confirmar constraseña:',validators=[validators.required()])
    rol=SelectField("Asignar Rol / Perfil:",choices=[("0","Select Perfil:"),("1","Superadministrador"),("2","Administrador"),("3","Usuario Final")],validators=[validators.required()])    	
    editar_registro = SubmitField()

class FormElimUsuarios(FlaskForm):
    style={'style': 'width:100%;'}
    
    id_prov = StringField('Identif. Usuario:', render_kw=style)
    nombre = StringField('Nombre Completo:', render_kw=style)
    contrasena = StringField('Contraseña:', render_kw=style)
    confirm_contrasena = StringField('Confirmar constraseña:')



#################################################################
#####                        PRODUCTOS             ##############
#################################################################

class FormCrear_prod (FlaskForm):
    style={'style': 'width:100%; font-size:12px; font-family: tahoma;'}
    id_producto = StringField('Identif. (Referencia): ', validators=[validators.required(), validators.length(min=6,max=20)], render_kw=style) 
    producto = TextField('Nombre:', validators=[validators.required(), validators.length(min=6,max=50)], render_kw=style)
    descripcion = TextAreaField('Breve Descripcion:', validators=[validators.required(), validators.length(min=10, max=400)], render_kw=style)
    #cantidad_minima = DecimalField('Cantidad mínima',places=2, validators=[validators.required()])
    cantidad_minima = FloatField('Cantidad mínima Stock:', validators=[validators.required()], render_kw=style)
    

class FormElim_prod (FlaskForm):
    style={'style': 'width:100%;'}
    id_producto = StringField('Identif. del producto', render_kw=style) 
    producto = TextField('Nombre del producto', render_kw=style)
    descripcion = TextAreaField('Descripcion del producto', render_kw=style)
    cantidad_minima = FloatField('Cantidad mínima')
    


class FormAsociar_prod(FlaskForm):
    style={'style': 'width:100%; font-size:12px; font-family: tahoma;'}
    
    producto = TextField('Nombre del Producto:', validators=[validators.required()], render_kw=style)
    
    sel_prov = SelectField('Asignar Proveedor:', validators=[validators.required()],render_kw=style, choices = [(lista_prov[i]["cod_prov"], lista_prov[i]["nombre_prov"]) for i in range(len(lista_prov))])


class FormInv_prod(FlaskForm):
    style={'style': 'width:100%; font-size:12px; font-family: tahoma;'}
    
    id_producto = StringField('Identif. del producto', validators=[validators.required(), validators.length(min=6,max=20)], render_kw=style) 
    
    producto = TextField('Nombre del producto', validators=[validators.required(), validators.length(min=6,max=50)], render_kw=style)
    
    tipo_mov = SelectField('Tipo Movimiento:', validators=[validators.required()],render_kw=style, choices=[(1,"Entrada"),(2,"Salida")])

    cantidad_mov = FloatField('Cantidad:', validators=[validators.required()], render_kw=style)
    

#################################################################|
#####                        PROVEEDORES           ##############
#################################################################

class FormAddProveedores(FlaskForm):
    style={'style': 'width:100%;'}
    
    id_prov = StringField('Nit / CC: ', validators=[validators.required(),validators.length(min=6,max=20)], render_kw=style)
    nombre_prov = StringField('Nombre del Proveedor:', validators=[validators.required(),validators.length(min=6,max=50)], render_kw=style)
    direccion_prov = StringField('Dirección del Proveedor:', validators=[validators.required(),validators.length(min=6,max=150)], render_kw=style)
    telef_prov = StringField('Telf. Proveedor:', validators=[validators.length(min=6,max=20)], render_kw=style)

class FormAsociarProveedores(FlaskForm):
    style={'style': 'width:100%; font-size:12px; font-family: tahoma;'}
    
    nombre_prov = StringField('Nombre del Proveedor:', render_kw=style)
    lista_art = proveedores.listado_art()
    
    sel_prod = SelectField('Asignar Producto:', validators=[validators.required()],render_kw=style, choices = [(lista_art[i]["cod_prod"], lista_art[i]["producto"]) for i in range(len(lista_art))])
                        
class FormElimProveedores(FlaskForm):
    style={'style': 'width:100%;'}
    
    id_prov = StringField('Identif. del Proveedor:', render_kw=style)
    nombre_prov = StringField('Nombre del Proveedor:', render_kw=style)
    direccion_prov = StringField('Dirección del Proveedor:', render_kw=style)
    telef_prov = StringField('Telf. Proveedor:')
    
class FormListarProd_Prov(FlaskForm):
    style={'style': 'width:100%; font-size:12px; font-family: tahoma;'}
    sel_prov = SelectField(u'Asignar Proveedor:', render_kw=style, choices = [(lista_prov[i]["cod_prov"], lista_prov[i]["nombre_prov"]) for i in range(len(lista_prov))])

    
class FormListarProv_Prod(FlaskForm):
    style={'style': 'width:100%; font-size:12px; font-family: tahoma;'}
    sel_prod = SelectField(u'Asignar Producto:', render_kw=style, choices = [(lista_art[i]["cod_prod"], lista_art[i]["producto"]) for i in range(len(lista_art))])