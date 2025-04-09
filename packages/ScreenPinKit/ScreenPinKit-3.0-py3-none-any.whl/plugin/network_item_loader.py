import sys, requests
from requests import Session
from .plugin_inst_config import PluginInstConfig
from .plugin_config import *
from common import *

networkImageCache = {}

class WorkerSignals(QObject):
    loadFinishedSignal = pyqtSignal(PluginInstConfig, int)

class NetworkItemLoader(QRunnable):
    '''支持异步的插件加载器'''
    def __init__(self, configItem, index):
        super(NetworkItemLoader, self).__init__()
        self.configItem = configItem
        self.index = index
        self.signals = WorkerSignals()

    def run(self):
        try:
            temp = PluginInstConfig()
            temp.name = self.configItem["name"]
            temp.displayName = self.configItem["displayName"]
            temp.version = self.configItem["version"]
            temp.desc = self.configItem["desc"]
            temp.author = self.configItem["author"]
            temp.url = self.configItem["url"]
            temp.tags = self.configItem["tags"]
            temp.supportSystems = self.configItem["supportSystems"]
            temp.enable = False

            server = Session()

            # 加载网络Icon
            url = self.configItem["icon"]
            imageData = server.get(url).content
            iconPixmap = QPixmap()
            iconPixmap.loadFromData(imageData)
            temp.icon = QIcon(iconPixmap)

            global networkImageCache
            # 加载网络预览图片
            for imageUrl in self.configItem["previewImages"]:
                if imageUrl in networkImageCache:
                    imageData = networkImageCache[imageUrl]
                else:
                    imageData = server.get(imageUrl).content
                    networkImageCache[imageUrl] = imageData
                previewPixmap = QPixmap()
                previewPixmap.loadFromData(imageData)
                if not previewPixmap.isNull():
                    temp.previewImages.append(previewPixmap)

            self.signals.loadFinishedSignal.emit(temp, self.index)
        except Exception as e:
            logger.error(f"Error loading image: {e}")

class MarketWorker(QThread):
    loadFinishedSignal = pyqtSignal(object)

    def __init__(self, url:str) -> None:
        super().__init__()
        self.url = url

    def run(self):
        try:
            jsonData = requests.get(self.url).text
            if jsonData:
                jsonObj = json.loads(jsonData)
                self.loadFinishedSignal.emit(jsonObj)
        except Exception as e:
            if hasattr(e, "stderr"):
                _importErrorMsg = e.stderr
            else:
                _importErrorMsg = "\n".join([str(arg) for arg in e.args])
            logger.error(f"MarketWorker: load failed {_importErrorMsg}")

class NetworkLoaderManager(QObject):
    loadItemFinishedSignal = pyqtSignal(PluginInstConfig)
    loadAllFinishedSignal = pyqtSignal()

    def __init__(self, marketUrl:str, parent=None):
        super().__init__(parent)
        self.marketUrl = marketUrl
        self.taskDict = {}
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(5)

    def __getTestObj(self):
        with open("xxx/plugin_market/extensions.json", 'r', encoding='utf-8') as f:
            jsonData = f.read()

        if jsonData:
            jsonObj = json.loads(jsonData)
            return jsonObj

    def start(self):
        self.marketThread = MarketWorker(self.marketUrl)
        self.marketThread.loadFinishedSignal.connect(self.__executeThreadPool)
        self.marketThread.start()

    def startDebug(self):
        '''仅用于测试'''
        jsonObj = self.__getTestObj()
        self.__executeThreadPool(jsonObj)

    def __executeThreadPool(self, jsonObj:dict):
        for index, item in enumerate(jsonObj):

            # 跳过不支持当前系统的插件
            isSkip = True
            for system in item["supportSystems"]:
                if sys.platform.startswith(system):
                    isSkip = False

            if isSkip:
                continue

            self.taskDict[index] = 1
            loader = NetworkItemLoader(item, index)
            loader.signals.loadFinishedSignal.connect(self.__addNetworkItem)
            self.threadpool.start(loader)

    def __addNetworkItem(self, plugin: PluginInstConfig, index: int):
        self.taskDict[index] = 1
        self.taskDict.pop(index)
        self.loadItemFinishedSignal.emit(plugin)

        if (len(self.taskDict) == 0):
            self.loadAllFinishedSignal.emit()