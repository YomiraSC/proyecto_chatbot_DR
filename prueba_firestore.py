import os
from components.database_firestore_component import DataBaseFirestoreManager  # Asumiendo que tu clase está en firestore_manager.py

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./codigopagomaquisistema-firestore.json"
firestore_manager = DataBaseFirestoreManager()


def main():
    # # Crear instancia del manejador de Firestore
    
    
    # # Datos de prueba
    # celular = "+51993538942"
    # id_cliente = "1"
    # id_bot = "saasbot"  # 👈 importante este valor para que funcione como mencionaste
    # mensaje = "Hola, esto es un mensaje de prueba"
    # sender = "false"

    # # Crear documento en Firestore
    # firestore_manager.crear_documento(celular, id_cliente, id_bot, mensaje, sender)

    # # Recuperar mensajes de hoy
    # mensajes = firestore_manager.recuperar_mensajes_hoy(id_bot, celular)
    # print("📄 Mensajes recuperados:")
    # for msg in mensajes:
    #     print(msg)
    """
    Función HTTP que consulta los mensajes de hoy en Firestore usando recuperar_mensajes_hoy.
    """
    celular = "+51993538942"
    id_bot = "saasbot"

    try:
        #mensajes = firestore_manager.recuperar_mensajes_hoy(id_bot, celular)
        mensajes = firestore_manager.recuperar_mensajes_hoy(id_bot, celular)

        if not mensajes:
            response_text = f"📭 No se encontraron mensajes para {celular}."
        else:
            response_text = f"📨 Se encontraron {len(mensajes)} mensajes para {celular}:\n\n"
            for idx, msg in enumerate(mensajes, start=1):
                response_text += f"--- Mensaje {idx} ---\n"
                for key, value in msg.items():
                    response_text += f"{key}: {value}\n"
                response_text += "\n"

        print(response_text)

    except Exception as e:
        response_text = f"❌ Error al recuperar los mensajes: {e}"
        print(response_text)

    return response_text, 200

if __name__ == "__main__":
    main()
