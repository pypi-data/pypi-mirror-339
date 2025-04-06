import networkx as nx  # version == 2.3
import pandas as pd
import requests  # HTTP Client for Python
import json  # Standard JSON library
from py2cytoscape import util as cy
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import numpy as np
from colour import Color
from itertools import combinations
from importlib.resources import files
#   load interactome from String and convert to nx Graph


#DATAPATH = files("genelens").joinpath("data/miRNET/")

class MainNet:

    def __init__(self, interactome=None):
        if not isinstance(interactome, pd.DataFrame):
            string = pd.read_csv(files("genelens").joinpath("data/miRNET/baseData/String_interactome.csv"))
            self.G = nx.from_pandas_edgelist(string, 'Source', 'Target')
        else:
            interactome = pd.DataFrame(interactome)
            assert interactome.shape[1] == 2, 'It takes two columns: "Source" and "Target"'
            assert sum(interactome.columns == ['Source', 'Target']) == 2, 'Columns names are not "Source" and "Target"'
            self.G = nx.from_pandas_edgelist(interactome, 'Source', 'Target')
            print('interactome contain ', interactome.shape[0], ' rows')

    def get_LCCnd_centrality(self):
        """
        return: sorted dict of node centrality
        """
        centrality_node = nx.betweenness_centrality(self.get_LCC())
        degree_centrality = nx.degree_centrality(self.get_LCC())
        for k, v in centrality_node.items():
            centrality_node[k] = centrality_node[k] + degree_centrality[k]
        centrality_node = {k: v for k, v in sorted(centrality_node.items(), key=lambda item: item[1], reverse=True)}

        for nods, dct in self.LCC.nodes(data=True):
            dct['BtweenCentrl'] = centrality_node[nods]

        return centrality_node

    def get_LCC(self):
        """
        return: the Largest Connected Component, as NetrworkX object
        """
        CC_G = [self.G.subgraph(c).copy() for c in nx.connected_components(self.G)]
        self.LCC = max(CC_G, key=len)
        
        #old version NetworkX
        #CC_G = sorted(nx.connected_component_subgraphs(self.G), key=len, reverse=True)
        #self.LCC = CC_G[0]


        # print(len(CC_G), 'total connected components')
        # print(len(CC_G[0].nodes), 'LCC cardinality')
        
        print('LCC was extracted')
        print(f"Total connected components={len(CC_G)}, LCC cardinality={len(self.LCC)}")

    def select_nodes(self, gene_set):
        """
        param gene_set: tissue or another gene set
        """

        self.G = self.G.subgraph(gene_set)
        if self.LCC:
            self.LCC = self.LCC.subgraph(gene_set)
    
    def minimum_connected_subgraph(self, required_nodes):
        """
        Finds the minimal connected subgraph containing the specified nodes.
        
        This implementation computes the smallest subgraph (by edge count) that:
        1. Contains all nodes from the input set
        2. Maintains connectivity between all included nodes
        
        Parameters
        ----------
        required_nodes : Union[List, Set]
        Prespecified nodes that must be included in the subgraph.
        Can be provided as either a list or set of node identifiers.
        """
        req_top_gene_dict = required_nodes.copy()
        for gene in required_nodes.keys():
            if gene not in self.LCC.nodes():
                req_top_gene_dict.pop(gene)
                print(f'{gene} absent from LCC, excluded from further analysis')

        # Create an auxiliary graph between the given vertices
        auxiliary_graph = nx.Graph()
        for u, v in combinations(req_top_gene_dict.keys(), 2):
            # Find the length of the shortest path and its edges
            path_length = nx.shortest_path_length(self.LCC, source=u, target=v, weight='weight')
            auxiliary_graph.add_edge(u, v, weight=path_length)
        
        # Construct a minimum spanning tree of the auxiliary graph
        mst = nx.minimum_spanning_tree(auxiliary_graph, weight='weight')
        
        # Expand MST edges in the original graph to a complete subgraph
        subgraph_edges = set()
        for u, v in mst.edges:
            path = nx.shortest_path(self.LCC, source=u, target=v, weight='weight')
            subgraph_edges.update(zip(path[:-1], path[1:]))

        self.mst_subgraph = self.LCC.edge_subgraph(subgraph_edges).copy()
        
        print()
        print('mst-graph was extracted')
        print(f"Initial core feature={len(req_top_gene_dict.keys())}, mst-graph cardinality={len(self.mst_subgraph)}")


