#!/usr/bin/env python

from lxml import objectify



class AttributeFinder:

    def __init__ (self, xmlStruct, xmlTag):
        self.xmlStruct  = xmlStruct
        self.xmlTag     = xmlTag

    @staticmethod
    def __applyFunc (attributeString, func):
        if (type (func) is str):
            return func.format (attributeString)
        else:
            return func (attributeString)

    def getAttribute (self, attributeName, func):
        attributeString = self.xmlStruct.get (attributeName)
        if attributeString is not None:
            return AttributeFinder.__applyFunc (attributeString, func)
        else:
            find = objectify.ObjectPath ('{}.{}'.format (self.xmlTag, attributeName))
            try:
                attributeString = find (self.xmlStruct).text.strip ()
                return AttributeFinder.__applyFunc (attributeString, func)
            except:
                return None

    def isPresent (self, attributeName, trueValue, falseValue):
        find = objectify.ObjectPath ('{}.{}'.format (self.xmlTag, attributeName))
        try:
            isTrue = find (xmlStruct)
            return trueValue
        except:
            return falseValue
