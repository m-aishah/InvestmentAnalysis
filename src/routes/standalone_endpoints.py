from flask import Blueprint, request, jsonify
from src.modules.cost_comparison import run_cost_comparison_module
from src.modules.property_details_and_insights import run_property_details_and_insights
from src.modules.rental_income_forecast import run_rental_income_forecast
from src.modules.risk_analysis import run_risk_analysis_module

# Define the blueprint
standalone_bp = Blueprint('standalone', __name__)

@standalone_bp.route('/cost-comparison', methods=['POST'])
def cost_comparison():
    try:
        data = request.json
        result = run_cost_comparison_module(**data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@standalone_bp.route('/property-details', methods=['POST'])
def property_details():
    try:
        data = request.json
        result = run_property_details_and_insights(**data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@standalone_bp.route('/rental-income-forecast', methods=['POST'])
def rental_income_forecast():
    try:
        data = request.json
        result = run_rental_income_forecast(**data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@standalone_bp.route('/api/risk-analysis', methods=['POST'])
def risk_analysis():
    try:
        data = request.get_json()
        result = run_risk_analysis_module(**data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
