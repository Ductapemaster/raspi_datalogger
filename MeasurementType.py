from Base import Base
from sqlalchemy import Column, Integer, String


class MeasurementType(Base):
	__tablename__ = 'measurement_type'

	id = Column(Integer, primary_key=True, nullable=False)
	mtype = Column(String(32), nullable=False)
	units = Column(String(16), nullable=False)

	def __repr__(self):
		return "<MeasurementType(id={}, mtype='{}', units='{}')>".format(self.id, self.mtype, self.units)

	def __init__(self, id, mtype, units):
		self.id = id
		self.mtype = mtype
		self.units = units
