import mysql.connector
from mysql.connector import Error
from decouple import config
import json

class CuentaBancaria:
        
        def __init__(self,dni, nombre, apellido, edad, saldo) :
            
            self.__dni= self.validar_dni(dni)
            self.__nombre= nombre.capitalize()
            self.__apellido=apellido.capitalize()
            self.__edad= edad
            self.__saldo= self.validar_saldo(saldo)
                
        
        @property
        def dni(self):
            return self.__dni
        
        @property
        def nombre(self):
            return self.__nombre
        
        @property
        def apellido(self):
            return self.__apellido
        
        @property
        def edad(self):
            return self.__edad
        
        @property
        def saldo(self):
            return self.__saldo
        
        
        def __str__(self) :
            return  f"{self.nombre} {self.apellido}"    
        
                
            
        #Valido DNI
        @staticmethod
        def validar_dni(dni):
            try:
                dni_num = int(dni)
                if len(str(dni)) not in [7, 8]:
                    raise ValueError("El DNI debe tener como minimo 7 dígitos.")
                if dni_num <= 0:
                    raise ValueError("El DNI debe ser un número positivo.")
                return dni_num
            except ValueError:
                raise ValueError("El DNI debe ser un número y tener como minimo 7 dígitos.")
    
        #Valido Apellido
        @staticmethod
        def validar_nombre_apellido(nombre, apellido):            
            try:
                # Eliminamos espacios en blanco y que todo sea en minúsculas
                nombre = nombre.strip().lower()
                apellido = apellido.strip().lower()
                # Verificar si contienen solo letras
                if not nombre.isalpha() or not apellido.isalpha():
                    raise ValueError("El nombre y apellido deben contener solo letras.")
                # Verificar si están vacíos
                if not nombre or not apellido:
                    raise ValueError("El nombre y apellido no pueden estar vacíos.")
                
                return True
            except ValueError as e:
                print(f"Error: {e}")
                return False

        

        #Validar Saldo
        @staticmethod
        def validar_saldo(saldo):
            try:
                saldo = float(saldo)
                if saldo < 0:
                    raise ValueError("El saldo debe ser positivo.")
                return saldo
            except ValueError:
                raise ValueError("El saldo debe ser un número positivo.")
        
        
        
        def to_dict(self) :
            return{
                 "dni":self.dni,
                "nombre":self.nombre,
                "apellido":self.apellido,
                "edad":self.edad,
                "saldo":self.saldo                         
            }
        
         
class CuentaBancariaCorriente(CuentaBancaria):
    def __init__(self,dni, nombre, apellido, edad, saldo, descubierto ):
        super().__init__(dni, nombre, apellido,edad, saldo )        
        self.__descubierto = descubierto

    @property
    def descubierto(self):
        return self.__descubierto

    

    def to_dict(self):
        data = super().to_dict()
        data["descubierto"] = self.__descubierto
        return data

    def __str__(self):
        return f"{super().__str__()} - Descubierto: {self.__descubierto}"        


class CuentaBancariaAhorro(CuentaBancaria):    
    def __init__(self,dni,nombre, apellido, edad, saldo,intereses_mensuales ):
        super().__init__( dni, nombre, apellido, edad, saldo)     
        self.__intereses_mensuales = intereses_mensuales

    @property
    def intereses_mensuales(self):
        return self.__intereses_mensuales    
    
    def to_dict(self):
        data = super().to_dict()
        data["intereses_mensuales"] = self.__intereses_mensuales
        return data

    def __str__(self):
        return f"{super().__str__()} - Intereses Mensuales: {self.intereses_mensuales}"      

    

class GestionCuentaBancaria:


    
    def __init__(self):
        self.host = config('DB_HOST')
        self.database=config('DB_NAME')
        self.user=config('DB_USER')
        self.password=config('DB_PASSWORD')
        self.port=  config('DB_PORT')
    
    def connect(self):
        '''Establecer la conexión con la Base de Datos'''    
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if connection.is_connected():
                return connection

        except Error as e:
            print(f"Error al conectare a la base de datos {e}")
            return None
   ### Obsoleto     
    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al obtener datos del archivo: {error}')
        else:
            return datos
        
    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')    

