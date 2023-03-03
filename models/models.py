from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, INTEGER, String, TIMESTAMP, BIGINT, BOOLEAN, TEXT, Boolean, text, ForeignKey

Base = declarative_base()


class Tag(Base):
    __tablename__ = "tag"
    id = Column(INTEGER, primary_key=True)
    name = (Column(String(255), nullable=True))
    is_show = Column(Boolean, default=False)


class Category(Base):
    __tablename__ = "category"
    id = Column(INTEGER, primary_key=True)
    name = (Column(String(255), nullable=True))
    image_url = (Column(String(255), nullable=True))


class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(INTEGER, primary_key=True)
    category_id = Column(INTEGER, nullable=True)
    name = Column(String(255), nullable=True)
    description = Column(String(255))


class Definition(Base):
    __tablename__ = "definition"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=True)
    knowledge_id = Column(INTEGER, nullable=True)
    content = Column(TEXT())
    description = Column(String(255))


class Feature(Base):
    __tablename__ = "feature"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=True)
    knowledge_id = Column(INTEGER, nullable=True)
    content = Column(TEXT())
    description = Column(String(255))


class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=True)
    knowledge_id = Column(INTEGER, nullable=True)
    content = Column(TEXT())
    description = Column(String(255))


class Methodology(Base):
    __tablename__ = "methodology"
    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=True)
    knowledge_id = Column(INTEGER, nullable=True)
    content = Column(TEXT())
    description = Column(String(255))


class Knowledge_Tag(Base):
    __tablename__ = "knowledge_tag"
    id = Column(INTEGER, primary_key=True)
    knowledge_id = Column(INTEGER, ForeignKey('knowledge.id'))
    tag_id = Column(INTEGER, ForeignKey('tag.id'))
    # knowledge = relationship("Knowledge", backref="knowledge_tag")
    # tag = relationship("Category", backref="knowledge_tag")
