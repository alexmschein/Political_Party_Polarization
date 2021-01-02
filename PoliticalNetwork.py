#Alexandra Schein
#Network Science Final Project
#Political Network Analysis
#5/14/19

import csv
import networkx as nx
import matplotlib.pyplot as plt
plt.style.use('ggplot')

cong_to_votes = {} #dict of dicts, {congress1: {{id1:{1:1, 2:1, 3:6}, id2:{1:1, 2:6, 3:6}}},
                                    #congress2: {id3:{1:1, 2:1, 3:6}, id4:{1:1, 2:6, 3:6}}}
fh1 = open('Hall_votes.csv', 'r')
reader1 = csv.reader(fh1, delimiter=',')

for line in reader1:

    if line[0] == 'congress':
        #header line
        pass
    elif int(line[0]) >= 95 and int(line[0]) <= 116 : #only for 95th-116th congresses
        congress = int(line[0])#which congress

        if congress not in cong_to_votes.keys():
            cong_to_votes[congress] = {}

        elif congress in cong_to_votes.keys():#update this congress with new id
            person_id = int(line[3])#icpsr
            roll = int(line[2])#the vote id
            vote = int(line[4])#how they voted

            if person_id not in cong_to_votes[congress].keys():
                cong_to_votes[congress][person_id] = {}#adding the person id

            cong_to_votes[congress][person_id][roll] = vote #adding the roll and corresponding vote


fh1.close()

cong_to_party = {} #{cong1: {id1:party, id2:party}, cong2:{id3:party} }
cong_to_name = {}
fh2 = open('Hall_members.csv', 'r')
reader2 = csv.reader(fh2, delimiter=',')

for line in reader2:
    if line[0] == 'congress':
        # header line
        pass
    elif line[1] == 'House' and int(line[0])>=95 and int(line[0]) <= 116:#congresses 95-116
        congress = int(line[0])

        if congress not in cong_to_party.keys():
            cong_to_party[congress] = {} #add new congress
            cong_to_name[congress] = {}

        elif congress in cong_to_party.keys():#update this congress with new id
            person_id = int(line[2])
            party_id = int(line[6]) # 100=dem, 200=rep
            name = str(line[9]) #LASTNAME, FirstName
            if person_id not in cong_to_party[congress].keys():
                cong_to_party[congress][person_id] = {}#adding the person
            if person_id not in cong_to_name[congress].keys():
                cong_to_name[congress][person_id] = {}


            cong_to_party[congress][person_id] = party_id
            cong_to_name[congress][person_id] = name


fh2.close()

#find year of given congress
def dates(congress):
    """
    congress: the congress we're looking at now
    return: String, first year of acting congress
    """
    c1 = 95 #from 95th congress, 1977-1979
    start = 1977
    diff = congress - c1
    new_start = start + 2*diff #every congress for two years
    newDate = str(new_start)

    return newDate

def make_net(congress, threshold):#for one congress
    """
    congress: int, the congress we're looking at
    threshold: int
    x: boolean, if True --> only link reps and dems, if False --> link all
    return: nx graph
    """

    nodes = list(cong_to_votes[congress].keys())#list of ids
    n = len(cong_to_votes[congress].keys())

    G = nx.Graph()#network for congress x
    G.add_nodes_from(nodes)#nodes = people in congress x


    for person_i in G.nodes():
        for person_j in G.nodes():
            if person_i != person_j: #avoid self loops

                party_i = 0 #will get ignored if id not found and party not identified
                party_j = 0

                #find party affiliation
                if person_i in cong_to_party[congress].keys():
                    G.nodes[person_i]['party'] = int(cong_to_party[congress][person_i])
                    party_i = int(cong_to_party[congress][person_i])

                if person_j in cong_to_party[congress].keys():
                    G.nodes[person_j]['party'] = int(cong_to_party[congress][person_j])
                    party_j = int(cong_to_party[congress][person_j])

                same_votes = 0
                same_roll = 0


                #check if they're of different parties, specifically a dem and rep
                #100 = dem, 200 = rep
                if (party_i == 200 and party_j == 100) or (party_i == 100 and party_j == 200):
                    try:
                        for roll in cong_to_votes[congress][person_i].keys():
                            if roll in cong_to_votes[congress][person_j].keys():#if they voted on the same roll
                                same_roll += 1 #number of bills they both voted on
                                if cong_to_votes[congress][person_i][roll] == cong_to_votes[congress][person_j][roll]:#if they voted the same
                                    same_votes += 1 #voted the same on the bill
                    except:
                        pass


                if same_roll > 0:
                    if same_votes/same_roll > threshold:
                        G.add_edge(person_i,person_j)

    return G

