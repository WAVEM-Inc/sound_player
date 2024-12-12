class define:
    
    sound_vloume_max = 10
        
    SIREN = "siren"
    STRAIGHT = "straight"
    RECOVERY = "recovery"
    GEOFENCE = "2"  # detet_status # detet_user
    USER_END = "1"  # detet_status 사용자 정지
    FAIL_END = "0"  # detet_status 인식 실패
    FOLLOW = "3"    # detet_user 
    CLOSE = "0"     # detet_user
         
    detect_user_standby = 2  # 사용자 인식 대기
    detect_user_start = 1    # 인식 상태
    
    # group_service_status = "service_status"
    # group_rbt_status = "rbt_status"
    # group_obstacle_status = "obstacle_status"
    group_follow_cmd = "follow_cmd"
    group_follow_info = "follow_info"
    group_mission_result = "mission_result"
    group_battery_status = "battery_status"
    group_error_status = "error_status"
    

