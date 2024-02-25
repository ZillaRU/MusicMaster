import pygame
import textwrap
import random
import time
import argparse
import os
# 初始化Pygame
pygame.init()
# 设置窗口大小、标题和字体
WIDTH, HEIGHT = 400, 300  # 适当缩小窗口大小
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # 无边框窗口
pygame.display.set_caption("大调音阶记忆辅助程序")
# 设置字体和颜色
font_path = '/System/Library/Fonts/PingFang.ttc'  # 使用PingFang字体
FONT = pygame.font.Font(font_path, 20)  # 减小字体大小
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
# 添加命令行选项
def get_args():
    parser = argparse.ArgumentParser(description="大调音阶记忆辅助程序")
    parser.add_argument('--mode', '-m', type=int, default=1, help='0: 点击空格显示答案, 其他: 指定时间后自动显示答案')
    return parser.parse_args()
# 主程序
def main():
    args = get_args()
    clock = pygame.time.Clock()
    running = True
    # 将窗口移动到屏幕右下角
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pygame.display.Info().current_w - WIDTH, pygame.display.Info().current_h - HEIGHT)
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
        y = 50
        for line in wrapped_text:
            text_surface = FONT.render(line, True, QUESTION_COLOR)
            WINDOW.blit(text_surface, (50, y))
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
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        waiting = False
        else:
            time.sleep(args.mode)

        # 显示答案
        if question_type == 'degree_to_note':
            answer_text = f"级数 {target_degree} 的音名是: {answer_note}"
        elif question_type == 'note_to_degree':
            answer_text = f"音名 {target_note} 的级数是: {target_degree}"
        else:
            answer_text = f"这是{selected_scale[0]}大调"
        
        answer_surface = FONT.render(answer_text, True, ANSWER_COLOR)
        WINDOW.blit(answer_surface, (50, 200))

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