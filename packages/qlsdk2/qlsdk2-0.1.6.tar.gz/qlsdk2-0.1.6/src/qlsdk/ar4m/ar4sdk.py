import ctypes
from multiprocessing import Queue
import platform
from ctypes import (
    c_int, c_int32, c_int64, c_uint32, c_uint64, 
    c_char, c_char_p, c_void_p, 
    Structure, POINTER, CFUNCTYPE
)
from loguru import logger
from time import sleep, time
import os 

real_path = os.path.realpath(__file__)
dll_path = f'{os.path.dirname(real_path)}/libs/libAr4SDK.dll'

# 加载 DLL
if platform.system() == 'Windows':
    _dll = ctypes.CDLL(dll_path)
else:
    raise NotImplementedError(f"不支持非Windows平台：{platform.system()}")

#------------------------------------------------------------------
# 基础类型定义
#------------------------------------------------------------------
class Ar4MacStr(Structure):
    _fields_ = [("str", c_char * 17)]

class Ar4Name(Structure):
    _fields_ = [("str", c_char * 21)]

class Ar4Device(Structure):
    _fields_ = [
        ("slot", c_int32),
        ("mac", c_uint64),
        ("hub_name", Ar4Name)
    ]

class Ar4NotifyData(Structure):
    _fields_ = [
        ("time_stamp", c_int64),
        ("pkg_id", c_int64),
        ("notify_id", c_int64),
        ("eeg", POINTER(c_int32)),
        ("eeg_ch_count", c_int32),
        ("eeg_count", c_int32),
        ("acc", POINTER(c_int32)),
        ("acc_ch_count", c_int32),
        ("acc_count", c_int32)
    ]

#------------------------------------------------------------------
# 回调函数类型
#------------------------------------------------------------------
FuncAr4DataNotify = CFUNCTYPE(None, c_void_p, POINTER(Ar4NotifyData))
FuncAr4TriggerNotify = CFUNCTYPE(None, c_void_p, c_int64, c_int32, c_uint32)
FuncAr4RecorderDisconnected = CFUNCTYPE(None, c_void_p)
FuncAr4RecorderConnected = CFUNCTYPE(None, c_void_p)
FuncAr4RecorderTimeout = CFUNCTYPE(None, c_void_p, c_int64)
FuncAr4RecorderPkgLost = CFUNCTYPE(c_int, c_void_p, c_int64, c_int64, c_int64)
FuncAr4GetTime = CFUNCTYPE(c_int64)
FuncAr4SDKPrint = CFUNCTYPE(None, c_char_p, ctypes.c_size_t)

#------------------------------------------------------------------
# SDK 函数定义
#------------------------------------------------------------------
# 设备枚举
_dll.ar4_sdk_enum_device.restype = POINTER(Ar4Device)
_dll.ar4_sdk_enum_hub.restype = POINTER(Ar4Name)
_dll.ar4_sdk_enum_in_hub.argtypes = [Ar4Name]

# MAC地址转换
_dll.ar4_mac_to_str.argtypes = [c_uint64]
_dll.ar4_mac_to_str.restype = Ar4MacStr
_dll.ar4_str_to_mac.argtypes = [Ar4MacStr]
_dll.ar4_str_to_mac.restype = c_uint64

# 连接管理
_dll.ar4_sdk_connect.argtypes = [c_uint64, c_void_p]
_dll.ar4_sdk_connect.restype = c_void_p
_dll.ar4_sdk_disconnect.argtypes = [c_void_p]

# AR4信息查询
_dll.ar4_sdk_get_box_name.argtypes = [c_void_p]
_dll.ar4_sdk_get_box_name.restype = c_uint64

# 数据采集控制
_dll.ar4_sdk_start_acq.argtypes = [c_void_p]
_dll.ar4_sdk_start_acq.restype = c_int
_dll.ar4_sdk_stop_acq.argtypes = [c_void_p]
_dll.ar4_sdk_stop_acq.restype = c_int
_dll.ar4_sdk_get_record_sample_rate.argtypes = [c_void_p]
_dll.ar4_sdk_get_record_sample_rate.restype = c_char_p
_dll.ar4_sdk_get_acq_start_time.argtypes = [c_void_p]
_dll.ar4_sdk_get_acq_start_time.restype = c_int64

# 回调注册
_dll.ar4_sdk_register_data_notify.argtypes = [c_void_p, FuncAr4DataNotify]
_dll.ar4_sdk_register_data_notify.restype = None
_dll.ar4_sdk_register_trigger_notify.argtypes = [c_void_p, c_void_p]
_dll.ar4_sdk_register_conn_notify.argtypes = [c_void_p, FuncAr4RecorderConnected, FuncAr4RecorderDisconnected]
_dll.ar4_sdk_register_record_state_notify.argtypes = [c_void_p, FuncAr4RecorderConnected, FuncAr4RecorderDisconnected]
_dll.ar4_sdk_register_box_conn_notify.argtypes = [c_void_p, FuncAr4RecorderConnected, FuncAr4RecorderDisconnected]

