#!/usr/bin/env python2

from __future__ import print_function

import sys
import re
import os
import errno
import argparse
import pyparsing
import collections


def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise



class SUOKIFEntity(object):
  def __init__(self, parent_part, name):
    self.parent_part = parent_part
    self.name = name
    self.superclasses = {}
    self.subclasses = {}
    self.ancestors = {}


  def add_superclasses_by_name(self, superclass_names):
    for superclass_name in superclass_names:
      print('%s adding superclass %s' % (self.name, superclass_name))
      print('superclasses before:', self.superclasses)
      if not superclass_name in self.parent_part.parent_ontology.entities:
        superclass = SUOKIFEntity(self.parent_part, superclass_name)
        self.parent_part.parent_ontology.entities[superclass_name] = superclass
        self.parent_part.entities[superclass_name] = superclass
      superclass = self.parent_part.parent_ontology.entities[superclass_name]
      self.superclasses[superclass_name] = superclass


  def build_graph(self):
    for superclass_key in self.superclasses:
      pass
      #superclass = self.superclasses[superclass_key]
      #superclass.add_subclass(self.name)


  def plot(self, graph):
    graph.add_node(self.name)
    for superclass_key in self.superclasses:
      graph.add_edge(self.name, self.superclasses[superclass_key].name, label='superclass')

  def to_cpp(self, directory):
    print('name: ', self.name)
    print('superclasses: ', self.superclasses)
    header_str = ""
    include_guard_name = self.name.upper() + '_H'
    header_str += '#ifndef %s\n' % include_guard_name
    header_str += '#define %s\n' % include_guard_name
    header_str += '\n'
    header_str += '#include <string>\n'
    header_str += '#include <vector>\n'
    header_str += '#include <unordered_set>\n'
    header_str += '\n'
    for superclass_key in self.superclasses:
      header_str += '#include <%s.hpp>\n' % self.superclasses[superclass_key].name
    header_str += '\n'
    header_str += 'class %s%s\n' % (self.name, ':' if self.superclasses else '')
    for (superclass_idx, superclass_key) in enumerate(self.superclasses):
      header_str += '  public ' + self.superclasses[superclass_key].name + (',' if len(self.superclasses) > (1+superclass_idx) else '') + '\n'
    header_str += '{\n'
    header_str += '  public:\n'
    header_str += '    static const std::string ontoname;\n'
    header_str += '    static const std::unordered_set<std::string> superclasses;\n'
    header_str += '\n'
    header_str += '    %s();\n' % self.name
    header_str += '\n'
    header_str += '\n'
    header_str += '  protected:\n'
    header_str += '\n'
    header_str += '\n'
    header_str += '  private:\n'
    header_str += '};\n'
    header_str += '\n'
    header_str += '#endif // %s\n' % include_guard_name
    header_file = open(directory + '/include/' + self.name + '.hpp', 'w')
    header_file.write(header_str)
    header_file.close()

    source_str = ''
    source_str += '#include <algorithm>\n'
    source_str += '\n'
    source_str += '#include <%s.hpp>\n' % self.name
    source_str += '\n'
    source_str += '\n'
    source_str += '/* public */\n'
    source_str += 'const std::string %s::ontoname{"%s"};\n' % (self.name, self.name)
    source_str += 'const std::unordered_set<std::string> %s::superclasses{%s};\n' % (self.name, ', '.join(['"%s"' % ancestor.name for ancestor in self.ancestors]))
    source_str += '\n'
    source_str += '\n'
    source_str += '%s::%s()\n' % (self.name, self.name)
    source_str += '{\n'
    source_str += '}\n'
    source_str += '\n'
    source_str += '\n'
    source_str += '\n'
    source_str += '/* protected */\n'
    source_str += '\n'
    source_str += '\n'
    source_str += '\n'
    source_str += '/* private */\n'
    source_file = open(directory + '/src/' + self.name + '.cpp', 'w')
    source_file.write(source_str)
    source_file.close()




class SUOKIFPart(object):
  def __init__(self, parent_ontology, name, **kwargs):
    self.parent_ontology = parent_ontology
    self.entities = {}
    self.name = name
    self.name_re = re.compile(r'^;;\s+?(.*)\s+?;;$')

    if 'string' in kwargs:
      self.from_string(kwargs['string'])


  def build_graph(self):
    pass


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


  def add_subclass(self, child_name, superclass_name):
    if isinstance(superclass_name, str): # superclass_name is either a str or a sequence of str
      superclass_name_list = [superclass_name]
    else:
      superclass_name_list = [p for p in superclass_name]
    if not child_name in self.parent_ontology.entities:
      child = SUOKIFEntity(self, child_name)
      self.parent_ontology.entities[child_name] = child
      self.entities[child_name] = child
    self.parent_ontology.entities[child_name].add_superclasses_by_name(superclass_name_list)


  def to_cpp(self, directory):
    for entity_name in self.entities:
      self.entities[entity_name].to_cpp(directory)




class SUOKIFParser(object):
  def __init__(self):
    self.ontology_parts = []
    self.entities = {}


  def parse(self, kifs):
    entity_part = SUOKIFPart(self, 'ENTITY')
    self.entities['Entity'] = SUOKIFEntity(entity_part, 'Entity')
    entity_part.entities['Entity'] = self.entities['Entity']
    self.ontology_parts.append(entity_part)

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
        part_name = os.path.basename(kif).rstrip('.kif') + ('_' + str(kif_part_index) if kif_part_index != 0 else '')
        self.ontology_parts.append(SUOKIFPart(self, part_name, string=kif_part))

    for onto_part in self.ontology_parts:
      onto_part.build_graph()


  def plot_to_file(self, plot_filename):
    import pygraphviz as pgv
    graph = pgv.AGraph(directed=True, page='100')
    self.plot(graph)
    graph.draw(plot_filename, prog='dot')


  def plot(self, graph):
    for onto_part in self.ontology_parts:
      onto_part.plot(graph)


  def to_cpp(self, directory):
    mkdir_p(directory + '/include')
    mkdir_p(directory + '/src')
    for onto_part in self.ontology_parts:
      onto_part.to_cpp(directory)






def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('kifs', metavar='kif', nargs='+', help='SUO-KIF files')
  args = parser.parse_args()

  parser = SUOKIFParser()
  parser.parse(args.kifs)
  #parser.plot_to_file('/tmp/kifs.ps')
  parser.to_cpp('/tmp/ontoprog/cpp')


if __name__ == '__main__':
  main()
