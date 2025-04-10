class Node:
    """A node in a Binary Search Tree (BST).
    
    Attributes:
        data: The value stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
    """
    def __init__(self, data) -> None:
        """Initialize a new BST node.
        
        Args:
            data: The value to store in the node.
        """
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    """A Binary Search Tree (BST) implementation with common operations.
    
    Attributes:
        root: Reference to the root node of the tree.
    """
    
    def __init__(self) -> None:
        """Initialize an empty BST."""
        self.root = None

    def addNode(self, data) -> None:
        """Insert a new node with the given data into the BST.
        
        Args:
            data: The value to insert into the tree.
            
        Note:
            Duplicate values will be ignored with a message.
        """
        if not self.root:
            self.root = Node(data)
        else:
            self._insert(data, self.root)

    def _insert(self, data, current_node) -> None:
        """Recursively find the correct position and insert a new node.
        
        Args:
            data: The value to insert.
            current_node: The current node being examined in the recursion.
        """
        if data < current_node.data:
            if not current_node.left:
                current_node.left = Node(data)
            else:
                self._insert(data, current_node.left)
        elif data > current_node.data:
            if not current_node.right:
                current_node.right = Node(data)
            else:
                self._insert(data, current_node.right)
        else:
            print(f"Value {data} already exists in the tree.")

    def searchNode(self, data) -> bool:
        """Check if a value exists in the BST.
        
        Args:
            data: The value to search for.
            
        Returns:
            bool: True if value exists, False otherwise.
        """
        return self._search(data, self.root)

    def _search(self, data, current_node) -> bool:
        """Recursively search for a value in the BST.
        
        Args:
            data: The value to search for.
            current_node: The current node being examined.
            
        Returns:
            bool: True if value exists in subtree, False otherwise.
        """
        if not current_node:
            return False
        if data == current_node.data:
            return True
        elif data < current_node.data:
            return self._search(data, current_node.left)
        else:
            return self._search(data, current_node.right)

    def deleteNode(self, data) -> None:
        """Delete a node containing the specified value.
        
        Args:
            data: The value to delete from the tree.
        """
        self.root = self._deleteNode(data, self.root)

    def _deleteNode(self, data, current_node) -> Node:
        """Recursively find and delete the node with given value.
        
        Handles three cases:
        1. Node to delete has no children
        2. Node to delete has one child
        3. Node to delete has two children
        
        Args:
            data: The value to delete.
            current_node: Current node in recursion.
            
        Returns:
            Node: The modified subtree root after deletion.
        """
        if not current_node:
            return current_node

        if data < current_node.data:
            current_node.left = self._deleteNode(data, current_node.left)
        elif data > current_node.data:
            current_node.right = self._deleteNode(data, current_node.right)
        else:
            # Node with one or no child
            if not current_node.left:
                return current_node.right
            elif not current_node.right:
                return current_node.left

            # Node with two children
            current_node.data = self._minValue(current_node.right)
            current_node.right = self._deleteNode(current_node.data, current_node.right)

        return current_node

    def _minValue(self, node) -> int:
        """Find the minimum value in a subtree.
        
        Args:
            node: Root node of the subtree.
            
        Returns:
            The minimum value in the subtree.
        """
        current = node
        while current.left:
            current = current.left
        return current.data

    def inorder_traversal(self) -> list:
        """Return values in in-order traversal order.
        
        Returns:
            list: Values in left-root-right order.
        """
        return self._inorder(self.root, [])

    def _inorder(self, node, result) -> list:
        """Recursive helper for in-order traversal.
        
        Args:
            node: Current node in recursion.
            result: List accumulating values.
            
        Returns:
            list: Accumulated values in traversal order.
        """
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)
        return result

    def preorder_traversal(self) -> list:
        """Return values in pre-order traversal order.
        
        Returns:
            list: Values in root-left-right order.
        """
        return self._preorder(self.root, [])

    def _preorder(self, node, result) -> list:
        """Recursive helper for pre-order traversal."""
        if node:
            result.append(node.data)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result

    def postorder_traversal(self) -> list:
        """Return values in post-order traversal order.
        
        Returns:
            list: Values in left-right-root order.
        """
        return self._postorder(self.root, [])

    def _postorder(self, node, result) -> list:
        """Recursive helper for post-order traversal."""
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.data)
        return result
    
    def display(self):
        """Displays the tree in a hierarchical format."""
        if self.root:
            lines, *_ = self._display_helper(self.root)
            for line in lines:
                print(line)
        else:
            print("Empty tree")

    def _display_helper(self, node):
        """Returns list of strings for recursive tree display."""
        # Leaf node case
        if node.right is None and node.left is None:
            line = str(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child
        if node.right is None:
            lines, n, p, x = self._display_helper(node.left)
            s = str(node.data)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child
        if node.left is None:
            lines, n, p, x = self._display_helper(node.right)
            s = str(node.data)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children
        left, n, p, x = self._display_helper(node.left)
        right, m, q, y = self._display_helper(node.right)
        s = str(node.data)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2