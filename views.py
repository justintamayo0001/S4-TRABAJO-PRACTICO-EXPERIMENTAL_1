from models import Cliente, Estudiante
from shared.json_manager import GestorJSON


class ClienteController:
    """CONTROLADOR: realiza las operaciones CRUD. No imprime ni pide datos."""

    MODELO = Cliente
    ARCHIVO = "data/clientes.json"
    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "telefono",
        "ciudad"
    )

    _gestor = GestorJSON(ARCHIVO)

    # =========================================
    # MÉTODOS DE APOYO
    # =========================================

    @classmethod
    def _registros(cls):
        """Devuelve la lista de registros almacenados en JSON."""
        return cls._gestor.leer()

    @classmethod
    def emails_registrados(cls, excepto_id=None):
        """Conjunto de emails ya registrados."""
        return {
            registro["email"].lower()
            for registro in cls._registros()
            if registro["id"] != excepto_id
        }

    @classmethod
    def siguiente_id(cls):
        """Calcula automáticamente el siguiente ID."""
        ids = [
            registro["id"]
            for registro in cls._registros()
        ]

        return max(ids) + 1 if ids else 1

    @staticmethod
    def _coincide(registro, termino, campos):
        """Comprueba si el término aparece en alguno de los campos."""

        for campo in campos:

            if termino in str(
                registro.get(campo, "")
            ).lower():

                return True

        return False

    # =========================================
    # CREATE - CREAR
    # =========================================

    @classmethod
    def crear(cls, datos):
        """Crea un nuevo registro."""

        try:

            faltantes = [
                campo
                for campo in cls.MODELO.OBLIGATORIOS
                if not str(
                    datos.get(campo, "")
                ).strip()
            ]

            if faltantes:
                return (
                    False,
                    f"Faltan campos obligatorios: "
                    f"{', '.join(faltantes)}"
                )

            email = str(
                datos.get("email", "")
            ).strip().lower()

            if email in cls.emails_registrados():
                return (
                    False,
                    "Ese email ya está registrado"
                )

            valores = {
                campo: datos.get(campo, "")
                for campo in cls.MODELO.CAMPOS
            }

            objeto = cls.MODELO(
                cls.siguiente_id(),
                **valores
            )

            registros = cls._registros()

            registros.append(
                objeto.a_diccionario()
            )

            if not cls._gestor.guardar(registros):
                return (
                    False,
                    "No se pudo escribir el archivo"
                )

            return (
                True,
                f"{objeto.nombre_completo} "
                f"creado con id {objeto.id}"
            )

        except ValueError as error:
            return False, str(error)

    # =========================================
    # READ - LEER
    # =========================================

    @classmethod
    def listar(cls):
        """Devuelve una lista de objetos."""

        return [
            cls.MODELO.desde_diccionario(registro)
            for registro in cls._registros()
        ]

    @classmethod
    def obtener(cls, id_registro):
        """Busca un registro por ID."""

        for objeto in cls.listar():

            if objeto.id == id_registro:
                return objeto

        return None

    # =========================================
    # SEARCH - BUSCAR
    # =========================================

    @classmethod
    def buscar(cls, termino):
        """Busca coincidencias en varios campos."""

        termino = str(
            termino
        ).strip().lower()

        if not termino:
            return []

        return [
            cls.MODELO.desde_diccionario(registro)
            for registro in cls._registros()

            if cls._coincide(
                registro,
                termino,
                cls.CAMPOS_BUSCABLES
            )
        ]

    # =========================================
    # UPDATE - ACTUALIZAR
    # =========================================

    @classmethod
    def actualizar(cls, id_registro, cambios):
        """Actualiza los datos de un registro."""

        try:

            desconocidos = (
                set(cambios)
                - set(cls.MODELO.CAMPOS)
            )

            if desconocidos:
                return (
                    False,
                    f"Campos no válidos: "
                    f"{', '.join(sorted(desconocidos))}"
                )

            if not cambios:
                return (
                    False,
                    "No se indicó ningún cambio"
                )

            objeto = cls.obtener(id_registro)

            if objeto is None:
                return (
                    False,
                    f"No existe un registro "
                    f"con id {id_registro}"
                )

            if "email" in cambios:

                nuevo_email = str(
                    cambios["email"]
                ).strip().lower()

                if nuevo_email in cls.emails_registrados(
                    excepto_id=id_registro
                ):

                    return (
                        False,
                        "Ese email ya lo usa otro registro"
                    )

            for campo, valor in cambios.items():

                setattr(
                    objeto,
                    campo,
                    valor
                )

            registros = cls._registros()

            for indice, registro in enumerate(registros):

                if registro["id"] == id_registro:

                    registros[indice] = (
                        objeto.a_diccionario()
                    )

                    break

            if not cls._gestor.guardar(registros):
                return (
                    False,
                    "No se pudo guardar la actualización"
                )

            return (
                True,
                f"Registro {id_registro} actualizado "
                f"({len(cambios)} campo/s)"
            )

        except ValueError as error:
            return False, str(error)

    # =========================================
    # DELETE - ELIMINAR
    # =========================================

    @classmethod
    def eliminar(cls, id_registro):
        """Elimina un registro por ID."""

        registros = cls._registros()

        quedan = [
            registro
            for registro in registros
            if registro["id"] != id_registro
        ]

        if len(quedan) == len(registros):
            return (
                False,
                f"No existe un registro "
                f"con id {id_registro}"
            )

        if not cls._gestor.guardar(quedan):
            return (
                False,
                "No se pudo guardar el archivo"
            )

        return (
            True,
            f"Registro {id_registro} eliminado"
        )

    # =========================================
    # ESTADÍSTICAS
    # =========================================

    @classmethod
    def estadisticas(cls):

        registros = cls._registros()

        ciudades = {
            registro.get("ciudad", "")
            for registro in registros
            if registro.get("ciudad")
        }

        dominios = {
            registro["email"].split("@")[1]
            for registro in registros
            if "@" in registro["email"]
        }

        sin_telefono = [
            registro["nombre"]
            for registro in registros
            if not registro.get("telefono")
        ]

        return {
            "total": len(registros),
            "ciudades": sorted(ciudades),
            "dominios": sorted(dominios),
            "sin_telefono": sin_telefono,
        }


