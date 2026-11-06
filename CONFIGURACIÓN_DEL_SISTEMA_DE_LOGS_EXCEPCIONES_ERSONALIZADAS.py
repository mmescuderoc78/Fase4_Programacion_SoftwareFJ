# ============================================================
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
