from components.database_postgre_component import DataBasePostgreSQLManager

#Prueba exitosa de postgresql usando el componente postgresql

# 🔌 Inicializa la conexión con PostgreSQL
db_manager = DataBasePostgreSQLManager()


if __name__ == "__main__":

     # Corroborar conexión
    if db_manager._connect():
        print("✅ La conexión a PostgreSQL está activa y funcionando.")
        
        # Datos de prueba para insertar un cliente
        documento_identidad = "12345678"
        tipo_documento = "DNI"
        nombre = "Carlos"
        apellido = "Pérez"
        celular = "+51987654321"
        email = "carlos.perez@gmail.com"
        estado = "nuevo"  # El estado es opcional y por defecto es "nuevo"

        # Llamada al método insertar_cliente
        resultado = db_manager.insertar_cliente(
            documento_identidad,
            tipo_documento,
            nombre,
            apellido,
            celular,
            email,
            estado
        )
        
        # Verifica si el cliente fue insertado correctamente
        if resultado:
            print("✅ El cliente fue insertado correctamente.")
        else:
            print("❌ Hubo un error al insertar el cliente.")
    else:
        print("❌ No se pudo establecer la conexión a PostgreSQL.")