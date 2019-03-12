from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", title="404 Not Found"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html", title="500 Internal Server Error"), 500
