import matplotlib.pyplot
import networkx as nx
import itertools
import math

class Vrt:
    def __init__(self, path):
        self.path = path
        self.titles = {} # titles of threds on suomi24
        self.lines = [] # will hold single lines from file

        with open (path, encoding='utf-8') as file:
            self.lines = file.read().split("\n")[0:-1] # use [0:-1] to drop empty newline

        text_accumulator = []
        for line in self.lines:
            if line[0:5] == "<text": # this line was a title for new post
                current_title = line.split('"')[1]
                if current_title not in self.titles:
                    self.titles[current_title] = []
            elif not line[0:1] == "<": # no < means we are on line wiht normal text.
                new_word = line.split("\t")[2]
                for sub_word in new_word.split("|"): # break up combined words into sub words
                    text_accumulator.append(sub_word)
            if line[0:7] == "</text>":
                self.titles[current_title].append(text_accumulator)
                text_accumulator = []


def name_maker():
    for i in range(1955):
        yield "a"+str(i).zfill(4)+".vrt"


tags = ['pietari', 'molotov cocktail', 'ruotsi', 'panssarivaunu', 'rajat', 'ghettoutuminen', 'terrorismi', 'nationalismi', 'rajavalvonta', 'vapaus', 'poikkeusolot', 'internet', 'ruokahuolto', 'polttoainehuolto', 'schengen', 'supo', 'näkymätön sodankäynti', 'informaatiovääristymä', 'helsinki', 'sähkövoimala', 'vihreät', 'persut', 'vaihtoehtomedia', 'patriotismi', 'maamiinat', 'itäraja', 'kasvinsuojeluaineet', 'rasismi', 'pakolaiskriisi', 'haittamaahanmuutto', 'uskottava maanpuolustus', 'ydinaseet', 'kommunismi', 'seksuaalirikos', 'palokunta', 'vihreät miehet', 'viestikoelaitos', 'lääkehuolto', 'ilmatila', 'kybersodankäynti', 'hyvinvointivaltion romahdus', 'ulkopolitiikka', 'väestönsuoja', 'rynnäkkökivääri', 'poliisi', 'suojelupoliisi', 'islam', 'maahanmuutto','aseet', 'pelastuslaitos', 'krp', 'huoltovarmuus', 'lannoitteet', 'isänmaa', 'brexit', 'länsiraja', 'hybridivaikuttaminen', 'putin', 'reservi', 'kestävyysvajo', 'usa', 'vesihuolto', 'soldiers of odin', 'jussi halla-aho', 'järjestäytynyt rikollisuus', 'yksityistäminen', 'nato', 'syrjäytyminen', 'puolustusministeri', 'trump', 'tieverkko', 'sähkön jakelu', 'sähköverkko', 'väestönsuojelu', 'eu-rajat', 'peiteoperaatio', 'hävittäjä', 'turvasäiliö', 'taistelukaasu', 'sisäpolitiikka', 'kyberturvallisuus', 'eduskunta', 'maahanmuuttajat', 'biologiset aseet', 'terroristi', 'asepalvelus', 'varmuusvarasto', 'omavaraisuus', 'koulutusmalli', 'kannustinloukku', 'venäjä', 'niinistö', 'raiskaus', 'vakoilu', 'sairaala', 'tulli', 'feminismi', 'vartija', 'talvisota', 'luottamus', 'kaksoiskansalaisuus', 'ahvenanmaa', 'armeija', 'palkka-armeija', 'rikollisuus', 'agitattorit', 'rajavartiolaitos', 'kiina', 'maantie', 'verkkoturvallisuus', 'puolustusyhteistyö', 'tiedustelulaki', 'viro', 'poliisin määrärahat', 'kyber', 'antti rinne', 'kemialliset aseet', 'järjestäytynyt terrorismi', 'tietoliikenneyhteys', 'puolustusvoimat', 'teknologia', 'politiikka', 'eu', 'pakolaiset']


graph = nx.Graph()
graph.add_nodes_from(tags)
COUNTER = 0

for path in name_maker():
    print("STARTED NEW FILE", COUNTER)
    COUNTER += 1
    vrt = Vrt(path)
    # print("lankoja filussa:", len(vrt.titles))
    # input()
    for title in vrt.titles:
        for comment in vrt.titles[title]:
            sub_graph_names = [] # new fully connected subgraph to add to the final graph
            # print("=================", title, "=================")
            # print("======== posteja langassa", len(vrt.titles[title]), "========")
            for word in comment:
                # print(word, end=" ", flush=True)
                for tag in tags:
                    if tag==word:
                        sub_graph_names.append(tag)# add new node to subgraph

            subgraph = nx.complete_graph(len(sub_graph_names))
            dictionary = dict(zip([i for i in range(len(sub_graph_names))], sub_graph_names)) # mapping for renaming nodes (eg 0 to 4) into tags
            subgraph = nx.relabel_nodes(subgraph, dictionary)
            _ = nx.compose(graph, subgraph) # add subgraph to final graph # unknow bug? must use temp _ ?
            graph = _
            
            for start, end in itertools.combinations(sub_graph_names, r=2): # iterate over subgraph inside of the graph. increase weights
                try:
                    graph[start][end]["weight"] += 1
                except KeyError: # no weight was edded this specific path yet
                    graph[start][end]["weight"] = 1
        
    if (COUNTER%10 == 0) or (COUNTER==1954):

        print("=================================================================")
        print("number of nodes:", graph.number_of_nodes())
        print("number of edges:", graph.number_of_edges())
        print("maximum degree:", max(graph.degree(), key=lambda x:x[1]))
        print("average degree:", sum([i[1] for i in nx.degree(graph)])/graph.number_of_nodes())
        print("global clustering coefficient:", nx.average_clustering(graph))
        giant = max(nx.connected_component_subgraphs(graph), key=len)
        print("(giant) diameter:", nx.diameter(giant))
        print("(giant) average path length:", nx.average_shortest_path_length(giant))
        print("size of giant component:", giant.number_of_nodes(), "nodes and", giant.number_of_edges(), "edges")
        communities = []
        for clique in nx.find_cliques(graph):
            if len(clique) >= 3:
                communities.append(clique)
        community_edges = 0
        for community in communities:
            community_edges += (len(community)*(len(community)-1))/2
        nodes_in_communities = set(sum(communities, [])) # unique nodes
        print("number of communities:", len(communities))
        print("community node coverage quality measure:", len(nodes_in_communities)/graph.number_of_nodes())
        print("community edge coverage quality measure:", community_edges/graph.number_of_edges())
        print("=================================================================")
        
        print("saved graph pickle in file")
        nx.gpickle.write_gpickle(graph, "graph_pickle"+str(COUNTER))
        
        
        # nx.draw(graph, with_labels=True, pos=nx.circular_layout(graph))
        # matplotlib.pyplot.show()
        
        
        
        # import collections
        # #import matplotlib.pyplot as plt
        # #import networkx as nx

        # G = graafi
        # degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
        # # print "Degree sequence", degree_sequence
        # degreeCount = collections.Counter(degree_sequence)
        # deg, cnt = zip(*degreeCount.items())
        # fig, ax = plt.subplots()
        # plt.plot(deg, cnt, color='b')
        # plt.title("Degree graph (log)")
        # plt.ylabel("Count")
        # plt.xlabel("Degree")
        # ax.set_xticks([d + 0.4 for d in deg])
        # ax.set_xticklabels(deg)
        # ax.set_yscale('log')
        # plt.show()