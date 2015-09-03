#! /usr/bin/python
# -*- coding:utf-8 -*-

import vertex

class Parser:
	""" Allow to parse a path file """

	def __init__(self, input_file):
		self.input_file = input_file
		self.vertex_list = []
		self.number_of_verticle = None
		self.number_of_edge = None
		self.min_y = 0
		self.max_y = 0
		self.min_x = 0
		self.max_x = 0

	def parse(self):
		in_file = open(self.input_file, "r")
		first_couple = map(int, in_file.readline().split())
		node_dictionnary = {}
		self.number_of_verticle = first_couple[0]
		self.number_of_edge = first_couple[1]
		print "Verticle"
		for i in range(0, self.number_of_verticle):
			parsed_line = map(float, in_file.readline().split())
			vertex_id = parsed_line[0]
			vertex_x = parsed_line[1]
			vertex_y = parsed_line[2]
			self.max_x = vertex_x if vertex_x > self.max_x else self.max_x
			self.max_y = vertex_y if vertex_y > self.max_y else self.max_y
			self.min_x = vertex_x if vertex_x < self.min_x else self.min_x
			self.min_y = vertex_y if vertex_y < self.min_y else self.min_y

			vertex_instance = vertex.Vertex(vertex_id, vertex_x, vertex_y)
			node_dictionnary[vertex_id] = vertex_instance
			self.vertex_list.append(vertex_instance)
		print "Edge"
		for i in range(0, self.number_of_edge):
			edge =  map(int,in_file.readline().split())
			node_dictionnary[edge[0]].add_child(node_dictionnary[edge[1]])
		return self.vertex_list

	def clear_list(self, list):
		return_list = []
		for member in list:
			for sub_member in member:
				return_list.append(sub_member)
		return return_list

	def coordinate_string_to_array(self, coordinate_string):
		coordinate_string = coordinate_string[1:-1]
		coordinate_string =  coordinate_string.split(',')
		return_coordinate = []
		for item in coordinate_string:
			return_coordinate.append(int(item))
		return return_coordinate

