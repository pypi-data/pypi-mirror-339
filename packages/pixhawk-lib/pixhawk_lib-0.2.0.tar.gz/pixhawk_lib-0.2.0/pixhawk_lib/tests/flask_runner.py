#server side
from pixhawk_lib.pixhawk import PixHawk

if __name__ == "__main__":
    PixHawk.run_flask(connection_string='/dev/ttyACM0', host='0.0.0.0', port=5000)

# client side
from pixhawk_lib.pixhawk import PixHawk
from time import sleep

if __name__ == "__main__":
    pixhawk = PixHawk(host='raspberrypi.local', port=5000)
    
    # Example commands
    pixhawk.takeoff(10)
    pixhawk.get_state()  
    pixhawk.forward(2)
    sleep(5)        
    pixhawk.stop()       
    pixhawk.land()

