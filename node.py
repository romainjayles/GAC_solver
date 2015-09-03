#! /usr/bin/python
# -*- coding:utf-8 -*-

class Node(object):
	""" A simple implementation for the node of a tree """

	def __init__(self, variable_domain):
		self.variable_domain = variable_domain.copy()
		self.g = None
		self.f = None
		self.parent = None
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)

	def __str__(self):
		return "Node : " + str(self.variable_domain)

	def __eq__(self, obj):
		# Here we must check if all the domain are equals
		for key in self.variable_domain:
			if set(self.variable_domain[key]) != set(obj.variable_domain[key]):
				return False
		return True

	def __ne__(self, obj):
		return not self.__eq__(obj)