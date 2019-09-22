from . import resource_manager


cyconfig = resource_manager.get_visual_style()

nodesizeprop = cyconfig['cyVisualProperties'][1]['mappings']['NODE_SIZE']['definition']
nodesizeprop = nodesizeprop.split(',')
tmp = nodesizeprop[0].split('=')
tmp[1] = 'closeness'
tmp = '='.join(tmp)
nodesizeprop[0] = tmp
tmp = nodesizeprop[9].split('=')
tmp[2] = str(100000)
tmp = '='.join(tmp)
nodesizeprop[9] = tmp
nodesizeprop = ','.join(nodesizeprop)
cyconfig['cyVisualProperties'][1]['mappings']['NODE_SIZE']['definition'] = nodesizeprop

# print(nodesizeprop)