##Obsoleto
    def crear_cuenta(self, cuenta_bancaria):
        try:
            connection= self.connect()                           #Conecto a la base de datos
            if connection:
                with connection.cursor() as cursor:                #Si existe conección voy a usar cursor para poder moverme en la b.d.
                    #Verifico si existe el DNI asociado a la cuenta
                    cursor.execute('SELECT dni FROM  cuentabancaria WHERE dni = %s',(cuenta_bancaria.dni,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe una cuenta asociada a ese DNI :{cuenta_bancaria.dni}')
                        return
                    
                    # Insertar cuenta dependiendo del tipo                      
                                                                            # *Ver como modificar para simplificar codigo y no repetir
                    if isinstance(cuenta_bancaria,CuentaBancariaCorriente):
                        query='''  
                        INSERT INTO cuentabancaria (dni, nombre, apellido, edad, saldo )
                        VALUES (%s, %s, %s, %s, %s )
                    '''
                        cursor.execute(query, (cuenta_bancaria.dni, cuenta_bancaria.nombre, cuenta_bancaria.apellido, cuenta_bancaria.edad, cuenta_bancaria.saldo ))
                        query='''  
                        INSERT INTO cuentabancariacorriente (dni, descubierto  )
                        VALUES (%s, %s)
                    '''
                        print(f"INSERTANDO: DNI ={cuenta_bancaria.dni}, Nombre ={cuenta_bancaria.nombre}, Descubierto ={cuenta_bancaria.descubierto}")
                        cursor.execute(query, (cuenta_bancaria.dni, cuenta_bancaria.descubierto))

                    elif isinstance(cuenta_bancaria,CuentaBancariaAhorro):    
                        query='''  
                        INSERT INTO cuentabancaria (dni, nombre, apellido, edad, saldo )
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                        cursor.execute(query, (cuenta_bancaria.dni, cuenta_bancaria.nombre, cuenta_bancaria.apellido, cuenta_bancaria.edad, cuenta_bancaria.saldo ))
                        query='''  
                        INSERT INTO cuentabancariaahorro (dni, Intereses_Mensuales )
                        VALUES (%s, %s)
                    '''
                        print(f"INSERTANDO: DNI ={cuenta_bancaria.dni}, Nombre ={cuenta_bancaria.nombre}, Intereses Mensuales ={cuenta_bancaria.intereses_mensuales}")
                        cursor.execute(query, (cuenta_bancaria.dni, cuenta_bancaria.intereses_mensuales))
            
                    connection.commit()
                    print(f"Colaborador {cuenta_bancaria.nombre} {cuenta_bancaria.apellido} creado correctamente")    
                        
        except Exception as error:
            print(f'Error inesperado al crear colaborador: {error}')   


    def leer_cuenta(self, dni):
      try:
        connection = self.connect()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM cuentabancaria WHERE dni = %s', (dni,))
                cuenta_data = cursor.fetchone()

                if cuenta_data:
                    # Normalizar las claves del diccionario para que coincidan con los parámetros esperados
                    cuenta_data = {k.lower(): v for k, v in cuenta_data.items()}
                    
                    cursor.execute('SELECT Intereses_Mensuales FROM cuentabancariaahorro WHERE dni = %s', (dni,))
                    intereses_mensuales = cursor.fetchone()

                    if intereses_mensuales and 'intereses_mensuales' in intereses_mensuales:
                        cuenta_data['intereses_mensuales'] = intereses_mensuales['intereses_mensuales']
                        cuenta = CuentaBancariaAhorro(**cuenta_data)
                    else:
                        cursor.execute('SELECT descubierto FROM cuentabancariacorriente WHERE dni = %s', (dni,))
                        descubierto = cursor.fetchone()

                        if descubierto and 'descubierto' in descubierto:
                            cuenta_data['descubierto'] = descubierto['descubierto']
                            cuenta = CuentaBancariaCorriente(**cuenta_data)
                        else:
                            cuenta = CuentaBancaria(**cuenta_data)
                            print(f'Cuenta encontrada para el DNI: {dni}')
                    
                    return cuenta  # Devolver la cuenta si existe
                else:
                    return None  # Devolver None si no se encuentra la cuenta
        else:
            print('Error al conectar a la base de datos.')
            return None
      except Exception as e:
        print(f'Error al leer Cuenta Bancaria: {e}')
        return None
      finally:
        if connection.is_connected():
            connection.close()

        
            
    def leer_todas_las_cuentas(self):
         try:
             connection=self.connect()
             with connection.cursor(dictionary=True) as cursor:
                 cursor.execute('SELECT * FROM cuentabancaria')
                 cuenta_data= cursor.fetchall()

                 cuenta_bancarias= []
                 for cuenta_data in cuenta_data :
                     # Normalizar las claves a minúsculas
                     cuenta_data = {k.lower(): v for k, v in cuenta_data.items()}
                     dni= cuenta_data['dni']

                     cursor.execute('SELECT descubierto FROM cuentabancariacorriente WHERE dni = %s', (dni,)
                                    )
                     descubierto = cursor.fetchone()
                     
                     if descubierto:
                         cuenta_data['descubierto'] = descubierto['descubierto']
                         cuenta=CuentaBancariaCorriente(**cuenta_data)
                     else:  
                         cursor.execute('SELECT intereses_mensuales FROM cuentabancariaahorro WHERE dni = %s', (dni,))
                         intereses_mensuales = cursor.fetchone()
                         if intereses_mensuales:
                            # Asegurar que la clave coincide con la que espera el constructor
                            cuenta_data['intereses_mensuales'] = intereses_mensuales['intereses_mensuales']
                            cuenta = CuentaBancariaAhorro(**cuenta_data)
                         else:
                            cuenta = CuentaBancaria(**cuenta_data)
                            print(f'Cuenta encontrada para el DNI: {dni}')

                     cuenta_bancarias.append(cuenta)

         except Exception as e:
            print(f'Error al leer todas las cuentas bancarias: {e}')
         else:
             return cuenta_bancarias
         
         finally :
             
             if connection.is_connected() :
                connection.close()

    def actualizar_cuenta(self, dni, nuevo_saldo):
        '''Actualizamos el saldo de una cuenta en la base de datos'''
        try:
                connection =self.connect()
                if connection:
                    with connection.cursor() as cursor:
                        #Verificamos si el Dni existe
                        cursor.execute('SELECT * FROM cuentabancaria WHERE dni = %s', (dni, ))
                        if not cursor.fetchone():
                            print(f'No existe cuenta asociada al DNI: {dni} ')
                            return
                        # Actualizar  saldo
                        cursor.execute('UPDATE cuentabancaria SET saldo = %s WHERE dni =%s ', (nuevo_saldo, dni))
                        
                        
                        if cursor.rowcount > 0 :
                            connection.commit()
                            print(f'Saldo actualizado para la cuenta asociada al DNI: {dni}')#Se puede eliminar
                        else :
                            print('No se encontro cuenta asociada al DNI: {dni}}')

        except Exception as e:
                    print(f'Error al leer Cuenta Bancaria: {e}')
        finally:
            if connection.is_connected():
                connection.close()                 

    def eliminar_cuenta(self, dni):            
            try:
                connection =self.connect()
                if connection:
                    with connection.cursor() as cursor:
                        #Se verifica si el DNI esta asociado a una cuenta 
                        cursor.execute('SELECT * FROM cuentabancaria WHERE dni = %s', (dni,))
                        if not cursor.fetchone():
                            print(f'No existe cuenta asociada el DNI: {dni}.')
                            return
                        #Eliminar cuenta
                        cursor.execute('DELETE FROM cuentabancariaahorro WHERE dni = %s', (dni,))
                        cursor.execute('DELETE FROM cuentabancariacorriente WHERE dni = %s', (dni,))
                        cursor.execute('DELETE FROM cuentabancaria WHERE dni = %s', (dni,))
                        if cursor.rowcount > 0 :
                            connection.commit()
                            print(f'Cuenta asociada al DNI: {dni} ha sido eliminada correctamente ')
                        else:
                            print('No se encontro cuenta asociada al DNI: {dni}}')
            except Exception as e:
                    print(f'Error al leer Cuenta Bancaria: {e}')
            finally:
                    if connection.is_connected():
                        connection.close()             
