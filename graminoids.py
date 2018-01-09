# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import community
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as scist
from networkx.utils import is_string_like, open_file, make_str

import shlex
dry=nx.read_pajek("ngramdry.paj")
wet=nx.read_pajek("gramwet.paj")

#label categories for dry ecosystem
d={}
producers=["Periphyton","Macrophytes","Utricularia","Floating Veg."]
microbial=["Living Sediments","Living POC"]
invertebrates=["Apple snail","Freshwater Prawn","Crayfish","Mesoinverts","Other Macroinverts",
               "Large Aquatic Insects","Terrestrial Inverts","Fishing spider"]
fishes=["Gar","Shiners & Minnows","Chubsuckers","Catfish","Flagfish","Topminnows","Bluefin killifish",
        "Killifishes","Mosquitofishes","Poecilids","Pigmy Sunfish","Bluespotted Sunfish","Warmouth",
        "Dollar Sunfish","Redear Sunfish", "Spotted sunfish","Other Centrarchids","Largemouth Bass",
        "Cichlids","Other Large Fishes","Other Small Fishes"]
repsamphs=["Salamanders","Salamander larvae","Large frogs","Medium frogs","Small frogs",
           "Tadpoles","Turtles","Snakes","Lizards","Alligators"]
mammals=["Muskrats","Rats&Mice","Rabbits","Raccoons","Opossum","Otter","Mink","W-T Deer","Bobcat",
         "Panthers"]
birds=["Grebes","Bitterns","Ducks","Snailkites","Nighthawks","Gruiformes","CSSsparrow","Passerines"]
detritus=["Sediment Carbon","Labile Detritus","Refractory Detritus"]

for p in producers:
    d[p]="producers"
for b in microbial:
    d[b]="livingMicrobe"
for i in invertebrates:
    d[i]="inverts"
for r in repsamphs:
    d[r]="repamph"
for m in mammals:
    d[m]="mammals"
for b in birds:
    d[b]="birds"
for a in detritus:
    d[a]="detritus"
for f in fishes:
    d[f]="fish"

nx.set_node_attributes(dry,name='category',values=d)
nx.set_node_attributes(wet,name='category',values=d)

dry_simp=nx.Graph(dry)
wet_simp=nx.Graph(wet)
dry_dir_simp=nx.DiGraph(dry)
wet_dir_simp=nx.DiGraph(wet)

#pagerank for weighted wet directed 
ew_pgrk=nx.pagerank(wet_dir_simp, max_iter=10000,weight='weight')
filtered_ew={k: i for k, i in ew_pgrk.items() if i>0.0031 and i<0.0053}

names  = [str(v) for v in filtered_ew.keys()]
values = [float(v) for v in filtered_ew.values()]
color_dict_wet=nx.get_node_attributes(wet_simp,'category')
colorssd_wet =[color_dict_wet[v] for v in names]


eig_wet=sns.barplot(x=names,y=values,hue=colorssd_wet,dodge=False,palette=
                    dict(mammals="#9b59b6", fish="#3498db", birds="#95a5a6",
                         repamph="#cc0066",detritus="#993300",inverts="#009933",
                         livingMicrobe="#33ccff",producers="#00cc99"))
eig_wet.set_xticklabels(eig_wet.get_xticklabels(),rotation=80)
eig_wet.set_title("Predators: Wet Season")
eig_wet.grid(b=True, which='major')
eig_wet.set(ylim=(0.003, 0.005))

#pagerank for weighted dry directed
ed_pgrk = nx.pagerank(dry_dir_simp, weight='weight')
filtered_ed={k: i for k, i in ed_pgrk.items() if i>0.003 and i<0.0053}

namesd  = [str(v) for v in filtered_ed.keys()][1:-1]
valuesd = [float(v) for v in filtered_ed.values()][1:-1]
color_dict=nx.get_node_attributes(dry_simp,'category')
colorssd =[color_dict[v] for v in namesd]

eig_dry=sns.barplot(x=namesd,y=valuesd,hue=colorssd,dodge=False,palette=
                    dict(mammals="#9b59b6", fish="#3498db", birds="#95a5a6",
                         repamph="#cc0066",detritus="#993300",inverts="#009933",
                         livingMicrobe="#33ccff",producers="#00cc99"))
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

prod_eig_wet=sns.barplot(x=prod_names,y=prod_values,hue=colorssd_wet,dodge=False,palette=
                    dict(mammals="#9b59b6", fish="#3498db", birds="#95a5a6",
                         repamph="#cc0066",detritus="#993300",inverts="#009933",
                         livingMicrobe="#33ccff",producers="#00cc99"))
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

prod_eig_dry=sns.barplot(x=prod_namesd,y=prod_valuesd,hue=colorssd,dodge=False,palette=
                    dict(mammals="#9b59b6", fish="#3498db", birds="#95a5a6",
                         repamph="#cc0066",detritus="#993300",inverts="#009933",
                         livingMicrobe="#33ccff",producers="#00cc99"))
prod_eig_dry.set_xticklabels(prod_eig_dry.get_xticklabels(),rotation=80)
prod_eig_dry.set_title("Prey: Dry Season")
prod_eig_dry.grid(b=True, which='major')
prod_eig_dry.set(ylim=(0.003, 0.025))

