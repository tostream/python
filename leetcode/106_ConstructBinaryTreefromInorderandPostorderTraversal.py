# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        
        map_inorder = {}
        for i, val in enumerate(inorder): map_inorder[val] = i
        def recur(low, high):
            if low > high: return None
            x = TreeNode(postorder.pop())
            mid = map_inorder[x.val]
            x.right = recur(mid+1, high)
            x.left = recur(low, mid-1)
            return x
        return recur(0, len(inorder)-1)
      
# Definition for a  binary tree node
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    # @param inorder, a list of integers
    # @param postorder, a list of integers
    # @return a tree node
    # 12:00
    def buildTree(self, inorder, postorder):
        if not inorder or not postorder:
            return None
        
        root = TreeNode(postorder.pop())
        inorderIndex = inorder.index(root.val)

        root.right = self.buildTree(inorder[inorderIndex+1:], postorder)
        root.left = self.buildTree(inorder[:inorderIndex], postorder)

        return root
