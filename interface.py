#! /usr/bin/python
# -*- coding:utf-8 -*-

import parser
import Tkinter
import GAC
import Image, ImageDraw
import constraint
import sys
import time

class my_interface(Tkinter.Tk):

	HEIGHT = 700
	WIDTH = 700

	def __init__(self, parent):
		Tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.init_interface()

	def init_interface(self):
		self.vertex_size = 5
		self.grid()
		self.drawing_surface = Tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT, background='white')
		#self.drawing_surface.configure(scrollregion=(-400, -400, 400, 400))
		self.drawing_surface.grid(column=1,row=0, rowspan=20)

		button_bf = Tkinter.Button(self,text=u"Go", command=self.go_click)

		button_bf.grid(column=0,row=0)

	def calculate_display_settings(self, min_x, max_x, min_y, max_y):
		self.min_y = min_y
		self.max_y = max_y
		self.min_x = min_y
		self.max_x = max_x

	def resize_display_position(self, actual_x, actual_y):
		resize_x = (actual_x - self.min_x)*self.WIDTH/(self.max_x-self.min_x)
		resize_y = (actual_y - self.min_y)*self.HEIGHT/(self.max_y-self.min_y)
		return [resize_x, resize_y]


	def print_graph(self, vertex_list):
		# A changer !!!!!
		self.vertex_list = vertex_list
		for vertex in vertex_list:
			#position_x = vertex.x
			#position_y = vertex.y
			couple = self.resize_display_position(vertex.x, vertex.y)
			position_x = couple[0]
			position_y = couple[1]
			self.create_circle(position_x, position_y, self.vertex_size)
			for connected_vertex in vertex.children:
				couple = self.resize_display_position(connected_vertex.x, connected_vertex.y)
				connected_vertex_x = couple[0]
				connected_vertex_y = couple[1]
				self.drawing_surface.create_line(position_x, position_y, connected_vertex_x, connected_vertex_y)


	def go_click(self):
		print "GO"
		result = algo.solve(self)
		self.print_solution(result)

	def print_solution(self, result):
		self.drawing_surface.delete("all")
		for vertex in vertex_list:
			couple = self.resize_display_position(vertex.x, vertex.y)
			position_x = couple[0]
			position_y = couple[1]
			if len(result[vertex.variable_name]) == 1:
				copy = result[vertex.variable_name][:]
				color_number = copy.pop()
			else:
				color_number = 999
			color = 'white'
			if color_number == 0:
				color = 'red'
			elif color_number == 1:
				color = 'blue'
			elif color_number == 2:
				color = 'pink'
			elif color_number == 3:
				color = 'yellow'
			elif color_number == 4:
				color = 'orange'
			elif color_number == 5:
				color = 'black'
			elif color_number == 6:
				color = 'green'
			elif color_number == 7:
				color = 'purple'
			self.create_circle(position_x, position_y, self.vertex_size, fill=color)
			for connected_vertex in vertex.children:
				couple = self.resize_display_position(connected_vertex.x, connected_vertex.y)
				connected_vertex_x = couple[0]
				connected_vertex_y = couple[1]
				self.drawing_surface.create_line(position_x, position_y, connected_vertex_x, connected_vertex_y)
		self.update()


	def create_circle(self, x, y, r, **kwargs):
		""" Print a circle on the screen """
		return self.drawing_surface.create_oval(x-r,y-r, x+r,y+r, **kwargs)


if __name__ == "__main__":
	input_file = sys.argv[1]
	parser_instance = parser.Parser(input_file)
	vertex_list = parser_instance.parse()
	problem_instance = constraint.Constraint(vertex_list, 4)
	algo = GAC.GAC()
	algo.variable_domain = problem_instance.variable_domain
	algo.constraint = problem_instance.constraint_list
	app = my_interface(None)
	app.title('GAC')
	app.calculate_display_settings(parser_instance.min_x, parser_instance.max_x, parser_instance.min_y, parser_instance.max_x)
	app.print_graph(vertex_list)
	app.mainloop()

