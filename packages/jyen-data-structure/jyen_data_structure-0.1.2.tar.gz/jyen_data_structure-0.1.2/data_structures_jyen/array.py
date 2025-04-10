class Array:
    """A static array implementation with fixed capacity and common operations.
    
    Attributes:
        capacity (int): Maximum number of elements the array can hold
        size (int): Current number of elements in the array
    """
    
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self.elements = [None] * capacity
        self.size = 0

    def insert_at(self, index: int, value) -> None:
        """Insert a value at the specified index.
        
        Args:
            index: Position to insert (0 <= index <= size)
            value: Data to insert
            
        Raises:
            OverflowError: If array is full
            IndexError: If index is out of valid range
        """
        if self.is_full():
            raise OverflowError("Cannot insert into full array")
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of bounds [0, {self.size}]")
            
        # Shift elements to make space
        for i in range(self.size, index, -1):
            self.elements[i] = self.elements[i-1]
            
        self.elements[index] = value
        self.size += 1

    def remove_at(self, index: int):
        """Remove and return the element at specified index.
        
        Args:
            index: Position to remove from
            
        Returns:
            The removed element
            
        Raises:
            IndexError: If array is empty or index invalid
        """
        if self.is_empty():
            raise IndexError("Cannot remove from empty array")
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of bounds [0, {self.size-1})")
            
        removed = self.elements[index]
        
        # Shift elements to fill gap
        for i in range(index, self.size-1):
            self.elements[i] = self.elements[i+1]
            
        self.elements[self.size-1] = None
        self.size -= 1
        return removed

    def append(self, value) -> None:
        """Add an element to the end of the array."""
        self.insert_at(self.size, value)

    def prepend(self, value) -> None:
        """Add an element to the beginning of the array."""
        self.insert_at(0, value)

    def get(self, index: int):
        """Get element at specified index."""
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of bounds [0, {self.size-1})")
        return self.elements[index]

    def set(self, index: int, value) -> None:
        """Update element at specified index."""
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of bounds [0, {self.size-1})")
        self.elements[index] = value

    def search(self, value) -> int:
        """Return first index of matching element or -1 if not found."""
        for i in range(self.size):
            if self.elements[i] == value:
                return i
        return -1

    def reverse(self) -> None:
        """Reverse elements in-place."""
        left, right = 0, self.size-1
        while left < right:
            self.elements[left], self.elements[right] = self.elements[right], self.elements[left]
            left += 1
            right -= 1

    def sort(self) -> None:
        """Sort elements in ascending order (in-place)."""
        self.elements[:self.size] = sorted(self.elements[:self.size])

    def is_empty(self) -> bool:
        """Check if array contains no elements."""
        return self.size == 0

    def is_full(self) -> bool:
        """Check if array has reached capacity."""
        return self.size == self.capacity

    def __len__(self) -> int:
        """Return current number of elements."""
        return self.size

    def __str__(self) -> str:
        """String representation of array elements."""
        return str(self.elements[:self.size])

    def __repr__(self) -> str:
        """Official string representation."""
        return f"Array(capacity={self.capacity}, size={self.size}, elements={self.elements[:self.size]})"