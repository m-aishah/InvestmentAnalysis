from flask import Blueprint, jsonify, request
from functools import wraps
from datetime import datetime, timedelta

# Create a Blueprint for analytics
analytics_bp = Blueprint('analytics', __name__)

# Initialize counters and trackers
request_count = 0
active_users = {}

# Decorator to track requests and users
def track_requests(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global request_count
        request_count += 1

        # Track active users
        user_ip = request.remote_addr
        active_users[user_ip] = datetime.now()

        # Remove inactive users (not active in the last 10 minutes)
        cutoff_time = datetime.now() - timedelta(minutes=10)
        active_users_list = {ip: last_seen for ip, last_seen in active_users.items() if last_seen >= cutoff_time}
        return f(*args, **kwargs)

    return decorated_function

# Endpoint to provide dashboard data
@analytics_bp.route('/dashboard-data')
@track_requests
def dashboard_data():
    # Clean up old entries in active_users
    cutoff_time = datetime.now() - timedelta(minutes=10)
    active_users_list = {ip: last_seen for ip, last_seen in active_users.items() if last_seen >= cutoff_time}

    data = {
        'recent_analyses': request_count,
        'active_users': len(active_users_list),  # Number of active users
        'server_status': 'Online',  # Simple placeholder for now
        'investment_trends': get_investment_trends(),  # Real investment trends data
        'investment_trends_labels': get_investment_trends_labels()  # Real investment trends labels
    }
    return jsonify(data)

def get_investment_trends():
    # Example logic to simulate the number of times different modules are used
    # Replace with real data gathering logic
    return {
        'Cost Comparison': 25,
        'Rental Income': 18,
        'Risk Analysis': 15,
        'Recommendations': 30
    }

def get_investment_trends_labels():
    # Example labels for the modules
    return ['Cost Comparison', 'Rental Income', 'Risk Analysis', 'Recommendations']
