class Cliente:
    """MODELO: un cliente válido. Si los datos están mal, el objeto no se crea."""

    CAMPOS = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")
    OBLIGATORIOS = ("nombre", "apellido", "email")
    total_creados = 0

    def __init__(self, id_cliente, nombre, apellido, email,
                 telefono="", ciudad="", direccion=""):
        self.__id = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion
        Cliente.total_creados += 1

    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

    @staticmethod
    def es_email_valido(texto):
        texto = str(texto).strip()

        if texto.count("@") != 1:
            return False

        usuario, dominio = texto.split("@")

        return (
            len(usuario) > 0
            and "." in dominio
            and not dominio.endswith(".")
        )

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = Cliente.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = Cliente.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = Cliente.limpiar(valor)

        if not Cliente.es_email_valido(valor):
            raise ValueError(f"Email inválido: '{valor}'")

        self.__email = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = Cliente.limpiar(valor)

        if valor and not valor.isdigit():
            raise ValueError("El teléfono solo puede tener números")

        self.__telefono = valor

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, valor):
        self.__ciudad = Cliente.limpiar(valor).title()

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = Cliente.limpiar(valor)

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def dominio_email(self):
        return self.__email.split("@")[1]

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "telefono": self.__telefono,
            "ciudad": self.__ciudad,
            "direccion": self.__direccion,
        }

    def __str__(self):
        return f"[{self.__id}] {self.nombre_completo} - {self.__email}"

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos.get("telefono", ""),
            datos.get("ciudad", ""),
            datos.get("direccion", ""),
        )


class Estudiante:
    """MODELO: estudiante con materias y notas."""

    CAMPOS = ("nombre", "apellido", "email", "carnet")
    OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")

    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20

    total_creados = 0

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):

        self.__id = id_estudiante

        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        self.__notas = dict(notas) if notas else {}
        self.__materias = set(materias) if materias else set()

        Estudiante.total_creados += 1

    # ==========================
    # MÉTODOS ESTÁTICOS
    # ==========================

    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

    @staticmethod
    def es_nota_valida(nota):
        return (
            isinstance(nota, (int, float))
            and Estudiante.NOTA_MINIMA <= nota <= Estudiante.NOTA_MAXIMA
        )

    # ==========================
    # PROPIEDADES
    # ==========================

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = Estudiante.limpiar(valor)

        if "@" not in valor:
            raise ValueError(f"Email inválido: '{valor}'")

        self.__email = valor.lower()

    @property
    def carnet(self):
        return self.__carnet

    @carnet.setter
    def carnet(self, valor):
        valor = Estudiante.limpiar(valor).upper()

        if len(valor) < 4:
            raise ValueError("El carnet debe tener al menos 4 caracteres")

        self.__carnet = valor

    @property
    def materias(self):
        return set(self.__materias)

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def promedio(self):
        todas = []

        for lista_notas in self.__notas.values():
            todas.extend(lista_notas)

        if todas:
            return round(sum(todas) / len(todas), 2)

        return 0

    # PROPIEDAD PEDIDA EN LA TAREA
    @property
    def estado(self):
        if self.promedio >= 14:
            return "Aprobado"

        return "Reprobado"

    # ==========================
    # MÉTODOS DE INSTANCIA
    # ==========================

    def inscribir_materia(self, materia):
        materia = Estudiante.limpiar(materia).title()

        if not materia:
            raise ValueError("La materia no puede estar vacía")

        self.__materias.add(materia)

        return materia

    def agregar_nota(self, materia, nota):

        if not Estudiante.es_nota_valida(nota):
            raise ValueError(
                f"La nota debe estar entre "
                f"{Estudiante.NOTA_MINIMA} y "
                f"{Estudiante.NOTA_MAXIMA}"
            )

        materia = self.inscribir_materia(materia)

        self.__notas.setdefault(materia, []).append(nota)

    def notas_de(self, materia):
        materia = Estudiante.limpiar(materia).title()

        return list(
            self.__notas.get(materia, [])
        )

    def materias_en_comun(self, otro):
        return self.__materias & otro.materias

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "carnet": self.__carnet,
            "notas": self.__notas,
            "materias": sorted(self.__materias),
        }

    def __str__(self):
        return (
            f"[{self.__carnet}] "
            f"{self.nombre_completo} - "
            f"Promedio: {self.promedio} - "
            f"Estado: {self.estado}"
        )

    # ==========================
    # MÉTODO DE CLASE
    # ==========================

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(
                datos.get("materias", [])
            ),
        )