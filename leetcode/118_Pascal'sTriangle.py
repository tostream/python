class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
#iterating num for every row
#make hand and end to be 1 on each row
#iterate for each row start from second column until second last column
#sum the same position and preivous position of perivous row
        res = [[1]]
        for i in range(2,numRows+1):
            temp_arr = [1] * i
            for j in range(1,i-1):
                temp_arr[j] = res[i-2][j-1] + res[i-2][j]
            res.append(temp_arr)
        return res
