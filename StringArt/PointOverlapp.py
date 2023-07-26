import numpy as np


def Distance(Point1, Point2, Current):
    return np.linalg.norm(np.cross(Point2 - Point1, Point1 - Current)) / np.linalg.norm(
        Point2 - Point1
    )


SIGMA = 2


def Color(*args):
    return np.exp((Distance(*args) / SIGMA) ** 2 * -0.5)


def Color2(*args):
    return 1 - Distance(*args) / 4


def f(*args):
    D = abs(Distance(*args))
    if D < 0.5:
        return 0.6
    if 0.5 <= D < 3.5:
        return -0.2 * D + 0.5
    return 0


def Test(Point1, Point2):
    [Bottom, Top], [Left, Right] = sorted([Point1[1], Point2[1]]), sorted(
        [Point1[0], Point2[0]]
    )

    values = set()

    for y in np.arange(Bottom, Top):
        for x in np.arange(Left, Right):
            val = np.array(
                f(
                    Point1,
                    Point2,
                    np.array([x, y]),
                )
                * np.array([255, 255, 255])
            ).astype(int)
            if max(val) > 127:
                values.add((tuple(val), (x, y)))
    # print(data)

    # from PIL import Image, ImageDraw

    # im = Image.new("RGB", (Top - Bottom, Right - Left))
    # draw = ImageDraw.Draw(im)

    # for Y, y in enumerate(data):
    #     for X, x in enumerate(y):
    #         draw.point((Y, X), tuple(x.astype(int)))

    # im.save("Test3.png", "PNG")


def Test2(Point1, Point2):
    Vector = Point2 - Point1
    Current = Point1.copy().astype(np.float32)
    SCALE = sum(abs(Vector))
    Points = set()
    while np.linalg.norm(Current - Point2) >= 0.04:
        Current += Vector / SCALE
        # yield tuple(np.rint(Current).astype(np.intc))
        Points.add(tuple(np.rint(Current).astype(np.intc)))


def Temp(Point1, Point2):
    from shapely._geometry import LineString

    # from shapely.ops import unary_union

    line = LineString((Point1, Point2))
    n = 100
    distances = np.linspace(0, line.length, n)
    points = [line.interpolate(distance) for distance in distances]
    # multipoint = unary_union(points)


if __name__ == "__main__":
    from timeit import default_timer as timer

    All = set()

    start = timer()
    for _ in range(360):
        All.add(Test2(np.array([0, 0]), np.array([2000, 2000])))
    end = timer()
    print(end - start)
