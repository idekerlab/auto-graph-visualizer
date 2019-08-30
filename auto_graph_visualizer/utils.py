import igraph
import seaborn as sns


def getCommunityEdge(g, community):
    num_edges = g.ecount()
    edge_community = [-1]*num_edges
    comms = community
    sources = [i for i, _ in g.get_edgelist()]
    targets = [j for _, j in g.get_edgelist()]
    for i in range(num_edges):
        sidx = sources[i]
        tidx = targets[i]
        source = comms[sidx]
        target = comms[tidx]

        if source == target:
            edge_community[i] = source
    return edge_community


def communityToColors(members):
    basecolor = '#AAAAAA'
    num_members = len(members)
    num_communities = max(members)+1
    colors = [basecolor]*num_members

    colorp = sns.color_palette("hls", num_communities)

    colorpalette = [rgb2hex(int(a[0]*255), int(a[1]*255),
                            int(a[2]*255)) for a in colorp]

    for i in range(num_members):
        newcolor = colorpalette[members[i]]
        if(members[i] == -1):
            newcolor = basecolor
        colors[i] = newcolor
    return colors


def rgb2hex(r, g, b):
    color = (r, g, b)
    html_color = '#%02X%02X%02X' % (color[0], color[1], color[2])
    return html_color


def search_interaction(df, src, tgt):
    if len(df[(df['source'] == src) & (df['target'] == tgt)]):
        return df[(df['source'] == src) & (df['target'] == tgt)]['interaction'].values[0]
    else:
        return df[(df['source'] == tgt) & (df['target'] == src)]['interaction'].values[0]
