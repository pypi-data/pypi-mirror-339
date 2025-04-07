class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # Pointer to the next node


class LinkedList:
    def __init__(self):
        self.head = None  # Start of the list
        self.count = 0    # Number of nodes

    def append(self, data):
        """Add a new result at the end."""
        new_node = Node(data)
        if not self.head:  # If the list is empty
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Traverse to the last node
                current = current.next
            current.next = new_node  # Attach new node
        self.count += 1

    def insert(self, data, position):
        """Insert at a specific position (1-based index)."""
        if position < 1 or position > self.count + 1:
            print("Invalid position!")
            return

        new_node = Node(data)

        if position == 1:  # Insert at the beginning
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 2):  # Traverse to node before target
                current = current.next
            new_node.next = current.next
            current.next = new_node

        self.count += 1

    def delete(self, position):
        """Delete a result by its position (1-based index)."""
        if position < 1 or position > self.count:
            print("Invalid position!")
            return

        if position == 1:  # Delete the first node
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(position - 2):  # Traverse to node before target
                current = current.next
            current.next = current.next.next  # Remove node

        self.count -= 1

    def count_nodes(self):
        """Return the number of nodes."""
        return self.count

    def get_all(self):
        """Retrieve all results as a list."""
        results = []
        current = self.head
        while current:
            results.append(current.data)
            current = current.next
        return results

    def display(self):
        """Display all results with numbering (for console debugging)."""
        current = self.head
        index = 1
        while current:
            print(f"{index}. {current.data}")
            current = current.next
            index += 1
