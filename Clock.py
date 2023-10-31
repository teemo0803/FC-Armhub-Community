# "时钟"游戏小项目程序模板

import simpleguitk as gui
import math
from datetime import datetime

# 定义全局变量
button_string1 = '开启数显'
button_string2 = '播放音乐'

date = ''
time = ''

display_digit = False
play_music = False
success = False

tenth_second = 0

hour_rotation = 0
minute_rotation = 0
second_rotation = 0

# 加载图像资源
clock_face = gui.load_image("http://202.201.225.74/video/PythonResoure/ProjectResource/images/project3/ClockFace.jpg")
hour = gui.load_image("http://202.201.225.74/video/PythonResoure/ProjectResource/images/project3//Hour.png")
minute = gui.load_image("http://202.201.225.74/video/PythonResoure/ProjectResource/images/project3/Minute.png")
second = gui.load_image("http://202.201.225.74/video/PythonResoure/ProjectResource/images/project3//Second.png")
# 加载并设置音乐资源
music_box = gui.load_sound("http://202.201.225.74/video/PythonResoure/ProjectResource/sounds/project3/music_box.ogg")
music_box.set_volume(0.5)


def get_time():
    """定义获取日期时间的辅助函数，获取日期时间"""
    global date, time, hour_rotation, minute_rotation, second_rotation, tenth_second

    dt = datetime.now()

    month_str = ''
    minute_str = ''
    day_str = ''
    hour_str = ''
    second_str = ''

    minute_rotation = 2.0 * math.pi * (dt.minute + float(dt.second) / 60.0) / 12.0
    second_rotation = 2.0 * math.pi * dt.second / 60.0
    if dt.hour >= 12:
        hour_rotation = 2.0 * math.pi * ((dt.hour - 12.0) + float(dt.minute) / 60.0) / 12.0
    else:
        hour_rotation = 2.0 * math.pi * (dt.hour + float(dt.minute) / 60.0) / 12.0

    # 将输出时间格式化
    if dt.month < 10:
        month_str = '0' + str(dt.month)
    else:
        month_str = str(dt.month)
    if dt.day < 10:
        day_str = '0' + str(dt.day)
    else:
        day_str = str(dt.day)
    if dt.hour < 10:
        hour_str = '0' + str(dt.hour)
    else:
        hour_str = str(dt.hour)
    if dt.minute < 10:
        minute_str = '0' + str(dt.minute)
    else:
        minute_str = str(dt.minute)
    if dt.second < 10:
        second_str = '0' + str(dt.second)
    else:
        second_str = str(dt.second)

    # 定义毫秒
    tenth_second = dt.microsecond // 100000

    # 定义输出时间
    date = str(dt.year) + '年' + month_str + '月' + str(dt.day) + '日'
    time = hour_str + '时' + minute_str + '分' + second_str + '秒' + str(tenth_second)


def toggle_display_digit():
    """定义按钮“开启数显”的事件处理函数，切换数显"""
    global display_digit
    if display_digit:
        button1.set_text('开启数显')
        display_digit = False

    else:
        button1.set_text('关闭数显')
        display_digit = True


def toggle_music_play():
    """定义按钮“播放音乐”的事件处理函数，切换音乐播放"""
    global play_music, success, tenth_second
    success = False
    if not play_music:

        play_music = True
        music_box.rewind()
        music_box.play()
        button2.set_text('关闭音乐')
        timer.start()
    else:
        if tenth_second == 0:
            success = True
            play_music = False
            music_box.pause()
            button2.set_text('开启音乐')


def tick():
    """定义时钟事件的处理函数（每0.1秒被系统调用1次）"""
    global success, timer
    if success:
        timer.stop()
    elif not success:
        get_time()
        timer.start()


def draw(canvas):
    """定义绘制屏幕的处理函数"""
    global display_digit
    canvas.draw_image(clock_face, [300, 300], [600, 600], [300, 300], [600, 600])
    canvas.draw_image(hour, [8, 300], [16, 600], [302, 300], [12, 600], hour_rotation)
    canvas.draw_image(minute, [6, 300], [12, 600], [302, 300], [12, 600], minute_rotation)
    canvas.draw_image(second, [15, 300], [30, 600], [302, 300], [12, 600], second_rotation)
    if display_digit:
        canvas.draw_text(date, (220, 190), 20, 'black')
        canvas.draw_text(time, (220, 440), 20, 'black')


# 创建窗口
frame = gui.create_frame('时钟', 600, 600)

button1 = frame.add_button('开启数显', toggle_display_digit, 40)
button2 = frame.add_button('播放音乐', toggle_music_play, 40)
# 注册事件处理器
frame.set_draw_handler(draw)

# 启动时钟
timer = gui.create_timer(100, tick)
timer.start()

# 调用获取日期时间函数
get_time()
# 启动窗口
frame.start()
