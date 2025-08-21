from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

mysql_port = 3306
mysql_user = 'root'
mysql_password = 'password'
mysql_host = '10.106.154.84'
mysql_database = 'learning_italian'

# Database URL format: 'mysql+mysqlconnector://username:password@localhost:3306/yourdatabase'
DATABASE_URL = f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'

# Create a database engine to interact with MySQL
engine = create_engine(DATABASE_URL)

#Create Base
Base = declarative_base()

# Create a session factory to handle database operations
Session = sessionmaker(bind=engine)

def init_db():
    """Creates tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
