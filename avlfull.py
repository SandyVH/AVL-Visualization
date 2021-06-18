from graphics import *
import random
import time
import math

class AVLTreeNode(object):

	def __init__(self, keyData):
		self.keyData = keyData
		self.count = 1
		self.depth = 0
		self.height = 0		
		self.order = -1
		self.parent = None
		self.left = None
		self.right = None
		self.balance = 0

	def isLeftChild(self):
		return ((self.parent != None) and (self.parent.left == self))

	def isRightChild(self):
		return ((self.parent != None) and (self.parent.right == self))
		
	def isLeaf(self):
		return ((self.left == None) and (self.right == None))
		
	def isRoot(self):
		return (self.parent == None)
		
	def hasGrandParent(self):
		return ((self.parent != None) and (self.parent.parent != None))
		
	def leftSubTreeHeight(self):
		leftSubTreeHeight = -1
		if (self.left != None):
			leftSubTreeHeight = self.left.height
		return leftSubTreeHeight
		
	def rightSubTreeHeight(self):
		rightSubTreeHeight = -1
		if (self.right != None):
			rightSubTreeHeight = self.right.height
		return rightSubTreeHeight
			
	def maxSubTreeHeight(self):
		leftSubTreeHeight = self.leftSubTreeHeight()
		rightSubTreeHeight = self.rightSubTreeHeight()
		if (leftSubTreeHeight > rightSubTreeHeight):
			return leftSubTreeHeight
		else:
			return rightSubTreeHeight
			
	def isBalanced(self):
		leftSubTreeHeight = -1
		rightSubTreeHeight = -1
		if (self.left != None):
			leftSubTreeHeight = self.left.height
		if (self.right != None):
			rightSubTreeHeight = self.right.height
		self.balance = leftSubTreeHeight - rightSubTreeHeight
		if (abs(self.balance) > 1):
			return False
		else:
			return True
		
	def rightMostNodeInLeftSubtree(self):
		c = self
		if (c.left != None):
			c = c.left
			while (c.right != None):
				c = c.right
			return c
		else:
			return None

	def leftMostNodeInRightSubtree(self):
		c = self
		if (c.right != None):
			c = c.right
			while (c.left != None):
				c = c.left
			return c
		else:
			return None

	def parentOfNearestAncestorThatIsLeftChild(self):
		c = self
		if (c.isRightChild()):
			while (c.isRightChild()):
				c = c.parent
			if (c.isLeftChild()):
				return c.parent
			else:
				return None
		else:
			return None
	
	def parentOfNearestAncestorThatIsRightChild(self):
		c = self
		if (c.isLeftChild()):
			while (c.isLeftChild()):
				c = c.parent
			if (c.isRightChild()):
				return c.parent
			else:
				return None
		else:
			return None
								
	def next(self):
		if (self.isRoot()):
			if (self.right != None):
				return self.leftMostNodeInRightSubtree()
			else:
				return None
		elif (self.isLeftChild()):
			if (self.right != None):
				return self.leftMostNodeInRightSubtree()
			else:
				return self.parent
		else:
			if (self.right != None):
				return self.leftMostNodeInRightSubtree()
			else:
				return self.parentOfNearestAncestorThatIsLeftChild()
				
	def prev(self):
		if (self.isRoot()):
			if (self.left != None):
				return self.rightMostNodeInLeftSubtree()
			else:
				return None
		elif (self.isLeftChild()):
			if (self.left != None):
				return self.rightMostNodeInLeftSubtree()
			else:
				return self.parentOfNearestAncestorThatIsRightChild()
		else:
			if (self.left != None):
				return self.rightMostNodeInLeftSubtree()
			else:
				return self.parent
	
	def insert(self, delegateTree, keyData):
		if (self.keyData == keyData):
			self.count += 1
			return None
		elif (self.keyData > keyData):
			if (self.left == None):
				self.left = AVLTreeNode(keyData)
				self.left.parent = self
				self.left.depth = self.depth+1
				delegateTree.numNodes += 1
				return self.left
			else:
				return self.left.insert(delegateTree, keyData)
		else:
			if (self.right == None):
				self.right = AVLTreeNode(keyData)
				self.right.parent = self
				self.right.depth = self.depth+1
				delegateTree.numNodes += 1
				return self.right
			else:
				return self.right.insert(delegateTree, keyData)		

	def remove(self, delegateTree):
		if (self.isLeaf()):
			if (self.isLeftChild()):
				self.parent.left = None
				self.parent.bubbleUp(delegateTree)
			elif (self.isRightChild()):
				self.parent.right = None
				self.parent.bubbleUp(delegateTree)
			else:
				delegateTree.rootNode = None
		else:
			if ((self.left != None) and (self.right != None)):
				if (self.prev().isLeaf()):
					self.swapIn(delegateTree, self.prev().remove(delegateTree))
				else:
					self.swapIn(delegateTree, self.next().remove(delegateTree))					
			else:
				if (self.right != None):
					self.swapIn(delegateTree, self.next().remove(delegateTree))
				else:
					self.swapIn(delegateTree, self.prev().remove(delegateTree))			
		return self
			
	def swapIn(self, delegateTree, newNode):
		newNode.parent = self.parent
		newNode.left = self.left
		newNode.right = self.right
		newNode.height = self.height
		newNode.depth = self.depth
		if (self.left != None):
			self.left.parent = newNode
		if (self.right != None):
			self.right.parent = newNode
		if (self.isLeftChild()):
			self.parent.left = newNode
		if (self.isRightChild()):
			self.parent.right = newNode
		if (self.isRoot()):
			delegateTree.rootNode = newNode
			
	def bubbleUp(self, delegateTree):
		self.height = self.maxSubTreeHeight() + 1
		if (self.isBalanced() == False):
			#print("imbalance at " + str(self.keyData) + " node")
			self.rotate(delegateTree)
		if (self.parent != None):
			self.parent.bubbleUp(delegateTree)
			
	def rotate(self, delegateTree):	
		p = self.parent
		if (self.leftSubTreeHeight() > self.rightSubTreeHeight()):
			if (self.left.leftSubTreeHeight() > self.left.rightSubTreeHeight()):
				#    z
				#  y/
				#x/
				print("Doing LL Rotation...")
				z = self
				y = self.left
				x = self.left.left					
				T_0 = x.left
				T_1 = x.right
				T_2 = y.right
				T_3 = z.right
			else:
				#    z
				#x/
				#  \y
				print("Doing LR Rotation...")
				z = self
				y = self.left.right
				x = self.left
				T_0 = x.left
				T_1 = y.left 
				T_2 = y.right 
				T_3 = z.right 
				
			if (z.isLeftChild()):
				p.left = y
			elif (z.isRightChild()):
				p.right = y
			else:
				delegateTree.rootNode = y
		else:
			if (self.right.rightSubTreeHeight() > self.right.leftSubTreeHeight()):
				#x
				# \y
				#   \z
				print("Doing RR Rotation...")
				z = self.right.right
				y = self.right
				x = self 
				T_0 = x.left 
				T_1 = y.left 
				T_2 = z.left 
				T_3 = z.right
			else:
				#x
				#   \z
				# y/
				print("Doing RL Rotation...")
				z = self.right 
				y = self.right.left 
				x = self 
				T_0 = x.left 
				T_1 = y.left 
				T_2 = y.right 
				T_3 = z.right
				
			if (x.isLeftChild()):
				p.left = y
			elif (x.isRightChild()):
				p.right = y
			else:
				delegateTree.rootNode = y
			
		y.parent = p
		y.left = x
		y.right = z
		
		x.parent = y
		z.parent = y
		
		if (T_0 != None):
			T_0.parent = x
		if (T_1 != None):
			T_1.parent = x
		if (T_2 != None):
			T_2.parent = z
		if (T_3 != None):
			T_3.parent = z
		
		x.left = T_0
		x.right = T_1
		z.left = T_2
		z.right = T_3
		
		x.height = x.maxSubTreeHeight()+1
		z.height = z.maxSubTreeHeight()+1
		y.height = y.maxSubTreeHeight()+1
					
		if (p != None):
			y.setDepth(p.depth+1)
		else:
			y.setDepth(0)
			
	def setDepth(self, depth):
		if (self.left != None):
			self.left.setDepth(depth+1)
		self.depth = depth
		if (self.right != None):
			self.right.setDepth(depth+1)
			

