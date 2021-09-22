import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

PROJECT_NAME = 'PingPongAI'
PROJECT_PATH = os.getcwd().rsplit(PROJECT_NAME)[0] + PROJECT_NAME
SAVED_MODEL_PATH = PROJECT_PATH + '/ai/agent/model/saved_model/game_model.h5'
