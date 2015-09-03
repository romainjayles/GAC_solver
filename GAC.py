#! /usr/bin/python
# -*- coding:utf-8 -*-

from itertools import cycle
import node

class GAC:
	def __init__(self):
		# This will be a dictionaries, the key will be the string name
		self.variable_domain = {}
		self.constraint = []
		self.request_queue = []


	def todo_revise(self):
		pass

	def revise(self, couple):
		""" Return true if the domain is reduced """
		domain_reduced = False
		focal_variable = couple[0]
		constraint = couple[1]
		# We create the list of variable which appears in the constraint
		argument_list = list(constraint.func_code.co_varnames)
		# We remove the focal variable
		argument_list.remove(focal_variable)
		# The domain of the focal variable
		focal_domain = self.variable_domain[focal_variable]
		# Contains iterators on the domain of all the variable in the constraint, except the focal one
		iterator_list = {}
		# The dictionnary of next value to be tested
		current_variable_domain = {}
		size_variable_domain = {}
		position_iterator = {}
		# Translate the index to the variable name
		translation_index_to_variable = []
		remove_list = []
		for variable_name in argument_list:
			iterator_list[variable_name] = cycle(self.variable_domain[variable_name])
			size_variable_domain[variable_name] = len(self.variable_domain[variable_name])
			# we initialise all the value of the variables
			current_variable_domain[variable_name] = next(iterator_list[variable_name])
			position_iterator[variable_name] = 0
			translation_index_to_variable.append(variable_name)
		for x in focal_domain:
			continu = True
			# Tells when values can be aquired
			take_value = True
			# Define if this ...
			exist_true = False
			iterator_index = 0
			current_variable_domain[focal_variable] = x
			while continu:
				# When in this condition, the function can be tested
				if take_value:
					exist_true = exist_true or self.test_constraint_on_variable(constraint, current_variable_domain)
				current_variable = translation_index_to_variable[iterator_index]
				current_variable_domain[current_variable] = iterator_list[current_variable].next()
				position_iterator[current_variable] = position_iterator[current_variable] + 1
				if position_iterator[current_variable] >= size_variable_domain[current_variable]:
					position_iterator[current_variable] = 0
					iterator_index = iterator_index + 1
					take_value = False
				else:
					take_value = True
					iterator_index = 0
				if iterator_index >= len(translation_index_to_variable):
					continu = False
					for key in position_iterator:
						position_iterator[key] = 0
			if not exist_true:
				remove_list.append(x)
				domain_reduced = True
		# We remove the variable from the domain
		focal_domain = [x for x in focal_domain if x not in remove_list]
		self.variable_domain[focal_variable] = focal_domain
		return domain_reduced

	def rerun(self, variable_domain, assumption_variable):
		self.variable_domain = variable_domain
		for index, constraint in enumerate(self.constraint):
			constraint_argument = constraint.func_code.co_varnames
			if assumption_variable in constraint_argument:
				for var_name in self.variable_domain:
					if var_name in constraint_argument and var_name != assumption_variable:
						self.request_queue.append((var_name, constraint))
		self.domain_filtering_loop()
		return self.variable_domain
				

	def test_constraint_on_variable(self, constraint, dictionnary):
		""" Test the variables on the constraint """
		return constraint(**dictionnary)



	def initialisation(self):
		for index, constraint in enumerate(self.constraint):
			# Constraint_argument is the list of variables which are present in constraint
			constraint_argument = constraint.func_code.co_varnames
			for var_name in self.variable_domain:
				# if this variable appears in this constraint
				if var_name in constraint_argument:
					self.request_queue.append((var_name, constraint))




	def domain_filtering_loop(self):
		while self.request_queue:
			couple = self.request_queue.pop()
			if self.revise(couple):
				if not self.variable_domain[couple[0]]:
					raise NameError('Impossible to solve this problem')
				for index, constraint in enumerate(self.constraint):
					constraint_argument = constraint.func_code.co_varnames
					if couple[1] != constraint and couple[0] in constraint_argument:
						for var_name in self.variable_domain:
							if var_name in constraint_argument and var_name != couple[0]:
								self.request_queue.append((var_name, constraint))

	def is_a_solution(self, node):
		for var_name in node.variable_domain:
			if len(node.variable_domain[var_name]) > 1:
				# print "False"
				return False
		return True

	def h(self, node):
		h = 0
		for var_name in node.variable_domain:
			h = h + len(node.variable_domain[var_name])-1
		return h

	def generate_successors(self, parent_node):
		""" Make asumption on some variables, return the tuple (liste_of_node, assumption_variable) """
		def sort(key):
			return int(key[3:])
		succ = []
		for var_name in sorted(parent_node.variable_domain, key=sort):
			print "name : " + var_name
			if len(parent_node.variable_domain[var_name]) > 1:
				for value in parent_node.variable_domain[var_name]:
					# We reduce the domain of a variable to a singleton
					new_variable_domain = parent_node.variable_domain.copy()
					new_variable_domain[var_name] = [value]
					new_node = node.Node(new_variable_domain)
					succ.append(new_node)
				#for nodes in succ:
					#print "Add in succ " + str(nodes)
				return (succ, var_name)

	def sort_function(self, node1, node2):
		if node1.f > node2.f :
			return -1
		elif node1.f < node2.f :
			return 1
		else:
			return 0

	def astar(self, interface_instance):
		log = 0
		maxi = 0
		var_asumed = []
		""" Conduct the Astar reduction """
		# !!!!!!!!!!!!!!!!!!!!!!!!!! Need the other boucle !!!!!!
		print "------- Astar ----------"
		open_list = []
		closed_list = []
		S0 = node.Node(self.variable_domain)
		S0.g = 0
		S0.f = self.h(S0)
		open_list.append(S0)
		print S0.variable_domain
		print S0.f
		while True:
			if not open_list:
				print "Error"
				return
			#print "---- Open ----"
			#for truc in open_list:
			#	print truc
			#print "---- End ----"
			current = open_list.pop()
			interface_instance.print_solution(current.variable_domain)
			closed_list.append(current)
			if self.is_a_solution(current):
				print "Found !"
				print current.variable_domain
				return current.variable_domain
			couple = self.generate_successors(current)
			succ = couple[0]
			assumption_variable = couple[1]
			for node_generated in succ:
				fetch_from = None
				child_node = node_generated
				if node_generated in open_list:
					fetch_from = open_list
				elif node_generated in closed_list:
					fetch_from = closed_list
				if fetch_from:
					index = fetch_from.index(node_generated)
					child_node = fetch_from[index]
					print "Fetched"
				if fetch_from == None:
					try:
						child_node.variable_domain = self.rerun(child_node.variable_domain, assumption_variable)
						# print "Generated : " + str(node_generated) + " on variable " + assumption_variable
						child_node.g = current.g + 1
						child_node.f = self.h(child_node) + child_node.g
						#print "Assuming : " + assumption_variable + " size " + str(child_node.g)
						child_node.parent_node = current
						open_list.append(child_node)
						open_list.sort(cmp=self.sort_function)
						if child_node.g > maxi:
							maxi = child_node.g
							print maxi
						#if child_node.g > 250:
						#	f = open(assumption_variable+str(log) + '.log', 'w+')
						#	for key in child_node.variable_domain:
						#		f.write("Var : " + key + " : " + str(child_node.variable_domain[key]) +'\n')
						#	f.close()
						#	log = log+1
					except NameError:
						pass
						#print "Rerun fail"



			

	def solve(self, interface_instance):
		self.initialisation()
		#try:
		self.domain_filtering_loop()
		print self.variable_domain
		return self.astar(interface_instance)

		#except NameError:
		#	print "This problem is Impossible to solve."

def makefunc(var_names, expression, envir=globals()):
	args=""
	for n in var_names: args=args+ "," + n
	return eval("(lambda " + args[1:] + ": " + expression + ")", envir)

