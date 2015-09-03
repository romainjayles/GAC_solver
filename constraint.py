#! /usr/bin/python
# -*- coding:utf-8 -*-

class Constraint(object):

	def __init__(self, vertex_list, color_range):
		self.vertex_list = vertex_list
		self.color_range = color_range
		self.constraint_list = []
		self.variable_list = []
		self.variable_domain = {}
		self.generate_constraint()

	def makefunc(self, var_names, expression, envir=globals()):
		args=""
		for n in var_names: args=args+ "," + n
		return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

	def generate_constraint(self):
		for vertex in self.vertex_list:
			self.variable_domain[vertex.variable_name] = range(0, self.color_range)
			for connected_vertex in vertex.children:
				variable_list = [vertex.variable_name, connected_vertex.variable_name]
				constraint = vertex.variable_name + ' != ' + connected_vertex.variable_name
				self.constraint_list.append(self.makefunc(variable_list, constraint, locals()))
