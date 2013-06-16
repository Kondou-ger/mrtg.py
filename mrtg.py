from flask import Flask, session, render_template, redirect, request, url_for
from rrdtool import graph as rrdgraph
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'SecretKeyHere'

rrdroot = "/path/to/rrd/files/"
imgroot = "/path/where/imgs/will/be/saved/"
graphs = {
		'charge': {
			'rrd': rrdroot+'charge.rrd',
			'prettyname': 'Load x 100',
			'v': "Load x 100",
			'aleg': "1 Minute",
			'bleg': "5 Minutes",
			'unit': "Load /"
		},
		'proc': {
			'rrd': rrdroot+'proc.rrd',
			'prettyname': 'Number of processes',
			'v': 'Processes',
			'aleg': 'PHP/uwsgi-Processes x 10',
			'bleg': 'Processes',
			'unit': '',
		},
		'cpu': {
			'rrd': rrdroot+'cpu.rrd',
			'prettyname': 'CPU usage in %',
			'v': '%',
			'aleg': 'User',
			'bleg': 'System & Nice',
			'unit': '%%',
		},
		'ram': {
			'rrd': rrdroot+'mem.rrd',
			'prettyname': 'RAM usage in %',
			'v': '%',
			'aleg': 'Active',
			'bleg': 'RAM',
			'unit': '%%',
		},
		'hdd': {
			'rrd': rrdroot+'espace.rrd',
			'prettyname': 'HDD usage in %',
			'v': '%',
			'aleg': '/boot',
			'bleg': '/',
			'unit': '%%',
		},
		'network': {
			'rrd': rrdroot+'network.rrd',
			'prettyname': 'Network usage in kB/s',
			'v': 'kB/s',
			'aleg': 'Incoming',
			'bleg': 'Outgoing',
			'unit': 'kB/s',
		},
		'nginx': {
			'rrd': rrdroot+'nginx.rrd',
			'prettyname': 'nGinx usage',
			'v': 'Coennections',
			'aleg': 'Waiting',
			'bleg': 'Active',
			'unit': 'Connections',
		},
	}

durations = {"day": "1d", "week": "7d", "month": "1m", "year": "1y"}

