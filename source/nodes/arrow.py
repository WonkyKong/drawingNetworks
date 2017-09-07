#!/usr/bin/env python

from source.nodes import Node
from source.AttributeFinder import AttributeFinder

class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid, arrows, text, justification):
        super (subnode, self).__init__ (nodeStruct, grid)
        self.TEXT_DISTANCE      = 0.3
        self.arrows             = arrows
        self.text               = text
        self.text_justification = justification


    @classmethod
    def fromXml (cls, nodeStruct, grid):
        af = AttributeFinder (nodeStruct, 'node')
        arrows          = af.getAttribute ('arrows',    '{}')
        text            = af.getAttribute ('text',      '{}', '')
        justification   = af.getAttribute ('text_justification', '[{}]', '')
        return cls (nodeStruct, grid, arrows, text, justification)


    def getTexString (self):
        texString = ''

        # Draw the arrows
        # TODO: option to change between 0 and 0.02?
        texString += super (subnode, self).addArrows ([-0.02, -0.02, 0.02, 0.02], self.arrows)

        # Add the text
        if self.text:
            texString += '\\rput{}({},{}){{\\fontsize{{8}}{{8}}\\selectfont ${}$}}\n'.format (
                self.text_justification,
                self.position[0],
                self.position[1] + self.TEXT_DISTANCE,
                self.text
            )

        return texString
