import configparser
import os
import pygame


class PlaySound:
    """
    Class that paly sound

    Attributes:
        home_path :  Your system's home directory
        config  : Object of class configparser
        file_path : sound file path
    """

    def __init__(self):
        self.home_path = os.path.expanduser("~")

        self.config = configparser.ConfigParser()
        self.config.read(self.home_path + "/RobotData/sound/config/config.ini")

        self.file_path = self.home_path + self.config["CONFIG"].get("file_path")
        self.play_priority = 100  # max priority for init value
        # Pygame 초기화
        pygame.init()
    
    def __del__(self):
        pygame.quit()
              
    def play_wav(self, code, priority):

        try:            
            if (priority >= self.play_priority and pygame.mixer.music.get_busy()):
                # print("Skipping music play because music is already playing.")
                return
            
            self.play_priority = priority
            # WAV 파일 재생
            wav_file_path = self.file_path + code + ".wav"
            pygame.mixer.music.load(wav_file_path)
            pygame.mixer.music.play()

            # 재생이 끝날 때까지 대기
            # while pygame.mixer.music.get_busy():
            #    pygame.time.Clock().tick(10)
             
        except Exception as e:
            print(str(e))
            return None        
        
        #finally:            
            #pygame.quit()