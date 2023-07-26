def GetTarget(
    Origin: str = "Celeste_strawberry_with_wings.png",
    CenterX: int = 0.55,
    CenterY: int = 0.6,
    R: int = 250,
):
    from PIL import Image
    import numpy as np

    T = Image.open(Origin)
    data = np.asarray(T).astype(np.ubyte)  # dtype=ubyte
    T.close()

    del T

    Height, Width = len(data), len(data[0])

    DxCenter, DyCenter = np.uintc(np.rint(Width * CenterX)), np.uintc(
        np.rint(Height * CenterY)
    )

    AddRowBefore, AddRowAfter = R - DyCenter, (DyCenter + R) - Height
    AddColumnBefore, AddColumnAfter = R - DxCenter, (DxCenter + R) - Width

    RowsAdded = 0
    if AddRowBefore > 0:
        RowsAdded += AddRowBefore
        RowsBefore = np.zeros((AddRowBefore, Width, 4), dtype=np.ubyte)
        data = np.concatenate([RowsBefore, data])
    if AddRowAfter > 0:
        RowsAdded += AddRowAfter
        RowsAfter = np.zeros((AddRowAfter, Width, 4), dtype=np.ubyte)
        data = np.concatenate([data, RowsAfter])
    if AddColumnBefore > 0:
        ColumnsBefore = np.zeros(
            (Height + RowsAdded, AddColumnBefore, 4), dtype=np.ubyte
        )
        data = np.concatenate([ColumnsBefore, data], axis=1)
    if AddColumnAfter > 0:
        ColumnsAfter = np.zeros((Height + RowsAdded, AddColumnAfter, 4), dtype=np.ubyte)
        data = np.concatenate([data, ColumnsAfter], axis=1)

    Top, Bottom, Left, Right = DyCenter - R, DyCenter + R, DxCenter - R, DxCenter + R

    print(Top, Bottom, Left, Right)

    data = data[Top:Bottom, Left:Right]

    del Top, Bottom, Left, Right, RowsAdded
    Rsqrd = R * R
    for Row in np.arange(-R, R):
        print(Row)
        for Column in np.arange(-R, R):
            if Row * Row + Column * Column > Rsqrd:
                data[Row + R][Column + R] = np.array([0, 0, 0, 0])

    data = data.reshape(((R * 2) ** 2, 4))
    Target = np.apply_along_axis(np.linalg.norm, 0, data)
    return Target


if __name__ == "__main__":
    GetTarget()
