"""
NAME:          views\controllers.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          18/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Views module. Renders HTML pages and passes in associated data to render on the
               dashboard.
"""

from flask import Blueprint, render_template, request, jsonify
from app.database.controllers import Database

views = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# get the database class
db_mod = Database()


# Set the route and accepted methods
@views.route('/home/', methods=['GET', 'POST'])
def home():
    """Render the home page of the dashboard passing in data to populate dashboard."""
    pcts = [r[0] for r in db_mod.get_distinct_pcts()]

    form = request.form
    if request.method == 'POST' and 'search' in form:
        search = db_mod.search_by_name_or_bnf_score(str(form['search']))
    else:
        search = db_mod.search_by_name_or_bnf_score('0101021B0AAAPAP')

    if request.method == 'POST' and 'pct-option' in form:
        pct_option = str(form['pct-option'])
        selected_pct_data = db_mod.get_n_data_for_PCT(pct_option, 5)
        bar_graph1_data = {
            "data": db_mod.total_number_on_PCT(pct_option),
            "labels": db_mod.get_distinct_GP_on_PCT(pct_option)
        }
    else:
        selected_pct_data = db_mod.get_n_data_for_PCT(str(pcts[0]), 5)
        bar_graph1_data = {
            "data": db_mod.total_number_on_PCT('01C'),
            "labels": db_mod.get_distinct_GP_on_PCT('01C')
        }

    # prepare data
    bar_data = generate_barchart_data()
    bar_values = bar_data[0]
    bar_labels = bar_data[1]
    title_data_items = generate_data_for_tiles()

    # render the HTML page passing in relevant data
    return render_template(
        'dashboard/index.html',
        tile_data=title_data_items,
        pct={
            'data': bar_values,
            'labels': bar_labels
        },
        bar_graph1=bar_graph1_data,
        pct_list=pcts,
        pct_data=selected_pct_data,
        avg_act=generate_avg_ACT(),
        search=search,
        max_quantity_in_total=round(
            generate_max_quantity_prescribing() / title_data_items[0] * 100,
            2),
        unique_item=generate_count_prescrib(),
        percentage=generate_percentages(),
    )


def generate_data_for_tiles():
    """Generate the data for the four home page titles."""
    return [db_mod.get_total_number_items()]


def generate_barchart_data():
    """Generate the data needed to populate the barchart."""
    data_values = db_mod.get_prescribed_items_per_pct()
    pct_codes = db_mod.get_distinct_pcts()

    # convert into lists and return
    data_values = [r[0] for r in data_values]
    pct_codes = [r[0] for r in pct_codes]
    return [data_values, pct_codes]


def generate_avg_ACT():
    return round(db_mod.get_avg_ACT(), 2)


def generate_max_quantity_prescribing():
    return db_mod.get_max_quantity_prescribing()


def generate_count_prescrib():
    return db_mod.get_count_prescrib()


def generate_percentages():
    return db_mod.get_treatment_percentage()


@views.route('/home/calculate_creatinine_clearance', methods=['GET'])
def ccc():
    """Calculate creatinine clearance"""

    sex = request.args.get('sex')
    age = float(request.args.get('age'))
    weight = float(request.args.get('weight'))
    serum = float(request.args.get('serum'))

    if sex == 'm':
        ret = str(((140 - age) * weight) / (serum * 72 / 88.40))
        return ret
    elif sex == 'f':
        ret = str(((140 - age) * weight) / (serum * 72 * 88.40) * 0.85)
        return ret
    else:
        return 'undefined'
