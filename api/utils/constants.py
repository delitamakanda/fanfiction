from datetime import datetime

SERVER_START_TIME = datetime.now()

BYTES_PER_MB = 1024 ** 2
BYTES_PER_GB = 1024 ** 3

STATUS = {
	"UP": "Server is running",
    "DOWN": "Server is down",
    "CRASHED": "Server has crashed",
    "RESTARTING": "Server is restarting",
    "MAINTENANCE": "Server is in maintenance"
}


