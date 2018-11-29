from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from startup_setup import Base, Startup, Founder

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/startup/<int:startup_id>/details/JSON')
def startupDetailsJSON(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founders = session.query(Founder).filter_by(startup_id=startup_id).all()
    return jsonify(founders=[f.serialize for f in founders])


@app.route('/startup/JSON')
def startupsJSON():
    startups = session.query(Startup).all()
    return jsonify(startups=[s.serialize for s in startups])


    # Show all restaurants
@app.route('/')
@app.route('/startup/')
def showStartups():
    startups = session.query(Startup).all()
    return render_template('startups.html', startups=startups)



@app.route('/startup/<int:startup_id>/details/')
def showStartupDetails(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founders = session.query(Founder).filter_by(startup_id=startup_id).all()
    return render_template('startupdetails.html', founders=founders, startup=startup)
    # return 'This page is the menu for restaurant %s' % restaurant_id        return render_template('startupdetails.html')


    # Create a new restaurant
@app.route('/startup/<int:startup_id>/founder/new/', methods=['GET', 'POST'])
def newFounder(startup_id):
    if request.method == 'POST':
        newFounder = Founder(name=request.form['name'], bio=request.form['bio'], startup_id=startup_id)
        session.add(newFounder)
        session.commit()
        flash("Successfully Added a New Founder!")
        return redirect(url_for('showStartupDetails', startup_id=startup_id))
    else:
        return render_template('newfounder.html', startup_id=startup_id)
    # return "This page will be for making a new restaurant"
   
    # return 'This page is for making a new menu item for restaurant %s'
    # %restaurant_id

# Edit a restaurant


@app.route('/startup/<int:startup_id>/<int:founder_id>/edit/', methods=['GET', 'POST'])
def editFounder(startup_id, founder_id):
    founderToEdit = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        if request.form['name']:
            founderToEdit.name = request.form['name']
        if request.form['bio']:
            founderToEdit.bio = request.form['bio']  
        session.add(founderToEdit)
        session.commit()
        flash("Successfully Edited a Founder!")      
        return redirect(url_for('showStartupDetails', startup_id=startup_id))
    else:
        return render_template(
            'editfounder.html', startup_id=startup_id, founder_id=founder_id, founder=founderToEdit)

    # return 'This page will be for editing restaurant %s' % restaurant_id

# Delete a restaurant


@app.route('/startup/<int:startup_id>/<int:founder_id>/delete/', methods=['GET', 'POST'])
def deleteFounder(startup_id, founder_id):
    founderToDelete = session.query(Founder).filter_by(id=founder_id).one()
    if request.method == 'POST':
        session.delete(founderToDelete)
        session.commit()
        flash("Successfully Deleted a Founder!")
        return redirect(url_for('showStartupDetails', startup_id=startup_id))
    else:
        return render_template('deletefounder.html', founder=founderToDelete)
    # return 'This page will be for deleting restaurant %s' % restaurant_id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)