class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.cargo)


def total(tree):
    if tree is None:
        return 0

    return total(tree.left) + total(tree.right) + tree.cargo


l = Tree(1)
r = Tree(2)
t = Tree(3, l, r)

print(l)
print(r)
print(t)
print(total(t))
