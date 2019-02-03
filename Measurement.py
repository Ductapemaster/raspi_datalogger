from Base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, Float, ForeignKey, text


class Measurement(Base):
	__tablename__ = 'measurement'

	id = Column(Integer, primary_key=True, nullable=False)
	ts = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
	mtype = Column(Integer, ForeignKey("measurement_type.id"), nullable=False)
	data = Column(Float, nullable=False)

	def __repr__(self):
		return "<Measurement(id={}, ts={}, mtype='{}', data={})>".format(self.id, self.ts, self.mtype, self.data)

	def __init__(self, id, ts, mtype, data):
		self.id = id
		self.ts = ts
		self.mtype = mtype
		self.data = data
