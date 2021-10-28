# Importamos la libreria yagmail
import os
# Importamos libreria verificar usuario autenticado
import functools

#import yagmail as yagmail
# Importamos la clase flask

from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from wtforms.fields.core import DecimalField

from forms import FormAddProveedores, FormElimProveedores, FormAsociarProveedores, FormEditarUsuarios, FormInv_prod, FormRegistroUsuarios, Login, FormCrear_prod, FormAsociar_prod, FormElim_prod, FormListarProd_Prov, FormListarProv_Prod

from models import productos, proveedores, prod_a_prov, prov_a_prod, usuarios, inventario

# Importamos las validaciones
# from validaciones import *

# Creo la variable app se le asigna una instancia de Flask que recibe de parametro la variable de entorno name
# que es el nombre del modulo que se esta ejecutando osea app.py
app = Flask(__name__)
app.config['SECRET_KEY'] = "86272a371c5acfb485b4701c837b922ab6d99134ad679002c36ebb136ad18412"

# Decorador para verificar que el usuario es autenticado
# INICIAR SESION
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        
        if g.user is None:
            return redirect( url_for('index'))
        
        return view(**kwargs)
    
    return wrapped_view


#Este decorador hace que flask ejecute la funcion definida 
#antes de que las peticiones ejecuten la función controladora que solicitan.
@app.before_request
def cargar_usuario_autenticado():
    cod_usu = session.get('cod_usu')
    if cod_usu is None:
        g.user = None
    else:
        g.user = usuarios.cargar(cod_usu)

# LOGOUT
@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))