@app.route('/')
def index():
	global graphs
	if 'nick' not in session:
		return redirect(url_for('login'))

	for graph in graphs:
		rrdgraph(imgroot+"%s/day/latest.png" %(graph), "-X 0", "-l 0", "-s now-1d",
			"-e now", "-S 300", "-z", "-E", "-w 600", "-h 150", "-v %s" %(graphs[graph]['v']),
			"DEF:ds0=%s:ds0:AVERAGE" %(graphs[graph]['rrd']), "DEF:ds1=%s:ds1:AVERAGE" %(graphs[graph]['rrd']),
			"AREA:ds0#00FF00:%s\t\t" %(graphs[graph]['aleg']), "LINE1:ds1#0000FF:%s\\l" %(graphs[graph]['bleg']),
			"VDEF:avg0=ds0,AVERAGE", "VDEF:avg1=ds1,AVERAGE", "VDEF:min0=ds0,MINIMUM", "VDEF:min1=ds1,MINIMUM",
			"VDEF:max0=ds0,MAXIMUM", "VDEF:max1=ds1,MAXIMUM",
			"GPRINT:avg0:AVG\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:avg1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
			"GPRINT:min0:MIN\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:min1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
			"GPRINT:max0:MAX\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:max1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']))
				
	return render_template("index.html", graphs=graphs)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['password'] == "mrtgpassword":
			session['nick'] = request.form['nick']
			return redirect(url_for('index'))
		# else:
		return render_template("login.html", wrongpw=True)
	else:
		if 'nick' not in session:
			return render_template("login.html")
		# else:
		return redirect(url_for('index'))

@app.route('/logout/')
def logout():
	session.pop('nick', None)
	return redirect(url_for('index'))

@app.route('/<graph>/')
def graphtype(graph=None):
	if 'nick' not in session:
		return redirect(url_for('index'))
	# else:
	global graphs,durations
	if graph in graphs:
		for key in durations:
			rrdgraph(imgroot+"%s/%s/latest.png" %(str(graph), key), "-X 0", "-l 0", "-s now-%s" %(durations[key]),
			"-e now", "-S 300", "-z", "-E", "-w 600", "-h 150", "-v %s" %(graphs[graph]['v']),
			"DEF:ds0=%s:ds0:AVERAGE" %(graphs[graph]['rrd']), "DEF:ds1=%s:ds1:AVERAGE" %(graphs[graph]['rrd']),
			"AREA:ds0#00FF00:%s\t\t" %(graphs[graph]['aleg']), "LINE1:ds1#0000FF:%s\\l" %(graphs[graph]['bleg']),
			"VDEF:avg0=ds0,AVERAGE", "VDEF:avg1=ds1,AVERAGE", "VDEF:min0=ds0,MINIMUM", "VDEF:min1=ds1,MINIMUM",
			"VDEF:max0=ds0,MAXIMUM", "VDEF:max1=ds1,MAXIMUM",
			"GPRINT:avg0:AVG\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:avg1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
			"GPRINT:min0:MIN\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:min1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
			"GPRINT:max0:MAX\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:max1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']))

		return render_template("graph.html", thisgraph=graph, graphs=graphs, durations=durations)
	# else:
	return redirect(url_for('index'))

@app.route('/<graph>/<duration>/more/')
def more(graph=None, duration=None):
	if 'nick' not in session:
		return redirect(url_for('index'))

	global graphs, durations
	if (duration in durations) and (graph in graphs):
		computerduration = durations[duration]
		wanteddurations = [[computerduration, "0"]]
		wanteddurationnumbers = [[computerduration[0], 0]]
		for i in range(2,6): # int i=1; for (i; i<=5; i++)
			wanteddurations.append([str(int(computerduration[0])*i)+computerduration[1], str(int(computerduration[0])*(i-1))+computerduration[1]])
		for j in range(2,6):
			wanteddurationnumbers.append([int(computerduration[0])*j, int(computerduration[0])*(j-1)])

		for k in range(0,4):
			rrdgraph(imgroot+"%s/%s/%s.png" %(str(graph), str(duration), wanteddurationnumbers[k][0]), "-X 0", "-l 0", "-s now-%s" %(wanteddurations[k][0]),
			"-e now-%s" %(wanteddurations[k][1]), "-S 300", "-z", "-E", "-w 600", "-h 150", "-v %s" %(graphs[graph]['v']),
			"DEF:ds0=%s:ds0:AVERAGE" %(graphs[graph]['rrd']), "DEF:ds1=%s:ds1:AVERAGE" %(graphs[graph]['rrd']),
			"AREA:ds0#00FF00:%s\t\t" %(graphs[graph]['aleg']), "LINE1:ds1#0000FF:%s\\l" %(graphs[graph]['bleg']),
			"VDEF:avg0=ds0,AVERAGE", "VDEF:avg1=ds1,AVERAGE", "VDEF:min0=ds0,MINIMUM", "VDEF:min1=ds1,MINIMUM",
			"VDEF:max0=ds0,MAXIMUM", "VDEF:max1=ds1,MAXIMUM",
			"GPRINT:avg0:AVG\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:avg1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
			"GPRINT:min0:MIN\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:min1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
			"GPRINT:max0:MAX\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
			"GPRINT:max1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']))
			
		return render_template("more.html", thisgraph=graph, graphs=graphs, durationname=duration, durations=wanteddurationnumbers)
	# else:
	return redirect(url_for('index'))

@app.route('/<graph>/own/', methods=['GET', 'POST'])
def own(graph=None):
	if 'nick' not in session:
		return redirect(url_for('index'))

	global graphs
	if graph in graphs:
		if request.method == 'POST':
			lazy = slopes = "-X 0"
			if 'lazy' in request.form:
				lazy = "-z"
			if 'slopes' in request.form:
				slopes = "-E"
			rrdgraph(imgroot+"%s/custom.png" %(str(graph)), "-X 0", "-l 0", "-s now-%s" %(str(request.form['start'])),
				"-e now-%s" %(str(request.form['end'])), "-S %s" %(str(request.form['step'])), "%s" %(lazy), "%s" %(slopes),
				"-w %s" %(str(request.form['width'])), "-h %s" %(str(request.form['height'])), "-v %s" %(str(request.form['vert-axis'])),
				"DEF:ds0=%s:ds0:AVERAGE" %(graphs[graph]['rrd']), "DEF:ds1=%s:ds1:AVERAGE" %(graphs[graph]['rrd']),
				"AREA:ds0%s:%s\t\t" %(str(request.form['area-color']), graphs[graph]['aleg']), "LINE1:ds1%s:%s\\l" %(str(request.form['line-color']), graphs[graph]['bleg']),
				"VDEF:avg0=ds0,AVERAGE", "VDEF:avg1=ds1,AVERAGE", "VDEF:min0=ds0,MINIMUM", "VDEF:min1=ds1,MINIMUM",
				"VDEF:max0=ds0,MAXIMUM", "VDEF:max1=ds1,MAXIMUM",
				"GPRINT:avg0:AVG\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
				"GPRINT:avg1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
				"GPRINT:min0:MIN\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
				"GPRINT:min1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']),
				"GPRINT:max0:MAX\: %%4.0lf %s %s" %(graphs[graph]['unit'], graphs[graph]['aleg']),
				"GPRINT:max1:%%4.0lf %s %s\\l" %(graphs[graph]['unit'], graphs[graph]['bleg']))
			return render_template("own-generated.html", thisgraph=graph)
		# else:
		return render_template("own-generate.html", thisgraph=graph)

if __name__ == "__main__":
	app.run()#host="0.0.0.0", debug=True)