#finds the highest degree in a network and returns that ids name, party, and degree centrality
def finding_degree(G,congress):
    """
    G: nx Graph, nodes = ids of a given congress
    return: String list, name with highest degree
    """
    all_degs = nx.degree_centrality(G) #degree centrality of every node in network

    temp = list(all_degs.values())

    highest = max(temp)

    person_id = 0 #id with highest deg

    for key,val in all_degs.items():
        if val == highest:
            person_id = key

    name = cong_to_name[congress][person_id] #name with highest deg
    temp1 = cong_to_party[congress][person_id] #corresponding party
    party = ""

    if temp1 == 100:
        party = "Democrat"
    elif temp1 == 200:
        party = "Republican"

    return name + ", " + party + ", Degree Centrality: " + str(highest)


def find_party(congress, ids):
    """
    congress: int, congress we're looking at
    ids: int list, all ids of people in a given congress
    return: list, list of two lists where R = [republicans] and D = [democrats]
    """
    parties = []
    D = [] #democrats
    R = [] #republicans

    for i in ids:
        try:
            if cong_to_party[congress][i] == 100: #dem
                D.append(i)
            elif cong_to_party[congress][i] == 200: #rep
                R.append(i)
        except:
            pass

    parties.append(D)
    parties.append(R)

    return parties

#creates a bipartite network where democrats are "actors" and republicans are "movies"

def make_bipartite(congress, threshold):
    """
    congress: int, congress we're looking at
    threshold: int
    return: bipartite betwork B
    """

    nodes = list(cong_to_votes[congress].keys())#nodes = ids
    n = len(cong_to_votes[congress].keys())
    B = nx.Graph() #bipartite graph
    E = [] #list of edges that get connected between reps and dems

    parties = find_party(congress,nodes) # [ [dem ids], [rep ids] ]
    D = parties[0] #list of dem ids
    R = parties[1] #list of rep ids

    B.add_nodes_from(D, bipartite=0) #actors
    B.add_nodes_from(R, bipartite=1) #movies

    same_roll = 0
    same_vote = 0

    for person_i in D:
        for person_j in R:
            for roll in cong_to_votes[congress][person_i].keys():
                try:
                    if roll in cong_to_votes[congress][person_j].keys():#if they voted on the same roll
                        same_roll += 1
                        if cong_to_votes[congress][person_i][roll] == cong_to_votes[congress][person_j][roll]:#if they voted the same
                            same_vote += 1
                except:
                    pass

        if same_roll > 0:
            if same_vote/same_roll > threshold:
                E.append((person_i, person_j))

    B.add_edges_from(E)

    return B


#AVERAGE DEGREE. compare congresses 95-116 over time, only connecting reps and dems
avg_degs = [] # <k> for every congress
x_axis = list(cong_to_party.keys())#list of congresses
x_n = len(cong_to_party.keys())

for i in range(x_n): #find starting dates of each congress
    date_i = dates(x_axis[i])
    x_axis[i] = str(x_axis[i]) + ": " + "\n" + date_i

congress = 95
while congress <= 116: #looking at congresses 95-116
    G = make_net(congress, 0.4)
    deg = (2*G.number_of_edges())/G.number_of_nodes()
    avg_degs.append(deg)

    #finds the congressperson with the highest <k> i.e. votes the most similarly to opposing party
    imp_people = finding_degree(G,congress)
    print(imp_people)

    congress += 1

#plot average degree as a function of congress
plt.plot(x_axis,avg_degs,'o-', alpha=0.8)
plt.xlabel('Congress')
plt.ylabel('<k>')
#plt.xticks(rotation=90)
plt.tick_params(labelsize=5)
title = 'How Similarly Republicans and Democrats Vote'
plt.title(title)
name = 'Degree_allParties.pdf'
plt.savefig(name)
plt.clf()


#finding threshold for 95th congress
xs = []
ys = []
for threshold in [0.1*i for i in range(1,10)]:
    G = make_net(95,threshold)
    deg = (2*G.number_of_edges())/G.number_of_nodes()
    print(threshold)
    xs.append(threshold)
    ys.append(deg)

plt.plot(xs,ys,'o', alpha=0.8)

plt.xlabel('Threshold')
plt.ylabel('<k>')
title = 'Threshold Analysis for the 95th Congress'
plt.title(title)
name = 'ThresholdAnalysis95.pdf'
plt.savefig(name)
plt.clf()
