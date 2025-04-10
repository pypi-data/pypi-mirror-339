class Node:
    """A node for a singly linked list.
    
    Attributes:
        data: The data stored in the node.
        next: Reference to the next node in the list.
    """
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """A singly linked list implementation.
    
    Supports common linked list operations with proper error handling.
    """

    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self.head = None

    def get_node_at_index(self, index) -> Node:
        """Get the node at a specific index.
        
        Args:
            index: The position of the node to retrieve (0-based).
            
        Returns:
            The node at the specified index, or None if index is invalid.
        """
        if index < 0 or index >= self.get_length():
            return None
        current_node = self.head
        current_index = 0
        while current_index < index:
            current_node = current_node.next
            current_index += 1
        return current_node

    def get_length(self) -> int:
        """Get the number of nodes in the list.
        
        Returns:
            The count of nodes in the linked list.
        """
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
        return count

    def insert_at_beginning(self, item) -> None:
        """Insert a new node at the beginning of the list.
        
        Args:
            item: The data to be inserted.
        """
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def insert_after(self, item, index) -> None:
        """Insert a new node after the specified index.
        
        Args:
            item: The data to be inserted.
            index: The position after which to insert.
            
        Raises:
            IndexError: If the index is invalid.
        """
        prev_node = self.get_node_at_index(index)
        if prev_node is None:
            raise IndexError("Invalid index for insertion")
        new_node = Node(item)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def insert_at_end(self, item) -> None:
        """Insert a new node at the end of the list.
        
        Args:
            item: The data to be inserted.
        """
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def delete_at_index(self, index) -> None:
        """Delete the node at the specified index.
        
        Args:
            index: The position of the node to delete.
            
        Raises:
            IndexError: If the index is invalid.
        """
        if index < 0 or index >= self.get_length():
            raise IndexError("Invalid index for deletion")
        
        if index == 0:
            self.head = self.head.next
            return
            
        prev_node = self.get_node_at_index(index-1)
        if prev_node is None or prev_node.next is None:
            raise IndexError("Invalid index for deletion")
        prev_node.next = prev_node.next.next

    def delete_item(self, item) -> bool:
        """Delete the first occurrence of the specified item.
        
        Args:
            item: The data to be deleted.
            
        Returns:
            True if the item was found and deleted, False otherwise.
        """
        temp = self.head
        prev = None
        
        if temp is not None and temp.data == item:
            self.head = temp.next
            return True
            
        while temp is not None:
            if temp.data == item:
                break
            prev = temp
            temp = temp.next
            
        if temp is None:
            return False
            
        prev.next = temp.next
        return True

    def display(self) -> None:
        """Display the contents of the linked list."""
        node = self.head
        while node:
            print(node.data, end=" -> ")
            node = node.next
        print("None")

    def search(self, item) -> bool:
        """Search for an item in the list.
        
        Args:
            item: The data to search for.
            
        Returns:
            True if the item is found, False otherwise.
        """
        current = self.head
        while current is not None:
            if current.data == item:
                return True
            current = current.next
        return False

    def access(self, index) -> any:
        """Access the data at a specific index.
        
        Args:
            index: The position to access.
            
        Returns:
            The data at the specified index.
            
        Raises:
            IndexError: If the index is invalid.
        """
        node = self.get_node_at_index(index)
        if node is None:
            raise IndexError("Index out of range")
        return node.data

    def update(self, index, new_data) -> None:
        """Update the data at a specific index.
        
        Args:
            index: The position to update.
            new_data: The new data to store.
            
        Raises:
            IndexError: If the index is invalid.
        """
        node = self.get_node_at_index(index)
        if node is None:
            raise IndexError("Index out of range")
        node.data = new_data

    def concatenate(self, other_list) -> None:
        """Concatenate another linked list to this one.
        
        Args:
            other_list: The linked list to concatenate.
        """
        if self.head is None:
            self.head = other_list.head
            return
            
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = other_list.head

    def reverse(self) -> None:
        """Reverse the linked list in place."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sort(self) -> None:
        """Sort the linked list in ascending order using bubble sort."""
        if self.head is None:
            return
            
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                if current.data > current.next.data:
                    # Swap data
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next

    def delete_from_beginning(self) -> None:
        """Delete the first node in the list.
        
        Raises:
            IndexError: If the list is empty.
        """
        if self.head is None:
            raise IndexError("Cannot delete from empty list")
        self.head = self.head.next

    def delete_from_end(self) -> None:
        """Delete the last node in the list.
        
        Raises:
            IndexError: If the list is empty.
        """
        if self.head is None:
            raise IndexError("Cannot delete from empty list")
            
        if self.head.next is None:
            self.head = None
            return
            
        second_last = self.head
        while second_last.next.next:
            second_last = second_last.next
        second_last.next = None