# Python-2048Game
这是使用Python编写的2048游戏，用户可以在main函数中自由设置赢数大小（如128，256,512等）。程序原理很简单：左右上下移动矩阵并且做数据合并操作。整体的程序流程使用的是“状态机（Sate Machine）”思想，主要是用某种action（在python中表现为def function），输入现在的状态，返回下一次的状态。在矩阵合并的同时，做Win和GameOver的判断。如果是，则进入此状态，并输出出来。
程序的缺点就是没有实现图形可视化，接下来需要做的是使用Pygame模块将游戏使用resources图形界面可视化，对图形进行操作。
