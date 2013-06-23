from sqlalchemy import (
    Column,
    Boolean,
    DateTime,
    Integer,
    Text,
    String,
    ForeignKey,
    DateTime,
)

# You will need to point this to wherever your declarative base is
from ...models import Base

class UltimateOXProfile(Base):
    __tablename__      = 'ultimate_ox_profiles'
    user               = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, primary_key=True)
    
    preferred_colour  = Column(Boolean, default=False)

class UltimateOXGame(Base):
    __tablename__ = 'ultimate_ox_games'
    id            = Column(Integer, primary_key=True)
    turn          = Column(Integer)
    
    started       = Column(DateTime, nullable=False)
    
    player1       = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    player2       = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    winner        = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    overall_state = Column(String, nullable=False)
    current_state = Column(String, nullable=False)
    active_board = Column(Integer, nullable=False)
    
    rematch = Column(Integer, ForeignKey("ultimate_ox_games.id"))
    source  = Column(Integer, ForeignKey("ultimate_ox_games.id"))

class UltimateOXMove(Base):
    __tablename__ = 'ultimate_ox_moves'
    id            = Column(Integer, primary_key=True)
    
    game          = Column(Integer, ForeignKey("ultimate_ox_games.id"), nullable=False)
    player        = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    move          = Column(Integer, nullable=False)
    timestamp     = Column(DateTime, nullable=False)
