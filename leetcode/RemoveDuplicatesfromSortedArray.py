class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        marked = {}
        length=0        
        dup_length=-1
        for i in range(len(nums)):
            if nums[i] not in marked:
                nums[length] = nums[i]
                marked[nums[i]] = 0
                length += 1
        for i in range(length,len(nums)):
            nums.pop()
