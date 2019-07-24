from flask import Flask, request, redirect, url_for, render_template

from dao.forms import ShipForm
from dao.shiphelper import ShipHelper

app = Flask(__name__)


@app.route('/edit_ship', methods=['GET',])
def edit_ship():
    form = ShipForm()

    if request.method == 'GET':
        ship_id = request.args.get('ship_id')
        print(ship_id)
        shiphelper = ShipHelper()

        ship = shiphelper.getShip(ship_id=ship_id)
        form.ship_id.data = ship.ship_id
        form.ship_number.data = ship.ship_number
        form.ship_date.data = ship.ship_date
        form.ship_name.data = ship.ship_name
        form.ship_address = ship.ship_address

        return render_template('ship_form.html', form=form, form_name="Edit ship", action="edit_ship")


@app.route('/save_ship', methods=['POST'])
def save_ship():
    form = ShipForm()
    if request.method == 'POST':
        ship_id = form.ship_id.data
        ship_number = form.ship_number.data
        ship_date = form.ship_date.data.strftime("%y-%m-%d")
        ship_name = form.ship_name.data
        ship_address = form.ship_address.data

        shiphelper = ShipHelper()
        shiphelper.updateShip(
            ship_id=ship_id,
            ship_number=ship_number,
            ship_date=ship_date,
            ship_name=ship_name,
            ship_address=ship_address,
        )

    return redirect(url_for('ship'))


if __name__ == '__main__':
    app.run()