class AVLTree(object):

	def __init__(self):
		self.rootNode = None
		self.numNodes = 0
		self.currentNode = None
		self.visited = []
		
	def find(self, keyData):
		if (self.rootNode != None):
			c = self.rootNode
			while (c != None):
				if (c.keyData == keyData):
					drawTree(tree, "AVL", 0, c)
					return c
				elif (c.keyData > keyData):
					drawTree(self, "AVL", c)
					c = c.left
				else:
					drawTree(self, "AVL", c)
					c = c.right
			print("\nELEMENT NOT FOUND! \n")
			return c
		else:
			print("INVALID SEARCH!, No AVL Tree present \n")
			return None
						
	def insert(self, keyData):
		if (self.rootNode == None):
			self.rootNode = AVLTreeNode(keyData)
			self.rootNode.height = 0
			self.rootNode.depth = 0
			self.rootNode.balance = 0
			self.numNodes = 1
		else:
			newNode = self.rootNode.insert(self, keyData)
			if (newNode != None):
				self.calcBalance(self.rootNode)
				drawTree(self, "AVL", newNode)
				newNode.bubbleUp(self)
	
	def remove(self, keyData):
		removedNode = self.find(keyData)
		if (removedNode != None):
			removedNode.remove(self)
			self.numNodes -= 1
		return removedNode
			
	def printTree(self):
		if (self.rootNode != None):
			c = self.rootNode
			while (c.left != None):
				c = c.left
			while (c != None):
				print(c.keyData)
				c = c.next()

	def inorder(self, root):
		if(root != None):
			self.inorder(root.left)
			drawTree(self, "AVL", root)
			self.visited.append(root)
			self.inorder(root.right)

	def preorder(self, root):
		if(root != None):
			drawTree(self, "AVL", root)
			self.visited.append(root)
			self.preorder(root.left)
			self.preorder(root.right)
	
	def postorder(self, root):
		if(root != None):
			self.postorder(root.left)
			self.postorder(root.right)
			drawTree(self, "AVL", root)
			self.visited.append(root)

	def calcBalance(self, root):
		if(root != None):
			if(root.left != None):
				self.calcBalance(root.left)
			if(root.right != None):
				self.calcBalance(root.right)
			root.height = root.maxSubTreeHeight() + 1
			root.isBalanced()

	def getFirst(self):
		if (self.rootNode != None):
			c = self.rootNode
			while (c.left != None):
				c = c.left
			return c
		else:
			return None
			
	def markOrder(self):
		if (self.rootNode != None):
			c = self.getFirst()
			n=0
			while (c != None):
				c.order = n
				n += 1
				c = c.next()



