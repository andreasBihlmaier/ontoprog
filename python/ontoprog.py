#!/usr/bin/env python2

from __future__ import print_function

import sys
import re
import os
import argparse
import pyparsing
import collections




class SUOKIFEntity(object):
  def __init__(self, name, parents = []):
    self.name = name
    self.parents = parents

  def plot(self, graph):
    graph.add_node(self.name)
    for parent in self.parents:
      graph.add_edge(self.name, parent, label='parent')




class SUOKIFPart(object):
  def __init__(self, name, **kwargs):
    self.entities = {}
    self.name = name
    self.name_re = re.compile(r'^;;\s+?(.*)\s+?;;$')

    if 'string' in kwargs:
      self.from_string(kwargs['string'])


  def plot(self, graph):
    graph.add_subgraph(self.entities.keys(), 'cluster_' + self.name, color='gray', label=self.name)
    for entity_name in self.entities:
      self.entities[entity_name].plot(graph)


  def from_string(self, string):
    lines = string.split('\n')
    lines = [line.strip() for line in lines]
    self.extract_name(lines)
    lines = [line.strip() for line in lines if line and not line.startswith(';')]
    while lines:
      lines = self.consume_item(lines)


  def extract_name(self, lines):
    for (line_index, line) in enumerate(lines):
      if line_index >= 1 and lines[line_index - 1].startswith(';;;;') and lines[line_index + 1].startswith(';;;;'):
        match = self.name_re.match(line)
        if match != None:
          text = match.group(1).strip()
          if not text.startswith('Start:'):
            self.name = text
            break
    print('part: %s' % self.name)
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
    #print('string:', string)
    parsed_string = pyparsing.nestedExpr().parseString(string)
    #print('parsed:', parsed_string)
    fun, args = parsed_string[0][0], parsed_string[0][1:]
    #print('fun: %s args: %s' % (fun, args))
    if fun == 'subclass':
      self.add_subclass(args[0], args[1])


  def add_subclass(self, child, parent):
    if isinstance(parent, str): # parent is either a str or a sequence of str
      parent_list = [parent]
    else:
      parent_list = [p for p in parent]
    if child in self.entities:
        self.entities[child].parents.extend(parent_list)
    else:
      self.entities[child] = SUOKIFEntity(child, parent_list)





class SUOKIFParser(object):
  def __init__(self):
    self.ontology_parts = []


  def parse(self, kifs):
    for (kif_index, kif) in enumerate(kifs):
      kif_file = open(kif, 'r')
      kif_parts = []
      kif_part = ''
      for kif_line in kif_file:
        if kif_line.startswith(';; BEGIN FILE'):
          kif_part = ''
        kif_part += kif_line
        if kif_line.startswith(';; END FILE'):
          kif_parts.append(kif_part)
      if not kif_parts: # kif file does not contain 'subfiles'
        kif_parts.append(kif_part)
      kif_file.close()
      for (kif_part_index, kif_part) in enumerate(kif_parts):
        self.ontology_parts.append(SUOKIFPart(os.path.basename(kif) + '_' + str(kif_part_index), string=kif_part))


  def plot_to_file(self, plot_filename):
    import pygraphviz as pgv
    graph = pgv.AGraph(directed=True, page='100')
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
  parser.plot_to_file('/tmp/kifs.ps')


if __name__ == '__main__':
  main()
