# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        result = []
        while(head):
            result.append(head.val)
            head = head.next
        itr_ans = ans  = ListNode()
        for i in range(len(result)-1,-1,-1):
            ans.next = ListNode()
            ans = ans.next
            ans.val = result[i]
        
        return itr_ans.next

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        temp_node = ListNode()
        ans = None
        while(head):
            temp_node = head
            head = head.next
            temp_node.next = ans
            ans = temp_node
        return ans
