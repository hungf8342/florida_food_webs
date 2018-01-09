#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:56:12 2017

@author: Frances
"""
#import community
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as scist
from networkx.utils import is_string_like, open_file, make_str
import shlex
dry=nx.read_pajek("baydry.paj")
wet=nx.read_pajek("baywet.paj")

d={}
producers=["2um Spherical Phytoplankt","Synedococcus","Oscillatoria","Small Diatoms (<20um)",
           "Big Diatoms (>20um)","Dinoflagellates","Other Phytoplankton","Benthic Phytoplankton",
           "Thalassia","Halodule","Syringodium","Roots","Drift Algae","Epiphytes",
           "Free Bacteria","Water Flagellates","Water Cilitaes"]
invertebrates=["Acartia Tonsa","Oithona nana","Paracalanus","Other Copepoda","Meroplankton",
               "Other Zooplankton","Benthic Flagellates","Benthic Ciliates","Meiofauna",
               "Sponges","Coral","Other Cnidaridae","Echinoderma","Bivalves","Detritivorous Gastropods",
               "Epiphytic Gastropods","Predatory Gastropods","Detritivorous Polychaetes",
               "Predatory Polychaetes","Suspension Feeding Polych","Macrobenthos",
               "Benthic Crustaceans","Detritivorous Amphipods","Herbivorous Amphipods",
               "Isopods","Herbivorous Shrimp","Predatory Shrimp","Pink Shrimp","Thor Floridanus",
               "Lobster","Detritivorous Crabs","Omnivorous Crabs","Predatory Crabs",
               "Callinectus sapidus","Stone Crab"]
fishes=["Sharks","Rays","Tarpon","Bonefish","Sardines","Anchovy","Bay Anchovy",
        "Lizardfish","Catfish","Eels","Toadfish","Brotalus","Halfbeaks","Needlefish",
        "Other Killifish","Goldspotted killifish","Rainwater killifish","Snook",
        "Sailfin Molly","Silverside","Other Horsefish","Gulf Pipefish","Dwarf Seahorse",
        "Grouper","Jacks","Pompano","Other Snapper","Gray Snapper","Mojarra",
        "Grunt","Porgy","Pinfish","Scianids","Spotted Seatrout","Red Drum",
        "Spadefish","Parrotfish","Mackerel","Mullet","Barracuda","Blennies",
        "Code Goby","Clown Goby","Flatfish","Filefishes","Puffer",
        "Other Pelagic Fishes","Other Demersal Fishes"]
reptiles=["Crocodiles","Loggerhead Turtle","Green Turtle","Hawksbill Turtle"]
mammals=["Dolphin","Manatee"]
birds=["Loon","Greeb","Pelican","Comorant","Big Herons & Egrets",
       "Small Herons & Egrets","Ibis","Roseate Spoonbill","Herbivorous Ducks",
       "Omnivorous Ducks","Predatory Ducks","Raptors","Gruiformes",
       "Small Shorebirds","Gulls & Terns","Kingfisher"]
detritus=["Water POC","Benthic POC","DOC"]
others=["Input","Output","Respiration"]


for p in producers:
    d[p]="producers"
for i in invertebrates:
    d[i]="invertebrates"
for f in fishes:
    d[f]="fishes"
for r in reptiles:
    d[r]="reptiles"
for m in mammals:
    d[m]="mammals"
for b in birds:
    d[b]="birds"
for a in detritus:
    d[a]="detritus"
for o in others:
    d[o]="others"

nx.set_node_attributes(dry,name='category',values=d)
nx.set_node_attributes(wet,name='category',values=d)

dry_simp=nx.Graph(dry)
wet_simp=nx.Graph(wet)
dry_dir_simp=nx.DiGraph(dry)
wet_dir_simp=nx.DiGraph(wet)

#pagerank for weighted wet directed
ew_pgrk=nx.pagerank(wet_dir_simp, max_iter=10000,weight='weight')
filtered_ew={k: i for k, i in ew_pgrk.items() if i > 0.0015 and i < 0.0035}

names  = [str(v) for v in filtered_ew.keys()][1:-1]
values = [float(v) for v in filtered_ew.values()][1:-1]
color_dict_wet=nx.get_node_attributes(wet_simp,'category')
colorssd_wet =[color_dict_wet[v] for v in names]


eig_wet=sns.barplot(x=names,y=values,hue=colorssd_wet,dodge=False,palette=
                    dict(mammals="#9b59b6", fishes="#3498db", birds="#95a5a6",
                         reptiles="#cc0066",detritus="#993300",invertebrates="#009933",
                         others ="#33ccff",producers="#00cc99"))
eig_wet.set_xticklabels(eig_wet.get_xticklabels(),rotation=80)
eig_wet.set_title("Predators: Wet Season")
eig_wet.grid(b=True, which='major')
eig_wet.set(ylim=(0.0015, 0.0035))

#pagerank for weighted dry directed
ed_pgrk = nx.pagerank(dry_dir_simp, weight='weight')
filtered_ed={k: i for k, i in ed_pgrk.items() if i>0.003 and i<0.0053}

namesd  = [str(v) for v in filtered_ed.keys()][1:-1]
valuesd = [float(v) for v in filtered_ed.values()][1:-1]
color_dict=nx.get_node_attributes(dry_simp,'category')
colorssd =[color_dict[v] for v in namesd]

eig_dry=sns.barplot(x=names,y=values,hue=colorssd_wet,dodge=False,palette=
                    dict(mammals="#9b59b6", fishes="#3498db", birds="#95a5a6",
                         reptiles="#cc0066",detritus="#993300",invertebrates="#009933",
                         others ="#33ccff",producers="#00cc99"))
eig_dry.set_xticklabels(eig_dry.get_xticklabels(),rotation=80)
eig_dry.set_title("Predators: Dry Season")
eig_dry.grid(b=True, which='major')
eig_dry.set(ylim=(0.0028, 0.005))

scist.chisquare([float(v) for v in ew_pgrk.values()]*1000,[float(v) for v in ed_pgrk.values()]*1000)

#reverse,reverse!
prod_dry=nx.reverse(dry)
prod_wet=nx.reverse(wet)

prod_dry_simp=nx.Graph(prod_dry)
prod_wet_simp=nx.Graph(prod_wet)
prod_dry_dir_simp=nx.DiGraph(prod_dry)
prod_wet_dir_simp=nx.DiGraph(prod_wet)

#pagerank for weighted wet directed
prod_ew_pgrk=nx.pagerank(prod_wet_dir_simp, max_iter=10000,weight='weight')
prod_filtered_ew={k: i for k, i in prod_ew_pgrk.items() if i>0.0049 and i<0.025}

prod_names  = [str(v) for v in prod_filtered_ew.keys()][1:-1]
prod_values = [float(v) for v in prod_filtered_ew.values()][1:-1]
colorssd_wet =[color_dict_wet[v] for v in prod_names]

prod_eig_wet=sns.barplot(x=names,y=values,hue=colorssd_wet,dodge=False,palette=
                    dict(mammals="#9b59b6", fishes="#3498db", birds="#95a5a6",
                         reptiles="#cc0066",detritus="#993300",invertebrates="#009933",
                         others ="#33ccff",producers="#00cc99"))
prod_eig_wet.set_xticklabels(prod_eig_wet.get_xticklabels(),rotation=80)
prod_eig_wet.set_title("Prey: Wet Season")
prod_eig_wet.grid(b=True, which='major')
prod_eig_wet.set(ylim=(0.003, 0.025))

#pagerank for weighted dry directed
prod_ed_pgrk = nx.pagerank(prod_dry_dir_simp, weight='weight')
prod_filtered_ed={k: i for k, i in prod_ed_pgrk.items() if i>0.0049 and i<0.025}

prod_namesd  = [str(v) for v in prod_filtered_ed.keys()][1:-1]
prod_valuesd = [float(v) for v in prod_filtered_ed.values()][1:-1]
colorssd =[color_dict[v] for v in prod_namesd]

prod_eig_dry=sns.barplot(x=names,y=values,hue=colorssd_wet,dodge=False,palette=
                    dict(mammals="#9b59b6", fishes="#3498db", birds="#95a5a6",
                         reptiles="#cc0066",detritus="#993300",invertebrates="#009933",
                         others ="#33ccff",producers="#00cc99"))
prod_eig_dry.set_xticklabels(prod_eig_dry.get_xticklabels(),rotation=80)
prod_eig_dry.set_title("Prey: Dry Season")
prod_eig_dry.grid(b=True, which='major')
prod_eig_dry.set(ylim=(0.003, 0.025))