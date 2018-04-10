from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()

DB_CONNECT_STRING = 'mysql+mysqldb://root:123456@localhost/'


class MySqlSaver(object):
    def __init__(self, db_name):
        print('init MySqlSaver')
        engine = create_engine(DB_CONNECT_STRING + db_name, echo=True)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def save(self, data_object):
        try:
            self.session.add(data_object)
        except:
            self.session.rollback()
            raise
        # finally:
        #     self.session.close()

    def commit(self):
        try:
            print('commit')
            self.session.commit()
            self.session.close()
        except IntegrityError as e:
            logging.debug('save body error ')
            logging.debug(e.args)
            if str(e.args).find('Duplicate entry') == -1:
                raise
            else:
                return

    def query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

    def update(self, entity):
        self.session.query(entity).update()
