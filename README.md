
# sound player manager


**`Documentation`** |
------------------- |


[ubuntu](https://ubuntu.com/) 및 [ROS2](https://docs.ros.org) 환경에서 [Python](https://www.python.org/)으로 개발하였다.

KEC 자율주행 차량에서 사용되는 안내 메시지를 출력 한다.


## Config
환경 파일(config.ini)은 다음 경로에 있어야 한다.
~/RobotData/sound/config

사운드 파일의 위치 및 파일명은 config.ini에 설정하여 사용한다.
정의된 사운드 파일들은 설정한 위치에 위치 하여야 한다.

## Build

소스를 빌드 하기 위해서는 먼저 ROS2 설치 및 워크스페이스가 구성되어 있어야 하고 의존 관계 msg 패키지들이 구성되어 있어야 한다.

```shell
$ pip install -r requirements.txt
$ colcon build --packages-select sound_player
```

## Run

```shell
$ source install/setup.bash
$ ros2 launch sound_player sound_player.launch.py
```

## Custom Service 


## Service guidelines
KEC-D-002-코드정의서를 참고한다.
사운드 파일 및 환경 파일은 resource/sound 디렉토리를 참고 한다.

## License


