"""Lógica de negocio: cola de pendientes (FIFO) y pila de historial (LIFO). Sin clases."""

cola_pendientes = []
pila_historial = []
siguiente_id = 1
canceladas = 0


def reiniciar():
    """Deja todo en blanco (útil para las pruebas)."""
    global siguiente_id, canceladas
    cola_pendientes.clear()
    pila_historial.clear()
    siguiente_id = 1
    canceladas = 0


def mostrar_estado():
    print("\nPendientes:", cola_pendientes)
    print("Historial:", pila_historial)


def registrar_solicitud(cliente, asunto):
    global siguiente_id
    if not cliente.strip() or not asunto.strip():
        return None
    solicitud = {
        "id": siguiente_id,
        "cliente": cliente.strip(),
        "asunto": asunto.strip(),
        "estado": "pendiente",
    }
    cola_pendientes.append(solicitud)
    siguiente_id += 1
    return solicitud


def atender_siguiente():
    if not cola_pendientes:
        return None
    solicitud = cola_pendientes.pop(0)
    solicitud["estado"] = "atendida"
    pila_historial.append(solicitud)
    return solicitud


def deshacer_ultima_atencion():
    if not pila_historial:
        return None
    solicitud = pila_historial.pop()
    solicitud["estado"] = "pendiente"
    cola_pendientes.insert(0, solicitud)
    return solicitud


# ---------- Reto 1 ----------
def consultar_siguiente():
    """Devuelve la próxima solicitud sin extraerla (o None)."""
    return cola_pendientes[0] if cola_pendientes else None


# ---------- Reto 2 ----------
def buscar_solicitud(id_solicitud):
    """Devuelve (registro, 'pendiente' | 'historial') o None. No altera el orden."""
    for s in cola_pendientes:
        if s["id"] == id_solicitud:
            return s, "pendiente"
    for s in pila_historial:
        if s["id"] == id_solicitud:
            return s, "historial"
    return None


# ---------- Reto 3 ----------
def cancelar_solicitud(id_solicitud):
    """Quita una solicitud pendiente conservando el orden de las demás."""
    global canceladas
    for i, s in enumerate(cola_pendientes):
        if s["id"] == id_solicitud:
            cancelada = cola_pendientes.pop(i)
            cancelada["estado"] = "cancelada"
            canceladas += 1
            return cancelada
    return None


# ---------- Reto 4 ----------
def deshacer_varias(cantidad):
    """Deshace hasta `cantidad` atenciones. None si la cantidad es inválida;
    lista (posiblemente vacía) con las restauradas en caso contrario."""
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:
        return None
    restauradas = []
    while len(restauradas) < cantidad:
        s = deshacer_ultima_atencion()
        if s is None:
            break
        restauradas.append(s)
    return restauradas


# ---------- Reto 5 ----------
def es_duplicado(cliente, asunto):
    """True si ya hay una solicitud PENDIENTE con el mismo cliente y asunto."""
    c, a = cliente.strip().lower(), asunto.strip().lower()
    return any(s["cliente"].lower() == c and s["asunto"].lower() == a
               for s in cola_pendientes)


def registrar_con_control(cliente, asunto):
    """Devuelve (solicitud, error); error: None, 'invalido' o 'duplicado'."""
    if not cliente.strip() or not asunto.strip():
        return None, "invalido"
    if es_duplicado(cliente, asunto):
        return None, "duplicado"
    return registrar_solicitud(cliente, asunto), None


def estadisticas():
    return {
        "pendientes": len(cola_pendientes),
        "atendidas": len(pila_historial),
        "canceladas": canceladas,
        "registradas": siguiente_id - 1,
    }
