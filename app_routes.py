
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
                None, request.form['name'], request.form['country'],
                request.form['ship_description'], request.form['built_year']
            )

            message = get_db().insert_ship(ship)
            flash(message)
            return redirect(url_for('show_all'))
    countries = get_db().get_countries()
    return render_template('new.html', countries=countries)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    ship = None
    if request.method == 'POST':
        if (not request.form['name'] or
                not request.form['country'] or
                not request.form['ship_description']):
            flash('Please enter all the fields', 'error')
        else:
            ship = Ship(
                request.form['ship_id'], request.form['name'], request.form['country'],
                request.form['ship_description'], request.form['built_year']
            )
            message = get_db().update_ship(ship)
            flash(message)
            return redirect(url_for('show_all'))
    else:
        ship_name = request.args.get('name')
        if ship_name:
            ship = get_db().get_ship_by_name(ship_name)
    countries = get_db().get_countries()
    return render_template('edit.html', ship=ship, countries=countries)


@app.route('/delete', methods=["GET"])
def delete():
    """
    Receive ship name as get parameter and remove it from db
    :return:
    """
    ship_name = request.args.get('name')
    get_db().del_ship(ship_name)

    return redirect(url_for('show_all'))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
