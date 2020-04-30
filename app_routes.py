
from flask import current_app as app
from flask import (
    request, flash, url_for, redirect, g, render_template)

from db_pg import get_db
from ship import Ship


@app.route('/')
def show_all():
    app.logger.info(f'app logger {request}')
    return render_template('ships.html', ships=get_db().get_ships())


@app.route('/new', methods=['GET', 'POST'])
def new():
    app.logger.info(request)
    if request.method == 'POST':
        if (not request.form['name'] or
                not request.form['country'] or
                not request.form['ship_description']):
            flash('Please enter all the fields', 'error')
        else:
            ship = Ship(
                request.form['name'], request.form['country'],
                request.form['ship_description'], request.form['built_year']
            )

            get_db().upsert_ship(ship)
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/edit')
def edit():
    """
    Two methods - get and post
    Receive ship name as get parameter and fill form like new
    Post method - reads form data and updates value in db
    :return:
    """
    # TODO: implement edit ship
    return 'Edit action'


@app.route('/delete')
def delete():
    """
    Receive ship name as get parameter and remove it from db
    :return:
    """
    # TODO: implement delete ship
    return 'Delete action'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