def tissue_selector(ans=None, tissue_id=None):
    
    if ans is None:
        ans = int(str(input('"Human Protein Atlas"(0) or "GTEx"(1) ? ')))
    if ans == 1:
        dt = pd.read_csv(
            files("genelens").joinpath("data/miRNET/addData/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct"),
            sep='\t')  # loading med(TPM) from GTEx

        print('Gene universe is...')

        labels = sorted(dt.columns)
        index = [i for i in range(0, len(dt.columns))]

        if tissue_id is None:
            for i in index:
                print(index[i], '-----', labels[i]) 
            print("give me int, or input 'all'", sep='\n')
            tissue_id = str(input('Your choice: '))
        else:
            print(labels[int(tissue_id)], 'was used', sep=' ')

        if tissue_id != 'all':
            tissue = labels[int(tissue_id)]
            tissue_genes = set(dt['Description'][dt[tissue] > 0])
            print('your tissue is ', tissue, ' number of genes: ', len(tissue_genes))

            return tissue_genes
        else:
            return 'all'

    elif ans == 0:
        dt = pd.read_csv(
            files("genelens").joinpath("data/miRNET/addData/Hum_Atas_normal_tissue.tsv"),
            sep='\t')
        print('Gene universe is...')

        labels = sorted(list(map(str, set(dt['Tissue']))))
        index = [i for i in range(0, len(labels))]
        if tissue_id is None:
            for i in index:
                print(index[i], '-----', labels[i])
            print("give me int, or input 'all'", sep='\n')
            tissue_id = str(input('Your choice: '))
        else:
            print(labels[int(tissue_id)], 'was used', sep=' ')

        if tissue_id != 'all':
            tissue = labels[int(tissue_id)]
            tissue_genes = set(dt[(dt['Tissue'] == tissue) & (dt['Level'] != 'Not detected')]['Gene name'])
            print('your tissue is ', tissue, ' number of genes: ', len(tissue_genes))
            return tissue_genes
        else:
            return 'all'
    else:
        return tissue_selector()


class KeyNodesExtractor:

    def __init__(self, MirNet):
        self.key_nodes = dict()
        self.net = MirNet.get_LCC()
        self.node_centrality = MirNet.get_LCCnd_centrality()
        self.graph_features = {'card_LCC': [len(self.net.nodes())],
                               'n_CC': [len(list(nx.connected_component_subgraphs(self.net)))],
                               'transitivity': [nx.transitivity(self.net)],
                               'sh_path': [nx.average_shortest_path_length(self.net) / len(self.net.nodes())]}

    @staticmethod
    def inflection_finder(card_LCC, n_CC, sigma):
        """
        :param sigma: smoothing
        :param card_LCC: cardinality of the LCC
        :param n_CC: number of connected components in the Network
        :return: the index of the last key node, after the removal of which the network stops rapidly falling apart
        """

        y = gaussian_filter1d(card_LCC, sigma=sigma)
        dy = np.diff(y)  # first derivative
        idx_max_dy = np.argmax(dy)
        if card_LCC[idx_max_dy] > n_CC[idx_max_dy]:
            return KeyNodesExtractor.inflection_finder(card_LCC, n_CC, sigma + 0.2)
        else:
            return idx_max_dy

    def extraction(self):

        for k, v in self.node_centrality.items():

            if v == 0:
                break
            self.net.remove_node(k)
            if len(self.net.nodes()) == 0:
                break
            LCC_curent = sorted(nx.connected_component_subgraphs(self.net), key=len, reverse=True)[0]   # get LCC
            self.graph_features['card_LCC'].append(len(LCC_curent.nodes()))
            self.graph_features['n_CC'].append(len(list(nx.connected_component_subgraphs(self.net))))
            self.graph_features['transitivity'].append(nx.transitivity(LCC_curent))
            self.graph_features['sh_path'].append(nx.average_shortest_path_length(LCC_curent) / len(LCC_curent.nodes()))

        # find inflection point of function

        idx_max_dy = KeyNodesExtractor.inflection_finder(card_LCC=self.graph_features['card_LCC'],
                                                         n_CC=self.graph_features['n_CC'],
                                                         sigma=0.0001)

        self.graph_features['cutoff_point'] = idx_max_dy

        for i in range(0, idx_max_dy + 1):
            nods = list(self.node_centrality.keys())[i]
            self.key_nodes[nods] = self.node_centrality[nods]

        return self.key_nodes.keys()


