import configparser
import os
import pygame
from ..config.define import define as DEFINE
from rclpy.logging import get_logger

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
        
        try:
          
            if self.config["CONFIG"].get("SDL_AUDIODRIVER") is not None and self.config["CONFIG"].get("AUDIODEV") is not None:
                os.environ['SDL_AUDIODRIVER'] = self.config["CONFIG"].get("SDL_AUDIODRIVER")  #'alsa'
                os.environ['AUDIODEV'] = self.config["CONFIG"].get("AUDIODEV")  #'plughw:0,3'
                print(str("SDL_AUDIODRIVER : " + str(self.config["CONFIG"].get("SDL_AUDIODRIVER")) + 
                          " / AUDIODEV : " + str(self.config["CONFIG"].get("AUDIODEV"))))

            self.play_priority = 100  # max priority for init value

            if (self.config["CONFIG"].get("sound_volume") is not None and self.config["CONFIG"].get("sound_volume").isdecimal()):
                self.volume = int(self.config["CONFIG"].get("sound_volume"))
                
                if (self.volume > DEFINE.sound_vloume_max):    
                    self.volume = DEFINE.sound_vloume_max
                elif (self.volume < 0):
                    self.volume = 0            
            else:
                self.volume = DEFINE.sound_vloume_max
               
            # Pygame 초기화
            pygame.init()
            pygame.mixer.init()
            
            #pygame.mixer.music.set_volume(float(self.volume)/10.0)

        except Exception as e:
            print(str(e))
            return None   
        # self.volume = DEFINE.sound_vloume_max   # default value - max volume
       
    def getVolume(self):
        return self.volume
     
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
            pygame.mixer.music.set_volume(float(self.volume)/10.0)
            pygame.mixer.music.play()
         
            # 재생이 끝날 때까지 대기
            # while pygame.mixer.music.get_busy():
            #    pygame.time.Clock().tick(10)
             
        except Exception as e:
            print(str(e))
            return None        
        
        # finally:            
            # pygame.quit()