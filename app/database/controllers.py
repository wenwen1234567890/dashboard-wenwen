"""
NAME:          database\controllers.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          17/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Contains the Database class that contains all the methods used for accessing the database
"""

from sqlalchemy.sql import func, or_
from flask import Blueprint

from app import db
from app.database.models import PrescribingData, PracticeData

database = Blueprint('dbutils', __name__, url_prefix='/dbutils')


class Database:
    """Class for managing database queries."""
    def get_total_number_items(self):
        """Return the total number of prescribed items."""
        return int(
            db.session.query(
                func.sum(
                    PrescribingData.items).label('total_items')).first()[0])

    def get_prescribed_items_per_pct(self):
        """Return the total items per PCT."""
        return db.session.query(
            func.sum(PrescribingData.items).label('item_sum')).group_by(
                PrescribingData.PCT).all()

    def get_distinct_pcts(self):
        """Return the distinct PCT codes."""
        return db.session.query(PrescribingData.PCT).distinct().all()

    def get_n_data_for_PCT(self, pct, n):
        """Return all the data for a given PCT."""
        return db.session.query(PrescribingData).filter(
            PrescribingData.PCT == pct).limit(n).all()

    def get_avg_ACT(self):
        return db.session.query(func.avg(PrescribingData.ACT_cost)).scalar()

    def get_max_quantity_prescribing(self):
        return db.session.query(func.max(PrescribingData.quantity)).scalar()

    def get_count_prescrib(self):
        return db.session.query(func.count(PrescribingData.id)).scalar()

    def get_treatment_total(self):
        """Return the total items of treatment durg"""
        return db.session.query(func.sum(PrescribingData.items)).filter(
            PrescribingData.BNF_code.like("05%")).first()[0]

    def get_treatment_percentage(self):
        code = db.session.query(func.substr(PrescribingData.BNF_code,1,4)\
            .label('Code'),PrescribingData.id).subquery()
        r = db.session.query(func.sum(PrescribingData.items))\
            .outerjoin(code,PrescribingData.id==code.c.id)\
            .filter(PrescribingData.BNF_code.like("05%"))\
            .group_by(code.c.Code)

        treatment_total = int(self.get_treatment_total())
        ret = []
        for i in range(5):
            ret.append(round(int(r[i][0]) / treatment_total * 100, 2))
        return ret

    def search_by_name_or_bnf_score(self, search, n=10):
        return db.session.query(PrescribingData).group_by(
            PrescribingData.BNF_code).filter(
                or_(PrescribingData.BNF_name.like(search + '%'),
                    PrescribingData.BNF_code.like(search +
                                                  '%'))).limit(n).all()

    def total_number_on_PCT(self, pct):
        return db.session.query(func.sum(PrescribingData.items)).filter(
            PrescribingData.BNF_code.like("0501%")).filter(
                PrescribingData.PCT == pct).group_by(
                    PrescribingData.practice).all()

    def get_distinct_GP_on_PCT(self, pct):
        return db.session.query(PrescribingData.practice).filter(
            PrescribingData.BNF_code.like("0501%")).filter(
                PrescribingData.PCT == pct).distinct().all()
