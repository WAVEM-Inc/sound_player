from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.logging import get_logger

from route_msgs.msg import DriveState
from ktp_data_msgs.msg import ServiceStatus
from ktp_data_msgs.msg import Status as RbtStatus
from obstacle_msgs.msg import Status as ObstacleStatus
from sensor_msgs.msg import BatteryState

from ..config.config import Config
from .play_sound import PlaySound
from .define import define as DEFINE


class SoundService(Node):
    """
    ROS node class for sound play

    Attributes:
       sndPlayer : sound play object
       play_state : play flag for state changing
    """
   
    def __init__(self):
        super().__init__("SoundService")

        self.get_logger().info("Start sound play service")
       
        self.sndPlayer = PlaySound()

        conf = Config()
        self.sound_list = conf.get_sound_list()   

        self.play_state = {}  # 상태 변경시 한번만 실행하기 위한 플래그
        self.subscription_map = {}
        
        self._register_subscribe(self.sound_list)
          
    def _listener_service_status(self, status: ServiceStatus) -> None:
        """
        callback function for ServiceStatus

        Args:
            status : topic message

        Returns:
           
        Raises:

        """
        
        get_logger(self.get_name()).debug("_listener_service_status : " + str(status))
        
        try:
            sound_list = list(filter(lambda sl: sl.code in {DEFINE.sound_code_1001,
                                                            DEFINE.sound_code_1002,
                                                            DEFINE.sound_code_1003,
                                                            DEFINE.sound_code_1004,
                                                            DEFINE.sound_code_1006},
                                     self.sound_list))
            get_logger(self.get_name()).debug("_listener_service_status  sound_list: " + str(sound_list))
            self._play_sound(status.task[0].status if status.task else None, sound_list)
            # self._play_sound(status.reserve, sound_list)

        except Exception as e:
            get_logger(self.get_name()).error("_listener_service_status : " + str(e))
            
    def _listener_drive_info(self, status: DriveState) -> None:
        """
        callback function for DriveState

        Args:
            mstatus : topic message

        Returns:
           
        Raises:

        """   
        get_logger(self.get_name()).debug("_listener_drive_info : " + str(status))
        
        try:
            # if (status.code not in {DEFINE.DRV_CROSS, DEFINE.DRV_PARKING}):
            #     status.code = DEFINE.SIREN
            
            sound_list = list(filter(lambda sl: sl.code in {DEFINE.sound_code_1005,
                                                            DEFINE.sound_code_2003},
                                     self.sound_list))
            self._play_sound(status.code, sound_list)
                
        except Exception as e:
            get_logger(self.get_name()).error("_listener_drive_info : " + str(e))

    def _listener_rtb_status(self, status: RbtStatus) -> None:
        """
        callback function for RbtStatus

        Args:
            mstatus : topic message

        Returns:
           
        Raises:

        """           
        get_logger(self.get_name()).debug("_listener_rtb_status : " + str(status))

        try:            
            sound_list = list(filter(lambda sl: sl.code in {DEFINE.sound_code_1007}, 
                                     self.sound_list))
            self._play_sound(str(status.drive_status), sound_list)
                            
        except Exception as e:
            get_logger(self.get_name()).error("_listener_rtb_status : " + str(e))  
    
    def _listener_obstacle_status(self, status: ObstacleStatus) -> None:
        """        
        callback function for ObstacleStatus

        Args:
            mstatus : topic message

        Returns:
           
        Raises:

        """    
        get_logger(self.get_name()).debug("_listener_obstacle_status : " + str(status))
       
        try:            
            if(status.obstacle_value is False):
                return
             
            sound_list = list(filter(lambda sl: sl.code in {DEFINE.sound_code_2001,
                                                            DEFINE.sound_code_2002},
                                     self.sound_list))
            self._play_sound(status.obstacle_status, sound_list) 
                
        except Exception as e:
            get_logger(self.get_name()).error("_listener_obstacle_status : " + str(e))      
    
    def _listener_battery_status(self, status: BatteryState) -> None:
        """        
        callback function for BatteryState

        Args:
            mstatus : topic message

        Returns:
           
        Raises:

        """    
        get_logger(self.get_name()).debug("_listener_battery_status : " + str(status))
       
        try:
            sound_list = list(filter(lambda sl: sl.code in {DEFINE.sound_code_3001},
                                     self.sound_list))

            if not sound_list:
                get_logger(self.get_name()).error("not found battery code in sound option list : ")
                return
            
            warning_level = float(sound_list[0].status[0])   # 배터리 한계 기준 값
            percentage = status.percentage
            
            if (percentage > warning_level):
                self.sndPlayer.play_wav(sound_list[0].code, sound_list[0].priority)
        
        except Exception as e:
            get_logger(self.get_name()).error("_listener_battery_status : " + str(e))

    def _play_sound(self, msg_status, sound_list):
        """        
        play sound 

        Args:
            msg_status : Output conditions for each information message
            sound_list : List of sound output environments and conditions

        Returns:
           
        Raises:

        """         
        try:    
            get_logger(self.get_name()).debug("_play_sound msg_status : " + str(msg_status) + " / " + str(sound_list))
            if (msg_status is None):
                return
           
            for snd in sound_list:
                if (str(msg_status) in snd.status):                       
                    if (snd.count == "state" and self.play_state[snd.code] is False):  # 상태 변경 시 에만 출력 된다.
                       #get_logger(self.get_name()).info("_play_sound : " + str(snd.count) + str(self.play_state[snd.code]))
                       break
                       
                    self.play_state[snd.code] = False
                    get_logger(self.get_name()).info("_play_sound : " + str(snd.code) +
                                                     ",  priority : " + str(snd.priority))
                    self.sndPlayer.play_wav(snd.code, snd.priority)
                    break
                elif (snd.count == "state"):  # 플레이 조건은 아닌데 count 가 "state" 이면 다음 조건에 도달시 플레이 되도록 True로 변경
                    self.play_state[snd.code] = True
                
        except Exception as e:
            get_logger(self.get_name()).error("_play_sound : " + str(e))

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
                        
        qos_profile = QoSProfile(depth=10)
       
        for sound in sound_list:
            topic = sound.topic
            self.play_state[sound.code] = True
            
            get_logger(self.get_name()).info("code : " + sound.code + " - topic :" + topic + "   => " +str(sound))
            
            if (self._check_topic_existence(topic) is True):
                continue
                             
            self.subscription_map[topic] = True
            
            if (sound.code == DEFINE.sound_code_1001
                or sound.code == DEFINE.sound_code_1002
                or sound.code == DEFINE.sound_code_1003
                or sound.code == DEFINE.sound_code_1004
                or sound.code == DEFINE.sound_code_1006):
                self.service_subscriber = self.create_subscription(
                    ServiceStatus, 
                    topic,  
                    self._listener_service_status, 
                    qos_profile                     
                )                  
                          
            elif (sound.code == DEFINE.sound_code_1007):
                self.rtbstatus_subscriber = self.create_subscription(
                    RbtStatus, 
                    topic, 
                    self._listener_rtb_status, 
                    qos_profile                   
                    )
    
            elif (sound.code == DEFINE.sound_code_1005
                    or sound.code == DEFINE.sound_code_2003):
                self.drive_subscriber = self.create_subscription(
                        DriveState, 
                        topic, 
                        self._listener_drive_info, 
                        qos_profile 
                    )
          
            elif (sound.code == DEFINE.sound_code_2001
                  or sound.code == DEFINE.sound_code_2001):
                self.opstacle_subscriber = self.create_subscription(
                    ObstacleStatus, 
                    topic, 
                    self._listener_obstacle_status,
                    qos_profile
                    )    

            elif (sound.code == DEFINE.sound_code_3001):
                self.battery_subscriber = self.create_subscription(
                    BatteryState, 
                    topic, 
                    self._listener_battery_status, 
                    qos_profile
                    )
            else:
                get_logger(self.get_name()).error("topic : " + topic + " is an undefined topic.")
            
            if ( self._check_topic_existence(topic) is True):
                get_logger(self.get_name()).info("topic : " + topic + "   (subscribe)")

        get_logger(self.get_name()).info("end subscribe") 
        
# def main(args=None):
#     rclpy.init(args=args)

#     service = SoundService()

#     rclpy.spin(service)

#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()