import random
from flask import Flask, request
from flask.json import jsonify
from pymongo import MongoClient, GEO2D
from flask_cors import CORS 

grid_width = 200
grid_height = 200

def get_slope(p1,p2):
	if p1[0] == p2[0]:
		return float('inf')
	else:
		return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])


def generate_random_polygon(width,height):
	coords = []
	#random number of sides
	num_points = random.randint(4,5)
	for p in range(num_points):
		x = None
		y = None
		quad = p%4
		if quad == 2:
			x = random.randint(0,width/2)
			y = random.randint(height/2,height-1)
		if quad == 3:
			x = random.randint(width/2,width-1)
			y = random.randint(height/2,height-1)
		if quad == 0:
			x = random.randint(0,width/2)
			y = random.randint(0,height/2)
		if quad == 1:
			x = random.randint(width/2,width-1)
			y = random.randint(0,height/2)
		coords.append([x,y])
	coords.sort(key=lambda x: [x[0],x[1]])
	start = coords.pop(0)
	coords.sort(key=lambda p: (get_slope(p,start), -p[1],p[0]))
	all_coords = [start]
	all_coords.extend(coords)
	return all_coords

def generate_points(width,height):
	points = []
	count = 0
	for i in range(width):
		for j in range(height):
			points.append({'pt': [i,j], 'id': count})
			count += 1
	return points

#connect to db
client = MongoClient("mongodb://127.0.0.1:27017/admin")
client = client.get_database("admin")
db = client["demo"]
#right now dropping everything then re-creating
db.coords.drop()
db.coords.create_index([('pt', GEO2D)], min=0, max=grid_width)
points = generate_points(grid_width,grid_height)
db.coords.insert_many(points)



app = Flask(__name__)
CORS(app)

@app.route('/get_points')
def get_index():
	pts = db.coords.find({}, {'_id': 0})
	res = list(pts)
	output = {'results': res, 'control_points': [[[0,0],[0,0]]]}
	return jsonify(output)


@app.route('/get_polygon_points')
def get_roi_points():
	#polygon/2D-ROI example
	polygon_points = generate_random_polygon(grid_width,grid_height)
	lines = []
	p1 = polygon_points[0]
	for p in polygon_points[1:]:
		lines.append([p1,p])
		p1 = p
	last_line = [p1,lines[0][0]]
	lines.append(last_line)
	#point in polygon query
	query = {"pt": {"$geoWithin": {"$polygon": polygon_points}}}
	result = db.coords.find(query, {'_id': 0})
	res = list(result)
	output = {'results': res, 'control_points': lines}
	return jsonify(output)