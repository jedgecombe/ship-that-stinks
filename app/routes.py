from collections import namedtuple
from datetime import datetime
import logging

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import and_, desc, func
from werkzeug.urls import url_parse

from app import app, db
from app.forms import AccountForm, EventForm, LoginForm, ResponseForm, \
    RegistrationForm, RegisterAttendanceForm
from app.models import Attendance, EventEvents, Event, ProposalResponse, User
from app.points import attendance_score, notice_score

logger = logging.getLogger(__name__)


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
    # TODO fix for when it is the creator of the event
    # TODO NEXT finish here
    event_id = request.args['event_id']
    logger.debug(f'Responding to event id {event_id}')
    focus_event = Event.query.get(event_id)

    form = ResponseForm()
    if form.validate_on_submit():
        if request.args.get('modify'):
            ProposalResponse.query.filter_by(id=request.args.get('response_id')).update(
                dict(is_active=False))
        new_response = ProposalResponse(description=form.response.data, is_active=True,
                                        event_id=event_id,
                                        user_id=current_user.id)
        db.session.add(new_response)
        db.session.commit()
        flash(f"You've responded to the event")
        return redirect(url_for('index'))
    return render_template('response.html', title='Respond to an event proposal',
                           event=focus_event, form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    # start_at, location, id, name, organised_by
    #
    # query = db.session.query(
    #     Event.nickname,
    #     func.coalesce(func.count(Attendance.id), 0).label('attendance_cnt'),
    #     func.coalesce(func.sum(EventEvents.points_pp), 0).label('points_sum')
    # ).join(Attendance, User.id == Attendance.user_id).join(
    #     EventEvents, Attendance.event_id == EventEvents.id
    # ).filter(Attendance.is_active).group_by(User.id).order_by(
    #     desc('points_sum'), desc('attendance_cnt'), "nickname")

    # TODO update to filter on events
    q = EventEvents.query.filter(and_(EventEvents.start_at > datetime.now(),
                                           EventEvents.is_active, EventEvents.is_active_update)).order_by(EventEvents.start_at)
    print(q)
    events = q.all()
    return render_template('index.html', title='Home', events=events)


@app.route('/points')
@login_required
def points():
    # TODO fix to show 0 plunder for someone with no events - need to LEFT JOIN but also subquery to avoid filter forcing inner
    query = db.session.query(
        User.nickname,
        func.coalesce(func.count(Attendance.id), 0).label('attendance_cnt'),
        func.coalesce(func.sum(EventEvents.points_pp), 0).label('points_sum')
    ).join(Attendance, User.id == Attendance.user_id).join(
        EventEvents, Attendance.event_id == EventEvents.id
    ).filter(Attendance.is_active).group_by(User.id).order_by(
        desc('points_sum'), desc('attendance_cnt'), "nickname")
    logger.debug(f"points query: {query}")
    results = query.all()
    logger.debug(f"points results: {results}")
    UserGrp = namedtuple("UserGrp", ["nickname", "attendance_cnt", "points_sum"])
    html_input = []
    for nn, ac, ps in results:
        html_input.append(UserGrp(nn, ac, ps))
    return render_template('points.html', title='Points', users=html_input)


@app.route('/previous_events')
@login_required
def previous_events():
    events = EventEvents.query.filter(
        and_(EventEvents.start_at <= datetime.now(), EventEvents.is_active)).order_by(
        EventEvents.start_at.desc()).all()
    return render_template('previous_events.html', title='Home', events=events)


def get_event_params(form) -> dict:
    start_at = dt_from_sql(f"{form.start_date.data} {form.start_time.data}")
    end_at = dt_from_sql(f"{form.end_date.data} {form.end_time.data}")
    notice_days = (start_at - datetime.now()).days
    return {
        "name": form.name.data,
        "start_at": start_at,
        "end_at": end_at,
        "notice_days": notice_days,
        "notice_mult": notice_score(notice_days),
        "location": form.location.data,
        "organised_by": current_user.id
    }


def create_new_event_id() -> str:
    new_event_id = Event(organised_by=current_user.id, created_at=datetime.now())
    db.session.add(new_event_id)
    db.session.commit()
    event_id = db.session.query(Event.id).filter(
        Event.organised_by == current_user.id).order_by(
        desc(Event.created_at), desc(Event.id)).first()
    return event_id


def delete_event():
    REMOVE_KEYS = ['_sa_instance_state', 'id']
    update_id = request.args.get('id')
    logger.debug(f"deleting id: {update_id}")
    original_event = EventEvents.query.filter_by(id=update_id)
    # create new event with same parameters, except no longer active
    event_kwargs = original_event.first().__dict__
    for k in REMOVE_KEYS:
        if k in event_kwargs:
            del event_kwargs[k]
    event_kwargs["is_active"] = False
    event_kwargs["is_active_update"] = True
    event_kwargs["update_created_at"] = datetime.now()
    new_event = EventEvents(**event_kwargs)
    logger.debug(f"creating new event with attributes: {event_kwargs}")
    new_event.is_active = False
    db.session.add(new_event)
    # update original event to have is_active_update=False
    original_event.update(dict(is_active_update=False))
    db.session.commit()


def modify_event(form):
    MAX_HOURS_DIFF = 6  # maximum number of hours before an event is considered a new event
    update_id = request.args.get('id')
    original_event = EventEvents.query.filter_by(id=update_id)
    original_event_id = original_event.first().event_id
    if form.validate_on_submit():
        event_kwargs = get_event_params(form)
        prev_start_ats = db.session.query(EventEvents.start_at).filter(
            EventEvents.event_id == original_event_id).all()
        start_diffs = [abs((event_kwargs["start_at"] - x).total_seconds()) / 3600 for (x, ) in prev_start_ats]
        max_start_diff = max(start_diffs)
        if max_start_diff <= MAX_HOURS_DIFF:
            event_kwargs["event_id"] = original_event_id
            logger.debug(f"modifying existing event: {original_event_id}")
        else:
            event_kwargs["event_id"] = create_new_event_id()
            logger.debug(f"creating new event id: {event_kwargs['event_id']} (from "
                         f"event_id: {original_event_id})")
        event_kwargs["is_active"] = True
        event_kwargs["is_active_update"] = True
        event_kwargs["update_created_at"] = datetime.now()
        updated_event = EventEvents(**event_kwargs)
        db.session.add(updated_event)
        original_event.update(dict(is_active_update=False, is_active=False))
        db.session.commit()
        flash(f"EventEvents proposal for '{form.name.data}' sent")
        return redirect(url_for("index"))


def new_event(form):
    if form.validate_on_submit():
        event_kwargs = get_event_params(form)
        event_kwargs["event_id"] = create_new_event_id()
        event_new = EventEvents(**event_kwargs)
        db.session.add(event_new)
        db.session.commit()
        flash(f"EventEvents proposal for '{form.name.data}' sent")
        return redirect(url_for("index"))


def dt_from_sql(time_string):
    # TODO move to a utils module
    return datetime.strptime(f"{time_string}", "%Y-%m-%d %H:%M:%S")

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
# TODO change name to not create_event()
def create_event():
    if request.args.get('delete'):
        delete_event()
        return redirect(url_for("index"))
    else:
        if request.args.get('modify'):
            update_id = request.args.get('id')
            original_event = EventEvents.query.get(update_id)
            form = EventForm(obj=original_event)
            modify_event(form)
        else:
            form = EventForm()
            new_event(form)
            # TODO change so that it returns to index
        return render_template("create_event.html", title="Create an event", form=form)


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
    if event_id and current_user.id == EventEvents.query.get(event_id).organised_by:
        focus_event = EventEvents.query.get(event_id)
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
            notice_mult = EventEvents.query.get(event_id).notice_mult
            EventEvents.query.filter_by(id=event_id).update(
                dict(attendee_cnt=attendance_cnt,
                     attendee_mult=attendance_mult,
                     points_pp=round(attendance_mult * notice_mult, 1),
                     has_happened=True))
            db.session.commit()
            return redirect(url_for('previous_events'))
    else:
        return redirect(url_for('previous_events'))
    return render_template('register_attendance.html', title='Register attendance',
                           form=form)
