from flask import Flask, render_template, jsonify
import io
import random
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
from yahoo import chartData, stockToCSV
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def index():
    num_x_points = int(request.args.get("num_x_points", 50))
    x = 121
    return render_template('index.html', x=x)

@app.route('/ticker/<ticker>')
@cross_origin()
def dataPoints(ticker="AMZN"):
    data = chartData(ticker)
    return jsonify(data)

@app.route('/backtest/<ticker>')
@cross_origin()
def backtest(ticker="AMZN"):
    from backtesting import execute_backtest
    data = execute_backtest(ticker)
    data['legends'] = []
    data['values'] = []
    for val in data['trades']:
        parsed_data = val.replace('CREATE', '').split(', ')
        data['legends'].append(parsed_data[0])
        data['values'].append(parsed_data[1])
    print(data)
    return jsonify(data)

@app.route("/lol")
def lol():
    return render_template('random.html')

"""
    <h1>Flask and Matplotlib</h1>
        <h2>Random data with {num_x_points} random points</h2>
            <form method=get action="/">
                <input name="num_x_points" type=number value="{num_x_points}" />
                <input type=submit value="update graph">
            </form>
            <h3>Plot as a png</h3>
            <img src="/matplot-as-image-{num_x_points}.png"
                alt="random points as png"
                height="200"
            >
            <h3>Plot as a SVG</h3>
            <img src="/matplot-as-image-{num_x_points}.svg"
                alt="random points as svg"
                height="200"
            >
    """

@app.route("/register", methods=['POST','GET'])
def register():
	if request.method=='POST':
		x=request.form['x']

		return render_template('index.html', x=x)
	else:
		return render_template('index.html', x=x)

@app.route("/matplot-as-image-<int:x>.png")
def plot_png(x=50):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(x)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
