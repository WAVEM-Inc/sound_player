from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.logging import get_logger

# from cmd_msgs.msg import MissionResult
from follow_msgs.msg import Detect
from follow_msgs.msg import UiClient
#from sensor_msgs.msg import BatteryState
from std_msgs.msg import String

from ..config.config import Config
from .play_sound import PlaySound
from ..config.define import define as DEFINE
import time


class SoundService(Node):
    """
    ROS node class for sound play

    Attributes:
       sndPlayer : sound play object
       play_state : play flag for state changing
    """
    
    def __init__(self):
        super().__init__("SoundService")

        self.get_logger().info("Start sound play service - " + str(self.get_name()))
       
        self.sndPlayer = PlaySound()

        conf = Config()
        self.sound_list = conf.get_sound_list()   
        self.state_period = conf.get_state_period()
        self.detect_sleep = conf.get_detect_sleep()
               
        self.play_state = {}  # 상태 변경시 한번만 실행하기 위한 플래그
        self.subscription_map = {}
        
        self.follow_running = False
         
        self._register_subscribe(self.sound_list)
                    
    def _listener_flollow_cmd(self, status: UiClient) -> None:
        """
        callback function for ServiceStatus

        Args:
            status : topic message

        Returns:
           
        Raises:

        """
        
        get_logger(self.get_name()).debug("_listener_flollow_cmd : " + str(status))
        
        try:
            sound_list = list(filter(lambda sl: sl.group == DEFINE.group_follow_cmd, self.sound_list))
            get_logger(self.get_name()).debug("_listener_flollow_cmd  sound_list: " + str(sound_list))
            
            if status.cmd == 1: 
                self.follow_standby = True
                self.follow_running = True
    
            if self.follow_standby is False:
                return

            self._play_sound(None, status.cmd, sound_list)  
            
            time.sleep(int(self.detect_sleep))
            
            if self.follow_standby is False:
                return
                
            status.cmd = 2   #'{"cmd":2}'
            self.sound_publisher.publish(status)                

        except Exception as e:
            get_logger(self.get_name()).error("_listener_flollow_cmd : " + str(e))
        
    def _listener_flollow_info(self, status: Detect) -> None:
        """
        callback function for ServiceStatus

        Args:
            status : topic message

        Returns:
           
        Raises:

        """
        
        get_logger(self.get_name()).debug("_listener_flollow_info : " + str(status) + 
                                          " / follow runnung : "+str(self.follow_running))
        
        if (self.follow_running is False):
            return

        try:
            sound_list = list(filter(lambda sl: sl.group == DEFINE.group_follow_info, self.sound_list))           
            
            if (status.detect_user not in (DEFINE.detect_user_standby, DEFINE.detect_user_start)):
                self.follow_standby = False   #다른 추종 상태 진입시 감지 중 비프음 사운드 중지 - _listener_flollow_cmd 가 호출되지 않도록함
                get_logger(self.get_name()).debug("다른 추종 상태 진입시 감지 중 비프음 사운드 중지")
                                
            #get_logger(self.get_name()).debug(str(status.detect_status) + ":" + DEFINE.GEOFENCE)
            if (int(status.detect_user) != int(DEFINE.FOLLOW) and int(status.detect_status) != int(DEFINE.GEOFENCE)):
                self._reset_status(DEFINE.group_follow_info, sound_list)
            
            if ((int(status.detect_user) == int(DEFINE.CLOSE) and int(status.detect_status) == int(DEFINE.USER_END))
                or (int(status.detect_user) == int(DEFINE.CLOSE) and int(status.detect_status) == int(DEFINE.FAIL_END))) : #정지 이면
                   self.follow_running = False
                     
            get_logger(self.get_name()).debug("_listener_flollow_info  sound_list: " + str(sound_list))
            #self._play_sound(status.task_code if status.task_code else None, status.status if status.status else None, sound_list)
            self._play_sound(status.detect_user, status.detect_status, sound_list)  
            
        except Exception as e:
            get_logger(self.get_name()).error("_listener_flollow_info : " + str(e))      
                                   
    def _listener_error_status(self, msg: String) -> None:
        """        
        callback function for ErrorStatus

        Args:
            status : topic message

        Returns:
           
        Raises:

        """    
        get_logger(self.get_name()).debug("_listener_error_status : " + str(msg))
       
        try:
            sound_list = list(filter(lambda sl: sl.group == DEFINE.group_error_status, self.sound_list))
            self._play_sound(None, msg.data, sound_list)  
                    
        except Exception as e:
            get_logger(self.get_name()).error("_listener_error_status : " + str(e))   
            
    def _play_sound(self, task_code, msg_status, sound_list):
        """        
        play sound 

        Args:
            msg_status : Output conditions for each information message
            sound_list : List of sound output environments and conditions

        Returns:
           
        Raises:

        """         
        try:    
            get_logger(self.get_name()).debug("_play_sound msg_status : " 
                                              + str(msg_status) + " / " + str(task_code) + " / " + str(sound_list))            
            for snd in sound_list:
                if (str(msg_status) in snd.status and (snd.task_code is None or str(task_code) == snd.task_code)):
                    if (snd.count == "state" and self.play_state[snd.code] is False):  # 상태 변경 시 에만 출력 된다.
                        get_logger(self.get_name()).debug("_play_sound reject: " + str(snd.count)+" / " + str(self.play_state[snd.code]))
                        return
                    
                    get_logger(self.get_name()).debug(" play_sound : " + str(snd.code) + " / " + str(task_code) +
                                                     ",  priority : " + str(snd.priority) + "/"+str(self.play_state[snd.code]))  
                    
                    get_logger(self.get_name()).info("play_wav: " + str(msg_status) + " / " + str(task_code) + " / " + str(snd))      
                    self.play_state[snd.code] = False
                    self.sndPlayer.play_wav(snd.code, snd.priority)
                    break
                
        except Exception as e:
            get_logger(self.get_name()).error("_play_sound : " + str(e))
    
    def _reset_status(self, group_code, sound_list):
        for snd in sound_list:
            if (snd.count == "state" 
                and snd.group == group_code):     
                self.play_state[snd.code] = True                    
                get_logger(self.get_name()).debug(" reset : " + str(snd.code) + " / " + str(group_code) +
                                                  ",  priority : " + str(snd.priority) + "/"+str(self.play_state[snd.code]))
                               
    def _check_topic_existence(self, desired_topic):
        """        
        Check whether topic is registered or not

        Args:
            desired_topic : Topic name to check registration status

        Returns:
           
        Raises:

        """    
        if desired_topic in self.subscription_map:
            return True
        else:
            return False
               
        # topic_names_and_types = self.get_topic_names_and_types()
        # topics = [topic[0] for topic in topic_names_and_types]

        # if desired_topic in topics:
        #     print(f"Desired topic '{desired_topic}' is registered.")
        #     return True
        # else:
        #     print(f"Desired topic '{desired_topic}' is NOT registered.")
        #     return False

    def _register_subscribe(self, sound_list) -> None:
        """        
        Register a callback function.

        Args:
            sound_list : List of sound output environments and conditions

        Returns:
           
        Raises:

        """
        self.play_state["val"] = True
                        
        qos_profile = QoSProfile(depth=1)
       
        for sound in sound_list:
            topic = sound.topic
            self.play_state[sound.code] = True
            
            get_logger(self.get_name()).info("code : " + sound.code + " - topic :" + topic + "   => " + str(sound))
            
            if (self._check_topic_existence(topic) is True):
                continue
                             
            self.subscription_map[topic] = True
            
            if (sound.group == DEFINE.group_follow_cmd):
                self.service_subscriber = self.create_subscription(
                    UiClient, 
                    topic,  
                    self._listener_flollow_cmd, 
                    qos_profile              
                )                  
                self.sound_publisher = self.create_publisher(UiClient, topic, 10)
                
            elif (sound.group == DEFINE.group_follow_info):
                self.service_subscriber = self.create_subscription(
                    Detect, 
                    topic,  
                    self._listener_flollow_info, 
                    qos_profile                  
                )      
            # elif (sound.group == DEFINE.group_mission_result):
            #     self.drive_subscriber = self.create_subscription(
            #             MissionResult, 
            #             topic, 
            #             self._listener_mission_result, 
            #             qos_profile 
            #         )
            elif (sound.group == DEFINE.group_error_status):    
                self.opstacle_subscriber = self.create_subscription(
                    String, 
                    topic, 
                    self._listener_error_status,
                    qos_profile
                    )    
            # elif (sound.group == DEFINE.group_battery_status):  
            #     self.battery_subscriber = self.create_subscription(
            #         BatteryState, 
            #         topic, 
            #         self._listener_battery_status, 
            #         qos_profile
            #         )
            else:
                get_logger(self.get_name()).error("topic : " + topic + " is an undefined topic.")
            
  
      
            
            if (self._check_topic_existence(topic) is True):
                get_logger(self.get_name()).info("topic : " + topic + "   (subscribe)")

        get_logger(self.get_name()).info("end subscribe") 
        
# def main(args=None):
#     rclpy.init(args=args)

#     service = SoundService()

#     rclpy.spin(service)

#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()