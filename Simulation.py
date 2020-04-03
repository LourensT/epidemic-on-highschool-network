from Distribution import Distribution
from PIL import Image
import matplotlib.pyplot as plt
import random
from collections import deque
from scipy import stats
import numpy as np
import os
import networkx as nx
import networkx.drawing

class Simulation:
    def __init__(self, p, network):
        self.p = p
        self.network = network
        self.network_dicts = nx.convert.to_dict_of_dicts(self.network) #convert to dictionaryform
        self.N = len(set(self.network_dicts.keys()))
        self.distr = Distribution(stats.bernoulli(self.p))
        print("transmission-probability: {}, populationsize: {}".format(self.p, self.N))

    def simulate(self, verbose=False, makeGIF=False):

        simres = SimulationResults(self.network)

        susceptible = set(self.network_dicts.keys())
        infected = set()
        recovered = set()

        first_infect = random.sample(susceptible, 1)[0]
        susceptible.remove(first_infect)
        infected.add(first_infect)

        t=0
        while len(infected) > 0:

            assert len(susceptible) + len(infected) + len(recovered)==self.N, "incorrect populationsize"
            simres.registerState(susceptible, infected, recovered, drawGIF=makeGIF)

            #new infects
            new_infects = set()
            for person in infected:
                for friend in self.network_dicts[person].keys():
                    if friend in susceptible:
                        if self.distr.rvs():
                            new_infects.add(friend)

            #move infected to susceptible
            recovered = recovered.union(infected)
            susceptible = susceptible.difference(new_infects)
            infected = new_infects

            t+=1

        if verbose:
            print("not-infected: {}, recovered: {}, timesteps: {}".format(len(susceptible), len(recovered), t))
            simres.plotStates()

        simres.registerFinalAffected(recovered)

        return simres

class SimulationResults:
    """
    Class for storing results from Simulation, also return type
    """
    def __init__(self, network):
        self.sState = deque()
        self.iState = deque()
        self.rState = deque()
        self.tState = deque([0,])
        self.network = network
        self.pos = nx.spring_layout(network)

    def registerState(self, s, i, r, drawGIF=False):
        self.sState.append(len(s))
        self.iState.append(len(i))
        self.rState.append(len(r))
        self.tState.append(self.tState[-1]+1)

        if drawGIF:
            self.makeGIFFrame(s, i, r)

    def registerFinalAffected(self, recovered):
        self.affected = recovered

    def getSusceptipleDevelopment(self):
        return self.sState

    def getRecoveredDevelopment(self):
        return self.rState

    def getTotalTimesteps(self):
        return self.tState[-1]

    def makeGIFFrame(self, s, i, r):
        colormap = []
        for node in self.network:
            if node in r:
                colormap.append("Orange")
            elif node in i:
                colormap.append("Red")
            elif node in s:
                colormap.append("Blue")
            else:
                print("shouldnt happen")
                colormap.append("Blue")

        plt.figure(figsize=(30,20))
        nx.draw(self.network, node_color=colormap, with_labels=True, pos=self.pos, node_size=600)
        if not os.path.isdir("./GIF"):
            os.mkdir("./GIF")

        plt.savefig(os.getcwd() + "\\GIF\\frame_"+str(self.tState[-1]).zfill(3)+".png")
        plt.clf()

    def makeGIF(self, fp):
        # Create the frames
        frames = []
        imgs = [os.getcwd() + "\\GIF\\"+x for x in os.listdir(os.getcwd() + "\\GIF\\")]
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)

        # Save into a GIF file that loops forever
        frames[0].save(fp, format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=300, loop=1)

        #remove saved frames and the folder
        for img in imgs:
            os.remove(img)
        os.rmdir(os.getcwd() + "\\GIF\\")

    def plotStates(self):
        '''make plot of evoltuion of system states'''
        plt.figure(figsize=(8,6))
        plt.plot(self.sState, color='blue')
        plt.plot(self.iState, color='red')
        plt.plot(self.rState, color='green')
        #plt.title("first infect: " + str(self.firstInfect), size=10)
        plt.legend(['suspectible', 'infected', 'recovered'])
        plt.grid(True)
        plt.show()
