from redis import StrictRedis

import config

redis = StrictRedis(
    unix_socket_path=config.REDIS_UNIX_SOCK,
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_AUTH,
    ssl=config.REDIS_SSL,
    ssl_certfile=config.REDIS_SSL_CERT,
    ssl_keyfile=config.REDIS_SSL_KEY,
    ssl_ca_certs=config.REDIS_SSL_CA_CERT,
    ssl_cert_reqs=config.REDIS_SSL_CERT_REQS,
    # decode_responses=True,
)
