# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None and root2 is None: return None
        temp_node = TreeNode(0)
        temp_node.val = (0 if root1 is None else root1.val)  +  (0 if root2 is None else root2.val)
        temp_node.left = self.mergeTrees((None if root1 is None else root1.left),(None if root2 is None else root2.left))
        temp_node.right = self.mergeTrees((None if root1 is None else root1.right), (None if root2 is None else root2.right))
        return temp_node
