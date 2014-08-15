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
  def __init__(self, name, parents = []):
    self.name = name
    self.parents = parents

  def plot(self, graph):
    graph.add_node(self.name)
    for parent in self.parents:
      graph.add_edge(self.name, parent, label='parent')

  def to_cpp(self, directory):
    header_str = ""
    include_guard_name = self.name.upper() + '_H'
    header_str += '#ifndef %s\n' % include_guard_name
    header_str += '#define %s\n' % include_guard_name
    header_str += '\n'
    header_str += '#include <string>\n'
    header_str += '#include <vector>\n'
    header_str += '\n'
    for parent in self.parents:
      header_str += '#include <%s.hpp>\n' % parent
    header_str += '\n'
    header_str += 'class %s\n' % self.name
    if self.parents:
      header_str += ' :public ' + self.parents[0] + (',' if len(self.parents) > 1 else '') + '\n'
      for (parent_idx, parent) in enumerate(self.parents[1:]):
        header_str += '  public ' + parent + (',' if len(self.parents) > (2+parent_idx) else '') + '\n'
    header_str += '{\n'
    header_str += '  public:\n'
    header_str += '    static const std::string ontoname;\n'
    header_str += '\n'
    header_str += '    static std::vector<std::string> superclasses();\n'
    header_str += '    static void superclasses(std::vector<std::string>& superclass_vec);\n'
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
    source_str += 'const std::string %s::ontoname("%s");\n' % (self.name, self.name)
    source_str += '\n'
    source_str += 'void\n'
    source_str += '%s::superclasses(std::vector<std::string>& superclass_vec)\n' % self.name
    source_str += '{\n'
    source_str += '  if (std::find(superclass_vec.begin(), superclass_vec.end(), %s::ontoname) == superclass_vec.end()) {\n' % self.name
    source_str += '    superclass_vec.push_back(%s::ontoname);\n' % self.name
    for parent in self.parents:
      source_str += '    %s::superclasses(superclass_vec);\n' % parent
    source_str += '  }\n'
    source_str += '}\n'
    source_str += '\n'
    source_str += 'std::vector<std::string>\n'
    source_str += '%s::superclasses()\n' % self.name
    source_str += '{\n'
    source_str += '  std::vector<std::string> superclass_vec;\n'
    source_str += '  %s::superclasses(superclass_vec);\n' % self.name
    source_str += '  return superclass_vec;\n'
    source_str += '}\n'
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


  def to_cpp(self, directory):
    for entity_name in self.entities:
      self.entities[entity_name].to_cpp(directory)




class SUOKIFParser(object):
  def __init__(self):
    self.ontology_parts = []


  def parse(self, kifs):
    entity_part = SUOKIFPart('ENTITY')
    entity_part.entities['Entity'] = SUOKIFEntity('Entity')
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
        self.ontology_parts.append(SUOKIFPart(part_name, string=kif_part))


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
