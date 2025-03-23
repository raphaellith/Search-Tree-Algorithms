from abc import ABC, abstractmethod


class AbstractSearchInterface(ABC):
    '''
    Abstract class to support search/insert operations (plus underlying data structure)

    '''

    @abstractmethod
    def insertElement(self, element):
        '''
        Insert an element in a search tree
            Parameters:
                    element: string to be inserted in the search tree (string)

            Returns:
                    "True" after successful insertion, "False" if element is already present (bool)
        '''

        pass


    @abstractmethod
    def searchElement(self, element):
        '''
        Search for an element in a search tree
            Parameters:
                    element: string to be searched in the search tree (string)

            Returns:
                    "True" if element is found, "False" otherwise (bool)
        '''

        pass


class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  #set intial height to 1

    def get_height(self, node):
        if node:
            return node.height
        else:
            return 0

    def get_balance(self, node):
        if node:
            return self.get_height(node.left) - self.get_height(node.right)
        else:
            return 0

    def right_rotate(self, ub_node):
        #right rotate the unbalanced Node ub_node
        left_c = ub_node.left
        right_c_of_left_c = left_c.right

        #right rotate
        left_c.right = ub_node
        ub_node.left = right_c_of_left_c

        #update heights
        ub_node.height = 1 + max(self.get_height(ub_node.left), self.get_height(ub_node.right))
        left_c.height = 1 + max(self.get_height(left_c.left), self.get_height(left_c.right))

        #return the new root node after rotation
        return left_c

    def left_rotate(self, ub_node):
        #left rotate the unbalanced Node ub_node
        right_c = ub_node.right
        left_c_of_right_c = right_c.left

        #left rotate
        right_c.left = ub_node
        ub_node.right = left_c_of_right_c

        #update heights
        ub_node.height = 1 + max(self.get_height(ub_node.left), self.get_height(ub_node.right))
        right_c.height = 1 + max(self.get_height(right_c.left), self.get_height(right_c.right))

        #return the new root node after rotation
        return right_c

    def insert(self, root, value):
        #BST insert
        if not root:
            return self.__class__(value)
        elif value < root.value:
            root.left = self.insert(root.left, value)
        else:
            root.right = self.insert(root.right, value)

        #update height of current node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        #check if unbalanced and rotate
        balance = self.get_balance(root)
        #case LL: left tree is too high and new node is on left side of left child
        if balance > 1 and value < root.left.value:
            #right rotate current node
            return self.right_rotate(root)

        #case RR: right tree is too high and new node is on right side of right child
        if balance < -1 and value > root.right.value:
            #left rotate current node
            return self.left_rotate(root)

        #case LR: left tree is too high and new node is on right side of left child
        if balance > 1 and value > root.left.value:
            #first left rotate left child of current node
            #then right rotate current node
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        #case RL: right tree is too high and new node is on left side of right child
        if balance < -1 and value < root.right.value:
            #first right rotate right child of current node
            #then left rotate current node
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, value):
        #BST search
        if root is None:
            return False
        if value == root.value:
            return True
        elif value < root.value:
            return self.search(root.left, value)
        else:
            return self.search(root.right, value)


class AVLTree(AbstractSearchInterface):
    def __init__(self):
        self.root = None

    def searchElement(self, element):
        if self.root is None:
            return False
        return self.root.search(self.root, element)

    def insertElement(self, element):
        if self.searchElement(element):
            return False
        if self.root is None:
            self.root = AVLNode(element)
            print(f"{element} was inserted as a root")
        else:
            self.root = self.root.insert(self.root, element)
        return True

def AVL_test():
    tree = AVLTree()
    elements = ["D", "B", "A", "C", "F", "E", "G"]

    print("Insert test：")
    # insert
    for elem in elements:
        result = tree.insertElement(elem)
        print(f"insert {elem}: {result}")

    # insert duplicate element
    duplicate = "B"
    result = tree.insertElement(duplicate)
    print(f"insert duplicate element {duplicate}: {result}")

    print("\nSearch test：")
    # search exist element
    for elem in ["A", "B", "C", "D", "E", "F", "G"]:
        found = tree.searchElement(elem)
        print(f"search {elem}: {found}")

    # search non exist element
    for elem in ["H", "Z"]:
        found = tree.searchElement(elem)
        print(f"search {elem}: {found}")

if __name__ == '__main__':
    AVL_test()
    
