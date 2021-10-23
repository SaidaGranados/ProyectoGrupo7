import db
import db
from werkzeug.security import generate_password_hash,check_password_hash

# Modificadores de Acceso
# _ Protected
# __Privated
# Sin guión, es Public


class prov_a_prod():
    cod_prod = 0
    cod_prov = 0

    def __init__(self, pcod_prod, pcod_prov):
        self.cod_prod = pcod_prod
        self.cod_prov = pcod_prov

    def asociar_prov_a_prod(self):
        sql = "SELECT * FROM prov_prod WHERE cod_prod = ? and cod_prov = ?; "
        resultado = db.ejecutar_select(sql, [self.cod_prod, self.cod_prov])
        if resultado:
            return True
        else:
            sql = "insert into prov_prod (cod_prod, cod_prov) values (?, ?); "
            afectadas = db.ejecutar_insert(sql, [self.cod_prod, self.cod_prov])
            return (afectadas > 0)
        
    def eliminar_asociar(self):
        sql = "delete from prov_prod where cod_prod = ? and cod_prov =  ?; "
        afectadas = db.ejecutar_insert(sql, [self.cod_prod, self.cod_prov])
        return (afectadas > 0)

class prod_a_prov():
    cod_prov = 0
    cod_prod = 0

    def __init__(self, pcod_prov, pcod_prod):
        self.cod_prov = pcod_prov
        self.cod_prod = pcod_prod

    def asociar_prod_a_prov(self):
        sql = "SELECT * FROM prov_prod WHERE cod_prov = ? and cod_prod = ?; "
        resultado = db.prov_select(sql, [self.cod_prov, self.cod_prod])
        if resultado:
            return True
        else:
            sql = "insert into prov_prod (cod_prov, cod_prod) values (?, ?); "
            afectadas = db.insert_prov(sql, [self.cod_prov, self.cod_prod])
            return (afectadas > 0)


class proveedores():

    cod_prov = 0
    id_prov = ''
    nombre_prov = ''
    direccion_prov = ''
    telef_prov = ''

    def __init__(self, pcod_prov, pid_prov, pnombre_prov, pdireccion_prov, ptelef_prov):
        self.cod_prov = pcod_prov
        self.id_prov = pid_prov
        self.nombre_prov = pnombre_prov
        self.direccion_prov = pdireccion_prov
        self.telef_prov = ptelef_prov

    # Sobrecarga de un controlador, que permite instancias de una clase de diferentes formas
    @classmethod
    def cargar(cls, pcod_prov):
        sql = "SELECT * FROM proveedores WHERE cod_prov = ?; "
        resultado = db.prov_select(sql, [pcod_prov])
        if resultado:
            if len(resultado) > 0:
                return cls(pcod_prov,
                           resultado[0]["id_prov"],
                           resultado[0]["nombre_prov"],
                           resultado[0]["direccion_prov"],
                           resultado[0]["telef_prov"]
                           )

        return None
    
    def agregar_prov(self):
        sql = "insert into proveedores (id_prov, nombre_prov, direccion_prov, telef_prov) values (?, ?, ?, ?); "
        afectadas = db.insert_prov(
            sql, [self.id_prov, self.nombre_prov, self.direccion_prov, self.telef_prov])
        # Validamos que si es mayor que 0, o sea, que al menos insertó un registro
        return (afectadas > 0)

    def eliminar_prov(self):
        sql = "DELETE FROM proveedores where cod_prov = ?; "
        afectadas = db.insert_prov(sql, [self.cod_prov])
        # Validamos que si es mayor que 0, o sea, que al menos insertó un registro
        return (afectadas > 0)
        

    def actualizar_prov(self):
        sql = "UPDATE proveedores SET id_prov = ?, nombre_prov = ?, direccion_prov = ?, telef_prov= ? where cod_prov = ?; "
        afectadas = db.insert_prov(
            sql, [self.id_prov, self.nombre_prov, self.direccion_prov, self.telef_prov, self.cod_prov])
        # Validamos que si es mayor que 0, o sea, que al menos insertó un registro
        return (afectadas > 0)
    

    @classmethod
    def productos_prov(cls, pcod_prov):
        sql = "SELECT proveedores.cod_prov, proveedores.id_prov, proveedores.nombre_prov, proveedores.direccion_prov, proveedores.telef_prov, prov_prod.cod_prod, productos.id_producto, productos.producto, productos.descripcion, productos.cantidad_minima, productos.cantidad_disponible FROM (prov_prod LEFT OUTER JOIN productos ON (prov_prod.cod_prod = productos.cod_prod)) INNER JOIN proveedores ON (proveedores.cod_prov = prov_prod.cod_prov) where proveedores.cod_prov = ?; "
        return db.prov_select(sql, [pcod_prov])
    
    @classmethod
    def proveedor_prod(cls, pcod_prod):
        sql = "SELECT proveedores.cod_prov, proveedores.id_prov, proveedores.nombre_prov, proveedores.direccion_prov, proveedores.telef_prov, prov_prod.cod_prod, productos.cod_prod, productos.id_producto, productos.producto, productos.descripcion, productos.cantidad_minima, productos.cantidad_disponible FROM (prov_prod LEFT OUTER JOIN productos ON (prov_prod.cod_prod = productos.cod_prod)) INNER JOIN proveedores ON (proveedores.cod_prov = prov_prod.cod_prov) where productos.cod_prod = ?; "
        return db.prov_select(sql, [pcod_prod])

    @staticmethod
    def listado_prov():
        sql = "select * From proveedores order by nombre_prov; "
        return db.prov_select(sql, None)

    @staticmethod
    def listado_art():
        sql = "select * From productos order by producto; "
        return db.prov_select(sql, None)



############################################################################
########                    PRODUCTOS                            ###########
############################################################################

