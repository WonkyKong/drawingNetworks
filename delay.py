#!/usr/bin/env python

from Node import Node


class subnode (Node):

    def __init__ (self, nodeStruct, grid):
        Node.__init__ (self, nodeStruct, grid)
        self.HEIGHT             = 0.6
        self.WIDTH              = 0.8
        self.SUPERCRIPT_NUDGE   = 0.08
        self.arrows             = self.getAttribute ('arrows', '{}')

    def getTexString (self):
        texString = ''

        # Draw the arrows
        shapeLimits = [x * 0.5 for x in [-self.WIDTH, -self.HEIGHT, self.WIDTH, self.HEIGHT]]
        texString += super (subnode, self).addArrows (shapeLimits, self.arrows)

        # Draw the box
        texString += '\\psframe[{}]({},{})({},{})\n'.format (
            'fillstyle=solid,fillcolor=white',
            self.position[0] - self.WIDTH  * 0.5,
            self.position[1] - self.HEIGHT * 0.5,
            self.position[0] + self.WIDTH  * 0.5,
            self.position[1] + self.HEIGHT * 0.5,
        )

        # Add the text inside the box
        texString += '\\rput({},{}){{\\fontsize{{8}}{{8}}\\selectfont$z\\ \\,\\,$}}'.format (
            self.position[0],
            self.position[1]
        )
        texString += '\\rput({},{}){{\\ \\ \\fontsize{{6}}{{6}}\\selectfont-1}}'.format (
            self.position[0],
            self.position[1] + self.SUPERCRIPT_NUDGE
        )

        return texString
