class Stack:
    """
    A stack data structure implementation using a list.

    Follows LIFO (Last In First Out) principle. Supports standard stack operations.

    Attributes:
        _Stack__items (list): Private list storing stack elements.
    """

    def __init__(self, items=None) -> None:
        """
        Initialize a new Stack object.

        Args:
            items (iterable, optional): Optional iterable to initialize the stack.
                Defaults to empty stack. Creates a copy to prevent aliasing issues.
        """
        if items is None:
            self.__items = []
        else:
            self.__items = list(items)  # Create copy to avoid reference issues

    def push(self, element) -> None:
        """
        Add an element to the top of the stack.

        Args:
            element: The element to be added to the stack
        """
        self.__items.append(element)

    def pop(self) -> None:
        """
        Remove and return the element from the top of the stack.

        Returns:
            The removed element from the top of the stack

        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.__items.pop()

    def top(self):
        """
        Return the top element without removing it.

        Returns:
            The element at the top of the stack

        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Top from empty stack")
        return self.__items[-1]

    def peek(self):
        """
        Alias for top() to match common stack terminology.

        Returns:
            The element at the top of the stack
        """
        return self.top()

    def size(self):
        """
        Return the number of elements in the stack.

        Returns:
            int: Number of elements in the stack
        """
        return len(self.__items)

    def is_empty(self) -> bool:
        """
        Check if the stack contains no elements.

        Returns:
            bool: True if stack is empty, False otherwise
        """
        return len(self.__items) == 0

    def display_stack(self) -> None:
        """
        Display the entire stack contents.

        Shows elements from bottom to top (insertion order).
        """
        print(self.__items)