def drawTree(tree, windowTitle, s, found = None):
	cellSize = 72
	nodeSize = 34.56
	halfCellSize = cellSize / 2			
	tree.markOrder()
	if (tree.rootNode != None):
	
		h = tree.rootNode.height
		w = tree.numNodes		
		win = GraphWin(windowTitle, 1000, 1000)
		
		for x in range(0,tree.numNodes):
			p1 = Point(x*cellSize,0)
			p2 = Point((x+1)*cellSize, (h+1)*cellSize)
			rect = Rectangle(p1,p2)
			# color_rgb(133 - (x%2)*5,240 - (x%2)*5, 245 - (x%2)*5)
			rect.setFill(color_rgb(212, 211, 207))
			rect.draw(win)
			
		c = tree.getFirst()	
		x = math.pow(2, c.order)
		y = math.pow(2, c.depth)	
		while (c != None):
			if (c.parent != None):
				p1 = Point(c.order*cellSize+halfCellSize, (c.depth*cellSize+halfCellSize))
				p2 = Point(c.parent.order*cellSize+halfCellSize, (c.parent.depth*cellSize+halfCellSize))
				lin = Line(p1,p2)
				lin.setWidth(3)
				lin.draw(win)
			c = c.next()
		
		c = tree.getFirst()
		column = 0
		while (c != None):
			c.height = c.maxSubTreeHeight() + 1
			c.isBalanced()
			p = Point(column*cellSize+halfCellSize, (c.depth*cellSize+halfCellSize))
			circ = Circle(p, nodeSize)
			circ2 = Circle(p, nodeSize-7)
			string = str(c.keyData)+", "+str(c.balance)
			txt = Text(p, string)
			txt.setSize(15)
			txt.setStyle("bold")

			if(c != s):
				circ.setFill(color_rgb(0,255,0))
			else:
				circ.setFill(color_rgb(255,0,0))

			if(c == found):
				circ.setFill(color_rgb(0,0,255))

			if(c in tree.visited):
				circ.setFill(color_rgb(0,0,255))
				
			circ2.setFill(color_rgb(255,255,255))
			circ.draw(win)
			circ2.draw(win)
			txt.draw(win)
			c = c.next()
			column += 1
		time.sleep(4)
		#input("Press Enter to continue...")
		win.close()

tree = AVLTree()
option = 1
while(option != 5):
	print("MENU:\n1.Insert\n2.Search\n3.Remove\n4.Traversals\n5.Exit")
	option = int(input("Enter your choice: "))
	if(option == 1):
		val = int(input("Enter the element to be inserted: "))
		tree.insert(val)
		tree.calcBalance(tree.rootNode)
		drawTree(tree, "AVL", 0)
	elif(option == 2):
		val = int(input("Enter the element to be searched: "))
		s = tree.find(val)
	elif(option == 3):
		val = int(input("Enter the element to be removed: "))
		# s = tree.find(val)
		# drawTree(tree, "AVL", s)
		s = tree.remove(val)
		tree.calcBalance(tree.rootNode)
		drawTree(tree, "AVL", s)
	elif(option == 4):
		print("MENU:\n1.Inorder\n2.Preorder\n3.Postorder")
		choice = int(input("Enter your choice: "))
		if(choice == 1):
			tree.inorder(tree.rootNode)
			drawTree(tree, "AVL", 0)
			tree.visited = []
		elif(choice == 2):
			tree.preorder(tree.rootNode)
			drawTree(tree, "AVL", 0)
			tree.visited = []
		elif(choice == 3):
			tree.postorder(tree.rootNode)
			drawTree(tree, "AVL", 0)
			tree.visited = []
		else:
			print("Invalid option!\n")
	elif(option == 5):
		break
	else:
		print("Invalid option!\n")
