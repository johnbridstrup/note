import os
import pytz
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, ForeignKey, Index, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

from .utils import DB_PATH, INITIAL_NOTEBOOK


Base = declarative_base()
tags_note_table = Table(
    "tags_link",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)
tags_notebook_table = Table(
    "notebooks_link",
    Base.metadata,
    Column("notebook_id", Integer, ForeignKey("notebooks.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

class Notebook(Base):
    __tablename__ = "notebooks"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    default = Column(Boolean, default=False)
    tags = relationship('Tag', secondary=tags_notebook_table, back_populates='notebooks')

    def __repr__(self):
        return f"<Notebook: {self.name}>"
    
    @classmethod
    def create(cls, name, session, default=False):
        nb = cls(name=name, default=default)
        session.add(nb)
        session.commit()
        return nb

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    note = Column(String)
    notebook = Column(ForeignKey("notebooks.id"))
    tags = relationship('Tag', secondary=tags_note_table, back_populates='notes')
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        utc = pytz.utc
        aware_ts = utc.localize(self.timestamp) 
        return f"{aware_ts.astimezone(pytz.timezone('US/Pacific'))}: {self.note}"

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    notes = relationship('Note', secondary=tags_note_table, back_populates='tags')
    notebooks = relationship('Notebook', secondary=tags_notebook_table, back_populates='tags')

    def __repr__(self):
        return f"<Tag: {self.name}>"

Index("idx_note_timestamp", Note.timestamp)
Index("idx_note_notebook", Note.notebook)

if not os.path.exists(DB_PATH):
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Base.metadata.create_all(engine)
else:
    engine = create_engine(f"sqlite:///{DB_PATH}")

Session = sessionmaker(bind=engine)
session = Session()

notebooks = session.query(Notebook)
if len(notebooks.all()) == 0:
    Notebook.create(INITIAL_NOTEBOOK, session, default=True)
session.close()
