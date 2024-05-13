import sys
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj
from math import radians, sin, cos, sqrt, atan2, degrees

def haversine_distance(lat1, lon1, lat2, lon2):
    # 지구 반지름 (km 단위)
    R = 6371.0

    # 경위도를 라디안 단위로 변환
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine 공식
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 두 지점 사이의 거리 계산
    distance = R * c

    return distance


def convert_latlon_to_utm(latitude, longitude):
    # 경위도 좌표계를 UTM 좌표계로 변환하는 객체 생성
    utm_converter = Proj(proj="utm", zone=52, ellps="WGS84")

    # 경위도를 UTM 좌표로 변환
    utm_x, utm_y = utm_converter(longitude, latitude)

    return utm_x, utm_y


# 두 점 사이의 거리를 계산하는 함수
def distanceBetween(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# 두 좌표를 연결한 직선과 외부 점 사이의 거리를 계산하는 함수
def distance_from_line(x1, y1, x2, y2, x0, y0):

    # 직선의 방정식 이용
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    # 거리 계산
    distance = numerator / denominator

    return distance


# 두 점을 연결하는 직선에 수직이고 시작 좌표를 지나는 직선과 외부 점 사이의 거리를 계산하는 함수
def distance_from_perpendicular_line(x1, y1, x2, y2, x0, y0):
    # (y2 - y1) 또는 (x2 - x1) 가 0 인 경우는 별도 계산 해야함
    if (y2 - y1) == 0:
        distance = distanceBetween(x2, y0, x0, y0)
    elif (x2 - x1) == 0:
        distance = distanceBetween(x0, y2, x0, y0)
    else:
        # 시작 점을 지나는 직선의 기울기는
        perpendicular_m = (x2 - x1) / (y2 - y1) * -1
        # 시작 점을 지나는 직선의 방정식은 y - y1 = perpendicular_m * (x - x1)
        # 이 직선과 외부 점 사이의 거리를 계산
        distance = abs(
            (perpendicular_m * x0 - y0 + y2 - perpendicular_m * x2)
            / sqrt(1 + perpendicular_m * perpendicular_m)
        )

    return distance


# 직선 A와 직선 B가 만나는 지점의 좌표를 계산하는 함수
def calculate_intersection_point(x1, y1, x2, y2, x0, y0):
    # 두 점을 연결하는 직선의 기울기 계산
    slope_b = (y2 - y1) / (x2 - x1)

    # 직선 A의 기울기 계산
    slope_a = -1 / slope_b

    # 두 직선이 만나는 지점의 x 좌표 계산
    intersection_x = (slope_a * x2 - slope_b * x0 + y0 - y2) / (slope_a - slope_b)

    # 두 직선이 만나는 지점의 y 좌표 계산
    intersection_y = slope_a * (intersection_x - x2) + y2

    return intersection_x, intersection_y


def calculate_line_angle(x1, y1, x2, y2):
    # 두 점 사이의 x, y 변화량 계산
    delta_x = x2 - x1
    delta_y = y2 - y1

    # 직선과 x축 사이의 각도 계산 (라디안 단위)
    angle_rad = atan2(delta_y, delta_x)

    # 각도를 시계 반대 방향으로 변환하여 반환 (0도는 오른쪽 방향부터 시작)
    angle_deg = degrees(angle_rad) - 90
    angle_deg = (
        angle_deg + 360
    ) % 360  # 음수 각도를 처리하기 위해 360을 더하고 모듈로 연산을 수행

    return angle_deg


def calculate_speed_for_deceleration(distance_to_stop, current_speed, max_deceleration):
    # 현재 속도가 0이거나 감속이 불가능한 경우 현재 속도를 반환
    if current_speed == 0 or distance_to_stop == 0:
        return 0
    
    # 감속할 수 있는 최대 거리 계산
    max_distance_to_stop = current_speed**2 / (2 * max_deceleration)
    
    # 남은 거리가 최대 감속 거리보다 작거나 같으면 현재 속도를 반환
    # if distance_to_stop >= max_distance_to_stop:
    #     return current_speed
    
    print("val :" + str(2 * max_deceleration * distance_to_stop / current_speed**2))
    # 남은 거리에 따른 감속 계수 계산
    deceleration_factor = np.sqrt(2 * max_deceleration * distance_to_stop / current_speed**2)
    #deceleration_factor = np.exp(2 * max_deceleration * (distance_to_stop) / current_speed**2)
    #deceleration_factor = (2 * max_deceleration * distance_to_stop / current_speed**2)
    
    # 감속 속도 계산
    deceleration_speed = current_speed * deceleration_factor
    
    return deceleration_speed


def main():
    
    
    print(np.exp(10))
    print(np.exp(9))
    print(np.exp(8))
    # 시뮬레이션 매개 변수 설정
    current_speed = 10  # 현재 속도 (m/s)
    distance_to_stop = 50 # 멈추기까지의 거리 (m)
    max_deceleration = 4  # 최대 감속도 (m/s^2)
    deceleration_speed = current_speed 
    # 감속을 위한 속도 계산
    for i in reversed(range(distance_to_stop)):
      #deceleration_speed = calculate_speed_for_deceleration(distance_to_stop, current_speed, max_deceleration)
      deceleration_speed = calculate_speed_for_deceleration(i, deceleration_speed, max_deceleration)
      print("감속을 위한 속도:", i ,"m -> ", deceleration_speed, "m/s")
    

    # x1, y1 = 2, 2  # 시작 좌표
    # x2, y2 = 3, 1  # 종료 좌표
    # angle = calculate_line_angle(x1, y1, x2, y2)

    # print(a)
    # if ( len(sys.argv)  != 5 ):
    #     print("invalide parameter")
    #     print("st_lat st_lon ed_lat ed_lon")
    #     return
      
       
    # # print(sys.argv[1]) 
    # # print(sys.argv[2]) 
    # # print(sys.argv[3])
    # # print(sys.argv[4])
     
    # y1, x1 = convert_latlon_to_utm(float(sys.argv[1]), float(sys.argv[2]))
    # y2, x2 = convert_latlon_to_utm(float(sys.argv[3]), float(sys.argv[4]))
    
    # # y1, x1 = convert_latlon_to_utm(37.3061467, 127.2401776)
    # # y2, x2 = convert_latlon_to_utm(37.3061114, 127.2401561)
    # # y3, x3 = convert_latlon_to_utm(37.3060611, 127.2401137)
    # angle = calculate_line_angle(y1, x1, y2, x2)    
    # print("두 좌표의 각도:", angle)
    
    # dist = distanceBetween(y1, x1, y2, x2)
    # print("두 좌표의 거리:", dist)
    
    # # # 예제 입력값
    # # lat1, lon1 = 36.114598, 128.369384  # 시작 노드
    # # lat2, lon2 = 36.114591, 128.369128  # 종료 노드
    # # lat0, lon0 = 36.114611, 128.369169  # 차량 위치

    # # # lat1, lon1 = map(float, input("Enter  first point (x1 y1): ").split())
    # # # lat2, lon2 = map(float, input("Enter  second point (x2 y2): ").split())
    # # # lat0, lon0 = map(float, input("Enter external point (x0 y0): ").split())

    # # x1, y1 = convert_latlon_to_utm(lat1, lon1)
    # # x2, y2 = convert_latlon_to_utm(lat2, lon2)
    # # x0, y0 = convert_latlon_to_utm(lat0, lon0)

    # # # 1. 두 좌표(x1,y1,x2,y2)를 연결하는 직선에 수직이고 도착 좌표(x2,y2)를 지나는 직선과 외부 점(x0,y0) 사이의 거리를 계산
    # # dist = distance_from_perpendicular_line(x1, y1, x2, y2, x0, y0)
    # # print("Distance :", dist)
    # # # 2. 두 좌표(x1,y1,x2,y2)를 연결한 직선과 외부 점(x0,y0) 사이의 거리를 계산
    # # # dist = distance_from_line(x1, y1, x2, y2, x0, y0)

    # # # 3. 두 경위도 사이의 거리 계산
    # # # distance = haversine_distance(lat1, lon1, lat2, lon2)

    # # # 4. 두 경위도 사이의 각도 (정북 기준 반시계)
    # # # 직선 A와 직선 B가 만나는 지점의 좌표 계산
    # # intersection_x, intersection_y = calculate_intersection_point(
    # #     x1, y1, x2, y2, x0, y0
    # # )
    # # # print("Intersection point coordinates:", intersection_x, intersection_y)
    # # angle = calculate_line_angle(x0, y0, intersection_x, intersection_y)
    # # print("두 좌표의 각도:", angle)

    # # # # 두 지점 사이의 거리 계산
    # # # distance = haversine_distance(lat1, lon1, lat2, lon2)* 1000
    # # # distance = distanceBetween(utm_x1, utm_y1, utm_x2, utm_y2)
    # # # print("Distance  :", distance, "m")


if __name__ == "__main__":
    main()