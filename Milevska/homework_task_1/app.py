
from flask import Flask, render_template, request, redirect, url_for
from forms.search_form import SearchForm
from dao.orm.model import *
from dao.db import OracleDb
from forms.owner_form import OwnerForm
from sqlalchemy.sql import func

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import json

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/car', methods=['GET'])
def car():

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormCar).all()

    return render_template('car.html', cars=result)


@app.route('/ownercar', methods=['GET'])
def ownercar():

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormOwner).join(ormCarOwner).join(ormCar).all()

    return render_template('ownercar.html', owners=result)


@app.route('/search', methods=['GET', 'POST'])
def search():

    search_form = SearchForm()

    if request.method=='GET':
        return render_template('search.html', form=search_form, result=None)
    else:
        return render_template('search.html', form=search_form, result=search_form.get_result())


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    db = OracleDb()

    query1 = (db.sqlalchemy_session.query(ormOwner.owner_phone,
                                          func.count(ormCarOwner.owner_phone
                                                     ).label('car_count')
                                          ).outerjoin(ormCarOwner).group_by(
        ormOwner.owner_phone, ormOwner.owner_birthday)).all()

    query2 = (db.sqlalchemy_session.query(ormCar.car_number,
                                          func.count(ormCarOwner.owner_phone
                                                     ).label('owner_count')
                                          ).outerjoin(ormCarOwner).group_by(
        ormCar.car_number)).all()

    owners, car_counts = zip(*query1)
    bar = go.Bar(
        x=owners,
        y=car_counts
    )

    cars, owner_count = zip(*query2)
    pie = go.Pie(
        labels=cars,
        values=owner_count
    )

    data = {"bar":[bar], "pie":[pie]}
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)


@app.route('/new_owner', methods=['GET','POST'])
def new_owner():

    form = OwnerForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('owner_form.html', form=form, form_name="New owner", action="new_owner")
        else:
            new_owner = ormOwner(
                                owner_phone=form.owner_phone.data,
                                owner_birthday=form.owner_birthday.data.strftime("%d-%b-%y"),
                            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_owner)
            db.sqlalchemy_session.commit()

            return redirect(url_for('owner'))

    return render_template('owner_form.html', form=form, form_name="New owner", action="new_owner")


@app.route('/edit_owner', methods=['GET','POST'])
def edit_owner():

    form = OwnerForm()

    if request.method == 'GET':

        owner_phone = request.args.get('owner_phone')
        db = OracleDb()
        owner = db.sqlalchemy_session.query(ormOwner).filter(ormOwner.owner_phone == owner_phone).one()

        form.owner_phone.data = owner.owner_phone
        form.owner_birthday.data = owner.owner_birthday

        return render_template('owner_form.html', form=form, form_name="Edit owner", action="edit_owner")

    else:
        if form.validate() == False:
            return render_template('owner_form.html', form=form, form_name="Edit owner", action="edit_owner")
        else:
            db = OracleDb()
            owner = db.sqlalchemy_session.query(ormOwner).filter(ormOwner.owner_phone == form.owner_phone.data).one()

            owner.owner_phone = form.owner_phone.data
            owner.owner_birthday = form.owner_birthday.data.strftime("%d-%b-%y")

            db.sqlalchemy_session.commit()

    return redirect(url_for('owner'))


@app.route('/delete_owner', methods=['POST'])
def delete_owner():

    owner_phone = request.form['owner_phone']

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormOwner).filter(ormOwner.owner_phone == owner_phone).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return owner_phone


if __name__ == '__main__':
    app.run(debug=True)
