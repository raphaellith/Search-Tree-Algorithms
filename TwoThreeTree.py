class Node:
    def __init__(self, keys, parent = None):
        self.keys = list([keys]) #ensures that "keys" is always a list, even when setting it to a single element
        self.parent = parent #a single Node
        self.children = [] #list of child Nodes

    def isLeaf(self):
        return len(self.children) == 0
    
    def searchElement(self, key):
        found = False

        #base case: found the key
        if key in self.keys:
            found = True
            print(f"Key: {key} found!")
            return found
        
        #base case: couldn't find the key and reached the end of the tree
        elif self.isLeaf():
            print(f"Key: {key} was not found")
            return found
        
        elif key < self.keys[0]:#key is less than everything in the node, so recursively search left child
            return self.children[0].searchElement(key)
        elif key > self.keys[-1]: # key is more than everything in the node, so search right child
            return self.children[-1].searchElement(key)
        else: #this should only be reached when encountering a 3-node, and the value of "key" is between the keys in the node
            return self.children[1].searchElement(key)


    def insertElement(self, node):
        inserted = False

        if self.isLeaf():
            self.addNode(node)
            inserted = True
            print(f"{node.keys[0]} was inserted!")
            return inserted

        elif node.keys[0] < self.keys[0]:  # key is less than everything in the node, so recursively search left child
            return self.children[0].insertElement(node)
        elif node.keys[0] > self.keys[-1]:  # key is more than everything in the node, so search right child
            return self.children[-1].insertElement(node)
        else:  # this should only be reached when encountering a 3-node, and the value of "key" is between the keys in the node
            return self.children[1].insertElement(node)


    def addNode(self, node):
        #necessary for when dealing with 4-nodes (see below)
        for child in node.children:
            child.parent = self

        self.keys.extend(node.keys)
        self.keys.sort()
        self.children.extend(node.children)
        
        if len(self.children) > 1:
            self.children.sort(key=lambda node: node.keys) #Because children is a list of "nodes", must specify that we sort by the keys
        if len(self.keys) > 2:
            self.splitNode()
    
    #splitting a 4-node
    def splitNode(self):
        """
        NOTES:
        - self = Originally the middle key of the 4-node, it merges with the parent above it
        - leftChild = Originally the left key of the 4-node, it becomes a child of "self"
        - rightChild = Originally the right key of the 4-node, it also becomes a child of "self"
        """

        leftChild = Node(self.keys[0], self) #make "self" the parent because we are going to move the middle element up to create a new layer
        rightChild = Node(self.keys[2], self)

        #must check this because we could have created a 4-node that is also a leaf
        if self.children != []:
            #if the 4-node has children, then it must have exactly 4 of them, so:
            self.children[0].parent = leftChild
            self.children[1].parent = leftChild
            self.children[2].parent = rightChild
            self.children[3].parent = rightChild
            leftChild.children = [self.children[0], self.children[1]]
            rightChild.children = [self.children[2], self.children[3]]

        self.children = [leftChild, rightChild]
        self.keys = [self.keys[1]]

        if self.parent:
            if self in self.parent.children:
                self.parent.children.remove(self) #remove "self" from the list of children because we are merging "self" and its former parent
            self.parent.addNode(self) #recursively go up the tree until there are no 4-nodes
        else:
            leftChild.parent = self
            rightChild.parent = self

class TwoThreeTree():
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root == None:
            self.root = Node(key)
            print(f"{key} was inserted as a root!")
        else:
            node = Node(key)
            self.root.insertElement(node)
            #this is in case splitting the node creates a new root. just ensures that the root always has the correct assignment
            while self.root.parent:
                self.root = self.root.parent

    def search(self, key):
        return self.root.searchElement(key)



def test_two_three_tree():
    # Initialize the tree
    tree = TwoThreeTree()

    # Insert string keys
    keys = ["apple", "banana", "cherry", "date", "fig", "grape", "kiwi"]
    for key in keys:
        tree.insert(key)

    # Search for existing keys
    assert tree.search("apple") == True
    assert tree.search("banana") == True
    assert tree.search("cherry") == True

    # Search for a non-existing key
    assert tree.search("mango") == False

    # Insert additional keys to test tree balancing
    additional_keys = ["orange", "peach", "pear", "plum", "raspberry"]
    for key in additional_keys:
        tree.insert(key)

    # Search for the newly added keys
    for key in additional_keys:
        assert tree.search(key) == True

    # Edge case: insert a duplicate key (should not break the tree)
    tree.insert("apple")
    assert tree.search("apple") == True

    print("All tests passed!")


if __name__ == "__main__":
    test_two_three_tree()
