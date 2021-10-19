from flask import Blueprint
from api.controllers.threat_controller import get_threats

threats_bp = Blueprint('threats_bp', __name__)
threats_bp.route('/threats', methods=['GET'])(get_threats)
