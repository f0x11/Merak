#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import date
from sqlalchemy import Column, VARCHAR, Integer, Date, UniqueConstraint
from data.session_mysql import DeclarativeBase

__author__ = 'f0x11'


class HotWord(DeclarativeBase):
    __tablename__ = 'hot_word'

    number = Column(Integer, nullable=False)
    word = Column(VARCHAR(255), nullable=False)
    date = Column(Date, default=date.today, nullable=False)

    __table_args__ = (UniqueConstraint('number', 'date'),)

    def to_json(self):
        return {
            'number': str(self.number),
            'word': self.word,
            'date': self.date.strftime('%Y-%m-%d')
        }
