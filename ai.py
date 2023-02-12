import types

class AI_TYPE:
    Normal = "ENEMY.AI.NOR1"

class EnemyAI:
    @classmethod
    def ioad_ai(self,NAME):
        if NAME == AI_TYPE.Normal:
            return NormalAI
        else:
            return EnemyAI
    def __init__(self,x,y):
        self.__x = x
        self.__y = y
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    def get_loot(self):
        return []
    def get_optimal(self):
        return (0,0)

class NormalAI(EnemyAI):
    def __init__(self, x, y):
        super().__init__(x, y)
    def get_dif(self,pos1,pos2):
        return (abs(pos1[0] - pos2[0]),abs(pos1[1] - pos2[1]))
    def get_loot(self,start:tuple,target:tuple):
        n_left = (start[0] - 1,start[1])
        n_right = (start[0] + 1,start[1])
        n_bottom = (start[0],start[1] + 1)
        n_up = (start[0],start[1] - 1)
        if target in [n_left,n_right,n_bottom,n_up]:
            return (True,target)
        left = self.get_dif(n_left,target)
        right = self.get_dif(n_right,target)
        bottom = self.get_dif(n_bottom,target)
        up = self.get_dif(n_up,target)
        t_left = left[0] + left[1]
        t_right = right[0] + right[1]
        t_bottom = bottom[0] + bottom[1]
        t_up = up[0] + up[1]
        move = {
            t_left:n_left,
            t_right:n_right,
            t_bottom:n_bottom,
            t_up:n_up
        }
        index = min(t_left,t_right,t_bottom,t_up)
        return (False,move[index])
    def get_totaly(self,start,target):
        moves = [start]
        last = start
        for _ in range(1000):
            move = self.get_loot(last,target)
            moves.append(move[1])
            last = move[1]
            if move[0]:
                return moves
        return [target]
    def get_optimal(self,start,target):
        n_left = (start[0] - 1,start[1])
        n_right = (start[0] + 1,start[1])
        n_bottom = (start[0],start[1] + 1)
        n_up = (start[0],start[1] - 1)
        if target in [n_left,n_right,n_bottom,n_up]:
            return target
        left = self.get_totaly(n_left,target)
        right = self.get_totaly(n_right,target)
        bottom = self.get_totaly(n_bottom,target)
        up = self.get_totaly(n_up,target)
        t_left = len(left)
        t_right = len(right)
        t_bottom = len(bottom)
        t_up = len(up)
        move = {
            t_left:left,
            t_right:right,
            t_bottom:bottom,
            t_up:up
        }
        index = min(t_left,t_right,t_bottom,t_up)
        return move[index][0]