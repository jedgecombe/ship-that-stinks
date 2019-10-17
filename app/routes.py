from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import and_
from werkzeug.urls import url_parse

from app import app, db
from app.forms import AccountForm, EventForm, LoginForm, ResponseForm, RegistrationForm, RegisterAttendanceForm
from app.models import Attendance, Event, ProposalResponse, User
from app.points import attendance_score, notice_score


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
            dict(is_active=False))
        db.session.commit()
    focus_event = Event.query.get(request.args['event_id'])
    form = ResponseForm()
    if form.validate_on_submit():
        flash(f"You've responded to the event '{focus_event.name}'")
        new_response = ProposalResponse(description=form.response.data, is_active=True,
                                        event_id=focus_event.id,
                                        user_id=current_user.id)
        db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('response.html', title='Respond to an event proposal', event=focus_event, form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    events = Event.query.filter(and_(Event.start_at > datetime.now(),
                                     Event.is_active)).order_by(Event.start_at).all()
    return render_template('index.html', title='Home', events=events)

@app.route('/previous_events')
@login_required
def previous_events():
    events = Event.query.filter(and_(Event.start_at <= datetime.now(), Event.is_active)).order_by(Event.start_at.desc()).all()
    return render_template('previous_events.html', title='Home', events=events)


@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.args.get('modify') or request.args.get('delete'):
        focus_event = Event.query.get(request.args.get('event_id'))
        Event.query.filter_by(id=focus_event.id).update(dict(is_active=False))
        db.session.commit()
        if request.args.get('delete'):
            return redirect(url_for('index'))
        else:
            form = EventForm(obj=focus_event)
    else:
        form = EventForm()
    if form.validate_on_submit():
        flash(f"Event proposal for '{form.name.data}' sent")
        start_at = datetime.strptime(
            f"{form.start_date.data} {form.start_time.data}", '%Y-%m-%d %H:%M:%S')
        end_at = datetime.strptime(f"{form.end_date.data} {form.end_time.data}",
                                         '%Y-%m-%d %H:%M:%S')
        notice_days = round((end_at - start_at).days, 1)
        new_event = Event(name=form.name.data,
                          start_at=start_at,
                          end_at=end_at,
                          notice_days=notice_days,
                          notice_mult=notice_score(notice_days),
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


@app.route('/register_attendance', methods=['GET', 'POST'])
@login_required
def register_attendance():
    event_id = request.args.get('event_id')
    if event_id and current_user.id == Event.query.get(event_id).organised_by:
        focus_event = Event.query.get(event_id)
        form = RegisterAttendanceForm(obj=focus_event)
        if request.method == "POST":
            selected_users = request.form.getlist("user_ids")
            currently_recorded = Attendance.query.filter_by(event_id=event_id)
            currently_recorded.update({"is_active": False})
            db.session.commit()
            for user in selected_users:
                attendance = Attendance(recorded_at=datetime.now(),
                                        event_id=event_id, user_id=user,
                                        is_active=True)
                db.session.add(attendance)
                db.session.commit()
            attendance_cnt = len(selected_users)
            attendance_mult = attendance_score(attendance_cnt)
            notice_mult = Event.query.get(event_id).notice_mult
            Event.query.filter_by(id=event_id).update(
                dict(attendee_cnt=attendance_cnt,
                     attendee_mult=attendance_mult,
                     points_pp=round(attendance_mult*notice_mult, 1)))
            db.session.commit()
            return redirect(url_for('previous_events'))
    else:
        return redirect(url_for('previous_events'))
    return render_template('register_attendance.html', title='Register attendance', form=form)

