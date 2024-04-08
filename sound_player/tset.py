import pygame
import time

# Pygame 초기화
pygame.init()

def play_music(music_file):
    # 현재 재생 중인 음악이 있는지 확인
    if pygame.mixer.music.get_busy():
        print("Skipping music play because music is already playing.")
        return

    # 음악 로드 및 재생
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

# 음악 파일 경로
music_file = "/home/wavem/RobotData/sound/files/3001.wav"

for i in range(1, 11):
    # 음악 재생
    play_music(music_file)
    time.sleep(1)

count = 0
# 재생이 끝날 때까지 대기
while pygame.mixer.music.get_busy():
    time.sleep(1)
    
print("Music play finished.")