class node:
	def __init__(self,value=None):
		self.value=value
		self.left_child=None
		self.right_child=None
		self.parent=None # pointer to parent node in tree
		self.height=1 # height of node in tree (max dist. to leaf) NEW FOR AVL

	def __repr__(self):
		return str(self.value)

class AVLTree:
	def __init__(self):
		self.root=None

	# Recursively re-calculates the heights for nodes
	# above cur_node, while re-calculating heights, if it
	# comes across an instance where the AVL rules are broken it 
	# will call the rebalance function to fix the problem.
	def _recalculate_heights(self,cur_node,path=[]):
		if cur_node.parent==None: return

		'''
		new_height=1+cur_node.height
		prior_height=cur_node.parent.height

		if new_height>prior_height:
			cur_node.parent.height=new_height
		'''

		path=[cur_node]+path
		'''
		left_height,right_height=0,0
		if cur_node.parent.left_child==cur_node and cur_node.parent.right_child!=None:
			left_height=cur_node.height 
			right_height=cur_node.parent.right_child.height
		if cur_node.parent.right_child==cur_node and cur_node.parent.left_child!=None:
			left_height=cur_node.parent.left_child.height
			right_height=cur_node.height 
		'''
		left_height,right_height=0,0
		if cur_node.parent.left_child!=None:
			left_height=cur_node.parent.left_child.height
		if cur_node.parent.right_child!=None:
			right_height=cur_node.parent.right_child.height

		if abs(left_height-right_height)>1:
			print 'AVL Broken'	
			#print 'Path: ',path
			path=[cur_node.parent]+path
			self._rebalance_nodes(path)
			#print 'After rebalancing:'
			#self.print_levels()
			#self._recalculate_heights(path[-1])
			return

		new_height=1+cur_node.height 
		if new_height>cur_node.parent.height:
			cur_node.parent.height=new_height

		self._recalculate_heights(cur_node.parent,path)

	# Returns the height of the provided node, value is based
	# on the max of the values of the nodes children. If node is
	# None, value will be 0.
	def get_height(self,cur_node):
		if cur_node==None:
			return 0
		return cur_node.height

	def right_rotate(self,z):
		sub_root=z.parent # save parent of input
		# perform rotation
		y=z.left_child
		t3=y.right_child
		y.right_child=z
		z.parent=y
		z.left_child=t3
		if t3!=None: t3.parent=z
		# Re-connect original parent of input
		y.parent=sub_root
		if y.parent==None:
				self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y		
		# Update heights
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def left_rotate(self,z):
		sub_root=z.parent # save parent of input
		# perform rotation
		y=z.right_child
		t2=y.left_child
		y.left_child=z
		z.parent=y
		z.right_child=t2
		if t2!=None: t2.parent=z
		# Re-connect original parent of input
		y.parent=sub_root
		if y.parent==None: 
			self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y
		# Update heights
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))


	# Provided an instance where AVL rules are broken from _recalculate_heights
	# this function will figure out which of the 4 cases the node is in and will
	# take action accordingly to fix the issue.
	def _rebalance_nodes(self,path):
		print "Rebalancing nodes: ",path
		# using rules from https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
		z=path[0] # first unbalanced node
		y=path[1] # child of z that comes on path from latest insert
		x=path[2] # grandchild of z that comes on path from latest insert

		if y==z.left_child and x==y.left_child:
			# left left case
			# right rotate z...
			print "Left Left Case"
			self.right_rotate(z)

		elif y==z.left_child and x==y.right_child:
			# left right case
			# left rotate y...
			print "Left Right Case"
			self.left_rotate(y)
			# right rotate z...
			self.right_rotate(z)

		elif y==z.right_child and x==y.right_child:
			# right right case
			# left rotate z...
			print "Right Right Case"
			self.left_rotate(z)

		elif y==z.right_child and x==y.left_child:
			# right left case
			# right rotate y...
			print "Right Left Case"
			self.right_rotate(y)
			# left rotate z...
			self.left_rotate(z)

		else:
			raise ValueError('Path state could not be identified!')

	def print_levels(self):
		import sys
		print "_"*15
		levels=[]
		cur_nodes=[self.root]
		while True:
			if len(cur_nodes)==0: break
			cur_values=[]
			next_nodes=[]
			for n in cur_nodes:
				if n.value!=None:       cur_values.append(n.value)
				if n.left_child!=None:  next_nodes.append(n.left_child)
				if n.right_child!=None: next_nodes.append(n.right_child)
			levels.append(cur_values)
			cur_nodes=next_nodes
		for i,level in enumerate(levels):
			sys.stdout.write("Level %d:  "%i)
			for n in level:
				sys.stdout.write("%d "%n)
			sys.stdout.write("\n")
		print "_"*15

	def insert(self,value):
		if self.root==None:
			self.root=node(value)
		else:
			self._insert(value,self.root)

	def _insert(self,value,cur_node):
		if value<cur_node.value:
			if cur_node.left_child==None:
				cur_node.left_child=node(value)
				cur_node.left_child.parent=cur_node # set parent
				self._recalculate_heights(cur_node.left_child)
			else:
				self._insert(value,cur_node.left_child)
		elif value>cur_node.value:
			if cur_node.right_child==None:
				cur_node.right_child=node(value)
				cur_node.right_child.parent=cur_node # set parent
				self._recalculate_heights(cur_node.right_child)
			else:
				self._insert(value,cur_node.right_child)
		else:
			print "Value already in tree!"

	def print_tree(self):
		if self.root!=None:
			self._print_tree(self.root)

	def _print_tree(self,cur_node):
		if cur_node!=None:
			self._print_tree(cur_node.left_child)
			print '%s, h=%d'%(str(cur_node.value),cur_node.height)
			self._print_tree(cur_node.right_child)

	def height(self):
		if self.root!=None:
			return self._height(self.root,0)
		else:
			return 0

	def _height(self,cur_node,cur_height):
		if cur_node==None: return cur_height
		left_height=self._height(cur_node.left_child,cur_height+1)
		right_height=self._height(cur_node.right_child,cur_height+1)
		return max(left_height,right_height)

	def find(self,value):
		if self.root!=None:
			return self._find(value,self.root)
		else:
			return None

	def _find(self,value,cur_node):
		if value==cur_node.value:
			return cur_node
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._find(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._find(value,cur_node.right_child)

	def delete_value(self,value):
		return self.delete_node(self.find(value))

	def delete_node(self,node):

		## -----
		# Improvements since prior lesson

		# Protect against deleting a node not found in the tree
		if node==None or self.find(node.value)==None:
			print "Node to be deleted not found in the tree!"
			return None 

		# If the node to be deleted is the root node
		if node.parent==None:
			self.root=None 
			return None 
		## -----

		# returns the node with min value in tree rooted at input node
		def min_value_node(n):
			current=n
			while current.left_child!=None:
				current=current.left_child
			return current

		# returns the number of children for the specified node
		def num_children(n):
			num_children=0
			if n.left_child!=None: num_children+=1
			if n.right_child!=None: num_children+=1
			return num_children

		# get the parent of the node to be deleted
		node_parent=node.parent

		# get the number of children of the node to be deleted
		node_children=num_children(node)

		# break operation into different cases based on the
		# structure of the tree & node to be deleted

		# CASE 1 (node has no children)
		if node_children==0:

			# remove reference to the node from the parent
			if node_parent.left_child==node:
				node_parent.left_child=None
			else:
				node_parent.right_child=None

		# CASE 2 (node has a single child)
		if node_children==1:

			# get the single child node
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			# replace the node to be deleted with its child
			if node_parent.left_child==node:
				node_parent.left_child=child
			else:
				node_parent.right_child=child

			# correct the parent pointer in node
			child.parent=node_parent

		# CASE 3 (node has two children)
		if node_children==2:

			# get the inorder successor of the deleted node
			successor=min_value_node(node.right_child)

			# copy the inorder successor's value to the node formerly
			# holding the value we wished to delete
			node.value=successor.value

			# delete the inorder successor now that it's value was
			# copied into the other node
			self.delete_node(successor)

	def search(self,value):
		if self.root!=None:
			return self._search(value,self.root)
		else:
			return False

	def _search(self,value,cur_node):
		if value==cur_node.value:
			return True
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._search(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._search(value,cur_node.right_child)
		return False 


a=AVLTree()



for i in range(10):
	print 'Inserting ',i
	a.insert(i)
	a.print_tree()
	a.print_levels()


'''
from random import randint
for _ in range(10):
	a.insert(randint(0,100))
	print '-'*10
	a.print_tree()
'''

'''
# Left Left Case
a.insert(10)
a.insert(5)
a.insert(15)
a.print_tree()

print '-'*10
a.insert(4)
a.print_tree()

print '-'*10
a.insert(3)
a.print_tree()
'''

'''
# Right Right Case
a.insert(10)
a.insert(5)
a.insert(15)

a.print_tree()

print '-'*10

a.insert(20)
a.print_tree()

print '-'*10

a.insert(30)
a.print_tree()
'''
