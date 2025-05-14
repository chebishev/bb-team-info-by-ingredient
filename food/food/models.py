from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    food_group = Column(String)
    url = Column(String, unique=True, nullable=False)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    nutrients = relationship("FoodNutrientValue", back_populates="food")


class Nutrient(Base):
    __tablename__ = "nutrients"
    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    name_bg = Column(String)

    foods = relationship("FoodNutrientValue", back_populates="nutrient")


class FoodNutrientValue(Base):
    __tablename__ = "food_nutrient_values"
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    nutrient_id = Column(Integer, ForeignKey("nutrients.id"))
    quantity = Column(Float)
    unit = Column(String)

    __table_args__ = (
        UniqueConstraint("food_id", "nutrient_id", name="uix_food_nutrient"),
    )

    food = relationship("Food", back_populates="nutrients")
    nutrient = relationship("Nutrient", back_populates="foods")
