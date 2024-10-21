



# 实现一个栈，并且实现一个函数，能够返回栈中最小的元素

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            if val == self.min_stack[-1]:
                self.min_stack.pop()

    def get_min(self) -> int:
        return self.min_stack[-1] if self.min_stack else float('inf')


# 测试
min_stack = MinStack()
min_stack.push(-2)
min_stack.push(0)
min_stack.push(-3)
print(min_stack.get_min())  # 输出 -3
min_stack.pop()
print(min_stack.top())     # 输出 0
print(min_stack.get_min())  # 输出 -2 