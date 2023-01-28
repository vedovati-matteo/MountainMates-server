import numpy as np

def suggest_friends(matrix, node):
    friends = []
    # Find the friends of the given node by finding the indices with value 1 in the matrix
    for i in range(len(matrix)):
        if matrix[node][i] == 1:
            friends.append(i)
    # Find the friends of the friends by checking the indices with value 1 in the matrix
    friends_of_friends = []
    for friend in friends:
        for i in range(len(matrix)):
            if matrix[friend][i] == 1 and i != node and i not in friends:
                friends_of_friends.append(i)
    return list(set(friends_of_friends))

# Create an adjacency matrix representing the graph
matrix = np.array([[0, 1, 1, 0], 
                   [1, 0, 1, 1], 
                   [1, 1, 0, 1], 
                   [0, 1, 1, 0]])

# Find friends of friends for node 0
suggested_friends = suggest_friends(matrix, 0)
print("Suggested friends for node 0:", suggested_friends)

