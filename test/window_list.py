import pygetwindow as gw

windows = gw.getAllWindows()

for i, w in enumerate(windows):
    if w.title:  # 只遍历有标题窗口
        print(f'{i}: {w.title}')