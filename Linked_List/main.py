
class node:
	def __init__(self,data=None):
		self.data=data
		self.next=None

class linked_list:
	def __init__(self):
		self.head=node()

	# Adds new node containing 'data' to the end of the linked list.
	def append(self,data):
		new_node=node(data)
		cur=self.head
		while cur.next!=None:
			cur=cur.next
		cur.next=new_node

	# Returns the length (integer) of the linked list.
	def length(self):
		cur=self.head
		total=0
		while cur.next!=None:
			total+=1
			cur=cur.next
		return total 

	# Prints out the linked list in traditional Python list format. 
	def display(self):
		elems=[]
		cur_node=self.head
		while cur_node.next!=None:
			cur_node=cur_node.next
			elems.append(cur_node.data)
		print elems

	# Returns the value of the node at 'index'. 
	def get(self,index):
		if index>=self.length():
			print "ERROR: 'Get' Index out of range!"
			return None
		cur_idx=0
		cur_node=self.head
		while True:
			cur_node=cur_node.next
			if cur_idx==index: return cur_node.data
			cur_idx+=1

	# Sets the data at index 'index' equal to 'data'.
	# Indices begin at 0. If the 'index' is greater than or equal 
	# to the length of the linked list the item will be appended onto
	# the end of the linked list.
	def set(self,index,data):
		if index>=self.length():
			self.append(data)
			return
		cur_node=self.head
		cur_idx=0
		while True:
			cur_node=cur_node.next
			if cur_idx==index: 
				cur_node.data=data
				return
			cur_idx+=1

	# Deletes the node at index 'index'.
	def erase(self,index):
		if index>=self.length():
			print "ERROR: 'Erase' Index out of range!"
			return 
		cur_idx=0
		cur_node=self.head
		while True:
			last_node=cur_node
			cur_node=cur_node.next
			if cur_idx==index:
				last_node.next=cur_node.next
				return
			cur_idx+=1

	# Allows for bracket operator syntax (i.e. a[0] to return first item).
	def __getitem__(self,index):
		return self.get(index)
