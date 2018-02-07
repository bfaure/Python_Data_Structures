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

	# prints out a string pictorial representation of the tree
	def __repr__(self):
		if self.root==None: return ''
		content='\n' # to hold final string
		cur_nodes=[self.root] # all nodes at current level
		cur_height=self.root.height # height of nodes at current level
		sep=' '*(2**(cur_height-1)) # variable sized separator between elements
		while True:
			cur_height+=-1 # decrement current height
			if len(cur_nodes)==0: break
			cur_row=' '
			next_row=''
			next_nodes=[]

			if all(n is None for n in cur_nodes):
				break

			for n in cur_nodes:

				if n==None:
					cur_row+='   '+sep
					next_row+='   '+sep
					next_nodes.extend([None,None])
					continue

				if n.value!=None:       
					buf=' '*((5-len(str(n.value)))/2)
					cur_row+='%s%s%s'%(buf,str(n.value),buf)+sep
				else:
					cur_row+=' '*5+sep

				if n.left_child!=None:  
					next_nodes.append(n.left_child)
					next_row+=' /'+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)

				if n.right_child!=None: 
					next_nodes.append(n.right_child)
					next_row+='\ '+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)

			content+=(cur_height*'   '+cur_row+'\n'+cur_height*'   '+next_row+'\n')
			cur_nodes=next_nodes
			sep=' '*(len(sep)/2) # cut separator size in half
		return content

	# Recursively re-calculates the heights for nodes
	# above cur_node, while re-calculating heights, if it
	# comes across an instance where the AVL rules are broken it 
	# will call the rebalance function to fix the problem.
	def _inspect_insertion(self,cur_node,path=[]):
		if cur_node.parent==None: return

		path=[cur_node]+path

		# figure out height of other child of parent of cur_node (if one)
		left_height,right_height=0,0
		if cur_node.parent.left_child!=None:
			left_height=cur_node.parent.left_child.height
		if cur_node.parent.right_child!=None:
			right_height=cur_node.parent.right_child.height

		# calculate the balance factor
		if abs(left_height-right_height)>1:
			path=[cur_node.parent]+path
			self._rebalance_insertion(path)
			return

		# possibly assign new height to parent of cur_node
		new_height=1+cur_node.height 
		if new_height>cur_node.parent.height:
			cur_node.parent.height=new_height

		self._inspect_insertion(cur_node.parent,path)

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


	# Provided an instance where AVL rules are broken from _inspect_insertion
	# this function will figure out which of the 4 cases the node is in and will
	# take action accordingly to fix the issue.
	def _rebalance_insertion(self,path):
		# using rules from https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
		z=path[0] # first unbalanced node
		y=path[1] # child of z that comes on path from latest insert
		x=path[2] # grandchild of z that comes on path from latest insert

		if y==z.left_child and x==y.left_child:
			# left left case
			self.right_rotate(z)

		elif y==z.left_child and x==y.right_child:
			# left right case
			self.left_rotate(y)
			self.right_rotate(z)

		elif y==z.right_child and x==y.right_child:
			# right right case
			self.left_rotate(z)

		elif y==z.right_child and x==y.left_child:
			# right left case
			self.right_rotate(y)
			self.left_rotate(z)

		else:
			raise ValueError('Path state could not be identified!')

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
				self._inspect_insertion(cur_node.left_child)
			else:
				self._insert(value,cur_node.left_child)
		elif value>cur_node.value:
			if cur_node.right_child==None:
				cur_node.right_child=node(value)
				cur_node.right_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.right_child)
			else:
				self._insert(value,cur_node.right_child)
		else:
			return
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

			if node_parent!=None:
				# remove reference to the node from the parent
				if node_parent.left_child==node:
					node_parent.left_child=None
				else:
					node_parent.right_child=None
			else:
				self.root=None

		# CASE 2 (node has a single child)
		if node_children==1:

			# get the single child node
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			if node_parent!=None:
				# replace the node to be deleted with its child
				if node_parent.left_child==node:
					node_parent.left_child=child
				else:
					node_parent.right_child=child
			else:
				self.root=child

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

			# exit function so we don't call the _inspect_deletion twice
			return

		if node_parent!=None:
			# fix the height of the parent of current node
			#node_parent.height+=-1
			#node_parent.height=self._height(node_parent,0)
			node_parent.height=1+max(self.get_height(node_parent.left_child),self.get_height(node_parent.right_child))

			# begin to traverse back up the tree checking if there are
			# any sections which now invalidate the AVL balance rules
			self._inspect_deletion(node_parent)

	# Provided a node in the tree, returns either the left or
	# right child, depending on which has the higher height value.
	def taller_child(self,cur_node):
		if cur_node.left_child!=None:
			left_height=cur_node.left_child.height
		else:
			return cur_node.right_child
		if cur_node.right_child!=None:
			right_height=cur_node.right_child.height
		else:
			return cur_node.left_child
		return cur_node.left_child if left_height>=right_height else cur_node.right_child

	# Provided an instance where AVL rules are broken from _inspect_deletion
	# this function will figure out which of the 4 cases the node is in and will
	# take action accordingly to fix the issue.
	def _rebalance_deletion(self,cur_node):
		# using rules from https://www.geeksforgeeks.org/avl-tree-set-2-deletion/
		z=cur_node # first unbalanced node
		y=self.taller_child(z) # larger-height child of z
		x=self.taller_child(y) # larger-height child of y

		#print "_rebalance_deletion: z=",z,"y=",y,"x=",x
		#return

		if y==z.left_child and x==y.left_child:
			# left left case
			self.right_rotate(z)

			# fix node heights
			x.height=1+max(self.get_height(x.left_child),self.get_height(x.right_child))
			z.height=1+max(self.get_height(z.left_child),self.get_height(z.right_child))
			y.height=1+max(self.get_height(y.left_child),self.get_height(y.right_child))

		elif y==z.left_child and x==y.right_child:
			# left right case
			self.left_rotate(y)
			self.right_rotate(z)

			# fix node heights
			y.height=1+max(self.get_height(y.left_child),self.get_height(y.right_child))
			z.height=1+max(self.get_height(z.left_child),self.get_height(z.right_child))
			x.height=1+max(self.get_height(x.left_child),self.get_height(x.right_child))

		elif y==z.right_child and x==y.right_child:
			# right right case
			self.left_rotate(z)

			# fix node heights
			z.height=1+max(self.get_height(z.left_child),self.get_height(z.right_child))
			x.height=1+max(self.get_height(x.left_child),self.get_height(x.right_child))
			y.height=1+max(self.get_height(y.left_child),self.get_height(y.right_child))

		elif y==z.right_child and x==y.left_child:
			# right left case
			self.right_rotate(y)
			self.left_rotate(z)

			# fix node heights
			z.height=1+max(self.get_height(z.left_child),self.get_height(z.right_child))
			y.height=1+max(self.get_height(y.left_child),self.get_height(y.right_child))
			x.height=1+max(self.get_height(x.left_child),self.get_height(x.right_child))

		else:
			raise ValueError('Node configuration could not be identified!')

	# Should only be called from delete_node, similar to _inspect_insertion
	# except it is not terminated once a single identified portion of the tree
	# is fixed, in the case of deletion fixing a single unbalanced section
	# may cause another to pop up higher in the tree.
	def _inspect_deletion(self,cur_node):
		#print "_inspect_deletion called on node: ",cur_node
		
		#if cur_node.parent==None: return
		if cur_node==None: return

		#cur_height=self._height(cur_node,0)
		#cur_height=cur_node.height

		#if cur_height!=self._height(cur_node,0):
		#	raise ValueError("cur_height did not equal calculated height!")

		'''
		if cur_node.height+1!=self._height(cur_node,0):
			print "Node ",cur_node,"stored height:",cur_node.height,"true:",self._height(cur_node,0)
			raise ValueError("Stored node height not correct!")
		'''

		#cur_height=self._height(cur_node,0)
		cur_height=cur_node.height

		'''
		# figure out height of other child of parent of cur_node (if one)
		left_height,right_height=0,0
		if cur_node.parent.left_child!=None:
			left_height=cur_node.parent.left_child.height
		if cur_node.parent.right_child!=None:
			right_height=cur_node.parent.right_child.height

		if cur_node==cur_node.parent.left_child:
			left_height=cur_height
		else:
			right_height=cur_height
		'''

		left_height,right_height=0,0
		if cur_node.left_child!=None:
			left_height=cur_node.left_child.height
		if cur_node.right_child!=None:
			right_height=cur_node.right_child.height

		#print "left_height: %d, right_height: %d"%(left_height,right_height)

		# calculate the balance factor
		if abs(left_height-right_height)>1:
			print 'Need to rebalance deletion!'
			#self._rebalance_deletion(cur_node.parent)
			self._rebalance_deletion(cur_node)
			#return

		'''
		# possibly assign new height to parent of cur_node
		new_height=1+cur_node.height 
		if new_height>cur_node.parent.height:
			cur_node.parent.height=new_height
		'''

		self._inspect_deletion(cur_node.parent)

	def validate_heights(self,cur_node=None):
		if cur_node==None:
			cur_node=self.root 
			if cur_node==None: return

		if cur_node.height!=self._height(cur_node,0):
			print "Node ",cur_node,"reported height:",cur_node.height,"true:",self._height(cur_node,0)

		if cur_node.left_child!=None:
			self.validate_heights(cur_node.left_child)
		if cur_node.right_child!=None:
			self.validate_heights(cur_node.right_child)

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

'''
a=AVLTree()

a.insert(10)
a.insert(15)
a.insert(5)
a.insert(1)
a.insert(20)
a.insert(11)
a.insert(30)

print a 
a.delete_value(1)
print a
a.delete_value(30)
print a
a.delete_value(20)
print a
a.delete_value(15)
print a
'''

def test(n=20):
	a=AVLTree()
	for i in range(n):
		a.insert(i)

	print "Full tree..."
	print a

	print "Validating heights..."
	a.validate_heights()
	print "Validation complete!"

	for i in range(n):
		print "deleting ",i
		a.delete_value(i)
		print a
		print "Validating heights..."
		a.validate_heights()
		print "Validation complete!"

	print a 

	print "Validating heights..."
	a.validate_heights()
	print "Validation complete!"

#test()


