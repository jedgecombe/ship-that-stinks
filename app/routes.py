from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import AccountForm, EventForm, LoginForm, ResponseForm
from app.models import event, proposal_response, shipmate


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = shipmate.query.filter_by(nickname=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/response', methods=['GET', 'POST'])
@login_required
def response():
    if request.args.get('modify'):
        proposal_response.query.filter_by(id=request.args.get('response_id')).update(
            dict(response_status="Closed"))
    focus_event = event.query.get(request.args['event_id'])
    form = ResponseForm()
    if form.validate_on_submit():
        flash("You've responded to the event '{}'".format(focus_event.event_name))
        new_response = proposal_response(response=form.response.data, event=focus_event.id, shipmate=current_user.id)
        db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('response.html', title='Respond to an event proposal', event=focus_event, form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    events = event.query.filter_by(event_status="Open").order_by(event.event_date).all()
#    proposals = user.proposals.all()
    return render_template('index.html', title='Home', events=events)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.args.get('modify'):
        focus_event = event.query.get(request.args.get('event_id'))
        form = EventForm(obj=focus_event)
        event.query.filter_by(id=focus_event.id).update(dict(event_status="Closed"))
    else:
        form = EventForm()
    if form.validate_on_submit():
        print(type(form.event_date.data), form.event_date.data)
        print(type(form.event_time.data), form.event_time.data)
        flash("Event proposal for '{}' sent".format(form.event_name.data))
        new_event = event(event_name=form.event_name.data,
                          event_date=form.event_date.data,
                          event_time=form.event_time.data,
                          event_location=form.event_location.data,
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
        print('POST')
        if form.validate_on_submit():
            print('VALIDATE')
            user = shipmate.query.filter_by(nickname=form.username.data).first()
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for('index'))
    return render_template('update_account.html', title='My account', form=form)
