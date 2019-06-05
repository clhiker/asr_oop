import logging

class Log(object):
    _inst = None

    def __new__(cls, *args, **kwargs):
        # 如果单例没有被创建就创建一个
        if not cls._inst:
            cls._inst = super(Log, cls).__new__(cls)
        # 如果已经创建就返回该类
        return cls._inst

    def initLogging(self, logFilename):
      """Init for logging
      """
      logging.basicConfig(
                        level    = logging.DEBUG,
                        format='%(asctime)s-%(levelname)s-%(message)s',
                        datefmt  = '%y-%m-%d %H:%M',
                        filename = logFilename,
                        filemode = 'w')
      console = logging.StreamHandler()
      console.setLevel(logging.INFO)
      formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
      console.setFormatter(formatter)
      logging.getLogger('').addHandler(console)

    def info(self, message):
        logging.info(message)
