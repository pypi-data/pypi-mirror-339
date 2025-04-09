import numpy as np

class Helper:
    def __init__(self):
        self.a = None
        self.b = None
        self.mat = None
        self.eVal = None
        self.eVec = None

    def set_vector(self, arr1: list, arr2: list):
        self.a = np.array(arr1)
        self.b = np.array(arr2)
    
    def set_matrix(self, arr: list):
        self.mat = np.array(arr)
        self.eVal, self.eVec = np.linalg.eig(self.mat)

    def dot(self):
        return self.a@self.b

    def cos(self):
        try:
            return (self.dot())/(np.linalg.norm(self.a-self.b))
        except:
            return 0.0
    
    def deg(self):
        return np.rad2deg(np.arccos(self.cos()))

    def diag(self):
        return np.diag([self.eVal[1], self.eVal[0]])

    def stack(self):
        return np.column_stack((self.eVec[:,1], self.eVec[:,0]))
    
    def matrix(self):
        return self.mat
    
    @staticmethod
    def inverse(a):
        try:
            return np.linalg.inv(a)
        except:
            return 0.0
        
    def case2(self, arr: list, n: int):
        self.set_matrix(np.array(arr))
        A = self.matrix()
        D = self.diag()
        P = self.stack()

        print(f"n이 {n}일때")
        print(f"A :\n{A}")
        print(f"P :\n{P}")
        print(f"D^n :\n{D**n}")
        print(f"P의 역행렬 :\n{self.inverse(P)}")

    def case1(self, a: list, b:list, rad: bool, deg: bool):
        self.set_vector(a, b)
        x = (self.a@self.b)/np.linalg.norm(self.a-self.b)
        if rad: print(x)
        if deg: print(np.rad2deg(np.arccos(x)))
