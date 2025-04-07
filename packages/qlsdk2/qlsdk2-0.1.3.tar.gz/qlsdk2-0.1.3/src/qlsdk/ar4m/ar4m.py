from ar4sdk import AR4SDK, AR4
from time import sleep, time
from threading import Lock, Timer
from loguru import logger

class AR4M(object):
    def __init__(self):
        self._lock = Lock()
        self._search_timer = None 
        self._search_running = False
        self._devices: dict[str, AR4] = {}
    
    @property
    def devices(self):
        return self._devices
    def search(self):
        if not self._search_running:
            self._search_running = True
            self._search()
        
    def _search(self):
        if self._search_running:

            self._search_timer = Timer(2, self._search_ar4)
            self._search_timer.daemon = True
            self._search_timer.start()
        
        
    def _search_ar4(self):
        try:                        
            devices = AR4SDK.enum_devices()
            logger.debug(f"_search_ar4 devices size: {len(devices)}")
            for dev in devices:
                logger.debug(f"slot: {dev.slot}, mac: {dev.mac}-{hex(dev.mac)}, hub_name: {dev.hub_name.str}")
                if dev.mac in list(self._devices.keys()):
                    ar4 = self._devices[dev.mac]
                    ar4.update_info()
                ar4 = AR4(hex(dev.mac), dev.slot, dev.hub_name.str)
                if ar4.init():
                    self._devices[dev.mac] = ar4
        except Exception as e:
            logger.error(f"_search_ar4 异常: {str(e)}")
        finally:
            self._search()
