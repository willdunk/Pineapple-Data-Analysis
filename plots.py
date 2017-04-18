import plotly.offline as offline
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import plotly.plotly as py
from plotly.graph_objs import *
import igraph as ig

import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import sys

ssidtofind=""

if(len(sys.argv)<=0 or len(sys.argv)>2):
  	print("No Arguments Provided")
else:
	ssidtofind=sys.argv[1]

tempdata = {'nodes':[], 'links':[]}
listofedges = []
for line in open('pineap.log'):
	temp = line.split(',\t')
	listofedges.append((temp[2], temp[3]))

listofedges = list(set(listofedges))

listofedges[:] = [x for x in listofedges if x != ""]

listofmacssid = [];

for edge in listofedges:
	if(not edge[0] in listofmacssid):
		tempdata['nodes'].append({'name': edge[0], 'group': 1})
		listofmacssid.append(edge[0])
	if(not edge[1] in listofmacssid):
		g = 2
		# print(edge[1][:-1])
		if(ssidtofind == edge[1][:-1]):
			g = 3
		tempdata['nodes'].append({'name': edge[1][:-1], 'group': g})
		listofmacssid.append(edge[1])
	tempdata['links'].append({'source': listofmacssid.index(edge[0]), 'target': listofmacssid.index(edge[1]), 'value': 1}) 

# Graph stuff

init_notebook_mode(connected = False)

data = tempdata

N=len(data['nodes'])

L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges, directed=False)

labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])

layt=G.layout('kk_3d', dim=3)

Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

trace1=Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )
trace2=Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='nodes',
               marker=Marker(symbol='dot',
                             size=6,
                             color=group,
                             colorscale='Viridis',
                             line=Line(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = Layout(
         title="Network connection requests by MAC address and SSID requested",
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),
        ),
     margin=Margin(
        t=100
    ),
    hovermode='closest')

data=Data([trace1, trace2])
fig=Figure(data=data, layout=layout)

offline.plot(fig, filename='Pineapple-MAC-SSID.html')

# -------------------------------

# 2D layout
G=ig.Graph(Edges, directed=False)

layt=G.layout('kk', dim=2)
Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates

Xe=[]
Ye=[]
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0]]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1]]

trace1=Scatter(x=Xe,
               y=Ye,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )
trace2=Scatter(x=Xn,
               y=Yn,
               mode='markers',
               name='nodes',
               marker=Marker(symbol='dot',
                             size=6,
                             color=group,
                             colorscale='Viridis',
                             line=Line(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = Layout(
         title="2D Network connection requests by MAC address and SSID requested",
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
        ),
     margin=Margin(
        t=100
    ),
    hovermode='closest')

data=Data([trace1, trace2])
fig=Figure(data=data, layout=layout)

offline.plot(fig, filename='2D-Pineapple-MAC-SSID.html')