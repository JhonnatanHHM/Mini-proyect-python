from api.usuarios_vista import UsuariosVista
from api.clientes_vista import ClientesVista
from api.productos_vista import ProductosVista
from api.extintores_vista import ExtintoresVista
from api.tickets_vista import TicketsVista

from repositories.usuarios_repo import UsuariosRepo
from repositories.clientes_repo import ClientesRepo
from repositories.productos_repo import ProductosRepo
from repositories.extintores_repo import ExtintoresRepo
from repositories.tickets_repo import TicketsRepo

from services.usuarios_service import UsuariosService
from services.clientes_service import ClientesService
from services.productos_service import ProductosService
from services.extintores_service import ExtintoresService
from services.tickets_service import TicketsService


def limpiar():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pantalla_inicio():
    limpiar()
    print("\n" + "="*60)
    print("         BIENVENIDO AL SISTEMA DE GESTIÓN")
    print("="*60)
    print("\nDebe iniciar sesión o registrarse para continuar.")
    print("\n1. Iniciar sesión")
    print("2. Crear cuenta")
    print("0. Salir")
    return input("\nSeleccione una opción: ").strip()


def menu_principal(usuario_actual):
    limpiar()
    print("\n" + "="*60)
    print("         SISTEMA DE GESTIÓN EXTINSIA")
    print("="*60)
    print(f"Usuario: {usuario_actual.nombre} ({usuario_actual.email})")
    print("\n1. Gestión de Usuarios")
    print("2. Gestión de Clientes")
    print("3. Gestión de Productos")
    print("4. Gestión de Extintores")
    print("5. Gestión de Tickets")
    print("6. Cerrar sesión")
    print("0. Salir")
    return input("\nSeleccione: ").strip()


def main():
    # === INICIALIZAR REPOSITORIOS ===
    usuarios_repo = UsuariosRepo()
    clientes_repo = ClientesRepo()
    productos_repo = ProductosRepo()
    extintores_repo = ExtintoresRepo()
    tickets_repo = TicketsRepo()

    # === INICIALIZAR SERVICIOS ===
    usuarios_service = UsuariosService(usuarios_repo)
    clientes_service = ClientesService(clientes_repo)
    productos_service = ProductosService(productos_repo)
    extintores_service = ExtintoresService(extintores_repo)
    tickets_service = TicketsService(tickets_repo, clientes_repo, productos_repo, extintores_repo)

    # === INICIALIZAR VISTAS ===
    usuarios_vista = UsuariosVista(usuarios_service)
    clientes_vista = ClientesVista(clientes_service)
    productos_vista = ProductosVista(productos_service)
    extintores_vista = ExtintoresVista(extintores_service)
    tickets_vista = TicketsVista(tickets_service)

    usuario_actual = None

    # === PANTALLA DE INICIO (OBLIGATORIA) ===
    while not usuario_actual:
        opcion = pantalla_inicio()

        if opcion == "1":
            usuario_actual = usuarios_vista.login()
        elif opcion == "2":
            usuario_actual = usuarios_vista.crear_usuario()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            return  # Sale del programa
        else:
            print("Opción inválida.")
        
        if not usuario_actual:
            input("\nPresione Enter para continuar...")
        else:
            print(f"\n¡Bienvenido, {usuario_actual.nombre}!")

    # === MENÚ PRINCIPAL (SOLO SI ESTÁ LOGUEADO) ===
    while usuario_actual:
        opcion = menu_principal(usuario_actual)

        if opcion == "0":
            print("\n¡Hasta luego!")
            break

        elif opcion == "6":  # Cerrar sesión
            confirm = input("\n¿Cerrar sesión? (s/N): ").strip().lower()
            if confirm == 's':
                usuario_actual = usuarios_vista.cerrar_sesion(usuario_actual)
                input("\nPresione Enter para volver al inicio...")
            usuario_actual = pantalla_inicio()

        elif opcion == "1":
            while True:
                op = usuarios_vista.mostrar_menu(usuario_actual)
                if op == "0": break
                if op == "1":
                    usuario_actual = usuarios_vista.actualizar_datos(usuario_actual)
                elif op == "2":
                    usuario_actual = usuarios_vista.cambiar_contrasena(usuario_actual)
                elif op == "3":
                    usuario_actual = usuarios_vista.eliminar_cuenta(usuario_actual)
                    if not usuario_actual:
                        print("Cuenta eliminada. Volviendo al inicio...")
                        input("\nEnter...")
                        break
                input("\nEnter para continuar...")

        elif opcion == "2":
            while True:
                op = clientes_vista.mostrar_menu()
                if op == "0": break
                if op == "1": clientes_vista.crear_cliente()
                elif op == "2": clientes_vista.listar_todos()
                elif op == "3": clientes_vista.buscar_por_nombre()
                elif op == "4": clientes_vista.clientes_por_vencimiento()
                elif op == "5": clientes_vista.actualizar_cliente()
                elif op == "6": clientes_vista.eliminar_cliente()
                input("\nEnter para continuar...")

        elif opcion == "3":
            while True:
                op = productos_vista.mostrar_menu()
                if op == "0": break
                if op == "1": productos_vista.crear_producto()
                elif op == "2": productos_vista.listar_todos()
                elif op == "3": productos_vista.buscar_por_nombre()
                elif op == "4": productos_vista.buscar_por_precio()
                elif op == "5": productos_vista.actualizar_producto()
                elif op == "6": productos_vista.eliminar_producto()
                input("\nEnter para continuar...")

        elif opcion == "4":
            while True:
                op = extintores_vista.mostrar_menu()
                if op == "0": break
                if op == "1": extintores_vista.crear_extintor()
                elif op == "2": extintores_vista.listar_todos()
                elif op == "3": extintores_vista.buscar_por_tipo()
                elif op == "4": extintores_vista.buscar_por_capacidad()
                elif op == "5": extintores_vista.actualizar_extintor()
                elif op == "6": extintores_vista.eliminar_extintor()
                input("\nEnter para continuar...")

        elif opcion == "5":
            while True:
                op = tickets_vista.mostrar_menu()
                if op == "0": break
                if op == "1": tickets_vista.crear_ticket()
                elif op == "2": tickets_vista.listar_todos()
                elif op == "3": tickets_vista.ver_por_cliente()
                elif op == "4": tickets_vista.actualizar_ticket()
                elif op == "5": tickets_vista.eliminar_ticket()
                input("\nEnter para continuar...")

        else:
            print("Opción inválida.")
            input("\nEnter para continuar...")


if __name__ == "__main__":
    main()