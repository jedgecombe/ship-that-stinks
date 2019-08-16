from flask import Blueprint, redirect, render_template, request, url_for

from ship_that_stinks.database.table_definitions import Shipmates
from ship_that_stinks.database.utils import DbUtils

crud = Blueprint("crud", __name__)


@crud.route("/")
def list():
    token = request.args.get("page_token", None)
    if token:
        token = token.encode("utf-8")

    shipmates, next_page_token = DbUtils.list(Shipmates, cursor=token)

    return render_template(
        "list.html", shipmates=shipmates, next_page_token=next_page_token
    )


@crud.route("/<id>")
def view(id):
    shipmate = DbUtils.read(Shipmates, id)
    return render_template("view.html", shipmate=shipmate)


@crud.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form.to_dict(flat=True)

        shipmate = DbUtils.insert(Shipmates, data)

        return redirect(url_for(".view", id=shipmate["id"]))

    return render_template("form.html", action="Add", shipmate={})


@crud.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    shipmate = DbUtils.read(Shipmates, id)

    if request.method == "POST":
        data = request.form.to_dict(flat=True)

        shipmate = DbUtils.update(Shipmates, data, id)

        return redirect(url_for(".view", id=shipmate["id"]))

    return render_template("form.html", action="Edit", shipmate=shipmate)


@crud.route("/<id>/delete")
def delete(id):
    DbUtils.delete(Shipmates, id)
    return redirect(url_for(".list"))
