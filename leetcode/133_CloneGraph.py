class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        marked = {}

        def dfs(node):
            if not node:
                return node
            #If it exists in the hash table, it directly returns the value stored in the hash table
            if node in marked:
                return marked[node]
            
            #If there is no hash table, clone the node and put it into the hash table
            clone_node = Node(node.val, [])
            marked[node] = clone_node
            #Traverse the adjacent points of nodes, and put the adjacent nodes in the adjacency list
            for neighbor in node.neighbors:
                clone_node.neighbors.append(dfs(neighbor))
            
            return clone_node
        
        return dfs(node)