# _dll对外封装类
class AR4SDK:
    @classmethod
    def enum_devices(cls):
        """枚举可用设备"""
        devices = []
        ptr = _dll.ar4_sdk_enum_device()
        if not ptr:
            logger.info("没有找到ar4设备")
            return devices
        
        index = 0
        while True:
            device = ptr[index]
            if not device or device.mac == 0:
                break
            # logger.debug(f"get device: {device.slot}, mac: {hex(device.mac)}, hub_name: {device.hub_name.str}")
            devices.append(device)
            index += 1
            
        return devices
    
    @classmethod
    def enum_hubs(cls):
        """枚举可用设备"""
        devices = []
        ptr = _dll.ar4_sdk_enum_hub()
        sleep(5)
        logger.debug(f"enum_hubs: {ptr}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
  

# 读取系统当前时间(ms)
def _get_time():
    cur_time = int(round(time()) * 1000)
    logger.debug(f"_get_time is {cur_time}")
    return cur_time  
    
# ar4设备对象
class AR4(object):
    def __init__(self, box_mac, slot, hub_name):
        self._handle = None
        self._box_type = None
        self._box_mac = box_mac
        self._box_id = None
        self._box_soc = None
        self._box_name = None
        self._box_version = None
        self._head_type = None
        self._head_mac = None
        self._head_version = None
        self._head_conn_state = None
        self._head_soc = None
        self._net_state = None
        self._hub_name = hub_name
        self._slot = slot
        self._connected = False
        self._conn_time = None
        self._last_time = None
        
        self._acq_info = {}
        # 回调函数
        self._data_callback = FuncAr4DataNotify(self._wrap_data_accept())        
        self._trigger_callback = FuncAr4TriggerNotify(self._trigger_accept)
        
        # 消息订阅
        self._consumers: dict[str, Queue] = {}
        
    @property
    def box_mac(self):
        return self._box_mac
    @property
    def slot(self):
        return self._slot
    @property
    def hub_name(self):
        return self._hub_name
    def init(self):
        # logger.info(f"init ar4 {self.box_mac}")
        if not self._handle:
            self._connected = self.connect()
            if self._connected:
                self._conn_time = _get_time()
                self.get_box_name()
                self.get_head_mac()
                self.get_record_conn_state()
                self._last_time = _get_time()
            logger.debug(self)
        return True

    def update_info(self):
        self._last_time = _get_time()
        
    # 设备连接
    def connect(self)-> bool:
        
            if self._box_mac:
                """连接设备"""
                # callback = FuncAr4GetTime(self._get_time)
                try:
                    self._handle = _dll.ar4_sdk_connect(int(self._box_mac, 16), c_void_p(0))
                    # logger.info(f"conn handle is {self._handle}")
                    self._handle = c_void_p(self._handle)     
                    logger.debug(f"ar4 {self._box_mac} 连接: {self._handle}")                   
                except Exception as e:
                    logger.error(f"ar4 {self._box_mac} 连接异常: {str(e)}")
            return self._handle is not None
    
    # 读取盒子名称
    def get_box_name(self):
        if self._handle:    
            try:        
                self._head_mac = _dll.ar4_sdk_get_recoder_mac(self._handle)
            except Exception as e:
                    logger.error(f"ar4 {self._box_mac} 获取盒子记录子mac异常: {str(e)}")
    # 读取记录子mac
    def get_head_mac(self):
        if self._handle:    
            try:        
                self._box_name = _dll.ar4_sdk_get_record_conn_state(self._handle)
            except Exception as e:
                    logger.error(f"ar4 {self._box_mac} 获取盒子名称异常: {str(e)}")
    # 读取记录子连接状态
    def get_record_conn_state(self):
        if self._handle:    
            try:        
                self._head_conn_state = _dll.ar4_sdk_get_record_conn_state(self._handle)
            except Exception as e:
                    logger.error(f"ar4 {self._box_mac} 获取盒子记录子连接状态异常: {str(e)}")

    # 数据采集启动
    def start_acquisition(self):
        logger.info(f"ar4 {self._box_mac} 启动数据采集...")
        """启动数据采集"""
        
        self._acq_info["start_time"] = _get_time()
        
        if self._handle:
            # 设置信号数据回调
            try:
                _dll.ar4_sdk_register_data_notify(self._handle, self._data_callback)
            except Exception as e:
                logger.error(f"ar4 {self._box_mac} 停止采集异常: {str(e)}")
                
            # 设置trigger数据回调
            # try:
            #     _dll.ar4_sdk_register_trigger_notify(self._handle, self._trigger_callback)
            # except Exception as e:
            #     logger.error(f"ar4 {self._box_mac} 停止采集异常: {str(e)}")
            # 启动采集
            try:
                logger.debug(f"ar4 {self._box_mac} 启动采集: {self._handle}")
                ret = _dll.ar4_sdk_start_acq(self._handle)
                logger.debug(f"ar4 {self._box_mac} 启动采集结果: {ret}")
                    
                return ret == 0
            except Exception as e:
                logger.error(f"ar4 {self._box_mac} 停止采集异常: {str(e)}")
        else:
            logger.info(f"ar4 {self._box_mac} 启动数据采集失败， 设备未连接")
            return False

    def stop_acquisition(self):
        """停止采集"""
        if self._handle:
            try:                
                self.get_acq_start_time() 
            except Exception as e:
                logger.error(f"ar4 {self._box_mac} 获取开始采集时间异常: {str(e)}")
            try:
                return _dll.ar4_sdk_stop_acq(self._handle) == 0
            except Exception as e:
                logger.error(f"ar4 {self._box_mac} 停止采集异常: {str(e)}")
        else:
            return False

    def disconnect(self):
        """断开连接"""
        if self._handle:
            _dll.ar4_sdk_disconnect(self._handle)

    def get_sample_rate(self):
        try:
            ret = _dll.ar4_sdk_get_record_sample_rate(self._handle)
            logger.debug(f"ar4 {self._box_mac} 获取采样率: {ret.contents.decode('utf-8')}")
        except Exception as e:
            logger.error(f"ar4 {self._box_mac} 获取采样率异常: {str(e)}")
            
    def get_acq_start_time(self):
        try:
            ret = _dll.ar4_sdk_get_acq_start_time(self._handle)
            # 更新采样开始时间
            if ret:
                self._acq_info["start_time"] = ret
            logger.debug(f"ar4 {self._box_mac} 获取采样开始时间: {ret}")
        except Exception as e:
            logger.error(f"ar4 {self._box_mac} 获取采样开始时间异常: {str(e)}")
       
    # 订阅推送消息 
    def subscribe(self, topic: str = None, q: Queue = Queue()):
        if topic is None:
            topic = f"msg_{_get_time()}"
        if topic in list(self._consumers.keys()):  
            logger.warning(f"ar4 {self._box_mac} 订阅主题已存在: {topic}")
            return topic, self._consumers[topic]
        self._consumers[topic] = q
        
        return topic, self._consumers[topic]
    
    def _wrap_data_accept(self):
        
        @FuncAr4DataNotify
        def data_accept(handle, data_ptr):
            self._data_accept(data_ptr)
            
        return data_accept
            
    def _data_accept(self, data_ptr):
        # logger.info(f"_eeg_accept 被调用")
        # logger.debug(f'handle:{self}, data_ptr:{data_ptr}')
        # data = cast(data_ptr, POINTER(Ar4NotifyData)).contents
        if len(self._consumers) > 0:
            packet = AR4Packet().transfer(data_ptr.contents)
            for consumer in self._consumers.values():
                consumer.put(packet)
            # logger.debug(f"EEG数据: {packet}")
        
    def _trigger_accept(self, time_ms, trigger_type, trigger_value):
        logger.info(f"_trigger_accept 被调用")
        logger.info(f"触发时间: {time_ms}, 触发类型: {trigger_type}, 触发值: {trigger_value}")
                
    def __str__(self):
        return f"""
                box mac: {self._box_mac}, 
                box name: {self._box_name}, 
                box soc: {self._box_soc}
                head conn state: {self._head_conn_state}
                head mac: {self._head_mac},
                head soc: {self._head_soc} 
                connected: {self._connected}
                connect time: {self._conn_time}
                last time: {self._last_time}
            """
            
class Packet(object):
    pass
            
class AR4Packet(Packet):
    def __init__(self):
        self.time_stamp = None
        self.pkg_id = None
        self.notify_id = None
        self.eeg_ch_count = None
        self.eeg_count = None
        self.eeg = None
        self.acc_ch_count = None
        self.acc_count = None
        self.acc = None
    
    def transfer(self, data: Ar4NotifyData):
        self.time_stamp = data.time_stamp
        self.pkg_id = data.pkg_id
        self.notify_id = data.notify_id
        self.eeg_ch_count = data.eeg_ch_count
        self.eeg_count = data.eeg_count
        self.acc_ch_count = data.acc_ch_count
        self.acc_count = data.acc_count
        # 读eeg数据
        if self.eeg_ch_count and self.eeg_count:
            self.eeg = [[] for _ in range(self.eeg_ch_count)]
            for i in range(self.eeg_ch_count):
                self.eeg[i] = [data.eeg[j + (i * self.eeg_count)] for j in range(self.eeg_count)]
        # 读acc数据
        if self.acc_ch_count and self.acc_count:
            self.acc = [[] for _ in range(self.acc_ch_count)]
            for i in range(self.acc_ch_count):
                self.acc[i] = [data.acc[j + (i * self.acc_count)] for j in range(self.acc_count)]
        
        return self
        
    def __str__(self):
        return f"""
            time_stamp: {self.time_stamp}
            pkg_id: {self.pkg_id}
            notify_id: {self.notify_id}
            eeg_ch_count: {self.eeg_ch_count}
            eeg_count: {self.eeg_count}
            acc_ch_count: {self.acc_ch_count}
            acc_count: {self.acc_count}
            eeg: {self.eeg}
            acc: {self.acc}
        """
