
# todo example:
# from sqlalchemy import select
# ss = SessionLocal()
# configs = ss.execute(
#     select(
#         database
#     )
# ).scalars().all()
# configs = {config.name: config.value for config in configs}
# SERVICE = {
#     "template": {
#         "url": configs.get("SERVICE_TEMPLATE_URL"),
#         "server-auth": configs.get("SERVICE_TEMPLATE_SERVICE_AUTH")
#     },
#     "kafka": {
#         "sasl_mechanism": configs.get("KAFKA_SASL_MECHANISM"),
#         "bootstrap_servers": configs.get("KAFKA_BOOTSTRAP_SERVERS"),
#         "security_protocol": configs.get("KAFKA_SECURITY_PROTOCOL"),
#         "sasl_plain_username": configs.get("KAFKA_SASL_PLAIN_USERNAME"),
#         "sasl_plain_password": configs.get("KAFKA_SASL_PLAIN_PASSWORD"),
#         "producer_topic": configs.get("KAFKA_PRODUCER_TOPIC"),
#         "message_max_bytes": configs.get("KAFKA_MESSAGE_MAX_BYTES"),
#     },
#     "redis": {
#         "host": configs.get("REDIS_HOST"),
#         "port": configs.get("REDIS_PORT"),
#         "password": configs.get("REDIS_PASSWORD"),
#         "database": configs.get("REDIS_DATABASE"),
#     },
#     "production": {
#         "production_flag": bool(
#             configs.get("PRODUCTION") if configs.get("PRODUCTION") in ["True", "true", "1"] else False)
#     }
# }
