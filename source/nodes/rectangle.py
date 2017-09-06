#!/usr/bin/env python

from source.nodes import Node


class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid):
        super (subnode, self).__init__ (nodeStruct, grid)

        LINEWIDTH = 0.015

        self.height = float (self.getAttribute ('height', '{}', 0.6))
        halfHeight = self.height * 0.5

        self.width = float (self.getAttribute ('width',  '{}', 0.8))
        halfWidth = self.width * 0.5


        alignment = self.getAttribute ('alignment', '{}', 'middle')
        if 'right' in alignment:
            self.leftEdge = self.position[0] - self.width
        elif 'left' in alignment:
            self.leftEdge = self.position[0]
        else:
            self.leftEdge = self.position[0] - halfWidth
        #--
        if 'top' in alignment:
            self.bottomEdge = self.position[1] - self.height + LINEWIDTH
        elif 'bottom' in alignment:
            self.bottomEdge = self.position[1] + (LINEWIDTH * 0.5)
        else:
            self.bottomEdge = self.position[1] - halfHeight


        self.frameFormat = self.getAttribute ('format', '{}', 'fillstyle=solid,fillcolor=white')
        self.opaque = (self.getAttribute ('opaque', '{}', 'true') == 'true')


        # The text and its alignment
        self.text = self.getAttribute ('text', '{}', '')
        textAlignment = self.getAttribute ('textAlignment', '{}', 'middle')
        self.textX = self.leftEdge + halfWidth
        self.textY = self.bottomEdge + halfHeight
        if 'middle' == textAlignment:
            self.rputAlignment = ''
        else:
            nudge = 0.1
            rputAlignment = ''
            nudgedHalfWidth = halfWidth - nudge
            if 'left' in textAlignment:
                rputAlignment += 'l'
                self.textX -= nudgedHalfWidth
            elif 'right' in textAlignment:
                rputAlignment += 'r'
                self.textX += nudgedHalfWidth

            nudgedHalfHeight = halfHeight - nudge
            if 'top' in textAlignment:
                rputAlignment += 't'
                self.textY += nudgedHalfHeight
            elif 'bottom' in textAlignment:
                rputAlignment += 'b'
                self.textY -= nudgedHalfHeight

            self.rputAlignment = '[{}]'.format (rputAlignment)

    def getTexString (self):
        texString = ''

        # Draw the box
        if self.opaque:
            texString += '\\psframe[{}]({},{})({},{})\n'.format (
                'fillstyle=solid,fillcolor=white',
                self.leftEdge,
                self.bottomEdge,
                self.leftEdge + self.width,
                self.bottomEdge + self.height,
            )
        texString += '\\psframe[{}]({},{})({},{})\n'.format (
            self.frameFormat,
            self.leftEdge,
            self.bottomEdge,
            self.leftEdge + self.width,
            self.bottomEdge + self.height,
        )

        # Add the text inside the box
        texString += '\\rput{}({},{}){{\\fontfamily{{phv}}\\fontsize{{8}}{{8}}\\selectfont{{{}}}}}'.format (
            self.rputAlignment,
            self.textX,
            self.textY,
            self.text,
        )

        return texString
