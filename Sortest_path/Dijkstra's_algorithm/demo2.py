#!/usr/bin/python3
import sys


# Creating the graph as an adjacency matrix 
# Creating topology
# vertices = [[0, 1, 1, 0],
#             [0, 0, 1, 0],
#             [0, 0, 0, 1],
#             [0, 0, 0, 0]]
# edges =  [[0, 3, 4, 0],
#           [0, 0, 0.5, 0],
#           [0, 0, 0, 1],
#           [0, 0, 0, 0]]

vertices = [[0,1,0,1,0,0,0],
            [0,0,1,0,1,0,0],
            [0,0,0,0,0,1,1],
            [0,0,0,0,1,0,0],
            [0,0,0,0,0,1,0],
            [0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0],]
edges = [[0,2,0,3,0,0,0],
         [0,0,5,0,4,0,0],
         [0,0,0,0,0,4,3],
         [0,0,0,0,5,0,0],
         [0,0,0,0,0,2,0],
         [0,0,0,0,0,0,1],
         [0,0,0,0,0,0,0]]

# vertices = [[0,1,0,1,0,0,0],
#             [0,0,1,0,0,0,0],
#             [0,0,0,0,0,1,1],
#             [0,0,0,0,1,0,0],
#             [0,0,0,0,0,0,0],
#             [0,0,0,0,0,0,1],
#             [0,0,0,0,0,0,0],]
# edges = [[0,2,0,3,0,0,0],
#          [0,0,5,0,0,0,0],
#          [0,0,0,0,0,4,3],
#          [0,0,0,0,5,0,0],
#          [0,0,0,0,0,0,0],
#          [0,0,0,0,0,0,1],
#          [0,0,0,0,0,0,0]]




# Function to find out which of the unvisited node 
# needs to be visited next
def to_be_visited():
  global visited_and_distance
  v = -10
  # Choosing the vertex with the minimum distance
  for index in range(number_of_vertices):
    if visited_and_distance[index][0] == 0 and (v < 0 or visited_and_distance[index][1] <= visited_and_distance[v][1]):
        v = index
  return v


number_of_vertices = len(vertices[0])

# The first element of the lists inside visited_and_distance 
# denotes if the vertex has been visited.
# The second element of the lists inside the visited_and_distance 
# denotes the distance from the source.
visited_and_distance = [[0, 0]]
previous_node = [-1]
for i in range(number_of_vertices-1):
    visited_and_distance.append([0, sys.maxsize])
    previous_node.append(-1)


for vertex in range(number_of_vertices):
  # Finding the next vertex to be visited.
  to_visit = to_be_visited()
  for neighbor_index in range(number_of_vertices):
    # Calculating the new distance for all unvisited neighbors
    # of the chosen vertex.
    if vertices[to_visit][neighbor_index] == 1 and visited_and_distance[neighbor_index][0] == 0:
      new_distance = visited_and_distance[to_visit][1] + edges[to_visit][neighbor_index]
      # Updating the distance of the neighbor if its current distance
      # is greater than the distance that has just been calculated
      if visited_and_distance[neighbor_index][1] > new_distance:
        visited_and_distance[neighbor_index][1] = new_distance
        previous_node[neighbor_index] = to_visit
      # Visiting the vertex found earlier
      visited_and_distance[to_visit][0] = 1



i = 0 
# Printing out the shortest distance from the source to each vertex
print("Node  Cost  Previous\n----------------------")       
for distance in visited_and_distance:
  # print("The shortest distance of ",chr(ord('a') + i),\
  # " from the source vertex a is:",distance[1],",previous node is ",chr(ord('a') + previous_node[i]))
  print("",chr(ord('a') + i),"   ",distance[1],"     ",chr(ord('a') + previous_node[i]))
  i = i + 1

a_next_node=[0]
for i in range(number_of_vertices-1):
  a_next_node.append(0)

def find(theNode,answerNode):
  for i in range(number_of_vertices):
    if previous_node[i] == theNode:
      a_next_node[i]=answerNode
      find(i,answerNode)

temp=[-1]
for i in range(number_of_vertices):
  if previous_node[i] == 0:
    temp.append(i)

for i in temp:
  find(i,i)

i=0
print("Routing Table for Node A")
fix_string="{0:>11}".format("Destination")  + "{0:>7}".format("Cost") + "{0:>11}".format("NextNode")
print(fix_string)
for distance in visited_and_distance:
  print(chr(ord('a') + i),"           ",distance[1],"{0:>6}".format(chr(ord('a') + a_next_node[i])))
  i+=1
# print(a_next_node)