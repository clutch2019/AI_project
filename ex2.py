
class A:
    def __init__(self, a1, a2):
         self.a1 = a1
         self.a2 = a2
    def pt(self):
        print(self.a1)

class B(A):
    def __init__(self,a1,a2,a3):
        super(B, self).__init__(a1, a2)
        self.a3 = a3

b = B(1,2,3)
print(b.a3)