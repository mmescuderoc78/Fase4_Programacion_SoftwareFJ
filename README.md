# Fase4_Programacion_SoftwareFJ
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
