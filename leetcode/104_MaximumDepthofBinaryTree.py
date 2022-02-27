# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node,level):
            if not node: return level
            level += 1 
            return max(dfs(node.left,level) , dfs(node.right,level))
        return dfs(root,0)

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        level = 1
        queue = deque([[root, level]])
        while queue:
            node, level = queue.popleft()
            if node.left:
                queue.append([node.left, level + 1])
            if node.right:
                queue.append([node.right, level + 1])
        return level
