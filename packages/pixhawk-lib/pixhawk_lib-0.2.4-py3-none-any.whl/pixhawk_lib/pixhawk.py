# pixhawk_lib/pixhawk.py
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative
import time
import logging
from .tunes import HAPPY_BIRTHDAY, DANGER, ALL_SAFE, EXPLODE
from pymavlink import mavutil
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PixHawk:
    MAX_SPEED = 5  # Maximum speed in m/s
    PWM_DEVIATION = 100  # PWM units for movement deviation (adjust based on testing)

    def __init__(self, connection_string=None, host=None, port=None, baud=115200, wait_until_done=False):
        """Initialize PixHawk with a connection string for direct control or host/port for remote control.

        Args:
            connection_string (str, optional): The connection string (e.g., '/dev/ttyACM0').
            host (str, optional): Hostname or IP of the Flask server.
            port (int, optional): Port number of the Flask server.
            baud (int): Baud rate for direct connection (default: 115200).
            wait_until_done (bool): If True, methods wait for actions to complete (default: False).

        Raises:
            ValueError: If both connection_string and host/port are provided, or neither is provided.
        """
        if connection_string and (host or port):
            raise ValueError("Cannot specify both connection_string and host/port")
        if not connection_string and not (host and port):
            raise ValueError("Must specify either connection_string or host and port")

        self.wait_until_done = wait_until_done
        self.current_speed = 0
        self.tunes = {
            'HAPPY_BIRTHDAY': HAPPY_BIRTHDAY,
            'DANGER': DANGER,
            'ALL_SAFE': ALL_SAFE,
            'EXPLODE': EXPLODE
        }

        if connection_string:
            self.is_remote = False
            self.connection_string = connection_string
            self.baud = baud
            self.vehicle = None
            self.connect()
            self.get_state_data = self._get_state_from_vehicle
        else:
            self.is_remote = True
            self.host = host
            self.port = port
            self.vehicle = None
            self.get_state_data = self._get_state_from_server

    ### Connection Method ###
    def connect(self):
        """Connect to the Pixhawk directly."""
        try:
            self.vehicle = connect(self.connection_string, baud=self.baud, wait_ready=True)
            logger.info(f"Connected to Pixhawk on {self.connection_string}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise ConnectionError(f"Failed to connect: {e}")

    ### State Fetching Methods ###
    def _get_state_from_vehicle(self):
        """Get state directly from the vehicle."""
        return {
            'battery': self.vehicle.battery.level,
            'gps': self.vehicle.gps_0.fix_type,
            'mode': self.vehicle.mode.name,
            'altitude': self.vehicle.location.global_relative_frame.alt,
            'heading': self.vehicle.heading
        }

    def _get_state_from_server(self):
        """Get state from the Flask server."""
        try:
            url = f"http://{self.host}:{self.port}/state"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                raise RuntimeError(f"Failed to fetch state: {response.text}")
        except Exception as e:
            logger.error(f"Server state fetch failed: {e}")
            raise

    def get_state(self):
        """Print the current state of the Pixhawk."""
        try:
            state_data = self.get_state_data()
            print(f"Battery: {state_data['battery']}%\n"
                  f"GPS Fix Type: {state_data['gps']} (3+ is 3D lock)\n"
                  f"Mode: {state_data['mode']}\n"
                  f"Altitude: {state_data['altitude']} meters\n"
                  f"Heading: {state_data['heading']} degrees")
        except Exception as e:
            logger.error(f"Error getting state: {e}")
            raise

    ### Command Methods ###
    def takeoff(self, altitude, mode="ALT_HOLD", climb_throttle=1600):
        """Take off to the specified altitude (in meters).

        Args:
            altitude (float): Target altitude in meters.
            mode (str): Mode for takeoff ("ALT_HOLD" or "GUIDED", default: "ALT_HOLD").
            climb_throttle (int): PWM value for throttle during climb (default: 1600).

        Raises:
            RuntimeError: If mode setting, arming, or takeoff fails.
        """
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/takeoff"
                response = requests.post(url, json={'altitude': altitude, 'mode': mode, 'climb_throttle': climb_throttle}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to execute takeoff: {response.text}")
            except Exception as e:
                logger.error(f"Remote takeoff failed: {e}")
                raise RuntimeError(f"Remote takeoff failed: {e}")
        else:
            logger.info(f"Taking off to {altitude} meters in {mode} mode")
            try:
                self.vehicle.mode = VehicleMode(mode)
                timeout = time.time() + 10  # 10-second timeout
                while self.vehicle.mode.name != mode:
                    if time.time() > timeout:
                        raise RuntimeError(f"Failed to set mode to {mode}")
                    time.sleep(1)
                logger.info(f"Mode set to {mode}")

                self.vehicle.armed = True
                timeout = time.time() + 10
                while not self.vehicle.armed:
                    if time.time() > timeout:
                        raise RuntimeError("Failed to arm vehicle")
                    time.sleep(1)
                logger.info("Vehicle armed")

                if mode == "GUIDED":
                    self.vehicle.simple_takeoff(altitude)
                elif mode == "ALT_HOLD":
                    self.vehicle.channels.overrides = {'3': climb_throttle}
                    logger.info(f"Throttle set to {climb_throttle} PWM for climb")
                    timeout = time.time() + 30  # 30-second timeout
                    while self.vehicle.location.global_relative_frame.alt < altitude * 0.95:
                        if time.time() > timeout:
                            self.vehicle.channels.overrides = {'3': 1500}
                            raise RuntimeError(f"Failed to reach altitude {altitude} meters")
                        time.sleep(0.5)
                    self.vehicle.channels.overrides = {'3': 1500}
                    logger.info("Altitude reached, throttle set to neutral")

                if self.wait_until_done:
                    while self.vehicle.location.global_relative_frame.alt < altitude * 0.95:
                        time.sleep(0.5)
                    logger.info("Reached target altitude")
            except Exception as e:
                logger.error(f"Takeoff failed: {e}")
                self.vehicle.channels.overrides = {}
                self.vehicle.armed = False
                raise RuntimeError(f"Takeoff failed: {e}")

    def land(self):
        """Land the drone."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/land"
                response = requests.post(url, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to execute land: {response.text}")
            except Exception as e:
                logger.error(f"Remote land failed: {e}")
                raise RuntimeError(f"Remote land failed: {e}")
        else:
            logger.info("Landing...")
            try:
                self.vehicle.mode = VehicleMode("LAND")
                if self.wait_until_done:
                    while self.vehicle.armed:
                        time.sleep(0.5)
                    logger.info("Landed")
            except Exception as e:
                logger.error(f"Land failed: {e}")
                raise RuntimeError(f"Land failed: {e}")

    def clockwise(self, degrees):
        """Rotate clockwise by the specified degrees."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/rotate"
                response = requests.post(url, json={'direction': 'clockwise', 'degrees': degrees}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to execute clockwise: {response.text}")
            except Exception as e:
                logger.error(f"Remote clockwise failed: {e}")
                raise RuntimeError(f"Remote clockwise failed: {e}")
        else:
            logger.info(f"Rotating clockwise by {degrees} degrees")
            try:
                current_heading = self.vehicle.heading
                target_heading = (current_heading + degrees) % 360
                self.vehicle.condition_yaw(target_heading, relative=False)
                if self.wait_until_done:
                    while abs(self.vehicle.heading - target_heading) > 5:
                        time.sleep(0.5)
                    logger.info("Rotation completed")
            except Exception as e:
                logger.error(f"Clockwise rotation failed: {e}")
                raise RuntimeError(f"Clockwise rotation failed: {e}")

    def counterclockwise(self, degrees):
        """Rotate counterclockwise by the specified degrees."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/rotate"
                response = requests.post(url, json={'direction': 'counterclockwise', 'degrees': degrees}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to execute counterclockwise: {response.text}")
            except Exception as e:
                logger.error(f"Remote counterclockwise failed: {e}")
                raise RuntimeError(f"Remote counterclockwise failed: {e}")
        else:
            logger.info(f"Rotating counterclockwise by {degrees} degrees")
            try:
                current_heading = self.vehicle.heading
                target_heading = (current_heading - degrees) % 360
                self.vehicle.condition_yaw(target_heading, relative=False)
                if self.wait_until_done:
                    while abs(self.vehicle.heading - target_heading) > 5:
                        time.sleep(0.5)
                    logger.info("Rotation completed")
            except Exception as e:
                logger.error(f"Counterclockwise rotation failed: {e}")
                raise RuntimeError(f"Counterclockwise rotation failed: {e}")

    def play_tune(self, tune_name):
        """Play a predefined tune by name."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/play_tune"
                response = requests.post(url, json={'tune_name': tune_name}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to play tune: {response.text}")
            except Exception as e:
                logger.error(f"Remote play tune failed: {e}")
                raise RuntimeError(f"Remote play tune failed: {e}")
        else:
            try:
                if tune_name in self.tunes:
                    tune_string = self.tunes[tune_name]
                    for i in range(0, len(tune_string), 30):
                        segment = tune_string[i:i+30]
                        self.vehicle.play_tune(segment.encode('utf-8'))
                    logger.info(f"Played tune: {tune_name}")
                else:
                    logger.warning(f"Tune '{tune_name}' not found")
            except Exception as e:
                logger.error(f"Play tune failed: {e}")
                raise RuntimeError(f"Play tune failed: {e}")

    def disconnect(self):
        """Disconnect from the Pixhawk."""
        if not self.is_remote and self.vehicle:
            try:
                self.vehicle.close()
                logger.info("Disconnected")
            except Exception as e:
                logger.error(f"Disconnect failed: {e}")
                raise RuntimeError(f"Disconnect failed: {e}")

    ### Manual Motor Control ###
    def set_channel_overrides(self, overrides):
        """Set channel overrides for manual motor control.

        Args:
            overrides (dict): Dictionary of channel numbers to PWM values (e.g., {'3': 1600}).
        """
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_channel_overrides"
                response = requests.post(url, json={'overrides': overrides}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to set channel overrides: {response.text}")
            except Exception as e:
                logger.error(f"Remote set channel overrides failed: {e}")
                raise RuntimeError(f"Remote set channel overrides failed: {e}")
        else:
            try:
                self.vehicle.channels.overrides = overrides
                logger.info(f"Set channel overrides: {overrides}")
            except Exception as e:
                logger.error(f"Set channel overrides failed: {e}")
                raise RuntimeError(f"Set channel overrides failed: {e}")

    def clear_channel_overrides(self):
        """Clear all channel overrides."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/clear_channel_overrides"
                response = requests.post(url, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to clear channel overrides: {response.text}")
            except Exception as e:
                logger.error(f"Remote clear channel overrides failed: {e}")
                raise RuntimeError(f"Remote clear channel overrides failed: {e}")
        else:
            try:
                self.vehicle.channels.overrides = {}
                logger.info("Cleared all channel overrides")
            except Exception as e:
                logger.error(f"Clear channel overrides failed: {e}")
                raise RuntimeError(f"Clear channel overrides failed: {e}")

    ### Movement Commands ###
    def _move(self, direction, distance_cm):
        """Helper method to move in a specific direction by distance in cm."""
        distance_m = distance_cm / 100.0
        current_location = self.vehicle.location.global_relative_frame

        if direction == 'forward':
            target_location = LocationGlobalRelative(
                current_location.lat + (distance_m / 111111.0),
                current_location.lon,
                current_location.alt
            )
        elif direction == 'backward':
            target_location = LocationGlobalRelative(
                current_location.lat - (distance_m / 111111.0),
                current_location.lon,
                current_location.alt
            )
        elif direction == 'left':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon - (distance_m / (111111.0 * 0.7071)),
                current_location.alt
            )
        elif direction == 'right':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon + (distance_m / (111111.0 * 0.7071)),
                current_location.alt
            )
        elif direction == 'up':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon,
                current_location.alt + distance_m
            )
        elif direction == 'down':
            target_location = LocationGlobalRelative(
                current_location.lat,
                current_location.lon,
                current_location.alt - distance_m
            )
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.vehicle.simple_goto(target_location)
        if self.wait_until_done:
            while True:
                current_location = self.vehicle.location.global_relative_frame
                remaining_distance = self._get_distance(current_location, target_location)
                if remaining_distance < 0.1:
                    break
                time.sleep(0.5)
            logger.info(f"Moved {direction} by {distance_cm} cm")

    def _get_distance(self, loc1, loc2):
        """Calculate distance between two locations in meters."""
        dlat = loc2.lat - loc1.lat
        dlon = loc2.lon - loc1.lon
        return ((dlat * 111111.0)**2 + (dlon * 111111.0 * 0.7071)**2)**0.5

    def move_forward(self, distance_cm):
        """Move forward by the specified distance in cm."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/move"
                response = requests.post(url, json={'direction': 'forward', 'distance_cm': distance_cm}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move forward: {response.text}")
            except Exception as e:
                logger.error(f"Remote move forward failed: {e}")
                raise RuntimeError(f"Remote move forward failed: {e}")
        else:
            if self.vehicle.mode.name != "GUIDED":
                raise RuntimeError("Distance-based movement requires GUIDED mode")
            self._move('forward', distance_cm)

    def move_backward(self, distance_cm):
        """Move backward by the specified distance in cm."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/move"
                response = requests.post(url, json={'direction': 'backward', 'distance_cm': distance_cm}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move backward: {response.text}")
            except Exception as e:
                logger.error(f"Remote move backward failed: {e}")
                raise RuntimeError(f"Remote move backward failed: {e}")
        else:
            if self.vehicle.mode.name != "GUIDED":
                raise RuntimeError("Distance-based movement requires GUIDED mode")
            self._move('backward', distance_cm)

    def move_left(self, distance_cm):
        """Move left by the specified distance in cm."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/move"
                response = requests.post(url, json={'direction': 'left', 'distance_cm': distance_cm}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move left: {response.text}")
            except Exception as e:
                logger.error(f"Remote move left failed: {e}")
                raise RuntimeError(f"Remote move left failed: {e}")
        else:
            if self.vehicle.mode.name != "GUIDED":
                raise RuntimeError("Distance-based movement requires GUIDED mode")
            self._move('left', distance_cm)

    def move_right(self, distance_cm):
        """Move right by the specified distance in cm."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/move"
                response = requests.post(url, json={'direction': 'right', 'distance_cm': distance_cm}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move right: {response.text}")
            except Exception as e:
                logger.error(f"Remote move right failed: {e}")
                raise RuntimeError(f"Remote move right failed: {e}")
        else:
            if self.vehicle.mode.name != "GUIDED":
                raise RuntimeError("Distance-based movement requires GUIDED mode")
            self._move('right', distance_cm)

    def move_up(self, distance_cm):
        """Move up by the specified distance in cm."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/move"
                response = requests.post(url, json={'direction': 'up', 'distance_cm': distance_cm}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move up: {response.text}")
            except Exception as e:
                logger.error(f"Remote move up failed: {e}")
                raise RuntimeError(f"Remote move up failed: {e}")
        else:
            if self.vehicle.mode.name != "GUIDED":
                raise RuntimeError("Distance-based movement requires GUIDED mode")
            self._move('up', distance_cm)

    def move_down(self, distance_cm):
        """Move down by the specified distance in cm."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/move"
                response = requests.post(url, json={'direction': 'down', 'distance_cm': distance_cm}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move down: {response.text}")
            except Exception as e:
                logger.error(f"Remote move down failed: {e}")
                raise RuntimeError(f"Remote move down failed: {e}")
        else:
            if self.vehicle.mode.name != "GUIDED":
                raise RuntimeError("Distance-based movement requires GUIDED mode")
            self._move('down', distance_cm)

    ### Continuous Movement ###
    def _set_movement_overrides(self, roll=1500, pitch=1500, throttle=1500, yaw=1500):
        """Set channel overrides for continuous movement."""
        overrides = {
            '1': roll,
            '2': pitch,
            '3': throttle,
            '4': yaw
        }
        self.set_channel_overrides(overrides)

    def forward(self, speed=None):
        """Move forward at the specified or current speed (m/s)."""
        speed = self.current_speed if speed is None else speed
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_velocity"
                response = requests.post(url, json={'vx': speed, 'vy': 0, 'vz': 0}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move forward: {response.text}")
            except Exception as e:
                logger.error(f"Remote forward failed: {e}")
                raise RuntimeError(f"Remote forward failed: {e}")
        else:
            deviation = int(self.PWM_DEVIATION * (speed / self.MAX_SPEED))
            pitch_pwm = 1500 - deviation
            self._set_movement_overrides(pitch=pitch_pwm)
            logger.info("Moving forward")

    def backward(self, speed=None):
        """Move backward at the specified or current speed (m/s)."""
        speed = self.current_speed if speed is None else speed
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_velocity"
                response = requests.post(url, json={'vx': -speed, 'vy': 0, 'vz': 0}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move backward: {response.text}")
            except Exception as e:
                logger.error(f"Remote backward failed: {e}")
                raise RuntimeError(f"Remote backward failed: {e}")
        else:
            deviation = int(self.PWM_DEVIATION * (speed / self.MAX_SPEED))
            pitch_pwm = 1500 + deviation
            self._set_movement_overrides(pitch=pitch_pwm)
            logger.info("Moving backward")

    def left(self, speed=None):
        """Move left at the specified or current speed (m/s)."""
        speed = self.current_speed if speed is None else speed
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_velocity"
                response = requests.post(url, json={'vx': 0, 'vy': -speed, 'vz': 0}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move left: {response.text}")
            except Exception as e:
                logger.error(f"Remote left failed: {e}")
                raise RuntimeError(f"Remote left failed: {e}")
        else:
            deviation = int(self.PWM_DEVIATION * (speed / self.MAX_SPEED))
            roll_pwm = 1500 - deviation
            self._set_movement_overrides(roll=roll_pwm)
            logger.info("Moving left")

    def right(self, speed=None):
        """Move right at the specified or current speed (m/s)."""
        speed = self.current_speed if speed is None else speed
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_velocity"
                response = requests.post(url, json={'vx': 0, 'vy': speed, 'vz': 0}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move right: {response.text}")
            except Exception as e:
                logger.error(f"Remote right failed: {e}")
                raise RuntimeError(f"Remote right failed: {e}")
        else:
            deviation = int(self.PWM_DEVIATION * (speed / self.MAX_SPEED))
            roll_pwm = 1500 + deviation
            self._set_movement_overrides(roll=roll_pwm)
            logger.info("Moving right")

    def up(self, speed=None):
        """Move up at the specified or current speed (m/s)."""
        speed = self.current_speed if speed is None else speed
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_velocity"
                response = requests.post(url, json={'vx': 0, 'vy': 0, 'vz': -speed}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move up: {response.text}")
            except Exception as e:
                logger.error(f"Remote up failed: {e}")
                raise RuntimeError(f"Remote up failed: {e}")
        else:
            deviation = int(self.PWM_DEVIATION * (speed / self.MAX_SPEED))
            throttle_pwm = 1500 + deviation
            self._set_movement_overrides(throttle=throttle_pwm)
            logger.info("Moving up")

    def down(self, speed=None):
        """Move down at the specified or current speed (m/s)."""
        speed = self.current_speed if speed is None else speed
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/set_velocity"
                response = requests.post(url, json={'vx': 0, 'vy': 0, 'vz': speed}, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to move down: {response.text}")
            except Exception as e:
                logger.error(f"Remote down failed: {e}")
                raise RuntimeError(f"Remote down failed: {e}")
        else:
            deviation = int(self.PWM_DEVIATION * (speed / self.MAX_SPEED))
            throttle_pwm = 1500 - deviation
            self._set_movement_overrides(throttle=throttle_pwm)
            logger.info("Moving down")

    def stop(self):
        """Stop the drone by setting channels to neutral."""
        if self.is_remote:
            try:
                url = f"http://{self.host}:{self.port}/stop"
                response = requests.post(url, timeout=5)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to stop: {response.text}")
            except Exception as e:
                logger.error(f"Remote stop failed: {e}")
                raise RuntimeError(f"Remote stop failed: {e}")
        else:
            try:
                self._set_movement_overrides()
                logger.info("Stopped")
            except Exception as e:
                logger.error(f"Stop failed: {e}")
                raise RuntimeError(f"Stop failed: {e}")

    ### Speed Control ###
    def speed(self, value=None):
        """Get or set the speed (0 to 1)."""
        if value is None:
            return self.current_speed
        elif 0 <= value <= 1:
            self.current_speed = value * self.MAX_SPEED
            logger.info(f"Speed set to {self.current_speed} m/s")
        else:
            raise ValueError("Speed must be between 0 and 1")

    ### Flask Server ###
    @classmethod
    def run_flask(cls, connection_string, host='0.0.0.0', port=5000):
        """Run a Flask server to expose PixHawk commands as API endpoints."""
        from flask import Flask, request, jsonify
        app = Flask(__name__)
        pixhawk = cls(connection_string=connection_string, wait_until_done=False)

        @app.route('/takeoff', methods=['POST'])
        def takeoff():
            data = request.json
            altitude = data.get('altitude')
            mode = data.get('mode', "ALT_HOLD")
            climb_throttle = data.get('climb_throttle', 1600)
            if altitude is None:
                return "Missing altitude", 400
            pixhawk.takeoff(altitude, mode, climb_throttle)
            return "Takeoff command sent", 200

        @app.route('/land', methods=['POST'])
        def land():
            pixhawk.land()
            return "Land command sent", 200

        @app.route('/rotate', methods=['POST'])
        def rotate():
            data = request.json
            direction = data.get('direction')
            degrees = data.get('degrees')
            if direction == 'clockwise':
                pixhawk.clockwise(degrees)
            elif direction == 'counterclockwise':
                pixhawk.counterclockwise(degrees)
            else:
                return "Invalid direction", 400
            return "Rotation command sent", 200

        @app.route('/move', methods=['POST'])
        def move():
            data = request.json
            direction = data.get('direction')
            distance_cm = data.get('distance_cm')
            if direction == 'forward':
                pixhawk.move_forward(distance_cm)
            elif direction == 'backward':
                pixhawk.move_backward(distance_cm)
            elif direction == 'left':
                pixhawk.move_left(distance_cm)
            elif direction == 'right':
                pixhawk.move_right(distance_cm)
            elif direction == 'up':
                pixhawk.move_up(distance_cm)
            elif direction == 'down':
                pixhawk.move_down(distance_cm)
            else:
                return "Invalid direction", 400
            return "Move command sent", 200

        @app.route('/set_velocity', methods=['POST'])
        def set_velocity():
            data = request.json
            vx = data.get('vx', 0)
            vy = data.get('vy', 0)
            vz = data.get('vz', 0)
            if vx > 0:
                pixhawk.forward(vx)
            elif vx < 0:
                pixhawk.backward(-vx)
            if vy > 0:
                pixhawk.right(vy)
            elif vy < 0:
                pixhawk.left(-vy)
            if vz > 0:
                pixhawk.down(vz)
            elif vz < 0:
                pixhawk.up(-vz)
            return "Velocity set command received", 200

        @app.route('/stop', methods=['POST'])
        def stop():
            pixhawk.stop()
            return "Stop command sent", 200

        @app.route('/set_channel_overrides', methods=['POST'])
        def set_channel_overrides():
            data = request.json
            overrides = data.get('overrides', {})
            pixhawk.set_channel_overrides(overrides)
            return "Channel overrides set", 200

        @app.route('/clear_channel_overrides', methods=['POST'])
        def clear_channel_overrides():
            pixhawk.clear_channel_overrides()
            return "Channel overrides cleared", 200

        @app.route('/play_tune', methods=['POST'])
        def play_tune():
            data = request.json
            tune_name = data.get('tune_name')
            if tune_name is None:
                return "Missing tune_name", 400
            pixhawk.play_tune(tune_name)
            return "Tune play command sent", 200

        @app.route('/state', methods=['GET'])
        def get_state():
            state = pixhawk._get_state_from_vehicle()
            return jsonify(state)

        app.run(host=host, port=port)