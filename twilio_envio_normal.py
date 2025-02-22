from components.twilio_component import TwilioManager
from components.database_mongodb_component import DataBaseMongoDBManager
from components.database_mysql_component import DataBaseMySQLManager
from components.openai_component import OpenAIManager
from helpers.helpers import extraer_json
from datetime import datetime, timedelta

twilio_manager = TwilioManager()
dbMongoManager = DataBaseMongoDBManager()
dbMySQLManager = DataBaseMySQLManager()
openai_manager = OpenAIManager()


response_message = ""
celular = '+51997506654'
cliente_id_mysql = 1837
cliente_mysql = dbMySQLManager.obtener_cliente(cliente_id_mysql)

conversation_actual = dbMongoManager.obtener_conversacion_actual(cliente_mysql["celular"])

response_message = openai_manager.consulta(cliente_mysql,conversation_actual, None,False,"")
response_message = extraer_json(response_message)
print("Response message json:", response_message)
response_message = response_message["mensaje"]
response_message = response_message.replace("Asesor: ", "").strip('"')
twilio_manager.send_message(celular, response_message)

# Guardar la respuesta en la conversación actual
print("Response message:", response_message)
dbMongoManager.guardar_respuesta_ultima_interaccion_chatbot(celular, response_message)
dbMySQLManager.actualizar_fecha_ultima_interaccion_bot(cliente_id_mysql, datetime.now())