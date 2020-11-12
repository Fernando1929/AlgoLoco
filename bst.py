class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
    
    # A utility function to insert 
    # a new node with the given key
    
    
    def insert(root, key):
        if root is None:
            return Node(key)
        else:
            if root.val == key:
                return root
            elif root.val < key:
                root.right = Node.insert(root.right, key)
            else:
                root.left = Node.insert(root.left, key)
        return root
    
    # A utility function to do inorder tree traversal
    
    
    def inorder(root):
        if root:
            Node.inorder(root.left)
            print(root.val)
            Node.inorder(root.right)
    
    def inorderarr(root,ls):
        result = []
        if root:
            result = result + Node.inorderarr(root.left,result)
            result.append(root.val)
            result = result + Node.inorderarr(root.right,result)
        
        return result

    def search(root,key):
        # Base Cases: root is null or key is present at root
        if root is None or root.val == key:
            return root
    
        # Key is greater than root's key
        if root.val < key:
            return Node.search(root.right,key)
    
        # Key is smaller than root's key
        return Node.search(root.left,key)
 