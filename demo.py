from sensor.logger import logging
from sensor.Exception import apsException
import sys
from sensor.pipeline.training_pipeline import TrainPipeline


pipline  = TrainPipeline()
pipline.run_pipeline()



