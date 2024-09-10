from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, declared_attr

from constants import BASE_DIR, DATE_TIME, RESULTS


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class PepParse(Base):
    number = Column(Integer())
    name = Column(String(200))
    status = Column(String(200))


class PepParsePipeline:

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)
        self.status_counts = {}
        self.total = 0

    def process_item(self, item, spider):
        self.status_counts[item['status']] = self.status_counts.get(
            item['status'], 0) + 1
        self.total += 1
        pep = PepParse(
            number=item['number'],
            name=item['name'],
            status=item['status']
        )
        self.session.add(pep)
        self.session.commit()
        return item

    def close_spider(self, spider):
        result_dir = BASE_DIR / RESULTS
        result_dir.mkdir(exist_ok=True)
        filename = result_dir / f'status_summary_{DATE_TIME}.csv'

        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status, count in self.status_counts.items():
                f.write(f'{status},{count}\n')
            f.write(f'Total,{self.total}')

        self.session.close()
