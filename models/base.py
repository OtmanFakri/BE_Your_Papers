from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from configs import Base

class User(Base):
    __tablename__ = 'User'

    User_ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)


class Category(Base):
    __tablename__ = 'Category'

    Category_ID = Column(Integer, primary_key=True, autoincrement=True)
    Category_Name = Column(String(100), nullable=False)
    Description = Column(Text)


class Document(Base):
    __tablename__ = 'Document'

    Document_ID = Column(Integer, primary_key=True, autoincrement=True)
    Category_ID = Column(Integer, ForeignKey('Category.Category_ID', ondelete='CASCADE'), nullable=False)
    Title = Column(String(100), nullable=False)
    Description = Column(Text)
    Default_Content = Column(Text, nullable=False)


class Modified_Document(Base):
    __tablename__ = 'Modified_Document'

    Modification_ID = Column(Integer, primary_key=True, autoincrement=True)
    User_ID = Column(Integer, ForeignKey('User.User_ID', ondelete='CASCADE'), nullable=False)
    Document_ID = Column(Integer, ForeignKey('Document.Document_ID', ondelete='CASCADE'), nullable=False)
    Modified_Content = Column(Text, nullable=False)
    Modification_Date = Column(DateTime(timezone=True), server_default=func.now())
    Payment_Status = Column(Boolean, default=False)


class Payment(Base):
    __tablename__ = 'Payment'

    Payment_ID = Column(Integer, primary_key=True, autoincrement=True)
    Modification_ID = Column(Integer, ForeignKey('Modified_Document.Modification_ID', ondelete='CASCADE'),
                             nullable=False)
    Amount = Column(Numeric(10, 2), nullable=False)
    Payment_Date = Column(DateTime(timezone=True), server_default=func.now())
    Payment_Method = Column(String(50))