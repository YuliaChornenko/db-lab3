from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aecpuhnwzoonvi:e4c7df93fa1dd2f247e0f4cde9a151d746a069b479f3f0918ef6cd3d654b982f@ec2-18-215-111-67.compute-1.amazonaws.com:5432/d3oflggl341qqp'
db = SQLAlchemy(app)

class Composer(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    place = db.Column(db.String(64), index=True)


class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    year = db.Column(db.Integer)
    composer = db.Column(db.String(64), db.ForeignKey('composer.name'))


db.create_all()
db.session.commit()


@app.route('/delete_composition/<id>')
def delete_composition(id):
    dl = db.session.query(Composition).get(id)
    db.session.delete(dl)
    db.session.commit()
    return redirect('/index')

@app.route('/delete_composer/<name>')
def delete_composer(name):
    delete_list = Composition.query.filter_by(composer=name).all()
    for delete1 in delete_list:
        db.session.query(Composition).get(delete1.id)
        db.session.delete(delete1)
        db.session.commit()

    delete = db.session.query(Composer).get(name)
    db.session.delete(delete)
    db.session.commit()
    return redirect('/index')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    message = ''

    composer_posts = Composer.query.all()
    composition_posts = Composition.query.all()

    if request.method == 'POST':
        name = request.form.get('name_composer')
        place = request.form.get('place_composer')

        if name and place != '':
            try:
                add = Composer(name=name, place=place)
                db.session.add(add)
                db.session.commit()
                return redirect('/index')
            except:
                message = 'COMPOSER EXISTS!'


        name = request.form.get('name_composition')
        year = request.form.get('year_composition')
        composer = request.form.get('composer_composition')

        add = Composition(name=name, year=year, composer=composer)

        list_br = []
        all = Composer.query.all()
        for br in all:
            list_br.append(br.name)

        if name and year != '':
            if str(composer) in list_br:
                db.session.add(add)
                db.session.commit()
                return redirect('/index')
            message = "COMPOSER DOESN'T EXIST! FIRST OF ALL CREATE COMPOSER!"

    return render_template('index.html', composer_posts=composer_posts, composition_posts=composition_posts, message=message)


if __name__=="__main__":
    app.run(debug=True)