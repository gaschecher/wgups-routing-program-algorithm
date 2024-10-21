from flask import Blueprint, jsonify, request
from datetime import datetime, time

api = Blueprint('api', __name__)

def get_datetime_param(time_str=None):
    if time_str:
        time_obj = datetime.strptime(time_str, '%H:%M').time()
    else:
        time_obj = datetime.now().time()
    current_date = datetime.now().date()
    return datetime.combine(current_date, time_obj)

@api.route('/package/<int:package_id>', methods=['GET'])
def get_package_status(package_id):
    time_str = request.args.get('time')
    datetime_obj = get_datetime_param(time_str)
    
    package = api.package_hash.lookup(package_id)
    if package:
        status = package.get_status(datetime_obj)
        return jsonify({
            'id': package.package_id,
            'status': status,
            'address': package.address,
            'city': package.city,
            'state': package.state,
            'zip': package.zip_code,
            'weight': package.weight,
            'deadline': str(package.deadline),
            'delivery_time': str(package.delivery_time) if package.delivery_time else None
        })
    return jsonify({'error': 'Package not found'}), 404

@api.route('/packages', methods=['GET'])
def get_all_packages_status():
    time_str = request.args.get('time')
    datetime_obj = get_datetime_param(time_str)
    
    all_packages = []
    for i in range(1, 41):  # Assuming package IDs are from 1 to 40
        package = api.package_hash.lookup(i)
        if package:
            status = package.get_status(datetime_obj)
            all_packages.append({
                'id': package.package_id,
                'status': status,
                'address': package.address,
                'city': package.city,
                'state': package.state,
                'zip': package.zip_code,
                'weight': package.weight,
                'deadline': str(package.deadline),
                'delivery_time': str(package.delivery_time) if package.delivery_time else None
            })
    return jsonify(all_packages)

@api.route('/mileage', methods=['GET'])
def get_total_mileage():
    time_str = request.args.get('time')
    datetime_obj = get_datetime_param(time_str)
    
    total_mileage = sum(truck.get_mileage_at_time(datetime_obj) for truck in api.trucks)
    return jsonify({'total_mileage': total_mileage, 'time': str(datetime_obj.time())})