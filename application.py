import networkx as nx
import codecs
#import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import yaml

def find_route(source, dest, lang="japanese", walk_only=True):
    if source == None or dest == None:
        return "No input!"

    graph = nx.DiGraph()

    if lang == "english":
        source = source.lower()
        dest = dest.lower()
        with codecs.open("areas_en.yaml", "r", 'utf-8') as yml:
            net = yaml.load(yml, Loader=yaml.SafeLoader)
    else:
        with codecs.open("areas.yaml", "r", 'utf-8') as yml:
            net = yaml.load(yml, Loader=yaml.SafeLoader)

    for i in net['areas']:
        for j in i['destination']:
            if walk_only:
                if j['transportation']=="walk":
                    graph.add_edges_from([(i['name'], j['name'], {"transportation" : j['transportation'], "weight":j['weight']})])
            else:
                graph.add_edges_from([(i['name'], j['name'], {"transportation" : j['transportation'], "weight":j['weight']})])
    try:
        return nx.shortest_path(graph, source=source, target=dest)
    except nx.exception.NodeNotFound:
        return "No route found!"
# pos = nx.spring_layout(graph, k=1.2)
# nx.draw_networkx_nodes(graph, pos, alpha=0.6, node_size=500)
# nx.draw_networkx_labels(graph, pos, font_size=6, font_family="MS Gothic")
# nx.draw_networkx_edges(graph, pos, alpha=0.4)

# plt.show()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', \
		message = 'source', \
        result = 'none!')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
    source = request.form.get('source')
    destination = request.form.get('destination')
    bywalk = request.form.get('bywalk')

    if bywalk is None:
        bywalk = False

    lang = request.form.get('lang')

    result = find_route(source, destination, lang, bywalk)

    if destination=="モルディオン監獄":
        result = ['規約違反', 'モルディオン監獄']
    try:
        if destination.lower()=="mordion gaol":
            result = ['violation', 'mordion gaol']
    except AttributeError:
        pass

    return render_template('index.html', \
		message = 'sorce:{}, dist:{}, lang:{}, walk:{}'.format(source,destination,lang,bywalk),\
        result = result)

if __name__ == "__main__" :
    app.run()