class productos():
    cod_prod = 0  # se agrego
    id_producto = ''
    producto = ''
    descripcion = ''
    cantidad_minima = ''
    cantidad_disponible = ''

    def __init__(self, pcod_prod, pid_producto, pproducto, pdescripcion, pcantidad_minima, pcantidad_disponible):
        self.cod_prod = pcod_prod  # se agrego
        self.id_producto = pid_producto
        self.producto = pproducto
        self.descripcion = pdescripcion
        self.cantidad_minima = pcantidad_minima
        self.cantidad_disponible = pcantidad_disponible

    @classmethod
    def cargar(cls, pcod_prod):
        sql = "SELECT * FROM productos WHERE cod_prod = ?;"
        resultado = db.ejecutar_select(sql, [pcod_prod])
        if resultado:
            if len(resultado) > 0:
                return cls(pcod_prod, resultado[0]['id_producto'], resultado[0]["producto"],
                           resultado[0]["descripcion"], resultado[0]["cantidad_minima"], resultado[0]["cantidad_disponible"])

        return None

    def insertar(self):
        sql = "INSERT INTO productos (id_producto, producto, descripcion, cantidad_minima, cantidad_disponible) VALUES (?,?,?,?,?);"
        afectadas = db.ejecutar_insert(
            sql, [self.id_producto, self.producto, self.descripcion, self.cantidad_minima, self.cantidad_disponible])
        return (afectadas > 0)

    def eliminar(self):
        sql = "DELETE FROM productos where cod_prod = ?;"
        afectadas = db.ejecutar_insert(sql, [self.cod_prod])
        return (afectadas > 0)

    def editar(self):
        sql = "UPDATE productos SET id_producto = ?, producto = ?, descripcion =  ?, cantidad_minima = ?, cantidad_disponible = ? WHERE cod_prod = ?;"
        afectadas = db.ejecutar_insert(
            sql, [self.id_producto, self.producto, self.descripcion, self.cantidad_minima, self.cantidad_disponible, self.cod_prod])
        return (afectadas > 0)

    @staticmethod
    def listado():
        sql = "SELECT * FROM productos ORDER BY producto;"
        return db.ejecutar_select(sql, None)
    

    @staticmethod
    def listado_prov():
        sql = "select * From proveedores order by nombre_prov; "
        return db.ejecutar_select(sql, None)


############################################################################
########                    USUARIOS                            ############
############################################################################
class usuarios():

    cod_usu = 0
    id_usu = ''
    nombre_usu = ''
    contrasena_usu = ''
    cod_rol = ''

    def __init__(self,pcod_usu, pid_usu, pnombre_usu, pcontrasena_usu, pcod_rol):
        self.cod_usu = pcod_usu
        self.id_usu = pid_usu
        self.nombre_usu = pnombre_usu
        self.contrasena_usu = pcontrasena_usu
        self.cod_rol = pcod_rol


    #Metodo para verificar el usuario contra la bds
    def autenticar(self):
        #sql = "SELECT * FROM usuarios WHERE id_usu = '" + self.id_usu +"' AND contrasena_usu = '"+ self.contrasena_usu +"'"
        #sql = "SELECT * FROM usuarios WHERE id_usu = ? AND contrasena_usu = ?;"
        sql = "SELECT * FROM usuarios WHERE id_usu = ?;"      
        
        # Para prevenir inyeccion codigo sql
        obj = db.usu_select(sql, [self.id_usu])
        print(obj)
        if obj:
            if len(obj) > 0:
                if check_password_hash(obj[0]["contrasena_usu"],self.contrasena_usu):                    
                    return True
        return False


    @staticmethod
    def listado_usu():
        sql = "SELECT * From usuarios order by nombre_usu; "
        return db.usu_select(sql, None) 
        
    @classmethod
    def cargar(cls, pcod_usu):
        sql = "SELECT * FROM usuarios WHERE cod_usu = ?; "
        
        resultado = db.usu_select(sql, [pcod_usu])
        if resultado:
            if len(resultado) > 0:
                return cls(pcod_usu,
                           resultado[0]["id_usu"],
                           resultado[0]["nombre_usu"],
                           '',
                           resultado[0]["cod_rol"],            
                           )
        
        return None


    def agregar_usu(self):        
        sql = "INSERT INTO usuarios (id_usu, nombre_usu, contrasena_usu,cod_rol) values (?, ?, ?, ?)"
        hashed_pwd = generate_password_hash(self.contrasena_usu, method='pbkdf2:sha256',salt_length=32)
        afectadas = db.insert_usu(sql, [self.id_usu, self.nombre_usu, hashed_pwd, self.cod_rol])
        
        #afectadas = db.insert_usu(sql, [self.id_usu, self.nombre_usu, self.contrasena_usu, self.cod_rol])
        return (afectadas > 0)


    def eliminar_usu(self):
        sql = "DELETE FROM usuarios where cod_usu = ?"
        print(self.cod_usu)
        afectadas = db.insert_usu(sql, [self.cod_usu])
        return (afectadas > 0)


    def actualizar_usu(self):
        sql = "UPDATE usuarios SET id_usu = ?, nombre_usu = ?, contrasena_usu = ?, cod_rol= ? where cod_usu = ?; "
        hashed_pwd = generate_password_hash(self.contrasena_usu, method='pbkdf2:sha256',salt_length=32)
        afectadas = db.insert_usu(sql, [self.id_usu, self.nombre_usu, hashed_pwd, self.cod_rol, self.cod_usu])
        return (afectadas > 0) #Validamos que si es mayor que 0, o sea, que al menos insertó un registro


    @staticmethod
    def listado_usu():
        sql = "SELECT * From usuarios order by nombre_usu; "
        return db.usu_select(sql, None)      

