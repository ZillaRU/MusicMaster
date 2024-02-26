import pygame
import textwrap
import random
import time
import argparse
import os
import platform


# 根据操作系统选择字体
def get_font_path():
    if platform.system() == "Darwin":  # macOS
        return '/System/Library/Fonts/PingFang.ttc'
    elif platform.system() == "Windows":  # Windows
        return 'C:/Windows/Fonts/msyh.ttc'  # 假设微软雅黑字体在这个路径
    elif platform.system() == "Linux":  # Linux
        return '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # 假设DejaVu字体在这个路径
    else:
        raise NotImplementedError

# 添加命令行选项
def get_args():
    parser = argparse.ArgumentParser(description="大调音阶记忆辅助程序")
    parser.add_argument('--mode', '-m', type=int, default=3, help='0: 点击空格显示答案, 其他: 指定时间后自动显示答案')
    return parser.parse_args()

# 初始化Pygame
pygame.init()
# 设置窗口大小、标题和字体
WIDTH, HEIGHT = 250, 200  # 适当缩小窗口大小
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # 无边框窗口
pygame.display.set_caption("大调音阶记忆辅助程序")

# 获取屏幕尺寸
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# 设置窗口位置
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{screen_width - WIDTH},{screen_height - HEIGHT}"

# 设置窗口始终在最上层
os.environ['SDL_WINDOW_ALWAYS_ON_TOP'] = '1'

# 设置字体和颜色
# 获取字体路径
font_path = get_font_path()
FONT = pygame.font.Font(font_path, 16)  # 减小字体大小
QUESTION_COLOR = (50, 50, 50)  # 深灰色
ANSWER_COLOR = (0, 0, 255)  # 蓝色
# 定义大调音阶和级数-唱名
major_scales = {
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
}
solfege = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']


# 主程序
def main():
    args = get_args()
    clock = pygame.time.Clock()
    running = True

    while running:
        WINDOW.fill((255, 255, 255))  # 填充背景色为白色
        # 随机选择一个大调和起始音
        selected_tone = random.choice(list(major_scales.keys()))
        selected_scale = major_scales[selected_tone]
        # 随机选择一个音作为起始点
        start_note = random.choice(selected_scale)
        start_degree = selected_scale.index(start_note) + 1
        # 随机选择问题类型
        question_type = random.choice(['degree_to_note', 'note_to_degree', 'get_tone_mark'])
        # 生成问题
        if question_type == 'degree_to_note':
            # 给出音名，询问级数
            target_degree = start_degree
            while target_degree == start_degree:
                target_degree = random.choice(range(1, 8))
            answer_note = selected_scale[target_degree - 1]
            question_text = f"音名{start_note} (级数{start_degree},唱名{solfege[start_degree-1]})\n那级数为 {target_degree} 的音名是？"
        elif question_type == 'note_to_degree':
            # 给出级数，询问音名
            target_note = start_note
            while target_note == start_note:
                target_note = random.choice(selected_scale)
            target_degree = selected_scale.index(target_note) + 1
            question_text = f"音名{start_note} (级数{start_degree},唱名{solfege[start_degree-1]})\n那音名 {target_note} 的级数是？"
        else:
            target_note = random.choice(selected_scale)
            target_degree = selected_scale.index(target_note) + 1
            question_text = f"音名{start_note} (级数{start_degree},唱名{solfege[start_degree-1]})\n是什么调？"
        # 显示问题文本
        wrapped_text = textwrap.wrap(question_text, width=16)  # 设置每行的最大字符数
        y = 30
        for line in wrapped_text:
            text_surface = FONT.render(line, True, QUESTION_COLOR)
            WINDOW.blit(text_surface, (20, y))
            y += 30  # 每行文本之间的垂直间距
        # 更新显示
        pygame.display.update()

        # 根据模式等待用户按键或时间到
        if args.mode == 0:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN: # and event.key == pygame.K_SPACE:
                        waiting = False
        else:
            time.sleep(args.mode)

        # 显示答案
        if question_type == 'degree_to_note':
            answer_text = f"【{selected_scale[0]}大调】级数 {target_degree} 的音名是: {answer_note}"
        elif question_type == 'note_to_degree':
            answer_text = f"【{selected_scale[0]}大调】音名 {target_note} 的级数是: {target_degree}"
        else:
            answer_text = f" 这是{selected_scale[0]}大调"
        
        answer_surface = FONT.render(answer_text, True, ANSWER_COLOR)
        WINDOW.blit(answer_surface, (15, 150))

        # 更新显示
        pygame.display.update()
        # 等待用户按键后继续
        pygame.event.clear()  # 清空事件队列
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False
        # 检查是否退出
        if not running:
            break
    # 退出Pygame
    pygame.quit()


# 运行程序
if __name__ == "__main__":
    main()