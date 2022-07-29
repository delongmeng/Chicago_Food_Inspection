# coding: utf-8
from sqlalchemy import Column, ForeignKey, String, Float, Integer, Date, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Facility(Base):
    __tablename__ = 'facility'
    id = Column(String(20), primary_key=True, nullable=False)
    name_dba = Column(String(100))
    name_aka = Column(String(100))
    license_id = Column(String(20))
    facility_type = Column(String(20))
    address = Column(ForeignKey('address.street'))
    zip = Column(ForeignKey('address.zip'))

    facility__facility_risk = relationship('Facility_Risk', back_populates='facility_risk__facility')
    facility__facility_inspection = relationship('Facility_Inspection', back_populates='facility_inspection__facility')
    facility__address_street = relationship('Address', foreign_keys=[address], back_populates='address__facility_street')
    facility__address_zip = relationship('Address', foreign_keys=[zip], back_populates='address__facility_zip')
    #__mapper_args__ = {'polymorphic_identity': 'facility', 'inherit_condition': address == Address.street}


class Address(Base):
    __tablename__ = 'address'
    street = Column(String(100), primary_key=True, nullable=False)
    zip = Column(String(20), primary_key=True, nullable=False)
    city = Column(String(20))
    state = Column(String(20))
    latitude = Column(Integer)
    longitude = Column(Integer)

    address__facility_street = relationship('Facility', foreign_keys=[Facility.address], back_populates='facility__address_street')
    address__facility_zip = relationship('Facility', foreign_keys=[Facility.zip], back_populates='facility__address_zip')


class Risk(Base):
    __tablename__ = 'risk'
    code = Column(String(20), primary_key=True, nullable=False)
    level = Column(String(20), nullable=False)

    risk__facility_risk = relationship('Facility_Risk', back_populates='facility_risk__risk')


class Facility_Risk(Base):
    __tablename__ = 'facility_risk'
    facility_id = Column(ForeignKey('facility.id'), primary_key=True, nullable=False)
    risk_code = Column(ForeignKey('risk.code'), nullable=False)

    facility_risk__facility = relationship('Facility', back_populates='facility__facility_risk')
    facility_risk__risk = relationship('Risk', back_populates='risk__facility_risk')


class Inspection(Base):
    __tablename__ = 'inspection'
    id = Column(String(20), primary_key=True)
    date = Column(Date, nullable=False)
    type = Column(String(20), nullable=False)
    result = Column(String(20), nullable=False)

    inspection__facility_inspection = relationship('Facility_Inspection', back_populates='facility_inspection__inspection')
    inspection__inspection_violation = relationship('Inspection_Violation', back_populates='inspection_violation__inspection')


class Facility_Inspection(Base):
    __tablename__ = 'facility_inspection'
    facility_id = Column(ForeignKey('facility.id'), primary_key=True, nullable=False)
    inspection_id = Column(ForeignKey('inspection.id'), primary_key=True, nullable=False)

    facility_inspection__facility = relationship('Facility', back_populates='facility__facility_inspection')
    facility_inspection__inspection = relationship('Inspection', back_populates='inspection__facility_inspection')


class Violation(Base):
    __tablename__ = 'violation'
    code = Column(String(20), primary_key=True, nullable=False)
    description = Column(String(100), nullable=False)

    violation__inspection_violation = relationship('Inspection_Violation', back_populates='inspection_violation__violation')


class Inspection_Violation(Base):
    __tablename__ = 'inspection_violation'
    inspection_id = Column(ForeignKey('inspection.id'), primary_key=True, nullable=False)
    violation_code = Column(ForeignKey('violation.code'), primary_key=True, nullable=False)
    violation_comment = Column(String(1000), primary_key=True, nullable=False)

    inspection_violation__inspection = relationship('Inspection', back_populates='inspection__inspection_violation')
    inspection_violation__violation = relationship('Violation', back_populates='violation__inspection_violation')
