from Base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, Float, ForeignKey

# TODO: Add default for current timestamp in ts field.  Should be set client-side, but just in case


class Measurement(Base):
	__tablename__ = 'measurement'

	id = Column(Integer, primary_key=True, nullable=False)
	ts = Column(TIMESTAMP, nullable=False)
	mtype = Column(Integer, ForeignKey("measurement_type.id"), nullable=False)
	data = Column(Float, nullable=False)

	def __repr__(self):
		return "<Measurement(id={}, ts={}, mtype='{}', data={})>".format(self.id, self.ts, self.mtype, self.data)

	def __init__(self, ts, mtype, data, id=None):
		self.id = id
		self.ts = ts
		self.mtype = mtype
		self.data = data
