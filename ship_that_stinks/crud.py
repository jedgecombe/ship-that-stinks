from flask import Blueprint, redirect, render_template, request, url_for

from ship_that_stinks import get_model

crud = Blueprint('crud', __name__)


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    participants, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        participants=participants,
        next_page_token=next_page_token)


@crud.route('/<id>')
def view(id):
    participant = get_model().read(id)
    return render_template("view.html", participant=participant)


@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        participant = get_model().create(data)

        return redirect(url_for('.view', id=participant['id']))

    return render_template("form.html", action="Add", participant={})


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    participant = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        participant = get_model().update(data, id)

        return redirect(url_for('.view', id=participant['id']))

    return render_template("form.html", action="Edit", participant=participant)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
