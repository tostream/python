class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        nums=[i for i in set(nums)]
        nums.sort(reverse=True)
        print(nums)
        if len(nums) < 3:
            return nums[0]
        else:
            return nums[2]
            
#-------------------------#
class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        nums.sort()
        result = [nums[-1]]
        for i in range(len(nums)-2,-1,-1):
            if nums[i] != nums[i+1]:
                result.append(nums[i])
        if len(result) < 3:
            return result[0]
        else:
            return result[2]
