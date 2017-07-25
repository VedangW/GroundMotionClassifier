#!usr/bin/python

import plotly
import numpy as np
from Seismogram import Seismogram
import plotly.graph_objs as go

import plotly.dashboard_objs as dashboard

import IPython.display
from IPython.display import Image

def fileId_from_url(url):
    """Return fileId from a url."""
    index = url.find('~')
    fileId = url[index + 1:]
    local_id_index = fileId.find('/')

    share_key_index = fileId.find('?share_key')
    if share_key_index == -1:
        return fileId.replace('/', ':')
    else:
        return fileId[:share_key_index].replace('/', ':')

def main():
	smg1 = Seismogram("/home/vedang/Desktop/PS/Datasets/Kachchh", "pitsa001.003", "r")
	smg2 = Seismogram("/home/vedang/Desktop/PS/Datasets/Kachchh", "pitsa001.044", "r")
	amps1 = smg1.get_amplitudes()
	ndat1 = smg1.get_ndat()
	amps2 = smg2.get_amplitudes()
	ndat2 = smg2.get_ndat()
	t1 = np.arange(0., ndat1 * 0.02, 0.02)
	t2 = np.arange(0., ndat2 * 0.02, 0.02)
	m = 1
	c = 500

	trace0 = go.Scatter(x=t1, y=amps1, name='pitsa001.003')
	trace1 = go.Scatter(x=t1, y= m*t1 + c, name='Decision Boundary')
	trace2 = go.Scatter(x=t2, y=amps2, name='pitsa001.044')
	data1 = [trace0, trace1]
	data2 = [trace2]

	url1 = plotly.plotly.plot({
	    "data": data1,
	    "layout": go.Layout(title="Seismogram1")
	})

	url2 = plotly.plotly.plot({
		"data": data2,
		"layout": go.Layout(title="Seismogram2")
	})

	fileId_1 = fileId_from_url(url_1)
	fileId_2 = fileId_from_url(url_2)


	my_dboard = dashboard.Dashboard()
	my_dboard.get_preview()

	box_a = {
	    'type': 'box',
	    'boxType': 'plot',
	    'fileId': fileId_1,
	    'title': 'scatter-for-dashboard'
	}

	box_b = {
		'type': 'box',
		'boxType': 'plot',
		'fileId': fileId_2,
		'title': 'whatever'
	}
	 
	my_dboard.insert(box_a)
	my_dboard.insert(box_b, 'below', 1)

if __name__ == "__main__":
	main()

#FOOTERS:

	"""
	t = np.arange(-20., 20., 1)
	fig = plt.figure("Scatterplot of data")
	axes = plt.axis()
	print axes

	ax0 = fig.add_subplot(111)
	ax0.plot(X1, Y1, 'bo', label='Earthquakes', ms = 4)
	ax0.plot(X2, Y2, 'rx', label='Blasting')
	ax0.plot(t, clf.coef_[0][1] * t + clf.coef_[0][0], linewidth=1.0)
	ax0.set_xlabel('Complexity')
	ax0.set_ylabel('log Pe')
	ax0.legend()
	plt.show()
	"""

	"""
	print xi
	print len(xi)
	print yline
	print len(yline)

	app.layout = html.Div([
	    dcc.Graph(
	        id='complexity-vs-logPe',
	        figure={
	            'data': [
	                	go.Scatter(
		                    x=df[df['label'] == i]['complexity'],
		                    y=df[df['label'] == i]['logpoe'],
		                    text=df[df['label'] == i]['class'],
		                    mode='markers',
		                    opacity=0.7,
		                    marker={
		                        'size': 15,
		                        'line': {'width': 0.5, 'color': 'white'}
		                    },
		                    name=i,
		                ) for i in df.label.unique()
	            ],
	            'layout': go.Layout(
	            	plot_bgcolor='rgb(229, 229, 229)',
	                xaxis={'type': 'log', 'title': 'Complexity'},
	                yaxis={'title': 'log Pe'},
	                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
	                legend={'x': 0, 'y': 1},
	                hovermode='closest'
	            )
	        }
	    )
	])

	app.run_server()
	"""