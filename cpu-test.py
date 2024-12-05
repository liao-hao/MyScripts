import threading
import time
from typing import List

# 常量定义
THREAD_COUNT = 8
TEST_TYPES = 3
TEST_DURATION = 5000  # 毫秒

class CPUTask(threading.Thread):
    def __init__(self, test_type: int):
        super().__init__()
        self.test_type = test_type
        self.running = True
        self.operations = [0] * 3

    def stop(self):
        self.running = False

    def get_operations(self) -> List[int]:
        return self.operations

    def run(self):
        while self.running:
            if self.test_type == 0:    # 浮点运算
                x = 0.1
                for _ in range(1000):
                    x = x * x + 0.5
                self.operations[0] += 1

            elif self.test_type == 1:  # 整数运算
                x = 1
                for _ in range(1000):
                    x = (x * x + 1) % 1000000
                self.operations[1] += 1

            elif self.test_type == 2:  # 位运算
                bits = 0xFFFFFFFFFFFFFFFF
                for _ in range(1000):
                    bits = ((bits << 1) | (bits >> 63)) & 0xFFFFFFFFFFFFFFFF
                self.operations[2] += 1

def main():
    print("CPU 信息:")
    print(f"处理器数量: {THREAD_COUNT}")
    print("\n开始测试...")

    threads = [[None]*THREAD_COUNT for _ in range(TEST_TYPES)]
    tasks = [[None]*THREAD_COUNT for _ in range(TEST_TYPES)]

    # 启动所有测试线程
    for type_idx in range(TEST_TYPES):
        for i in range(THREAD_COUNT):
            tasks[type_idx][i] = CPUTask(type_idx)
            tasks[type_idx][i].start()
            threads[type_idx][i] = tasks[type_idx][i]

    time.sleep(TEST_DURATION/1000)

    # 停止所有线程并收集结果
    total_operations = [[0]*4 for _ in range(TEST_TYPES)]
    for type_idx in range(TEST_TYPES):
        for i in range(THREAD_COUNT):
            tasks[type_idx][i].stop()
            tasks[type_idx][i].join()
            total_operations[type_idx] = tasks[type_idx][i].get_operations()


    # 显示结果
    test_names = ["浮点运算", "整数运算", "位运算"]
    print("\n测试结果:")
    for i, name in enumerate(test_names):
        print(f"{name}: {sum(total_operations[i]):,} 次操作")

if __name__ == "__main__":
    main()