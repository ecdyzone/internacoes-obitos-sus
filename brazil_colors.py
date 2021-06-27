"""
module to create matplotlib colormaps for brazilian states/regions

######## HOW TO USE ########

1. The official order of states/regions is ok?      --> use get_brazil_colors()
2. Any case that doesn't follow the official order? --> use create_ordered_colormap()

######## EXAMPLES ########

1.
creating dictionaries colors:
brazil_colormaps, color_of_each_state_or_region = get_brazil_colors()

brazil_colormaps[key] is an instance of matplotlib.colors.ListedColormap
brazil_colormaps[key].colors is a numpy array with RGB code for the choosen region or state
color_of_each_state_or_region is a dict with (key,value) = (state or region name, color as array)

pandas.Dataframe.plot(colormap = brazil_colormaps['States'])
    here, brazil_colormaps['States'] is a matplotlib.colors.ListedColormap with 27 colors in the official order

sns.violinplot(palette = brazil_colormaps['Regions']).colors)
    here, brazil_colormaps['Regions']).colors is a matplotlib.colors.ListedColormap with 27 colors in the official order

pandas.Dataframe.plot(color = color_of_each_state_or_region['Nordeste'])
    here, color_of_each_state_or_region['Nordeste'] is a numpy array with the RGB color of chosen state or region

2.
my_colormap = create_ordered_colormap(index=['Nordeste', 'Sul', 'São Paulo'])
pandas.Dataframe.plot(colormap = my_colormap)

my_colormap2 = create_ordered_colormap(index=df.index, output_as_list=True)
sns.catplot(palette=my_colormap2)


##### WHAT'S INSIDE THE DICTIONARIES #####

## brazil_colormaps =
# {'Norte': <matplotlib.colors.ListedColormap at 0x7f37a7043670>,
#  'Nordeste': <matplotlib.colors.ListedColormap at 0x7f37a7043610>,
#  'Sudeste': <matplotlib.colors.ListedColormap at 0x7f37a7043460>,
#  'Sul': <matplotlib.colors.ListedColormap at 0x7f37a70436a0>,
#  'Centro Oeste': <matplotlib.colors.ListedColormap at 0x7f37a7043730>,
#  'Regions': <matplotlib.colors.ListedColormap at 0x7f37a7043820>,
#  'States': <matplotlib.colors.ListedColormap at 0x7f37a7043850>}

## color_of_each_state_or_region (showing first 3 items of the 32 items (27 state + 5 regions))
# {'Rondônia': array([0.77922338, 0.91323337, 0.75180315, 1.        ]),
#  'Acre': array([0.68104575, 0.87189542, 0.65620915, 1.        ]),
#  'Amazonas': array([0.5739331 , 0.82417532, 0.56061515, 1.        ]),
#  .... }
"""



#from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np

states_per_region = {'Norte': 7, 'Nordeste': 9, 'Sudeste': 4, 'Sul': 3, 'Centro Oeste': 4}

states_to_regions_oficial_order = {
 'Rondônia': 'Norte',
 'Acre': 'Norte',
 'Amazonas': 'Norte',
 'Roraima': 'Norte',
 'Pará': 'Norte',
 'Amapá': 'Norte',
 'Tocantins': 'Norte',
 'Maranhão': 'Nordeste',
 'Piauí': 'Nordeste',
 'Ceará': 'Nordeste',
 'Rio Grande do Norte': 'Nordeste',
 'Paraíba': 'Nordeste',
 'Pernambuco': 'Nordeste',
 'Alagoas': 'Nordeste',
 'Sergipe': 'Nordeste',
 'Bahia': 'Nordeste',
 'Minas Gerais': 'Sudeste',
 'Espírito Santo': 'Sudeste',
 'Rio de Janeiro': 'Sudeste',
 'São Paulo': 'Sudeste',
 'Paraná': 'Sul',
 'Santa Catarina': 'Sul',
 'Rio Grande do Sul': 'Sul',
 'Mato Grosso do Sul': 'Centro Oeste',
 'Mato Grosso': 'Centro Oeste',
 'Goiás': 'Centro Oeste',
 'Distrito Federal': 'Centro Oeste'}

def get_brazil_colors(stronger_colors=False):
    """
    :param stronger_colors: try stronger_colors=True if you need more contrast between colors
    :return: two dictionaries: the first with colormaps, and another with (key,value) = (state or region, its own color)

    (for more, see module brazil_colors.py docstring)
    """

    colors_to_parse = ['Greens', 'Reds','Purples', 'Blues', 'YlOrBr'] # Maybe 'Oranges' is better than 'YlOrBr'

    cmap5 = [] # 5 colors list for the 5 Regions colormap
    cmap27 = [] # 27 colors list for the 27 Regions colormap
    brazil_colormaps = {} # dictionary to aggregate all the colormaps
    
    for position, (region, number_of_states) in enumerate(states_per_region.items()):
    
        if stronger_colors:
            step = np.linspace(0.4,1,number_of_states)
        
        else: # smooth colors
            if number_of_states > 5:
                step = np.linspace(0.25,0.75,number_of_states)
            else:
                step = np.linspace(0.35,0.65,number_of_states)
    
        colors_of_each_region = plt.get_cmap(colors_to_parse[position])(step)
        
        cmap5.extend(plt.get_cmap(colors_to_parse[position])([0.6]))
        cmap27.extend(colors_of_each_region)
        tmp_list = [] # temporary list to be passed to ListedColormap
        tmp_list.extend(colors_of_each_region)
        brazil_colormaps[region] = ListedColormap(colors=tmp_list, name=f'{region}_cores')

    brazil_colormaps['Regions'] = ListedColormap(colors=cmap5, name='br_regions_5_colors')
    brazil_colormaps['States'] = ListedColormap(colors=cmap27, name='br_states_27_colors')
    
    color_of_each_state_or_region = dict(zip(states_to_regions_oficial_order.keys(), brazil_colormaps['States'].colors))
    individual_color_per_region = dict(zip(states_per_region.keys(), brazil_colormaps['Regions'].colors))
    color_of_each_state_or_region.update(individual_color_per_region)

    # returns two dictionaries: one with colormaps,
    # and the other with (key,value) = (state or region, its own color)
    return brazil_colormaps, color_of_each_state_or_region



def create_ordered_colormap(index, output_as_list=False, replace_state_color_by_region=False):
    """
    :param index: pandas Index or list-like object with the desired order of colors
    :param output_as_list: default output is a matplotlib cmap <matplotlib.colors.ListedColormap>
    :param replace_state_color_by_region: if True, all states of a region will have the same color.
                                          if False, each state keeps its own color.
    :return: list or matplotlib colormap

    create_ordered_colormap() uses the color_of_each_state_or_region dictionary the create a new Colormap or list
with given order.

    (for more, see module brazil_colors.py docstring)
    """

    new_colors = []
    
    if replace_state_color_by_region:
        for i in index:
            state_to_region = states_to_regions_oficial_order.get(i)
            region_color = color_of_each_state_or_region.get(state_to_region)
            new_colors.append(region_color)
    else:
        for i in index: 
            own_color = color_of_each_state_or_region.get(i)
            new_colors.append(own_color)
            
    
    if output_as_list:
        return new_colors
        
    else:
        return ListedColormap(colors=new_colors)
    

brazil_colormaps, color_of_each_state_or_region = get_brazil_colors()
# brazil_colormaps, color_of_each_state_or_region = get_brazil_colors(stronger_colors=True)
# create_ordered_colormap(index, output_as_list=False, replace_state_color_by_region=False)
