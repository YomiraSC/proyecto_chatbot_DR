import sqlalchemy
from sqlalchemy.orm import sessionmaker

#componente cuya funcion connect está basada en el programa que funcionó en cloud run

class DataBasePostgreSQLManager:
    def __init__(self):
        """Inicializa la conexión a PostgreSQL usando SQLAlchemy con Unix Socket."""
        self.engine = self._connect()
        self.Session = sessionmaker(bind=self.engine)

    def _connect(self) -> sqlalchemy.engine.base.Engine:
        """Establece la conexión a PostgreSQL mediante socket Unix."""
        db_user = "maquisistema"
        db_pass = "sayainvestments1601"
        db_name = "bdMaqui"
        db_host = "34.82.84.15"  # Cambia esto a la IP o host de tu servidor PostgreSQL -> ESTO PORQUE LO MANEJO EN WINDOWS, SI FUERA EN GCP SERÍA CON EL SOCKET
        db_port = "5432"  # El puerto predeterminado de PostgreSQL es 5432

        #unix_socket_path = "/cloudsql/codigopagomaquisistema:us-west1:bdmaquisistema"

        try:
            engine = sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL.create(
                    drivername="postgresql+pg8000",
                    username=db_user,
                    password=db_pass,
                    database=db_name,
                    host=db_host,
                    port=db_port
                    #query={"unix_sock": f"{unix_socket_path}/.s.PGSQL.5432"},
                )
            )
            print("✅ Conexión a PostgreSQL establecida correctamente.")
            return engine
        except Exception as e:
            print(f"❌ Error al conectar a PostgreSQL: {e}")
            return None

    def _reconnect_if_needed(self):
        """Verifica si la conexión sigue activa y la restablece si es necesario."""
        try:
            with self.engine.connect() as connection:
                connection.execute(sqlalchemy.text("SELECT 1"))  # Prueba de conexión
        except Exception as e:
            print(f"⚠ Conexión perdida, intentando reconectar... {e}")
            self.engine = self._connect()
            self.Session = sessionmaker(bind=self.engine)  # Reasigna la sesión

    def obtener_datos_cliente(self, cliente_id):
        """
        Obtiene los datos de un cliente por su ID.
        """
        self._reconnect_if_needed()  # 🔄 Verifica y restablece la conexión antes de consultar

        if not self.engine:
            print("❌ No hay conexión activa a PostgreSQL.")
            return None

        try:
            with self.engine.connect() as connection:
                # Asegurar que se usa el esquema correcto
                connection.execute(sqlalchemy.text("SET search_path TO saas"))

                query = sqlalchemy.text("""
                    SELECT * FROM clientes WHERE cliente_id = :cliente_id
                """)
                result = connection.execute(query, {"cliente_id": cliente_id}).fetchone()
                print(f"🔍 Resultado SQL: {result}") #verificar qué bota result
                if result:
                    #column_names = result.keys()  # Obtiene los nombres de columna
                    column_names = result._fields  # Esto devuelve los nombres exactos de las columnas en PostgreSQL
                    cliente = dict(zip(column_names, result))  # Convierte en diccionario
                    return cliente
                else:
                    return None
        except Exception as e:
            print(f"❌ Error al obtener datos del cliente: {e}")
            return None


    def existe_cliente_por_dni(self, dni):
        """
        Verifica si un cliente con el DNI dado existe en la base de datos.
        Retorna True si el cliente existe, False si no existe.
        """
        self._reconnect_if_needed()

        if not self.engine:
            print("❌ No hay conexión activa a PostgreSQL.")
            return None

        try:
            with self.engine.connect() as connection:
                connection.execute(sqlalchemy.text("SET search_path TO saas"))

                query = sqlalchemy.text("""
                    SELECT COUNT(*) FROM clientes WHERE documento_identidad = :dni
                """)
                result = connection.execute(query, {"dni": dni}).scalar()

                return result > 0  # Retorna True si el cliente existe, False si no
        except Exception as e:
            print(f"❌ Error al verificar existencia del cliente: {e}")
            return None

    def insertar_cliente(self, documento_identidad, tipo_documento, nombre, apellido, celular, email, estado="nuevo"):
        """
        Inserta un nuevo cliente en la base de datos si no existe previamente.
        Retorna True si se insertó correctamente, False si ya existía o hubo un error.
        """
        self._reconnect_if_needed()

        if not self.engine:
            print("❌ No hay conexión activa a PostgreSQL.")
            return None

        # Verificar si el cliente ya existe
        if self.existe_cliente_por_dni(documento_identidad):
            print(f"⚠ El cliente con DNI {documento_identidad} ya existe en la base de datos.")
            return False

        try:
            with self.engine.begin() as connection:
                connection.execute(sqlalchemy.text("SET search_path TO saas"))

                insert_query = sqlalchemy.text("""
                    INSERT INTO clientes (
                        documento_identidad, tipo_documento, nombre, apellido, celular, email, estado
                    ) VALUES (
                        :documento_identidad, :tipo_documento, :nombre, :apellido, :celular, :email, :estado
                    )
                """)

                connection.execute(insert_query, {
                    "documento_identidad": documento_identidad,
                    "tipo_documento": tipo_documento,
                    "nombre": nombre,
                    "apellido": apellido,
                    "celular": celular,
                    "email": email,
                    "estado": estado
                })

                print(f"✅ Cliente con DNI {documento_identidad} insertado correctamente.")
                return True
        except Exception as e:
            print(f"❌ Error al insertar cliente: {e}")
            return False



    def obtener_id_cliente_por_dni(self, dni):
        """
        Obtiene el 'cliente_id' de la tabla cliente mediante el DNI proporcionado.
        Retorna el cliente_id si se encuentra, de lo contrario retorna None.
        """
        self._reconnect_if_needed()

        if not self.engine:
            print("❌ No hay conexión activa a PostgreSQL.")
            return None

        try:
            with self.engine.connect() as connection:
                connection.execute(sqlalchemy.text("SET search_path TO saas"))

                query = sqlalchemy.text("""
                    SELECT cliente_id FROM clientes WHERE documento_identidad = :dni
                """)
                result = connection.execute(query, {"dni": dni}).fetchone()

                if result:
                    return result[0]  # Devuelve el cliente_id encontrado
                else:
                    return None  # Si no se encontró el cliente, retorna None
        except Exception as e:
            print(f"❌ Error al obtener cliente_id por DNI: {e}")
            return None


    def cliente_existe(self, cliente_id):
        """
        Verifica si un cliente con el cliente_id proporcionado existe en la tabla cliente.
        Retorna True si el cliente existe, False si no.
        """
        self._reconnect_if_needed()

        if not self.engine:
            print("❌ No hay conexión activa a PostgreSQL.")
            return False

        try:
            with self.engine.connect() as connection:
                connection.execute(sqlalchemy.text("SET search_path TO saas"))

                query = sqlalchemy.text("""
                    SELECT 1 FROM clientes WHERE cliente_id = :cliente_id
                """)
                result = connection.execute(query, {"cliente_id": cliente_id}).fetchone()

                return result is not None  # Retorna True si el cliente existe, False si no
        except Exception as e:
            print(f"❌ Error al verificar existencia de cliente: {e}")
            return False



    # def insertar_codigoPago(self, cliente_id, codigo, tipo_codigo, fecha_asignacion, id_contrato):
    #     """
    #     Inserta un nuevo código de pago en la tabla codigo_pago, asegurando que el cliente exista.
    #     """
    #     self._reconnect_if_needed()

    #     if not self.engine:
    #         print("❌ No hay conexión activa a PostgreSQL.")
    #         return False

    #     # 🔍 Verificar si el cliente existe antes de la inserción
    #     if not self.cliente_existe(cliente_id):
    #         print(f"⚠ No se puede insertar codigoPago: Cliente con ID {cliente_id} no existe.")
    #         return False

    #     try:
    #         with self.engine.connect() as connection:
    #             connection.execute(sqlalchemy.text("SET search_path TO saas"))

    #             query = sqlalchemy.text("""
    #                 INSERT INTO codigo_pago (cliente_id, codigo, tipo_codigo, fecha_asignacion, id_contrato)
    #                 VALUES (:cliente_id, :codigo, :tipo_codigo, :fecha_asignacion, :id_contrato)
    #             """)

    #             connection.execute(query, {
    #                 "cliente_id": cliente_id,
    #                 "codigo": codigo,
    #                 "tipo_codigo": tipo_codigo,
    #                 "fecha_asignacion": fecha_asignacion,
    #                 "id_contrato": id_contrato
    #             })

    #             print(f"✅ Código de pago insertado correctamente para Cliente ID {cliente_id}.")
    #             return True

    #     except Exception as e:
    #         print(f"❌ Error al insertar código de pago: {e}")
    #         return False
