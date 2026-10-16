import logica as lg


def nombres(lista):
    return [s["cliente"] for s in lista]


def cargar(*clientes):
    lg.reiniciar()
    for c in clientes:
        lg.registrar_solicitud(c, "asunto " + c)


def test_cola_vacia_atender():
    lg.reiniciar()
    assert lg.atender_siguiente() is None


def test_pila_vacia_deshacer():
    lg.reiniciar()
    assert lg.deshacer_ultima_atencion() is None


def test_atender_dos_veces():
    cargar("A", "B", "C")
    lg.atender_siguiente(); lg.atender_siguiente()
    assert nombres(lg.pila_historial) == ["A", "B"]
    assert nombres(lg.cola_pendientes) == ["C"]


def test_deshacer_una_vez():
    cargar("A", "B", "C")
    lg.atender_siguiente(); lg.atender_siguiente()
    lg.deshacer_ultima_atencion()
    assert nombres(lg.cola_pendientes) == ["B", "C"]
    assert nombres(lg.pila_historial) == ["A"]


def test_cancelar_intermedia():
    cargar("A", "B", "C")
    assert lg.cancelar_solicitud(2)["cliente"] == "B"
    assert nombres(lg.cola_pendientes) == ["A", "C"]
    assert lg.cancelar_solicitud(99) is None


def test_registro_vacio():
    lg.reiniciar()
    assert lg.registrar_solicitud("", "x") is None
    assert lg.registrar_solicitud("x", "   ") is None
    assert lg.cola_pendientes == []


def test_buscar():
    cargar("A", "B")
    lg.atender_siguiente()
    assert lg.buscar_solicitud(1)[1] == "historial"
    assert lg.buscar_solicitud(2)[1] == "pendiente"
    assert lg.buscar_solicitud(99) is None
    assert nombres(lg.cola_pendientes) == ["B"]  # sin alterar orden


def test_consultar_siguiente_no_extrae():
    lg.reiniciar()
    assert lg.consultar_siguiente() is None
    cargar("A", "B")
    assert lg.consultar_siguiente()["cliente"] == "A"
    assert len(lg.cola_pendientes) == 2


def test_deshacer_varias():
    cargar("A", "B", "C")
    for _ in range(3):
        lg.atender_siguiente()
    assert lg.deshacer_varias(0) is None
    assert lg.deshacer_varias("2") is None
    assert nombres(lg.deshacer_varias(2)) == ["C", "B"]
    assert nombres(lg.cola_pendientes) == ["B", "C"]
    assert len(lg.deshacer_varias(10)) == 1  # solo queda A en la pila
    assert nombres(lg.cola_pendientes) == ["A", "B", "C"]
    assert lg.deshacer_varias(3) == []


def test_duplicados_y_estadisticas():
    lg.reiniciar()
    assert lg.registrar_con_control("Ana", "Wi-Fi")[1] is None
    assert lg.registrar_con_control(" ana ", "WI-FI")[1] == "duplicado"
    assert lg.registrar_con_control("", "x")[1] == "invalido"
    lg.registrar_solicitud("Luis", "Impresora")
    lg.atender_siguiente()
    lg.cancelar_solicitud(2)
    assert lg.estadisticas() == {"pendientes": 0, "atendidas": 1,
                                 "canceladas": 1, "registradas": 2}


if __name__ == "__main__":
    for nombre, f in list(globals().items()):
        if nombre.startswith("test_"):
            f()
            print("OK", nombre)
