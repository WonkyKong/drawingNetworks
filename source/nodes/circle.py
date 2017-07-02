#!/usr/bin/env python

from source.nodes import Node


class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid):
        super (self.__class__, self).__init__ (nodeStruct, grid)
        self.radius = self.getAttribute ('radius', '{}')
        fill = self.getAttribute ('fill', '{}')
        if (fill != None):
            self.fill   = 'fillstyle=solid,fillcolor={}'.format (fill)
        else:
            self.fill = ''

    def getTexString (self):
        texString = ''
        texString += '\\pscircle[{}]({},{}){{{}}}\n'.format (self.fill,
                                                           self.position[0],
                                                           self.position[1],
                                                           self.radius)
        return texString
