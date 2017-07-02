#!/usr/bin/env python

from source.nodes import Node


class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid):
        super (self.__class__, self).__init__ (nodeStruct, grid)
        self.WIDTH          = 0.5
        self.GAP            = 0.07
        self.DEPTH          = 0.21
        self.TEXT_DISTANCE  = 0.5
        self.label          = self.getAttribute ('label',       '{}')
        self.orientation    = self.getAttribute ('orientation', '{}')
        if (self.orientation == None):
            self.orientation = 'v'

    def getTexString (self):
        texString = ''

        # Set the lengths according to the orientation
        if (self.orientation == 'v'):
            h1 = self.WIDTH / 2
            h2 = h1
            h3 = -self.TEXT_DISTANCE
            v1 = self.DEPTH / 2
            v2 = self.GAP / 2
            v3 = 0
        else:
            h1 = self.DEPTH / 2
            h2 = self.GAP / 2
            h3 = 0
            v1 = self.WIDTH / 2
            v2 = v1
            v3 = self.TEXT_DISTANCE


        # Draw the capacitor
        texString += '\\psframe[{}]({},{})({},{})\n'.format ('fillstyle=solid,fillcolor=black',
                                                             self.position[0] - h1,
                                                             self.position[1] - v1,
                                                             self.position[0] + h1,
                                                             self.position[1] + v1)
        texString += '\\psframe[{}]({},{})({},{})\n'.format ('fillstyle=solid,fillcolor=white,linecolor=white',
                                                             self.position[0] - h2,
                                                             self.position[1] - v2,
                                                             self.position[0] + h2,
                                                             self.position[1] + v2)
        # Add the text
        texString += "\\rput({},{}){{\\fontsize{{{}}}{{{}}}\\selectfont {}}}\n".format (self.position[0] + h3,
                                                                                        self.position[1] + v3,
                                                                                        8, 8, self.label)
        return texString
