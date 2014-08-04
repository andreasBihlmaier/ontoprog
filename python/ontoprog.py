#!/usr/bin/env python2

from __future__ import print_function

import sys
import re
import os
import argparse
import pyparsing




class SUOKIFEntity(object):
  def __init__(self, name):
    self.name = name

  def plot(self, graph):
    graph.add_node(self.name)




class SUOKIFPart(object):
  def __init__(self, **kwargs):
    self.entities = []
    self.name = ''
    self.name_re = re.compile(r'^;;\s+?(.*)\s+?;;$')

    if 'string' in kwargs:
      self.from_string(kwargs['string'])


  def plot(self, graph):
    graph.add_subgraph(self.entities, 'cluster_' + self.name, color='gray', label=self.name)
    for entity in self.entities:
      entity.plot(graph)


  def from_string(self, string):
    lines = string.split('\n')
    lines = [line.strip() for line in lines]
    lines = self.consume_name(lines)
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    while lines:
      lines = self.consume_item(lines)


  def consume_name(self, lines):
    for (line_index, line) in enumerate(lines):
      match = self.name_re.match(line)
      if match != None:
        self.name = match.group(1).strip()
        break
    return lines[line_index+1:]


  def consume_item(self, lines):
    quoted = False
    parenthesis_count = 0
    item_string = ''
    for (line_index, line) in enumerate(lines):
      for char in line:
        item_string += char
        if not quoted:
          if char == '(':
            parenthesis_count += 1
          elif char == ')':
            parenthesis_count -= 1
        if char == '"':
          quoted = not quoted
      if parenthesis_count == 0:
        break
      else:
        item_string += ' '
    self.parse_item(item_string)
    #print('Consumed item spanned %d lines' % (line_index + 1))
    return lines[line_index+1:]


  def parse_item(self, string):
    print('string:', string)
    parsed_string = pyparsing.OneOrMore(pyparsing.nestedExpr()).parseString(string)
    print('parsed:', parsed_string)





class SUOKIFParser(object):
  def __init__(self):
    self.ontology_parts = []


  def parse(self, kifs):
    for kif in kifs:
      kif_file = open(kif, 'r')
      kif_parts = []
      kif_part = ''
      for kif_line in kif_file:
        if kif_line.startswith(';; BEGIN FILE'):
          kif_part = ''
        kif_part += kif_line
        if kif_line.startswith(';; END FILE'):
          kif_parts.append(kif_part)
      for kif_part in kif_parts:
        self.ontology_parts.append(SUOKIFPart(string=kif_part))


  def plot_to_file(self, plot_filename):
    import pygraphviz as pgv
    graph = pgv.AGraph(directed=True)
    self.plot(graph)
    graph.draw(plot_filename, prog='dot')


  def plot(self, graph):
    for onto_part in self.ontology_parts:
      onto_part.plot(graph)






def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('kifs', metavar='kif', nargs='+', help='SUO-KIF files')
  args = parser.parse_args()

  parser = SUOKIFParser()
  parser.parse(args.kifs)
  parser.plot_to_file('/tmp/kifs.png')


if __name__ == '__main__':
  main()
