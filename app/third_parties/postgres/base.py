from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings.database import POSTGRES_CONFIG

DATABASE_URL = "oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}".format_map({
    'host': POSTGRES_CONFIG['host'],
    'port': POSTGRES_CONFIG['port'],
    'username': POSTGRES_CONFIG['username'],
    'password': POSTGRES_CONFIG['password'],
    'service_name': POSTGRES_CONFIG['service_name']
})

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData(schema=POSTGRES_CONFIG['service_name'])
Base = declarative_base(metadata=metadata)
