import logica as lg


def ejecutar_menu():
    while True:
        print("\n1. Registrar solicitud")
        print("2. Atender siguiente")
        print("3. Deshacer última atención")
        print("4. Mostrar estado")
        print("5. Ver siguiente turno")
        print("6. Buscar por ID")
        print("7. Cancelar pendiente")
        print("8. Deshacer varias")
        print("9. Estadísticas")
        print("0. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            s, err = lg.registrar_con_control(input("Cliente: "), input("Asunto: "))
            print("Registrada:", s if s else f"No registrada ({err})")
        elif op == "2":
            print("Atendida:", lg.atender_siguiente())
        elif op == "3":
            print("Restaurada:", lg.deshacer_ultima_atencion())
        elif op == "4":
            lg.mostrar_estado()
        elif op == "5":
            print("Siguiente:", lg.consultar_siguiente())
        elif op in ("6", "7", "8"):
            texto = input("Número: ").strip()
            if not texto.isdigit():
                print("Debe ser un número entero positivo")
                continue
            n = int(texto)
            if op == "6":
                print("Resultado:", lg.buscar_solicitud(n))
            elif op == "7":
                print("Cancelada:", lg.cancelar_solicitud(n))
            else:
                print("Restauradas:", lg.deshacer_varias(n))
        elif op == "9":
            print(lg.estadisticas())
        elif op == "0":
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    ejecutar_menu()
