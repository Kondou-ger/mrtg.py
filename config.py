secretkey = 'SecretKeyHere'
mrtgpassword = 'mrtgpassword'
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
