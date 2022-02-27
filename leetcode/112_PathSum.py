# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        def dfs(node,ans,targetSum):
            if not node: return False
            ans += node.val
            if ans == targetSum and not node.left and not node.right: return True
            return dfs(node.left,ans,targetSum) or dfs(node.right,ans,targetSum)
        return dfs(root,0,targetSum)
    
    
    


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False

        if not root.left and not root.right and root.val == targetSum:
            return True
        
        targetSum -= root.val

        return self.hasPathSum(root.left, targetSum) or self.hasPathSum(root.right, targetSum)
    # Solution 2: iterative - by adding up node values
class Solution:
    def hasPathSum(self, root: TreeNode, target: int) -> bool:
        if not root:
            return False
        
        stk = [(root, root.val)]      
        
        while stk:
            node, val = stk.pop()
            
            if val == target and not node.left and not node.right:
                return True
            else:
                if node.left:
                    stk.append((node.left, val+node.left.val))
                if node.right:
                    stk.append((node.right, val+node.right.val))
                    
        return False
    
