#listing for drivers and passengers

from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Model for Driver
# Driver - id, name, license_number, phone_number, vehicle_type

# write normal class for Driver model with __repr__ method without sqlalchemy
#class Driver:
    #def __init__(self, id, name, license_number, phone_number, vehicle_type):
        #self.id = id
        #self.name = name
        #self.license_number = license_number
        #self.phone_number = phone_number
        #self.vehicle_type = vehicle_type

    #def __repr__(self):
#return f'<Driver {self.name}, License: {self.license_number}>'

# Write driver class for sqlalchemy
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Driver {self.name}, License: {self.license_number}>'

# api for direver for listing
@app.route('/api/drivers' ,methods=['GET'])
def get_drivers():
        drivers = Driver.query.all()
        driver_list = []
        for driver in drivers:
            driver_list.append({
                'id': driver.id,
                'name': driver.name,
                'license_number': driver.license_number,
                'phone_number': driver.phone_number,
                'vehicle_type': driver.vehicle_type
            })
        return jsonify({'drivers': driver_list})

# get single driver by id
@app.route('/api/drivers/<int:id>', methods=['GET'])
def get_driver(id):
    driver = Driver.query.get(id)
    if not driver:
        return jsonify({'error': 'Driver not found'}), 404
    driver_data = {
        'id': driver.id,
        'name': driver.name,
        'license_number': driver.license_number,
        'phone_number': driver.phone_number,
        'vehicle_type': driver.vehicle_type
    }
    return jsonify(driver_data)



# post route to add driver

@app.route('/api/drivers', methods=['POST'])
def add_driver():
    data = request.get_json()
    new_driver = Driver(
        name=data['name'],
        license_number=data['license_number'],
        phone_number=data['phone_number'],
        vehicle_type=data['vehicle_type']
    )
    db.session.add(new_driver)
    db.session.commit()
    return jsonify({'message': 'Driver added successfully!'}), 201

if __name__ == '__main__':
    with app.app_context():
         db.create_all()
        
    app.run(debug=True)


