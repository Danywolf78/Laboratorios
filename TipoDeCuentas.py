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
    
    def __init__(self,archivo):
        self.archivo = archivo 
    
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


    def crear_cuenta(self, cuenta_bancaria):
        try:
            datos = self.leer_datos()
            dni = cuenta_bancaria.dni
            if  not str(dni) in datos.keys():
                datos[dni] = cuenta_bancaria.to_dict()
                self.guardar_datos(datos)
                print(f"Cuenta a nombre de {cuenta_bancaria.nombre} {cuenta_bancaria.apellido} creado correctamente.")
            else:
                print(f"Ya existe colaborador con DNI '{dni}'.")
        except Exception as error:
            print(f'Error inesperado al crear colaborador: {error}')   


    def leer_cuenta(self, dni):
        try:
            datos = self.leer_datos()
            if dni in datos:
                cuenta_data = datos[dni]
                if 'descubierto' in cuenta_data:
                    cuentas = CuentaBancariaCorriente(**cuenta_data)
                    
                else:
                    cuentas = CuentaBancariaAhorro(**cuenta_data)                     
                print(f'Cuenta bancaria encontrada con DNI {dni}') 
            else:
                print(f'No se encontró ninguna cuenta con DNI {dni}')

        except Exception as e:
            print('Error al leer Cuanta Bancaria: {e}')
            
    def leer_todas_las_cuentas(self):
        try:
            datos = self.leer_datos()
            cuenta = {}
            for dni, cuenta_data in datos.items():
                if "descubierto" in cuenta_data:
                    cuenta[dni] = CuentaBancariaCorriente(**cuenta_data)
                     
                else:
                    cuenta[dni] = CuentaBancariaAhorro(**cuenta_data)
                     
            return cuenta
        except Exception as e:
            print(f'Error al leer todas las cuentas bancarias: {e}')
            return {}    
    def actualizar_cuenta(self, dni, nuevo_saldo):
            try:
                datos = self.leer_datos()
                if str(dni) in datos:
                    datos[str(dni)]['saldo'] = nuevo_saldo
                    self.guardar_datos(datos)
                    print(f'Salario actualizado para la cuenta  DNI:{dni}')
                else:
                    print(f'No se encontró cuenta con número de DNI:{dni}')
            except Exception as e:
                print(f'Error al actualizar la cuenta: {e}')


    def eliminar_cuenta(self, dni):
            try:
                datos = self.leer_datos()
                if str(dni) in datos:
                    del datos[str(dni)]
                    self.guardar_datos(datos)
                    print(f'Cuenta numero:{dni} eliminado correctamente')
                else:
                    print(f'No se encontró cuenta con el siguiente DNI:{dni}')
            except Exception as e:
                print(f'Error al eliminar la cuenta: {e}')            