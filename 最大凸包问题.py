"""
    最大凸包问题的算法阐述
"""
import random
from matplotlib import pyplot


class point2d_t:
    MIN = 0
    MAX = 100

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    @staticmethod
    def generate_some_points(size: int) -> []:
        res = []
        for _ in range(size):
            p = point2d_t(random.randint(point2d_t.MIN, point2d_t.MAX), random.randint(point2d_t.MIN, point2d_t.MAX))
            res.append(p)
        return res

    def __str__(self):
        return "({},{})".format(self.x, self.y)


def sorted_point_set_by_x_ref_y(_point_set: list) -> []:
    bucket = [[_point_set[0], []]]
    # 首先按照主关键字坐标x排序，采用二分折半插入排序方式
    for point in _point_set[1:]:
        # locate
        low = 0
        high = len(bucket) - 1
        # 定位位置
        out_mid = 0
        while low <= high:
            mid = int((low + high) / 2)
            if point.x > bucket[mid][0].x:
                low = mid + 1
            else:
                high = mid - 1
                out_mid = mid
        # 如果相等，拉链加入到列表中
        if bucket[out_mid][0].x == point.x:
            if point.y < bucket[out_mid][0].y:
                temp = bucket[out_mid][0]
                bucket[out_mid][0] = point
                point = temp
            bucket[out_mid][1].append(point)
        else:
            bucket.insert(low, [point, []])
    # 对每个桶列表中的元素按照副关键字y排序
    for element in bucket:
        if element[1]:
            element[1].sort(key=lambda p: p.y)
    # 扁平化
    res = []
    for element in bucket:
        res.append(element[0])
        if element[1]:
            res.extend(element[1])
    return res


# 将点集依据x轴排序结果，分为上下两个凸包
def split_up_and_down(point_set: list) -> ():
    up_ = []
    down_ = []
    for point in point_set[1:-1]:
        if is_turn_left(point_set[0], point_set[-1], point):
            up_.append(point)
        elif is_turn_right(point_set[0], point_set[-1], point):
            down_.append(point)
    return up_, down_


# 判断点的走向是否右转
def is_turn_right(_p1: point2d_t, _p2: point2d_t, _p3: point2d_t) -> bool:
    return (_p1.x * _p2.y + _p3.x * _p1.y + _p2.x * _p3.y - _p3.x * _p2.y - _p2.x * _p1.y - _p1.x * _p3.y) < 0


# 判断点的走向是否左转
def is_turn_left(_p1: point2d_t, _p2: point2d_t, _p3: point2d_t) -> bool:
    return (_p1.x * _p2.y + _p3.x * _p1.y + _p2.x * _p3.y - _p3.x * _p2.y - _p2.x * _p1.y - _p1.x * _p3.y) > 0


def main():
    points = point2d_t.generate_some_points(100)
    points = sorted_point_set_by_x_ref_y(points)
    print("coordinate x => ", list(map(lambda p: p.x, points)))
    print("coordinate y => ", list(map(lambda p: p.y, points)))
    up, down = split_up_and_down(points)
    up.append(points[-1])
    down.append(points[-1])
    print("---------------------up----------------------")
    for u in up: print(u)
    print('-------------------down---------------------')
    for d in down: print(d)
    stack_up = [points[0], up[0]]
    stack_down = [points[0], down[0]]
    # 处理上凸包
    for up_point in up[1:]:
        stack_up.append(up_point)
        while len(stack_up) > 2 and not is_turn_right(stack_up[-3], stack_up[-2], stack_up[-1]):
            stack_up.pop(-2)
    # 处理下凸包
    for down_point in down[1:]:
        stack_down.append(down_point)
        while len(stack_down) > 2 and not is_turn_left(stack_down[-3], stack_down[-2], stack_down[-1]):
            stack_down.pop(-2)
    get_x = lambda p: p.x
    get_y = lambda p: p.y
    # 画出所有的点
    pyplot.scatter(
        list(map(get_x, points)), list(map(get_y, points)),
    )
    pyplot.plot(
        [points[0].x, points[-1].x], [points[0].y, points[-1].y], linestyle='--'
    )
    # 画出上凸包
    pyplot.plot(
        list(map(get_x, stack_up)), list(map(get_y, stack_up))
    )
    # 画出下凸包
    pyplot.plot(
        list(map(get_x, stack_down)), list(map(get_y, stack_down))
    )
    pyplot.show()


def test_sort():
    point_set = point2d_t.generate_some_points(100)
    sorted_point_set = sorted_point_set_by_x_ref_y(point_set)
    for point in sorted_point_set:
        print(point)


if __name__ == "__main__":
    main()
