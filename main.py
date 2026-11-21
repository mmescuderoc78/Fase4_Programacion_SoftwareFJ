# aporte manuel escudero============================================================
# SOFTWARE FJ - Sistema Integral de Gestión de Clientes,
# Servicios y Reservas
# ============================================================
# Este programa demuestra:
# - Abstracción (clases abstractas)
# - Herencia
# - Polimorfismo
# - Encapsulación
# - Manejo avanzado de excepciones (try/except/else/finally + encadenamiento)
# - Listas en memoria (sin base de datos)
# - Registro de eventos y errores en archivo de logs
# ============================================================

import abc
import logging
import re

# ============================================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ============================================================
# Se crea un archivo llamado "app.log" donde se registran
# todos los eventos importantes y los errores.
logging.basicConfig(
    filename='app.log',
    filemode='w',          # 'w' = sobrescribe el archivo cada vez que se ejecuta
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('SoftwareFJ')

print("=== INICIANDO SISTEMA SOFTWARE FJ ===")
logger.info("Sistema de Gestión Software FJ iniciado.")


# ============================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ============================================================
# Creamos una jerarquía de excepciones propias.
# Todas heredan de SoftwareFJError para poder capturarlas juntas si se desea.

class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos del cliente no son válidos."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no cumple los requisitos."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando hay un problema al confirmar, cancelar o procesar una reserva."""
    pass

class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando el cálculo de costos no es posible (ej: duración 0)."""
    pass


# Aporte Ronal Camaño=========================================
# 3. CLASE ABSTRACTA BASE (Abstracción)
# ============================================================
class EntidadBase(abc.ABC):
    """
    Clase abstracta que representa cualquier entidad del sistema
    (Cliente, Servicio, etc.). Obliga a las clases hijas a implementar
    el método obtener_resumen().
    """
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abc.abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto: todas las entidades deben poder describirse."""
        pass

# ============================================================
# 4. CLASE CLIENTE (Encapsulación + Validaciones)
# ============================================================
class Cliente(EntidadBase):
    """
    Representa a un cliente.
    Usa propiedades (getter/setter) para encapsular y validar los datos.
    """
    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre      # Usa el setter automáticamente
        self.email = email
        self.telefono = telefono

    # ---------- Nombre ----------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"El nombre '{valor}' es inválido (mínimo 3 caracteres).")
        self._nombre = valor.strip()

    # ---------- Email ----------
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, valor):
            raise ClienteInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._email = valor.strip()

    # ---------- Teléfono ----------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(f"El teléfono '{valor}' debe ser numérico y tener al menos 7 dígitos.")
        self._telefono = valor

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}]: {self.nombre} ({self.email})"

# Aporte Yeison Cueto=========================================
# 5. CLASE ABSTRACTA SERVICIO Y SUBCLASES (Abstracción, Herencia y Polimorfismo)
# ============================================================
class Servicio(EntidadBase):
    """
    Clase abstracta base para todos los servicios del sistema Software FJ.
    Hereda de EntidadBase e impone la definición de calcular_costo().
    """
    def __init__(self, id_servicio: str, nombre: str, precio_base: float):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.precio_base = precio_base

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float):
        if valor <= 0:
            raise CalculoInconsistenteError("El precio base del servicio debe ser mayor a 0.")
        self._precio_base = float(valor)

    @abc.abstractmethod
    def calcular_costo(self, duracion: int, descuento: float = 0.0) -> float:
        """Método abstracto polimórfico para calcular costo según la duración y descuento."""
        pass


# ------------------------------------------------------------
# Subclase 1: Servicio de Reserva de Salas
# ------------------------------------------------------------
class ServicioSalas(Servicio):
    """Servicio para alquiler de salas de reuniones o conferencias por hora."""
    def __init__(self, id_servicio: str, nombre: str, precio_por_hora: float, capacidad_personas: int):
        super().__init__(id_servicio, nombre, precio_por_hora)
        self.capacidad_personas = capacidad_personas

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError("La duración en horas de la sala debe ser mayor a 0.")
        subtotal = self.precio_base * duracion_horas
        total = subtotal * (1 - descuento)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        return f"Sala [{self.id_entidad}]: {self.nombre} (Capacidad: {self.capacidad_personas} p.) - ${self.precio_base}/h"


# ------------------------------------------------------------
# Subclase 2: Servicio de Alquiler de Equipos
# ------------------------------------------------------------
class ServicioEquipos(Servicio):
    """Servicio para alquiler de equipos tecnológicos por días."""
    def __init__(self, id_servicio: str, nombre: str, precio_por_dia: float, deposito_garantia: float):
        super().__init__(id_servicio, nombre, precio_por_dia)
        self.deposito_garantia = deposito_garantia

    def calcular_costo(self, duracion_dias: int, descuento: float = 0.0) -> float:
        if duracion_dias <= 0:
            raise CalculoInconsistenteError("La duración en días para equipos debe ser mayor a 0.")
        subtotal = (self.precio_base * duracion_dias) + self.deposito_garantia
        total = subtotal * (1 - descuento)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id_entidad}]: {self.nombre} - ${self.precio_base}/día (Garantía: ${self.deposito_garantia})"


# ------------------------------------------------------------
# Subclase 3: Servicio de Asesorías Especializadas
# ------------------------------------------------------------
class ServicioAsesorias(Servicio):
    """Servicio para consultorías profesionales con especialistas por hora."""
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialista: str):
        super().__init__(id_servicio, nombre, tarifa_hora)
        self.especialista = especialista

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0) -> float:
        if duracion_horas <= 0:
            raise CalculoInconsistenteError("La duración de la asesoría debe ser mayor a 0 horas.")
        subtotal = self.precio_base * duracion_horas
        total = subtotal * (1 - descuento)
        return round(total, 2)

    def obtener_resumen(self) -> str:
        return f"Asesoría [{self.id_entidad}]: {self.nombre} con {self.especialista} - ${self.precio_base}/h"


# ============================================================
# 6. CLASE RESERVA (Aporte Yeison Cueto)
# ============================================================
class Reserva(EntidadBase):
    """
    Gestiona el ciclo de vida de una reserva (Creación, Confirmación, Cancelación).
    Demuestra el uso avanzado de try/except/else/finally y logging.
    """
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(id_reserva)
        
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente asignado a la reserva no es válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio asignado a la reserva no es válido.")
        if duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser mayor a 0.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def confirmar_reserva(self, descuento: float = 0.0) -> float:
        """
        Confirma la reserva calculando el costo total.
        Demuestra el uso defensivo de try/except/else/finally.
        """
        try:
            if self._estado == "CANCELADA":
                raise ReservaInvalidaError("No se puede confirmar una reserva cancelada.")
            
            # Cálculo del costo usando el método polimórfico del servicio
            self._costo_total = self.servicio.calcular_costo(self.duracion, descuento)
            
        except SoftwareFJError as e:
            logger.error(f"Falla al confirmar reserva [{self.id_entidad}]: {e}")
            raise
        else:
            self._estado = "CONFIRMADA"
            logger.info(
                f"Reserva [{self.id_entidad}] CONFIRMADA exitosamente para "
                f"{self.cliente.nombre} | Costo Total: ${self._costo_total}"
            )
            return self._costo_total
        finally:
            print(f"-> Operación de confirmación procesada para Reserva ID: {self.id_entidad}")

    def cancelar_reserva(self):
        """Cancela la reserva actual registrando el evento en logs."""
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        self._estado = "CANCELADA"
        logger.info(f"Reserva [{self.id_entidad}] CANCELADA por el cliente {self.cliente.nombre}.")

    def obtener_resumen(self) -> str:
        return (f"Reserva [{self.id_entidad}] | Estado: {self._estado} | "
                f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
                f"Duración: {self.duracion} | Total: ${self._costo_total}")


# ============================================================
# BLOQUE DE PRUEBAS LOCALES DE APORTE
# ============================================================
if __name__ == "__main__":
    print("\n--- EJECUCIÓN DE PRUEBA DEL CONSOLIDADO GRUPAL COMPLETO ---")
    
    # 1. Crear Cliente
    c1 = Cliente("12345678", "Ana Pérez", "ana.perez@email.com", "3001234567")
    print(f"1. Cliente: {c1.obtener_resumen()}")
    
    # 2. Crear Servicios (Polimorfismo)
    sala = ServicioSalas("S01", "Sala Ejecutiva A", 50000.0, 10)
    equipo = ServicioEquipos("E01", "Proyector 4K", 30000.0, 100000.0)
    asesoria = ServicioAsesorias("A01", "Consultoría Arquitectura Software", 80000.0, "Ing. Gomez")
    
    print(f"2. {sala.obtener_resumen()}")
    print(f"3. {equipo.obtener_resumen()}")
    print(f"4. {asesoria.obtener_resumen()}")
    
    # 3. Crear y Confirmar Reserva (Uso de try/except/else/finally)
    r1 = Reserva("R01", c1, sala, 4)
    costo = r1.confirmar_reserva(descuento=0.10) # 10% de descuento
    print(f"5. Estado Reserva: {r1.obtener_resumen()}")

# Aporte Ronal Camaño==============================
# 7. GESTOR DEL SISTEMA (Listas en memoria)
# ============================================================
class SistemaGestion:
    """
    Administra las listas de clientes, servicios y reservas.
    No usa base de datos, todo está en memoria.
    """
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)
        logger.info(f"Cliente registrado: {cliente.obtener_resumen()}")

    def registrar_servicio(self, servicio: Servicio):
        self.servicios.append(servicio)
        logger.info(f"Servicio registrado: {servicio.obtener_resumen()}")

    def crear_reserva(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: float) -> Reserva:
        reserva = Reserva(id_reserva, cliente, servicio, duracion)
        self.reservas.append(reserva)
        logger.info(f"Reserva creada: {id_reserva} para cliente {cliente.nombre}")
        return reserva

# ========apote mnauel escudero====================================
# 8. SIMULACIÓN DE 10 OPERACIONES
# ============================================================
sistema = SistemaGestion()

print("\n--- SIMULACIÓN DE OPERACIONES EN SOFTWARE FJ ---\n")

def ejecutar_operacion(numero_op: str, descripcion: str, funcion_op):
    """
    Función auxiliar que ejecuta cada operación de forma segura.
    Captura cualquier error para que el programa NUNCA se detenga.
    """
    print(f"Op #{numero_op}: {descripcion}")
    try:
        funcion_op()
    except Exception as error:
        print(f"  ✗ ERROR (Controlado): {error}")
        logger.warning(f"Excepción atrapada en Op #{numero_op}: {error}")
    else:
        print(f"  ✓ Operación #{numero_op} finalizada correctamente.")
    finally:
        print("-" * 60)


# ---------- Operación 1 (VÁLIDA) ----------
def op1():
    c1 = Cliente("C01", "Carlos Mendoza", "carlos@mail.com", "3001234567")
    sistema.registrar_cliente(c1)
ejecutar_operacion("1", "Registro de Cliente válido (Carlos Mendoza)", op1)

# ---------- Operación 2 (INVÁLIDA) ----------
def op2():
    # Email sin @ → debe fallar
    c_bad = Cliente("C02", "Ana Gómez", "correo_invalido_sin_arroba", "3119876543")
    sistema.registrar_cliente(c_bad)
ejecutar_operacion("2", "Registro de Cliente con Email incorrecto", op2)

# ---------- Operación 3 (VÁLIDA) ----------
def op3():
    s1 = ReservaSala("S01", capacidad_personas=20, incluye_proyector=True, tarifa_base=60.0)
    sistema.registrar_servicio(s1)
ejecutar_operacion("3", "Creación de Servicio de Sala válido", op3)

# ---------- Operación 4 (INVÁLIDA) ----------
def op4():
    # Capacidad negativa → debe fallar
    s_bad = ReservaSala("S02", capacidad_personas=-5, incluye_proyector=False)
    sistema.registrar_servicio(s_bad)
ejecutar_operacion("4", "Creación de Sala con capacidad negativa", op4)

# ---------- Operación 5 (VÁLIDA) ----------
def op5():
    s2 = AsesoriaEspecializada("S03", especialista="Ing. Laura Pérez", nivel_experiencia="Senior", tarifa_base=120.0)
    sistema.registrar_servicio(s2)
ejecutar_operacion("5", "Creación de Asesoría Senior válida", op5)

# ---------- Operación 6 (INVÁLIDA) ----------
def op6():
    # Nivel de experiencia inválido → debe fallar
    s_bad = AsesoriaEspecializada("S04", especialista="Pedro", nivel_experiencia="Principiante")
    sistema.registrar_servicio(s_bad)
ejecutar_operacion("6", "Creación de Asesoría con nivel inválido", op6)

# ---------- Operación 7 (VÁLIDA) ----------
def op7():
    # CORREGIDO: se toman los objetos de las listas, no las listas enteras
    cliente = sistema.clientes[0]
    servicio = sistema.servicios[0]
    reserva1 = sistema.crear_reserva("R01", cliente, servicio, duracion=4.0)
    reserva1.confirmar()
    reserva1.procesar()
ejecutar_operacion("7", "Creación, confirmación y procesamiento de Reserva válida", op7)

# ---------- Operación 8 (INVÁLIDA) ----------
def op8():
    cliente = sistema.clientes[0]
    servicio = sistema.servicios[0]
    # Duración 0 → debe fallar al confirmar
    reserva_bad = sistema.crear_reserva("R02", cliente, servicio, duracion=0.0)
    reserva_bad.confirmar()
ejecutar_operacion("8", "Confirmación de Reserva con duración 0 horas", op8)

# ---------- Operación 9 (INVÁLIDA) ----------
def op9():
    cliente = sistema.clientes[0]
    servicio = sistema.servicios[1]   # Asesoría
    reserva_sin_confirmar = sistema.crear_reserva("R03", cliente, servicio, duracion=2.0)
    # Intentamos procesar sin confirmar → debe fallar
    reserva_sin_confirmar.procesar()
ejecutar_operacion("9", "Procesar Reserva en estado 'Pendiente'", op9)

# ---------- Operación 10 (VÁLIDA) ----------
def op10():
    cliente = sistema.clientes[0]
    s3 = AlquilerEquipo("S05", tipo_equipo="Servidor Dell PowerEdge", seguro_deposito=150.0, tarifa_base=40.0)
    sistema.registrar_servicio(s3)
    reserva_canc = sistema.crear_reserva("R04", cliente, s3, duracion=5.0)
    reserva_canc.cancelar()
ejecutar_operacion("10", "Creación de Alquiler de Equipo y Cancelación de Reserva", op10)


# ============================================================
# FIN DE LA SIMULACIÓN
# ============================================================
print("\n=== SIMULACIÓN FINALIZADA DE FORMA ESTABLE Y CONTINUA ===")
print("Consulte el archivo 'app.log' para ver el historial completo de logs.")
print(f"\nResumen final:")
print(f"  Clientes registrados  : {len(sistema.clientes)}")
print(f"  Servicios registrados : {len(sistema.servicios)}")
print(f"  Reservas creadas      : {len(sistema.reservas)}")
