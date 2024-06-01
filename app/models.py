from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Teams(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    players = relationship('Player', back_populates='team')
    coach_id = Column(Integer, ForeignKey('staff.id'))
    assistant_coach_id = Column(Integer, ForeignKey('staff.id'))
    manager_id = Column(Integer, ForeignKey('staff.id'))
    owner_id = Column(Integer, ForeignKey('staff.id'))


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    height = Column(Float)
    weight = Column(Float)
    years_pro = Column(Integer)
    birthdate = Column(Date)
    age = Column(Integer)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Teams', back_populates='players')


class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cellphone_number = Column(String)
    home_address = Column(String)
    years_in_team = Column(Integer)
    starting_date = Column(Date)
    position_id = Column(Integer, ForeignKey('organization_positions.id'))


class OrganizationPosition(Base):
    __tablename__ = "organization_positions"
    id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String)
