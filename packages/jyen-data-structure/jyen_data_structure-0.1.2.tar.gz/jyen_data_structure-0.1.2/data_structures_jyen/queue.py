class Queue:
    """
    A queue implementation using a list data structure.
    
    Follows FIFO (First-In First-Out) principle. Supports standard queue operations.
    
    Attributes:
        max_size (int|None): Maximum allowed elements (None for unlimited size)
        queue (list): Internal storage of queue elements
    """
    
    def __init__(self, max_size: int = None) -> None:
        """
        Initialize a new Queue instance.
        
        Args:
            max_size: Maximum number of elements allowed (None for unlimited)
        """
        self.queue = []
        self.max_size = max_size

    def enqueue(self, new_data) -> None:
        """
        Add an element to the end of the queue.
        
        Args:
            new_data: Element to be added to the queue
            
        Raises:
            OverflowError: If queue is at maximum capacity
        """
        if self.is_full():
            raise OverflowError("Queue is full")
        self.queue.append(new_data)

    def dequeue(self):
        """
        Remove and return the element from the front of the queue.
        
        Returns:
            The oldest element in the queue
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.queue.pop(0)

    def peek(self):
        """
        Return the front element without removing it.
        
        Returns:
            The oldest element in the queue
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.queue[0]

    def rear(self):
        """
        Return the element at the end of the queue.
        
        Returns:
            The newest element in the queue
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Rear from empty queue")
        return self.queue[-1]

    def is_full(self) -> bool:
        """
        Check if queue has reached maximum capacity.
        
        Returns:
            True if queue is full, False otherwise
        """
        if self.max_size is None:
            return False
        return len(self.queue) >= self.max_size

    def is_empty(self) -> bool:
        """
        Check if queue contains no elements.
        
        Returns:
            True if queue is empty, False otherwise
        """
        return len(self.queue) == 0

    def display_queue(self) -> None:
        """Display the queue contents in FIFO order."""
        print("Front ->", " | ".join(map(str, self.queue)), "<- Rear")

    def __len__(self) -> int:
        """Return number of elements in queue."""
        return len(self.queue)

    def __repr__(self) -> str:
        """Official string representation of the queue."""
        return f"Queue({self.queue})"