# =========================================================
# CONTROLADOR DE ESTUDIANTES
# =========================================================

class EstudianteController(ClienteController):
    """
    Hereda las operaciones CRUD de ClienteController
    y agrega las operaciones propias de Estudiante.
    """

    MODELO = Estudiante

    ARCHIVO = "data/estudiantes.json"

    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "carnet"
    )

    _gestor = GestorJSON(ARCHIVO)

    # =========================================
    # CARNETS
    # =========================================

    @classmethod
    def carnets_registrados(cls, excepto_id=None):
        """Devuelve un SET con todos los carnets registrados."""

        return {
            registro["carnet"].upper()
            for registro in cls._registros()
            if registro["id"] != excepto_id
        }

    # =========================================
    # CREAR ESTUDIANTE
    # =========================================

    @classmethod
    def crear(cls, datos):

        carnet = str(
            datos.get("carnet", "")
        ).strip().upper()

        if carnet in cls.carnets_registrados():

            return (
                False,
                "Ese carnet ya está registrado"
            )

        return super().crear(datos)

    # =========================================
    # ACTUALIZAR ESTUDIANTE
    # =========================================

    @classmethod
    def actualizar(cls, id_registro, cambios):

        if "carnet" in cambios:

            nuevo_carnet = str(
                cambios["carnet"]
            ).strip().upper()

            if nuevo_carnet in cls.carnets_registrados(
                excepto_id=id_registro
            ):

                return (
                    False,
                    "Ese carnet ya lo usa otro estudiante"
                )

        return super().actualizar(
            id_registro,
            cambios
        )

    # =========================================
    # AGREGAR NOTA
    # =========================================

    @classmethod
    def agregar_nota(
        cls,
        id_estudiante,
        materia,
        nota
    ):

        estudiante = cls.obtener(
            id_estudiante
        )

        if estudiante is None:

            return (
                False,
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

        try:

            estudiante.agregar_nota(
                materia,
                nota
            )

            registros = cls._registros()

            for indice, registro in enumerate(registros):

                if registro["id"] == id_estudiante:

                    registros[indice] = (
                        estudiante.a_diccionario()
                    )

                    break

            if not cls._gestor.guardar(registros):

                return (
                    False,
                    "No se pudo guardar la nota"
                )

            return (
                True,
                f"Nota {nota} agregada en "
                f"{materia}"
            )

        except ValueError as error:

            return (
                False,
                str(error)
            )

    # =========================================
    # MATERIAS OFERTADAS
    # =========================================

    @classmethod
    def materias_ofertadas(cls):
        """Devuelve todas las materias sin repetir."""

        materias = set()

        for estudiante in cls.listar():

            materias.update(
                estudiante.materias
            )

        return materias

    # =========================================
    # MATERIAS EN COMÚN
    # =========================================

    @classmethod
    def materias_en_comun(
        cls,
        id_a,
        id_b
    ):

        estudiante_a = cls.obtener(id_a)
        estudiante_b = cls.obtener(id_b)

        if estudiante_a is None:
            return None

        if estudiante_b is None:
            return None

        return estudiante_a.materias_en_comun(
            estudiante_b
        )

    # =========================================
    # ESTADÍSTICAS PARA ESTUDIANTES
    # =========================================

    @classmethod
    def estadisticas(cls):

        estudiantes = cls.listar()

        aprobados = [
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Aprobado"
        ]

        reprobados = [
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Reprobado"
        ]

        return {
            "total": len(estudiantes),
            "aprobados": len(aprobados),
            "reprobados": len(reprobados),
            "materias": sorted(
                cls.materias_ofertadas()
            ),
        }