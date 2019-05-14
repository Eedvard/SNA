import matplotlib.pyplot as plt
import networkx as nx
import itertools
import math
import time

thresholds = []
nodes = []
edges = []
maximum_degrees = [] # ('politiikka', 40)
average_degrees = []
global_clustering_coefficients = []
diameters = [] # giant of nothing else available
average_path_lenghts = [] # giant of nothing else available
giant_component_nodes = []
giant_component_edges = []
number_of_communities = []
community_node_coverage_quality_measure = []
community_edge_coverage_quality_measure = []






for threshold in range(0,2000):
    if threshold%1 == 0:
        print("entering threshold", threshold)
        graafi = nx.gpickle.read_gpickle("graph_pickle1954polyglot")
        if(threshold==0):
            plt.clf() #clear figure
            painot = [math.log(i) for i in list(nx.get_edge_attributes(graafi, "weight").values())]
            pos = nx.kamada_kawai_layout(graafi)
            #pos = nx.circular_layout(graafi)
            #pos = nx.spring_layout(graafi)
            nx.draw(graafi, pos, with_labels=True, font_size=8, node_size=30, width=painot, font_color="red", font_weight="bold")
            if(threshold == 0):
                plt.savefig("origpolykuvaaja.pdf", dpi=500)
        graafi.remove_nodes_from(list(nx.isolates(graafi))) # remove useless nodes. this removes those with 0 edges
        edges_to_remove = []
        for edge in nx.get_edge_attributes(graafi, "weight"):
            if nx.get_edge_attributes(graafi, "weight")[edge] < threshold:
                edges_to_remove.append(edge)
        graafi.remove_edges_from(edges_to_remove)
        graafi.remove_edges_from(graafi.selfloop_edges()) # remove self loops
        graafi.remove_nodes_from(list(nx.isolates(graafi))) # remove useless nodes. this removes those with 0 edges. new ones appeared when setting threshold


        
        
            ################## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #############

            # print("=================================================================")
            # print("threshold: ", threshold)
            # print("number of nodes:", graafi.number_of_nodes())
            # print("number of edges:", graafi.number_of_edges())
            # print("maximum degree:", max(graafi.degree(), key=lambda x:x[1]))
            # print("average degree:", sum([i[1] for i in nx.degree(graafi)])/graafi.number_of_nodes())
            # print("global clustering coefficient:", nx.average_clustering(graafi))
        giant = max(nx.connected_component_subgraphs(graafi), key=len)
        # print("(giant) diameter:", nx.diameter(giant))
        # print("(giant) average path length:", nx.average_shortest_path_length(giant))
        # print("size of giant component:", giant.number_of_nodes(), "nodes")
        # print("size of giant component:", giant.number_of_edges(), "edges")
        communities = []
        for clique in nx.find_cliques(graafi):
            if len(clique) >= 3:
                communities.append(clique)
        community_edges = 0
        for community in communities:
            community_edges += (len(community)*(len(community)-1))/2
        nodes_in_communities = set(sum(communities, [])) # unique nodes
        # print("number of communities:", len(communities))
        # print("community node coverage quality measure:", len(nodes_in_communities)/graafi.number_of_nodes())
        # print("community edge coverage quality measure:", community_edges/graafi.number_of_edges())
        # print("=================================================================")

        thresholds.append(threshold)
        nodes.append(graafi.number_of_nodes())
        edges.append(graafi.number_of_edges())
        maximum_degrees.append(max(graafi.degree(), key=lambda x:x[1])[1]) # ('politiikka', 40)
        average_degrees.append(sum([i[1] for i in nx.degree(graafi)])/graafi.number_of_nodes())
        global_clustering_coefficients.append(nx.average_clustering(graafi))
        diameters.append(nx.diameter(giant)) # giant of nothing else available
        average_path_lenghts.append(nx.average_shortest_path_length(giant)) # giant of nothing else available
        giant_component_nodes.append(giant.number_of_nodes())
        giant_component_edges.append(giant.number_of_edges())
        number_of_communities.append(len(communities))
        community_node_coverage_quality_measure.append(len(nodes_in_communities)/graafi.number_of_nodes())
        community_edge_coverage_quality_measure.append(community_edges/graafi.number_of_edges())
        if ((threshold == 0 or threshold == 5 or threshold == 25 or threshold == 47)): # skip on empty graph
            
            print("\n\nthresholds                             ", thresholds[-1])
            print("\n\nnodes                                  ", nodes[-1])
            print("\n\nedges                                  ", edges[-1])
            print("\n\nmaximum_degrees                        ", maximum_degrees[-1])
            print("\n\naverage_degrees                        ", average_degrees[-1])
            print("\n\nglobal_clustering_coefficients         ", global_clustering_coefficients[-1])
            print("\n\ndiameters                              ", diameters[-1])
            print("\n\naverage_path_lenghts                   ", average_path_lenghts[-1])
            print("\n\ngiant_component_nodes                  ", giant_component_nodes[-1])
            print("\n\ngiant_component_edges                  ", giant_component_edges[-1])
            print("\n\nnumber_of_communities                  ", number_of_communities[-1])
            print("\n\ncommunity_node_coverage_quality_measure", community_node_coverage_quality_measure[-1])
            print("\n\ncommunity_edge_coverage_quality_measure", community_edge_coverage_quality_measure[-1])
                        


print("\n\nthresholds                             ", thresholds)
print("\n\nnodes                                  ", nodes)
print("\n\nedges                                  ", edges)
print("\n\nmaximum_degrees                        ", maximum_degrees)
print("\n\naverage_degrees                        ", average_degrees)
print("\n\nglobal_clustering_coefficients         ", global_clustering_coefficients)
print("\n\ndiameters                              ", diameters)
print("\n\naverage_path_lenghts                   ", average_path_lenghts)
print("\n\ngiant_component_nodes                  ", giant_component_nodes)
print("\n\ngiant_component_edges                  ", giant_component_edges)
print("\n\nnumber_of_communities                  ", number_of_communities)
print("\n\ncommunity_node_coverage_quality_measure", community_node_coverage_quality_measure)
print("\n\ncommunity_edge_coverage_quality_measure", community_edge_coverage_quality_measure)

plt.clf()
plt.plot(nodes)
#plt.plot(edges)
plt.plot(maximum_degrees, linestyle="--")
plt.plot(average_degrees, linestyle="-.")
plt.plot(global_clustering_coefficients, linestyle=":")
plt.plot(diameters)
plt.plot(average_path_lenghts, linestyle="--")
plt.plot(giant_component_nodes, linestyle="-.")
#plt.plot(giant_component_edges)
plt.plot(number_of_communities, linestyle=":")
plt.plot(community_node_coverage_quality_measure)
plt.plot(community_edge_coverage_quality_measure, linestyle="--")


plt.legend(["nodes", "maximum_degrees", "average_degrees", "global_clustering_coefficients", "diameters", "average_path_lenghts", "giant_component_nodes", "number_of_communities", "community_node_coverage_quality_measure", "community_edge_coverage_quality_measure"], loc="upper right")
plt.xlabel("treshold")

#plt.show()
plt.savefig("final1_polyglot.pdf", dpi=500)


plt.clf() #clear figure
plt.plot(edges, linestyle="--")
plt.plot(giant_component_edges)
plt.legend(["edges", "giant_component_edges"], loc="upper right")
plt.xlabel("threshold")
plt.yscale('log')
#plt.show()
plt.savefig("final2_polyglot.pdf", dpi=500)



