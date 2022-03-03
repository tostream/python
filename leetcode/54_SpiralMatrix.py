class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        #go right
        #while result length < martix length end
        #get value to result array
        #if y ==  hit the right side of wall and going right then go down
        #if x == hit the bottom side of wall and going down then go left
        #if y == hit the left side of wall and going left then going up
        #if x == hit the top side of wall and going up then going right
        #get length
        m , n = len(matrix) , len(matrix[0])
        result = []
        x , y = 0, 0
        direction = 1
        #1 = right, 2=down, 3=left, 4 = up
        level_wall = 0
        while(len(result) < m*n):
            result.append(matrix[x][y])
            if direction == 1:
                if y == n-1 - level_wall:
                    direction = 2
                    x += 1
                else:
                    y += 1
            elif direction == 2:
                if x == m-1- level_wall:
                    direction = 3
                    y -= 1
                else:
                    x += 1
            elif direction == 3:
                if y == 0 + level_wall:
                    level_wall += 1
                    direction = 4
                    x -= 1
                else:
                    y -= 1
            elif direction == 4:
                if x == 0 + level_wall:
                    direction = 1
                    y += 1
                else:
                    x -= 1
        
        return result
                

        def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
            res = []
            if len(matrix) == 0:
                return res
            row_begin = 0
            col_begin = 0
            row_end = len(matrix)-1 
            col_end = len(matrix[0])-1
            while (row_begin <= row_end and col_begin <= col_end):
                for i in range(col_begin,col_end+1):
                    res.append(matrix[row_begin][i])
                row_begin += 1
                for i in range(row_begin,row_end+1):
                    res.append(matrix[i][col_end])
                col_end -= 1
                if (row_begin <= row_end):
                    for i in range(col_end,col_begin-1,-1):
                        res.append(matrix[row_end][i])
                    row_end -= 1
                if (col_begin <= col_end):
                    for i in range(row_end,row_begin-1,-1):
                        res.append(matrix[i][col_begin])
                    col_begin += 1
            return res
######what is zip?###
    def spiralOrder(self, matrix):
        return matrix and [*matrix.pop(0)] + self.spiralOrder([*zip(*matrix)][::-1])
