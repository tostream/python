# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
    
        ans = []
        queue = [root]
        while(queue):
            node = queue.pop()
            if node:
                ans.append(node.val)
                queue.append(node.right)
                queue.append(node.left)
        return ans
    
        def dfs(node,ans):
            if not node:
                return None
            ans.append(node.val)
            dfs(node.left,ans)
            dfs(node.right,ans)
            return ans
        
        return dfs(root,[])
