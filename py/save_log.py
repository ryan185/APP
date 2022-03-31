import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

class get_log(object):
	def setup_logger(logger_name, log_file, level=logging.DEBUG):
		logger = logging.getLogger(logger_name)
		logger.setLevel(level)
		formatter = logging.Formatter('%(asctime)s - %(message)s')
		fileHandler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=1, encoding='utf-8', delay=True)
		# fileHandler = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=1, encoding='utf-8', delay=True)
		fileHandler.setFormatter(formatter)
		logger.addHandler(fileHandler)
		
		#ログをコンソール出力するための設定
		sh = logging.StreamHandler()
		logger.addHandler(sh)
		return logger

	# def setup_logger(logger_name, log_file, level=logging.DEBUG):
	# 	l = logging.getLogger(logger_name)
	# 	l.setLevel(level)
	# 	formatter = logging.Formatter('%(asctime)s - %(message)s')
	# 	fileHandler = RotatingFileHandler(log_file, mode='a', maxBytes=20, backupCount=1, encoding='utf-8')
	# 	fileHandler.setFormatter(formatter)
	# 	l.addHandler(fileHandler)

	# 	return l


# get_log.setup_logger('log1', 'C:\\Users\\FaceRecogniton\\Desktop\\key\\new style(Chiba - version 1.1)\\Log Folder\\MainPage.log')
# get_log.setup_logger('log2', 'C:\\Users\\FaceRecogniton\\Desktop\\key\\new style(Chiba - version 1.1)\\Log Folder\\Rpilog.log')

# logger_1 = logging.getLogger('log1')
# logger_2 = logging.getLogger('log2')

# logger_1.info('111messasage 1')
# logger_2.info('222ersaror foo')