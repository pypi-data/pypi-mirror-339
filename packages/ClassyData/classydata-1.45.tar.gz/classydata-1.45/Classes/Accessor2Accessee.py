#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base

Accessor2Accessee = Table(
	'accessor2accessee',
	Base.metadata,
	Column('accessor_id', ForeignKey('accessor.id'), primary_key=True),
	Column('accessee_id', ForeignKey('access.id'), primary_key=True)
)