# Ruta index - login
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        formulario = Login()
        return render_template('index.html', form=formulario)
    else:
        formulario = Login(request.form)
        if formulario.validate_on_submit():

            usr_id = formulario.identificacion.data
            pwd = formulario.contrasena.data

            #Para prevenir inyección de cogigo sql            
            usr_id = usr_id.replace("'","")
            pwd = pwd.replace("'","")

            objeto_usuarios = usuarios(0,usr_id,'', pwd, '')              
            respuestaAutenticar =objeto_usuarios.autenticar()

            if respuestaAutenticar[0] == 'True':
                session.clear()
                session["cod_usu"] = respuestaAutenticar[2]
                return redirect(url_for('modulos'))


                flash(f" El Usuario: {formulario.identificacion.data.upper() }, se ha logueado en el Sistema correctamente.")
                return redirect(url_for('modulos'))
            else:
                return render_template('index.html', mensaje = "Identificacion de usuario o contraseña incorrecta.", form=formulario)

        else:
            return render_template('index.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", form=formulario)


# Ruta modulos


@app.route('/modulos/usuario')
@login_required
def modulos():
    return render_template('modulos.html')

# Ruta acercadenosotros


@app.route('/acercadenosotros')
def acerca_de_nosotros():
    return render_template('acercade.html')


@app.route('/usuarios/guardar', methods=['GET', 'POST'])
def guardar_usuarios():
    if request.method == "GET":
        formulario = FormRegistroUsuarios()
        return render_template('usuarios/add_usuarios.html', form=formulario)
    else:
        formulario = FormRegistroUsuarios(request.form)
        if formulario.validate_on_submit() == True and formulario.rol.data != "0":

            if (formulario.contrasena.data != formulario.confirm_contrasena.data):
                return render_template('usuarios/add_usuarios.html', mensaje="La contraseña no coincide.", form=formulario)
            else:
                objeto_usuarios = usuarios(0,formulario.identificacion.data, formulario.nombre.data, formulario.contrasena.data, int(formulario.rol.data))
                if objeto_usuarios.agregar_usu() > 0:
                    flash(f" El Usario: {formulario.nombre.data.upper() }, ha sido creado en el Sistema correctamente.")
                    return redirect(url_for('guardar_usuarios'))
                else:
                    return render_template('usuarios/add_usuarios.html', mensaje = "El Formulario presenta error al intentar guardar en la Base de Datos.", form=formulario)

        else:
            return render_template('usuarios/add_usuarios.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", form=formulario)


@app.route('/usuarios/editar/<cod_usu>', methods=['GET', 'POST'])
def editar_usuarios(cod_usu):
    if request.method == "GET":
        formulario = FormEditarUsuarios()

        objeto_usuarios = usuarios.cargar(cod_usu)

        if objeto_usuarios:

            formulario.identificacion.data = objeto_usuarios.id_usu

            formulario.nombre.data = objeto_usuarios.nombre_usu

            formulario.contrasena.data = objeto_usuarios.contrasena_usu

            formulario.rol.data = str(objeto_usuarios.cod_rol)

            return render_template('usuarios/edit_usuarios.html', id=objeto_usuarios.cod_usu, form=formulario)
        else:
            return render_template('usuarios/edit_usuarios.html', mensaje="El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)


    else:      

        formulario = FormEditarUsuarios(request.form)

        if formulario.validate_on_submit() == True and formulario.rol.data != "0":
            if (formulario.contrasena.data != formulario.confirm_contrasena.data):
                return render_template('usuarios/edit_usuarios.html', mensaje="La contraseña no coincide.", form=formulario)
            else:
                objeto_usuarios = usuarios.cargar(cod_usu)

                objeto_usuarios = usuarios(
                    cod_usu, formulario.identificacion.data, formulario.nombre.data, formulario.contrasena.data,formulario.rol.data)

                if objeto_usuarios.actualizar_usu():
                    flash(
                        f" El Usuario: {formulario.nombre.data.upper() }, ha sido actualizado en el Sistema correctamente.")
                    return render_template('usuarios/edit_usuarios.html', mensaje="", id=cod_usu, form=formulario)
                else:
                    return render_template('usuarios/edit_usuarios.html', mensaje="El Formulario presenta error al intentar actualizarlo en la Base de Datos.", id=cod_usu, form=formulario)

        else:
            return render_template('usuarios/edit_usuarios.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", id=cod_usu, form=formulario)


@app.route('/usuarios/eliminar/<cod_usu>', methods=["GET", "POST"])
def eliminar_usuarios(cod_usu):
    
        
        objeto_usuarios = usuarios.cargar(cod_usu)
       
        objeto_usuarios.eliminar_usu()

        return redirect(url_for('listar_usuarios'))


@app.route('/usuarios/listar', methods=["GET"])
def listar_usuarios():
    aux = usuarios.listado_usu()
    return render_template('usuarios/listado_usu.html', lista=aux)


#  Rutas modulo productos


##################################################################################################
#                                                                                                #
#                                PRODUCTOS                                                       #
#                                                                                                #
##################################################################################################

@app.route('/productos/guardar', methods=["GET", "POST"])
def guardar_productos():
    if request.method=="GET":
        formulario = FormCrear_prod()
        return render_template('productos/add_productos.html', form=formulario)
        
    else:
        formulario = FormCrear_prod(request.form)
        if formulario.validate_on_submit():
            
            objeto_productos = productos(0, formulario.id_producto.data, formulario.producto.data,
            formulario.descripcion.data, formulario.cantidad_minima.data)
           
            if objeto_productos.insertar():
                flash(f"El producto: {formulario.producto.data.upper()}, ha sido creado correctamente." )
                return redirect(url_for('guardar_productos'))
                #return render_template('productos/add_productos.html',mensaje="Su mensaje ha sido guardado.", form=FormCrear_prod())
        
            else:
                return render_template('productos/add_productos.html', mensaje = "Ocurrió un error al guardar el formulario, por favor intente nuevamente.", form=formulario)
        
        return render_template('productos/add_productos.html', mensaje="Verificar, existe error en este campo.", form=formulario)



@app.route('/productos/editar/<cod_prod>', methods=["GET", "POST"])
def editar_productos(cod_prod): #se agregó (id_producto)
    if request.method == "GET":
        formulario = FormCrear_prod()

        objeto_productos = productos.cargar(cod_prod)

        if objeto_productos:
            formulario.id_producto.data = objeto_productos.id_producto
            formulario.producto.data = objeto_productos.producto
            formulario.descripcion.data = objeto_productos.descripcion
            formulario.cantidad_minima.data = objeto_productos.cantidad_minima
            
            return render_template('productos/edit_productos.html', id=objeto_productos.cod_prod, form=formulario)
        else:
            return render_template('productos/edit_productos.html', mensaje = "El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)

    else:
        formulario = FormCrear_prod(request.form)

        if formulario.validate_on_submit():
            objeto_productos = productos.cargar(cod_prod)

            # Creamos un objeto con la Clase constructora provductos() del archivo models.py
            objeto_productos = productos(
                cod_prod, formulario.id_producto.data, formulario.producto.data,
            formulario.descripcion.data, formulario.cantidad_minima.data) 

            if objeto_productos.editar():
                flash(f"El producto: {formulario.producto.data.upper() }, ha sido actualizado correctamente.")
                return render_template('productos/edit_productos.html', mensaje ="", id=cod_prod, form=formulario)
                #return redirect(url_for('editar_productos'))

            else:
                return render_template('productos/edit_productos.html', mensaje = "l Formulario presenta error al intentar actualizarlo en la Base de Datos.", id=cod_prod, form=formulario)
        else:
            return render_template('productos/edit_productos.html', mensaje="Verificar, existe error en este campo.", id=cod_prod, form=formulario)


@app.route('/productos/eliminar/<cod_prod>', methods = ["GET", "POST"])
def eliminar_productos(cod_prod):
    if request.method == "GET":
        formulario = FormCrear_prod()
        
        objeto_productos = productos.cargar(cod_prod)

        if objeto_productos:
            formulario.id_producto.data = objeto_productos.id_producto
            formulario.producto.data = objeto_productos.producto
            formulario.descripcion.data = objeto_productos.descripcion
            formulario.cantidad_minima.data = objeto_productos.cantidad_minima
            
            
            return render_template('productos/elim_productos.html', id=objeto_productos.cod_prod, form=formulario)
        
        else:
            return render_template('productos/elim_productos.html', mensaje="El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)
    else:
        formulario = FormElim_prod(request.form)

        if formulario.validate_on_submit():
            
            objeto_productos = productos.cargar(cod_prod)

            objeto_productos = productos(cod_prod, formulario.id_producto,
            formulario.producto, formulario.descripcion, formulario.cantidad_minima)

            if objeto_productos.eliminar():
                
                flash(
                    f" El producto: {formulario.producto.data.upper() }, ha sido eliminado del sistema correctamente.")

                return render_template('productos/elim_productos.html', mensaje="", id=cod_prod, form=formulario)
            else:
                return render_template('productos/elim_productos.html', mensaje="El Formulario presenta error al intentar eliminarlo de la Base de Datos.", id=cod_prod, form=formulario)
            
        else:
            return render_template('productos/elim_productos.html', mensaje="Este campo del Formulario presenta errorres, revisar.", id=cod_prod, form=formulario)


@app.route('/productos/listar', methods=["GET"])
def listar_productos():
    return render_template('productos/listado_prod.html', lista=productos.listado())


@app.route('/productos/asociarproveedoraproducto/<cod_prod>', methods=["GET", "POST"])
def asociar_proveedor_a_producto(cod_prod):
    lista_prov = proveedores.listado_prov()

    if request.method == "GET":
        
        formulario = FormAsociar_prod()

        objeto_producto = productos.cargar(cod_prod)

        if objeto_producto:
            formulario.producto.data = objeto_producto.producto
            formulario.sel_prov.choices = [(lista_prov[i]["cod_prov"], lista_prov[i]["nombre_prov"]) for i in range(len(lista_prov))]

            return render_template('productos/asociar_prov.html', id = cod_prod, form=formulario)
        
        else:
            return render_template('productos/asociar_prov.html', mensaje = "El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)
    else:
        formulario = FormAsociar_prod(request.form)

        if formulario.validate_on_submit():

            cod_prov = int(formulario.sel_prov.data)
            nombre_prov = 'Proveedor sin nombre'
            #reaklizo la busqueda
            for i in range(len(lista_prov)):
                if int(lista_prov[i]["cod_prov"]) == int(cod_prov):
                    nombre_prov = lista_prov[i]["nombre_prov"]
            
            objeto_producto =   (cod_prov, cod_prod)
            
            if objeto_producto.asociar_prod_a_prov():
                flash(f" El Proveedor: { nombre_prov }, ha sido asociado al Producto {formulario.producto.data.upper() } en el Sistema correctamente.")
                
                return render_template('productos/asociar_prov.html', mensaje="", id=cod_prod, form=formulario)                
            else:
                return render_template('productos/asociar_prov.html', mensaje="El Formulario presenta error al intentar actualizarlo en la Base de Datos.", id=cod_prod, form=formulario)
            
        else:
            return render_template('productos/asociar_prov.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", id=cod_prod, form=formulario)


@app.route('/productos/buscarproveedorporproductos', methods=['GET', 'POST'])
def buscar_proveedor_por_productos():
    lista_art = proveedores.listado_art()
    if(len(lista_art)>0):
        cod_prod = lista_art[0]["cod_prod"]
    else:
        cod_prod =''
    
    if request.method == "GET":

        formulario = FormListarProv_Prod()

        formulario.sel_prod.choices = [(lista_art[i]["cod_prod"], lista_art[i]["producto"]) for i in range(len(lista_art))]
        print('Cod.Producto inicial: ', str(cod_prod))

        return render_template('productos/buscar_prov.html', lista=proveedores.proveedor_prod(cod_prod), form=formulario)
    
    else:
        formulario = FormListarProv_Prod(request.form)
        if request.form.get('action') is None:
            cod_prod = int(formulario.sel_prod.data)
            print('Cod. Producto cambio: ', str(cod_prod))
            return render_template('productos/buscar_prov.html', lista=proveedores.proveedor_prod(cod_prod),form=formulario)

        else:
            print('Cod. Producto: ', request.form.get('action'))
            cod_prov = request.form.get('action')
            cod_prod = int(formulario.sel_prod.data)
            print('Cod. Producto cambio: ', str(cod_prod))
            
            objeto_proveedores = prov_a_prod(cod_prod, cod_prov)

            if objeto_proveedores.eliminar_asociar():
            
                return render_template('productos/buscar_prov.html', lista=proveedores.proveedor_prod(cod_prod),form=formulario)
            else:
                
                return render_template('productos/buscar_prov.html', lista=proveedores.proveedor_prod(cod_prod),form=formulario)


#  Rutas modulo proveedores

##################################################################################################
#                                                                                                #
#                                PROVEEDORES                                                     #
#                                                                                                #
##################################################################################################

@app.route('/proveedores/editar/<cod_prov>', methods=["GET", "POST"])
def editar_proveedores(cod_prov):
    if request.method == "GET":
        formulario = FormAddProveedores()

        objeto_proveedores = proveedores.cargar(cod_prov)

        if objeto_proveedores:

                formulario.id_prov.data = objeto_proveedores.id_prov

                formulario.nombre_prov.data = objeto_proveedores.nombre_prov

                formulario.direccion_prov.data = objeto_proveedores.direccion_prov

                formulario.telef_prov.data = objeto_proveedores.telef_prov

                return render_template('proveedores/edit_proveedores.html', id=objeto_proveedores.cod_prov, form=formulario)

        else:
            return render_template('proveedores/edit_proveedores.html', mensaje="El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)
    else:
        formulario = FormAddProveedores(request.form)

        if formulario.validate_on_submit():

            objeto_proveedores = proveedores.cargar(cod_prov)

            # Creamos un objeto con la Clase constructora proveedores() del archivo models.py
            objeto_proveedores = proveedores(
                cod_prov, formulario.id_prov.data, formulario.nombre_prov.data, formulario.direccion_prov.data, formulario.telef_prov.data)

            if objeto_proveedores.actualizar_prov():
                flash(
                    f" El Proveedor: {formulario.nombre_prov.data.upper() }, ha sido editado en el Sistema correctamente.")

                return render_template('proveedores/edit_proveedores.html', mensaje="", id=cod_prov, form=formulario)
            else:
                return render_template('proveedores/edit_proveedores.html', mensaje="El Formulario presenta error al intentar actualizarlo en la Base de Datos.", id=cod_prov, form=formulario)

        else:
            return render_template('proveedores/edit_proveedores.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", id=cod_prov, form=formulario)



@app.route('/proveedores/eliminar/<cod_prov>', methods=["GET", "POST"])
def eliminar_proveedores(cod_prov):
    if request.method == "GET":
        formulario = FormAddProveedores()

        objeto_proveedores = proveedores.cargar(cod_prov)

        if objeto_proveedores:

                formulario.id_prov.data = objeto_proveedores.id_prov

                formulario.nombre_prov.data = objeto_proveedores.nombre_prov

                formulario.direccion_prov.data = objeto_proveedores.direccion_prov

                formulario.telef_prov.data = objeto_proveedores.telef_prov

                return render_template('proveedores/elim_proveedores.html', id=objeto_proveedores.cod_prov, form=formulario)

        else:
            return render_template('proveedores/elim_proveedores.html', mensaje="El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)
    else:
        formulario = FormElimProveedores(request.form)

        if formulario.validate_on_submit():

            objeto_proveedores = proveedores.cargar(cod_prov)

            # Creamos un objeto con la Clase constructora proveedores() del archivo models.py
            objeto_proveedores = proveedores(
                cod_prov, formulario.id_prov.data, formulario.nombre_prov.data, formulario.direccion_prov.data, formulario.telef_prov.data)

            if objeto_proveedores.eliminar_prov():
                flash(
                    f" El Proveedor: {formulario.nombre_prov.data.upper() }, ha sido eliminado del Sistema correctamente.")

                return render_template('proveedores/elim_proveedores.html', mensaje="", id=cod_prov, form=formulario)
            else:
                return render_template('proveedores/elim_proveedores.html', mensaje="El Formulario presenta error al intentar eliminarlo de la Base de Datos.", id=cod_prov, form=formulario)

        else:
            return render_template('proveedores/elim_proveedores.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", id=cod_prov, form=formulario)


@app.route('/proveedores/listar', methods = ["GET"])
def listar_proveedores():
    return render_template('proveedores/listado_prov.html', lista=proveedores.listado_prov())



@app.route('/proveedores/guardar_proveedores', methods=["GET", "POST"])
def guardar_proveedores():
    if request.method == "GET":
        formulario = FormAddProveedores()
        return render_template('proveedores/add_proveedor.html', form=formulario)
    else:
        formulario = FormAddProveedores(request.form)
        if formulario.validate_on_submit():
            
            # Creamos un objeto con la Clase constructora proveedores() del archivo models.py
            objeto_proveedores = proveedores(0, formulario.id_prov.data, formulario.nombre_prov.data, formulario.direccion_prov.data, formulario.telef_prov.data)
            
            if objeto_proveedores.agregar_prov():
                flash(f" El Proveedor: {formulario.nombre_prov.data.upper() }, ha sido creado en el Sistema correctamente.")
                return redirect(url_for('guardar_proveedores'))
            else:
                return render_template('proveedores/add_proveedor.html', mensaje = "El Formulario presenta error al intentar guardar en la Base de Datos.", form=formulario)
            
        else:
            return render_template('proveedores/add_proveedor.html', mensaje = "Este campo del Fomulario presenta error, favor verificar.", form=formulario)


@app.route('/proveedores/asociar_producto_a_proveedor/<cod_prov>', methods=["GET", "POST"])
def asociar_producto_a_proveedor(cod_prov):
    lista_art = proveedores.listado_art()
    
    if request.method == "GET":

        formulario = FormAsociarProveedores()

        objeto_proveedores = proveedores.cargar(cod_prov)

        if objeto_proveedores:
            formulario.nombre_prov.data = objeto_proveedores.nombre_prov
        
            formulario.sel_prod.choices = [(lista_art[i]["cod_prod"], lista_art[i]["producto"]) for i in range(len(lista_art))]

            return render_template('proveedores/asociar_prod.html', id = cod_prov,form=formulario)
        else:
            
            return render_template('proveedores/asociar_prod.html', mensaje="El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)
    else:
        formulario = FormAsociarProveedores(request.form)
        
        if formulario.validate_on_submit():

            cod_prod = int(formulario.sel_prod.data)
            articulo = 'Artículo sin nombre'
            
            #Realizo la búsqueda en el SelectField para encontrar el texto del campo
            for i in range(len(lista_art)):
                if int(lista_art[i]["cod_prod"]) == int(cod_prod): 
                    articulo = lista_art[i]["producto"]

            objeto_proveedores = prod_a_prov(cod_prov, cod_prod)

            if objeto_proveedores.asociar_prod_a_prov():
            
                flash(f" El Producto: { articulo }, ha sido asociado al Proveedor {formulario.nombre_prov.data.upper() } en el Sistema correctamente.")

                return render_template('proveedores/asociar_prod.html', mensaje="", id=cod_prov, form=formulario)
            else:
                return render_template('proveedores/asociar_prod.html', mensaje="El Formulario presenta error al intentar actualizarlo en la Base de Datos.", id=cod_prov, form=formulario)
            
        else:
            return render_template('proveedores/asociar_prod.html', mensaje="Este campo del Fomulario presenta error, favor verificar.", id=cod_prov, form=formulario)




@app.route('/proveedores/buscar', methods=['GET', 'POST'])
def buscar_productos_por_proveedor():
    lista_prov = proveedores.listado_prov()
    if(len(lista_prov)>0):
        cod_prov = lista_prov[0]["cod_prov"]
    else:
        cod_prov =''
    
    if request.method == "GET":

        formulario = FormListarProd_Prov()

        formulario.sel_prov.choices = [(lista_prov[i]["cod_prov"], lista_prov[i]["nombre_prov"]) for i in range(len(lista_prov))]
        print('Cod. Proveedor inicial: ', str(cod_prov))

        return render_template('proveedores/buscar_prod.html', lista=proveedores.productos_prov(cod_prov), form=formulario)
    
    else:
        formulario = FormListarProd_Prov(request.form)
        if request.form.get('action') is None:
            cod_prov = int(formulario.sel_prov.data)
            print('Cod. Proveedor cambio: ', str(cod_prov))
            return render_template('proveedores/buscar_prod.html', lista=proveedores.productos_prov(cod_prov),form=formulario)

        else:
            print('Cod. Producto: ', request.form.get('action'))
            cod_prod = request.form.get('action')
            cod_prov = int(formulario.sel_prov.data)
            print('Cod. Proveedor cambio: ', str(cod_prov))
            
            objeto_proveedores = prov_a_prod(cod_prod, cod_prov)

            if objeto_proveedores.eliminar_asociar():
            
                return render_template('proveedores/buscar_prod.html', lista=proveedores.productos_prov(cod_prov),form=formulario)
            else:
                
                return render_template('proveedores/buscar_prod.html', lista=proveedores.productos_prov(cod_prov),form=formulario)
                
            
    
    
    
    
    
    
    
@app.route('/productos/inventario/<cod_prod>', methods=["GET", "POST"])
def inv_producto(cod_prod): #se agregó (id_producto)
    if request.method == "GET":
        
        formulario = FormInv_prod()

        objeto_productos = productos.cargar(cod_prod)

        if objeto_productos:
            formulario.id_producto.data = objeto_productos.id_producto
            formulario.producto.data = objeto_productos.producto
            formulario.cantidad_mov.data = 0
            return render_template('productos/inv_productos.html', id=objeto_productos.cod_prod, form=formulario)
        else:
            return render_template('productos/inv_productos.html', mensaje = "El Formulario presenta error al intentar traer datos de la Base de Datos.", form=formulario)

    else:
        
        formulario = FormInv_prod(request.form)

        if formulario.validate_on_submit():

            tipo_mov = int(formulario.tipo_mov.data) # 1: Entrada, #2 Salida
            cant_mov = (formulario.cantidad_mov.data)
            nombre_prod = 'okoko'
            
            if(tipo_mov == 2):
                cant_mov = cant_mov * -1
            
            objeto_producto = inventario(cod_prod, cant_mov)
        
            if objeto_producto.insertar_inv():
                flash(f" El Producto: { nombre_prod }, ha recibido un movimiento en el Inventario correctamente.")
                
                return render_template('productos/inv_productos.html', mensaje="", id=cod_prod, form=formulario)                
            else:
                return render_template('productos/inv_productos.html', mensaje="El Formulario presenta error al intentar actualizarlo en la Base de Datos.", id=cod_prod, form=formulario)
