from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.db import Base

class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    category = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, unique=True, nullable=False)
    one_time_token = Column(String, nullable=True)
    token_expires = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="user")
    basket = relationship("Basket", back_populates="user")

class Basket(Base):
    __tablename__ = "baskets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    user = relationship("User", back_populates="basket")
    items = relationship("BasketItem", back_populates="basket", cascade="all, delete-orphan")

class BasketItem(Base):
    __tablename__ = "basket_items"
    id = Column(Integer, primary_key=True)
    basket_id = Column(Integer, ForeignKey("baskets.id"))
    dish_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)

    basket = relationship("Basket", back_populates="items")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dishes = Column(String, nullable=False)

    user = relationship("User", back_populates="orders")
