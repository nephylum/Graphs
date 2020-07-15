import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        #hold users as keys and their path as values for return

        #know which nodes have been visited
        visited = {}

        newq = Queue()
        #start traversal at user_id
        newq.enqueue([user_id])

        while newq.size() > 0:
            #try a path in the queue
            path = newq.dequeue()
            #check the latest step
            v = path[-1]

            if v not in visited:
                #add to visited to prevent duplicates
                visited[v] = path

                #add neighbors as new paths 
                for next in self.friendships[v]:
                    copy = list(path)
                    copy.append(next)
                    newq.enqueue(copy)

        return visited

    def populate_graph_linear(self, num_users, avg_friendships):
        #reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        #Add users
        for i in range(num_users):
            self.add_user(f"User {i+1}")

        target_friendships = num_users * avg_friendships

        total_friendships = 0
        collisions = 0

        while total_friendships < target_friendships:
            #keep trying to add friendships
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total_friendships += 2
            else:
                collisions += 1

    def populate_graph(self, num_users, avg_friendships):
         # Reset graph
         self.last_id = 0
         self.users = {}
         self.friendships = {}
         # Add users
         for i in range(0, num_users):
             self.add_user(f"User {i}")
         # Create Frienships
         # Generate all possible friendship combinations
         possible_friendships = []
         # Avoid duplicates by ensuring the first number is smaller than the second
         for user_id in self.users:
             for friend_id in range(user_id + 1, self.last_id + 1):
                 possible_friendships.append((user_id, friend_id))
         # Shuffle the possible friendships
         random.shuffle(possible_friendships)
         # Create friendships for the first X pairs of the list
         # X is determined by the formula: num_users * avg_friendships // 2
         # Need to divide by 2 since each add_friendship() creates 2 friendships
         for i in range(num_users * avg_friendships // 2):
             friendship = possible_friendships[i]
             self.add_friendship(friendship[0], friendship[1])

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print("friendships\n",sg.friendships)
    connections = sg.get_all_social_paths(1)
    print("\nconnections:\n", connections)
    #sg.populate_graph_linear(10,2)
