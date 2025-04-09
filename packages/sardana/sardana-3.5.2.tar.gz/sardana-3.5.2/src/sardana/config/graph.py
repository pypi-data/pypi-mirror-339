# -*- coding: utf-8 -*-

##############################################################################
##
## This file is part of Sardana
##
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2019 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""
Functionality to produce a graph of a Sardana Pool configuration.
"""


from typing import Tuple, Set, Optional

import sys
import click
import graphviz  # type: ignore
from ruamel.yaml import YAML
import tango

from .dump import dump_sardana_config


TYPE_COLORS = {
    "Motor": "lightgray",
    "CTExpChannel": "pink",
    "ZeroDExpChannel": "lightblue",
    "OneDExpChannel": "lightblue",
    "TwoDExpChannel": "lightblue",
    "PseudoMotor": "yellow",
    "PseudoCounter": "orange",
    "TriggerGate": "white",
    "IORegister": "violet",
}


NODE_STYLE = {"style": "filled"}


Edge = Tuple[str, str]


def get_subgraph(edges: Set[Edge], node: str) -> Set[Edge]:
    """
    Take a list of edges and a node name.
    Return only the edges that is connected to the node (to any degree)
    """
    subgraph = set()
    for a, b in edges:
        if a == node:
            subgraph.update(get_subgraph_right(edges, a))
        elif b == node:
            subgraph.update(get_subgraph_left(edges, b))
    return subgraph


def get_subgraph_left(edges: Set[Edge], node: str):
    subgraph = set()
    for a, b in edges:
        if b == node:
            subgraph.add((a, b))
            subgraph.update(get_subgraph_left(edges, a))
    return subgraph


def get_subgraph_right(edges: Set[Edge], node: str) -> Set[Edge]:
    subgraph = set()
    for a, b in edges:
        if a == node:
            subgraph.add((a, b))
            subgraph.update(get_subgraph_right(edges, b))
    return subgraph


def make_pool_graph(title: str, pool_config: dict, element: Optional[str] = None):

    g = graphviz.Digraph("graph", comment='Sardana')
    g.attr(rankdir="LR", labelloc="t", fontsize="20.0")
    if element:
        g.attr(label=f"{title} ({element})")
    else:
        g.attr(label=title)

    # Extract all the interesting info from the configuration
    controllers = []
    pseudo_controllers = []
    elements = []
    pseudo_elements = []
    edges = set()

    for ctrlname, ctrl in pool_config.get("controllers", {}).items():
        tooltip = f"Type: {ctrl['type']}\nClass: {ctrl['python_class']}"
        attrs = {"fillcolor": TYPE_COLORS.get(ctrl["type"]), "tooltip": tooltip}
        if ctrl["type"].startswith("Pseudo"):
            pseudo_controllers.append((ctrlname, attrs))
        else:
            controllers.append((ctrlname, attrs))
        for role, pel in ctrl.get("physical_roles", {}).items():
            edges.add((pel, ctrlname))

        for elname, el in ctrl.get("elements", {}).items():
            if ctrl["type"].startswith("Pseudo"):
                pseudo_elements.append((elname, attrs))
            else:
                elements.append((elname, attrs))
            edges.add((ctrlname, elname))

    # Now we have all connections
    if element:
        # Filter out everything not connected to the given element
        edges = get_subgraph(edges, element)
    all_nodes = set(sum(edges, ()))

    # Build the graph
    with g.subgraph(name="Controllers",
                    node_attr={"shape": "box", **NODE_STYLE}) as cs:
        cs.attr(rank="same")
        for name, attrs in controllers:
            if name in all_nodes:
                cs.node(name, **attrs,
                        penwidth="2" if name == element else None)

    with g.subgraph(name="Elements", node_attr={**NODE_STYLE}) as es:
        es.attr(rank="same")
        for name, attrs in elements:
            if name in all_nodes:
                es.node(name, **attrs,
                        penwidth="2" if name == element else None)

    with g.subgraph(name="Pseudo Controllers",
                    node_attr={"shape": "box", **NODE_STYLE}) as pcs:
        for name, attrs in pseudo_controllers:
            if name in all_nodes:
                pcs.node(name, **attrs,
                         penwidth="2" if name == element else None)

    with g.subgraph(name="Pseudo Elements", node_attr={**NODE_STYLE}) as pes:
        for name, attrs in pseudo_elements:
            if name in all_nodes:
                pes.node(name, **attrs,
                         penwidth="2" if name == element else None)

    for a, b in edges:
        g.edge(a, b)

    return g


@click.option("-c", "--config", type=click.File("r"), default=None,
              help="YAML sardana config file")
@click.option("-m", "--macroserver", help="Name of macroserver device")
@click.option("-p", "--pool", help="Config name of of pool to use")
@click.option("-e", "--element", help="Name of an element to filter for")
@click.option("-f", "--image-format", help="Output image format, e.g. 'svg'",
              default="svg")
@click.option("-o", "--output", help="Output image filename")
def graph_cmd(config, macroserver, pool, element, image_format, output):
    """
    Create a directed graph of all controllers and elements in a pool.
    If pool_name is not given, just render the first pool.
    The direction is such that "higher level" things are further right.
    E.g. motor controller -> motor -> pseudo controller -> pseudo motor.
    So "information" flows left->right

    If no config file is given, the config is taken from the local
    conrol system.

    Optionally an element may be given. In that case the graph will
    be limited to only elements that are connected to the element in
    some way. E.g. for a pseudo controller, all physical elements will
    be shown, together with their controllers etc. Also, all pseudo
    elements, along with any further pseudos taking them as inputs.
    """
    yaml = YAML()
    if config:
        config = yaml.load(config)
    else:
        if not macroserver:
            sys.exit("You must specify a config file or a macroserver device/alias")
        db = tango.Database()
        config = dump_sardana_config(db, macroserver)

    for poolname, poolconfig in config["pools"].items():
        if not pool or poolname.lower() != pool.lower():
            break
    else:
        raise RuntimeError("Could not find a matching pool!")

    g = make_pool_graph(poolname, poolconfig, element)
    if output:
        with open(output, "wb") as f:
            f.write(g.pipe(format=image_format))
    else:
        print(str(g))


if __name__ == "__main__":

    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(
        description="""
        This script takes a sardana configuration file, and builds a
        visual graph representation of it using grapviz syntax.
        Optionally it can render an image file of the graph.
        """
    )
    parser.add_argument("-c", "--config", type=FileType(), default=None,
                        help="YAML sardana config file")
    parser.add_argument("-m", "--ms", help="Name of macroserver")
    parser.add_argument("-p", "--pool", help="Name of of pool to use")
    parser.add_argument("-e", "--element", help="Name of an element to filter for")
    parser.add_argument("-f", "--format", help="Output image format, e.g. 'svg'",
                        default="svg")
    parser.add_argument("-o", "--out", help="Output image filename")

    args = parser.parse_args()

    graph_cmd(args.config, args.ms, args.pool, args.element, args.format, args.out)
