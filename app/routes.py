import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import and_
from werkzeug.urls import url_parse

from app import app, db
from app.forms import AccountForm, EventForm, LoginForm, ResponseForm, RegistrationForm
from app.models import Event, ProposalResponse, User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, surname=form.surname.data,
                        nickname=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/response', methods=['GET', 'POST'])
@login_required
def response():
    if request.args.get('modify'):
        ProposalResponse.query.filter_by(id=request.args.get('response_id')).update(
            dict(response_status="Closed"))
    focus_event = Event.query.get(request.args['event_id'])
    form = ResponseForm()
    if form.validate_on_submit():
        flash("You've responded to the event '{}'".format(focus_event.name))
        new_response = ProposalResponse(response=form.response.data,
                                         event=focus_event.id, user=current_user.id)
        db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('response.html', title='Respond to an event proposal', event=focus_event, form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    events = Event.query.filter_by(status="Open").order_by(Event.start_date).all()
#    proposals = user.proposals.all()
    return render_template('index.html', title='Home', events=events)

@app.route('/previous_events')
@login_required
def previous_events():
    events = Event.query.filter(and_(Event.start_date <= datetime.datetime.now(), Event.status=="Open")).all()
    return render_template('previous_events.html', title='Home', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.args.get('modify'):
        focus_event = Event.query.get(request.args.get('event_id'))
        form = EventForm(obj=focus_event)
        Event.query.filter_by(id=focus_event.id).update(dict(status="Closed"))
    else:
        form = EventForm()
    if form.validate_on_submit():
        flash("Event proposal for '{}' sent".format(form.name.data))
        new_event = Event(name=form.name.data,
                          start_date=form.start_date.data,
                          start_time=form.start_time.data,
                          end_date=form.end_date.data,
                          end_time=form.end_time.data,
                          location=form.location.data,
                          organised_by=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_event.html', title='Create an event', form=form)


@app.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = AccountForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=current_user.id).first()
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for('index'))
    return render_template('update_account.html', title='My account', form=form)