class Targets:
    """
    The class extracts and stores the targets of one microRNA and its name
    """

    def __init__(self, path_to_miRTarBase):
        self.miR_dict = {}
        with open(path_to_miRTarBase) as interact:  # import targets from miRTarBase
            for line in interact:
                (key, val) = line.strip().split(';')
                if key in self.miR_dict:
                    self.miR_dict[key] += [val]
                else:
                    self.miR_dict[key] = [val]

    def get_targets(self, miR_name):
        """
        miRTarBase contains different forms of miRNA, for example, miR-21- can correspond to
        miR-21-3p and miR-21-5p. The function concatenates targets of all forms of miRNA and removes duplicates,
        which arise because the same target can correspond to several lines due to
        different methods of its confirmation.
        """

        miR_names = self.miR_dict.keys()
        miR_dict = self.miR_dict

        res = set()
        mir_name_app = []

        for name in miR_names:
            if miR_name in name:
                res.update(miR_dict[name])
                mir_name_app.append(name)

        if not mir_name_app:
            print('miRNA', '"{}"'.format(miR_name), 'not found, use another name')
            return 1

        print('I found a miRNA with name:', *mir_name_app)
        print('and ', len(res), 'unique targets')

        return res

#   visualisation tools

class Plots:

    def __init__(self, MirNet, KeyNodesExtractor, miR_name):
        self.miR_G = MirNet.LCC
        self.key_nodes = KeyNodesExtractor.key_nodes
        self.miR_name = miR_name
        self.centrality_node = MirNet.get_LCCnd_centrality()
        self.card_LCC = KeyNodesExtractor.graph_features['card_LCC']
        self.n_CC = KeyNodesExtractor.graph_features['n_CC']
        self.idx_max_dy = KeyNodesExtractor.graph_features['cutoff_point']

    def central_distr(self):
        miR_G = self.miR_G
        key_nodes = self.key_nodes
        mir_name = self.miR_name

        """

        :param miR_G: a Graph of miRNA
        :param key_nodes: key_nodes from MainMiRNetwork.key_nodes
        :param mir_name: miR name for saving file
        :return: visualisation hist of centrality distribution
        """

        fig = plt.figure()
        ax = fig.add_subplot()
        N, bins, patches = ax.hist([miR_G.nodes[node]['BtweenCentrl'] for node in miR_G.nodes])
        ax.set(xlabel='Centrality',
               ylabel='Count of nodes')
        ax.yaxis.label.set_size(30)
        ax.xaxis.label.set_size(30)
        ax.tick_params(labelsize=20)

        ax.axvline(key_nodes[list(key_nodes.keys())[-1]], color='red', lw='4')

        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)

        # create gradient (grey_to_red hist path
        grey = Color('#cccccc')
        colors = list(grey.range_to(Color("red"), len(bins) - 1))
        for tmp_color, tmp_patch in zip(colors, patches):
            color = str(tmp_color)
            if len(color) < 7 and color[0] == '#':
                color = color + (7 - len(color)) * color[len(color) - 1]
            tmp_patch.set_facecolor(color)

        fig.set_figwidth(8.5)
        fig.set_figheight(8.5)

        plt.tight_layout()

        plt.savefig('./result/' + mir_name + '_centrality_distr.png', dpi=250)

    def graph_to_cytoscape(self):

        miR_G = nx.Graph(self.miR_G)  # unfreezing of the graph
        centrality_node = self.centrality_node
        rem_CC = 0

        for CC in list(nx.connected_components(miR_G)):
            if len(CC) < 3:
                miR_G.remove_nodes_from(CC)
                rem_CC += 1

        print(rem_CC, ' network components with less than two nodes have been removed', end='\n')

        PORT_NUMBER = 1234
        IP = 'localhost'
        BASE = 'http://' + IP + ':' + str(PORT_NUMBER) + '/v1/'

        requests.delete(BASE + 'session')  # Delete all networks in current session

        cytoscape_network = cy.from_networkx(miR_G)
        cytoscape_network['data']['name'] = 'miR_Net'
        res1 = requests.post(BASE + 'networks', data=json.dumps(cytoscape_network))
        res1_dict = res1.json()
        new_suid = res1_dict['networkSUID']
        requests.get(BASE + 'apply/layouts/force-directed/' + str(new_suid))

        # load and apply style

        res = requests.get(BASE + 'styles/miR_Net_Styles')
        if res.status_code != 200:

            with open('./options/cytoscape_styles/miR_Net_Styles.json') as json_file:
                miR_Net_Styles = json.load(json_file)

            for mapings in range(0, len(miR_Net_Styles['mappings'])):
                if miR_Net_Styles['mappings'][mapings]['visualProperty'] == 'NODE_LABEL_FONT_SIZE':
                    miR_Net_Styles['mappings'][mapings]['points'][1]['value'] = max(centrality_node.values())
                if miR_Net_Styles['mappings'][mapings]['visualProperty'] == 'NODE_SIZE':
                    miR_Net_Styles['mappings'][mapings]['points'][1]['value'] = max(centrality_node.values())
                if miR_Net_Styles['mappings'][mapings]['visualProperty'] == 'NODE_FILL_COLOR':
                    miR_Net_Styles['mappings'][mapings]['points'][1]['value'] = max(centrality_node.values())

            # Create new Visual Style
            res = requests.post(BASE + "styles", data=json.dumps(miR_Net_Styles))

        # Apply it to current network

        requests.get(
            BASE + 'apply/styles/' + 'miR_Net_Styles' + '/' + str(new_suid))  # !Это говно почему-то не работает

    def key_nodes_extractor(self):

        card_LCC = self.card_LCC
        n_CC = self.n_CC
        idx_max_dy = self.idx_max_dy
        mir_name = self.miR_name
        """

        :param card_LCC:
        :param n_CC:
        :param idx_max_dy:
        :param mir_name:
        :return: visualisation plot of key nodes selection
        """

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(card_LCC, linewidth=4, label='Cardinality of the LCC')
        ax.plot(n_CC, linewidth=4, label='Count of CC', color='tab:green', linestyle='dashed')
        # ax.plot(idx_max_dy, card_LCC[idx_max_dy], marker='o', markersize=20, color="red")
        ax.axvline(idx_max_dy, color='red', lw='4')
        ax.minorticks_on()
        ax.grid(which='major',
                color='w',
                linewidth=1.3)
        ax.grid(which='minor',
                color='w',
                linestyle=':')
        ax.set(xlabel='Number of top nodes removed',
               ylabel='LCC cardinality / Count of CC')
        ax.legend()

        right_side = ax.spines["right"]
        right_side.set_visible(False)
        top_side = ax.spines["top"]
        top_side.set_visible(False)

        #    plt.rc('font', size=10)  # controls default text sizes
        plt.rc('axes', labelsize=30)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=20)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=20)  # fontsize of the tick labels
        plt.rc('legend', fontsize=20)  # legend fontsize
        fig.set_figwidth(8)
        fig.set_figheight(8)
        plt.tight_layout()

        plt.savefig('./result/' + mir_name + 'key_nodes_selection.png', dpi=300)
