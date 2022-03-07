class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        if len(nums) == 1 :
            return nums[0]
        result = {}
        for i in nums:
            if i in result:
                result[i] +=1
            else:
                result[i] = 1
        for key,item in result.items():
            if item == 1: return key
            
