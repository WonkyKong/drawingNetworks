#!/usr/bin/env python

from source.nodes import Node


class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid):
        super (subnode, self).__init__ (nodeStruct, grid)
        self.TEXT_DISTANCE  = 0.3
        self.arrows         = self.getAttribute ('arrows',  '{}')

        self.text           = self.getAttribute ('text',    '{}')
        if (self.text == None):
            self.text = ''

        self.text_justification = self.getAttribute ('text_justification', '[{}]')
        if (self.text_justification == None):
            self.text_justification = ''

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
