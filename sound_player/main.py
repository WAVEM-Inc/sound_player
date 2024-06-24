
from .service.soundService import SoundService
import rclpy


def main(args=None):
    rclpy.init(args=args)

    service = SoundService()  
    # executor = rclpy.executors.MultiThreadedExecutor(num_threads=4) 
    # executor.add_node(service)
    
    try:
        # executor.spin()  
        rclpy.spin(service)
    finally:
        # executor.shutdown()
        service.destroy_node()
        rclpy.shutdown()
   
    
if __name__ == "__main__":
    main()
