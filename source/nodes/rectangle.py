#!/usr/bin/env python

from source.nodes import Node
from source.AttributeFinder import AttributeFinder

class subnode (Node.Node):

    def __init__ (self, nodeStruct, grid, height, width, alignment, frameFormat, opaque, text, textAlignment):
        super (subnode, self).__init__ (nodeStruct, grid)

        LINEWIDTH = 0.015

        self.height = height
        halfHeight = self.height * 0.5

        self.width = width
        halfWidth = self.width * 0.5

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

        self.frameFormat = frameFormat
        self.opaque = opaque

        # The text and its alignment
        self.text = text
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

    @classmethod
    def fromXml (cls, nodeStruct, grid):
        af = AttributeFinder (nodeStruct, 'node')
        height = float (af.getAttribute ('height', '{}', 0.6))
        width = float (af.getAttribute ('width',  '{}', 0.8))
        alignment = af.getAttribute ('alignment', '{}', 'middle')
        frameFormat = af.getAttribute ('format', '{}', 'fillstyle=solid,fillcolor=white')
        opaque = (af.getAttribute ('opaque', '{}', 'true') == 'true')
        text = af.getAttribute ('text', '{}', '')
        textAlignment = af.getAttribute ('textAlignment', '{}', 'middle')
        return cls (nodeStruct, grid, height, width, alignment, frameFormat, opaque, text, textAlignment)

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
