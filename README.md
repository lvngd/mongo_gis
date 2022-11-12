# Demo of Point in Polygon with MongoDB

Read more [in this blog post](https://lvngd.com/blog/point-polygon-search-mongodb/).

## Setup

To run the code:

*  Make sure you have MongoDB installed and running.
*  You need Python with a new virtualenv, activated.
*  `pip install -r requirements.txt` inside the virtualenv.
*  Run a web server to view the html, for example `python -m http.server`.

### This code has two main parts:

#### Flask + PyMongo - `app.py`

A Flask app with two endpoints.
  *  The root endpoint
  *  Endpoint to query point in polygon
     *  The backend generates a new random polygon and uses that to query MongoDB.
  
#### D3 Visualization - `viz.html`

*  Visualizes a 2-D grid of points.
*  On each iteration, calls the point-in-polygon endpoint to get a new polygon.
