# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        i_a=0
        arr_a = []
        i_b=0
        arr_b =[]
        ans=None
        while headA:
            arr_a.append(headA)
            i_a+=1
            headA=headA.next
        while headB:
            arr_b.append(headB)
            i_b+=1
            headB=headB.next
        i_a -=1
        i_b -= 1
        while i_a >= 0 and i_b >= 0:
            if arr_a[i_a] != arr_b[i_b]:
                return ans
            ans = arr_a[i_a]
            i_a -= 1
            i_b -= 1
        return ans
                
