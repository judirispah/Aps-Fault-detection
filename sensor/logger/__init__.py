import logging
import os
from datetime import datetime

dir_name="log"


log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

filepath=os.path.join(os.getcwd(),dir_name,log_file)

os.makedirs(dir_name, exist_ok=True)



logging.basicConfig(filename=filepath,
                    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG,)