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


# ============================================================
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
