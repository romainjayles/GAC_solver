#! /usr/bin/python
# -*- coding:utf-8 -*-

class Vertex(object):

	def __init__(self, id_vertex, x, y):
		self.id = int(id_vertex)
		self.x = x
		self.y = y
		self.variable_name = 'var' + str(self.id)
		#self.variable_name = str(self.id)
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)