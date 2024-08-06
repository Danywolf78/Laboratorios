
import os
import platform

from TipoDeCuentas import (
    CuentaBancariaAhorro,
    CuentaBancariaCorriente,
    GestionCuentaBancaria,
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') 


def mostrar_menu():
    print("========== Menú de Gestión de Cuentas Bancarias ==========")
    print('1. Crear Caja de Ahorro')
    print('2. Crear Cuenta Corriente')
    print('3. Buscar Cuenta por DNI')
    print('4. Actualizar Saldo')
    print('5. Eliminarar Cuenta por DNI')
    print('6. Mostrar Todas los Cuentas')
    print('7. Salir')
    print('======================================================')

def agregar_Cuenta(gestion, tipo_de_cuenta):
    try:
        dni = input('Ingrese DNI del Titular: ')
        nombre = input('Ingrese nombre del Titular: ')
        apellido = input('Ingrese apellido del Titular: ')
        edad = int(input('Ingrese edad del Titular: '))
        saldo = float(input('Ingrese saldo del Titular: '))

        if tipo_de_cuenta == '1':
            descubierto = float(input('Ingrese maximo descubierto: '))
            CuentaBancaria = CuentaBancariaCorriente(nombre, apellido, saldo, descubierto)
        elif tipo_de_cuenta == '2':
            intereses_mensuales = int(input('Ingrese los intereses mensuales de la cuenta: '))
            CuentaBancaria = CuentaBancariaAhorro(dni, nombre, apellido, edad, saldo,intereses_mensuales )
        else:
            print('Opción inválida')
            return

        gestion.crear_cuenta(CuentaBancaria)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_colaborador_por_dni(gestion):
    dni = input('Ingrese el DNI del titular de la Cuenta a buscar: ')
    gestion.leer_cuenta(dni)
    input('Presione enter para continuar...')

def actualizar_saldo_cuenta(gestion):
    dni = input('Ingrese el DNI del titular de la Cuenta para actualizar saldo: ')
    saldo = float(input('Ingrese el saldo de la cuenta'))
    gestion.actualizar_Cuenta(dni, saldo)
    input('Presione enter para continuar...') 

def eliminar_cuenta(gestion):
    dni = input('Ingrese el DNI del titular de la Cuenta a eliminar: ')
    gestion.eliminar_cuenta(dni)
    input('Presione enter para continuar...')   

def mostrar_todas_las_cuentas(gestion):
    print('=============== Listado  de las  Cuentas ==============')
    for CuentaBancaria in gestion.leer_cuenta().values():
        if 'descubierto' in CuentaBancaria:
            print(f"{CuentaBancaria['nombre']} - Descubierto {CuentaBancaria['descubierto']}")
        else:
            print(f"{CuentaBancaria['nombre']} - Intereses Mensuales {CuentaBancaria['intereses_mensuales']}")
    print('=====================================================================')
    input('Presione enter para continuar...')    

if __name__ == "__main__":
    archivo_colaboradores = 'cuentas.json'
    gestion = GestionCuentaBancaria(archivo_colaboradores)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_Cuenta(gestion, opcion)
        
        elif opcion == '3':
            buscar_colaborador_por_dni(gestion)

        elif opcion == '4':
            actualizar_saldo_cuenta(gestion)

        elif opcion == '5':
            eliminar_cuenta(gestion)

        elif opcion == '6':
            mostrar_todas_las_cuentas(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
        

