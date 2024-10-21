from flask import Blueprint, jsonify, request
from datetime import datetime
from src.main import package_hash, trucks

api = Blueprint('api', __name__)

@api.route('/package/<int:package_id>', methods=['GET'])
def get_package_status(package_id):
    time_str = request.args.get('time', '00:00')
    time = datetime.strptime(time_str, '%H:%M').time()
    package = package_hash.lookup(package_id)
    if package:
        status = package.get_status(time)
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
    time_str = request.args.get('time', '00:00')
    time = datetime.strptime(time_str, '%H:%M').time()
    all_packages = []
    for i in range(1, 41):  # Assuming package IDs are from 1 to 40
        package = package_hash.lookup(i)
        if package:
            status = package.get_status(time)
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
    total_mileage = sum(truck.mileage for truck in trucks)
    return jsonify({'total_mileage': total_mileage})