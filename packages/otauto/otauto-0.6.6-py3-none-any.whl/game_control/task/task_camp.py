from game_control.task_logic import TaskLogic #接入基本的任务逻辑信息
from loguru import logger #接入日志模块

class TaskCamp(TaskLogic):
    """
    任务详情:这里接入任务的具体操作内容
    def task_details(self),所有操作接入这个函数中
    vnc: vnc对象
    vnc_port: vnc端口号
    queue_handle: 队列操作对象
    task_welfare
    """
    def __init__(self,vnc,vnc_port,queue_handle):
        super().__init__(vnc,vnc_port,queue_handle)
        self.receive_num = 0 # 领取任务次数
        self.task_word_list=["敌","粮","路","魔"]
        self.task_word_key = ["敌军粮车", "梨花","点击交付"]
        self.accepted_task_list=[] #已领取任务列表
        self.res_task_list=[] #任务列表

    def task_任务领取人(self):
        self.node_current="task_任务领取人"

        if not self.role_running or not self.map_differences:

            if "阵营任务领取界面" in self.interface_info:
                self.accepted_task_list=list(set(self.accepted_task_list)) #去重
                if len(self.accepted_task_list) >= len(self.task_word_list) or self.receive_num >= len(self.task_word_list): #4个任务都领取完毕
                    self.interface_closes()
                    logger.info("阵营任务领取完毕,关闭")
                    self.receive_num= 0 # 重置领取次数
                    return True
                else:
                    self.res_task_list=self.find_word_scope(532, 277, 639, 398)
                    logger.error(f"任务信息:{self.res_task_list}")
                    if self.res_task_list:
                        self.queue_interval(5)
                        for task_word in self.task_word_list:
                            for task_name, x, y, _ in self.res_task_list :
                                if task_word in task_name and "接" in task_name:#任务已接
                                    self.accepted_task_list.append((task_word, x, y))
                                elif task_word in task_name and "接" not in task_name: #任务未接
                                    # logger.error(f"测试点{task_name,x,y}")
                                    self.mouse_left_click(x, y,delay_time=1)
                                    if self.find_data_from_keys_list_click(["领取"], self.unique_data["word"],delay_time=1):
                                        self.receive_num+=1
                    return True

            elif "地图界面" in self.interface_info:
                logger.info("地图界面.选择任务领取人")
                if self.find_data_from_keys_list(["收藏"],self.word_handle_data):
                    logger.info("收藏界面")
                    if self.find_data_from_keys_list_click([f"{self.role_factions}任务领取人"],self.word_handle_data,x3=20,y3=5,delay_time=1):
                        self.mouse_left_click(618,554,delay_time=25)
                        return True

                elif self.find_data_from_keys_list_click(["收藏"], self.word_handle_data, delay_time=1):
                    return True
                elif self.find_data_from_keys_list_click(["快捷搜索"], self.word_handle_data, delay_time=1):
                    return True
                elif self.find_data_from_keys_list_click(["resource/images_info/camp_task/地图_npc.bmp"], self.image_data,
                                                         delay_time=1):
                    return True

            elif "主界面" in self.interface_info:
                self.key_press("M",delay_time=1)

    def task_爵位领取(self):
        """
        1,移动到地方
        2,点击交付,完成退出
        :return:
        """
        self.node_current = "task_爵位领取"

        if self.find_data_from_keys_list_click(["确"], self.word_handle_data, delay_time=1):  # 界面关闭
            pass

        if self.find_data_from_all_keys_list(["爵位（完成"], self.word_acquire_data):
            self.find_data_from_keys_list_click(["提升"], self.word_handle_data, delay_time=3)
            logger.info("爵位提升完成")
            self.ls_progress = "task_finish"
            return "task_finish"

        if "爵位提升界面" in self.interface_info:
            logger.error("测试点")
            if self.find_data_from_keys_list(["一个爵位（未"],self.task_info):
                if self.find_data_from_keys_list_click(["陪"], self.word_handle_data,delay_time=1):
                    self.find_data_from_keys_list_click(["位"], self.word_handle_data,delay_time=1)
                    self.interface_closes()
                    return True
                else:
                    self.interface_closes()

        elif "主界面" in self.interface_info:
            logger.info("主界面")
            if self.find_data_from_keys_list_click(["提升"],self.word_handle_data,delay_time=3):
                logger.info("打开爵位提升界面")

            elif self.find_data_from_keys_list_click(["一个爵位（未完成）"], self.word_acquire_data,delay_time=5, x3=50,y3=8):
                logger.info("寻找爵位领取人")

    def task_任务中(self):
        self.node_current="task_任务中"

        if self.find_data_from_keys_list_click(["复活点"],self.word_handle_data,delay_time=5):
            logger.error("角色死亡")
            self.key_press("0",delay_time=3)
            return True

        if self.find_data_from_keys_list_click(["确定"], self.word_handle_data, delay_time=1):
            pass

        if not self.role_running or not self.map_differences:
            self.find_data_from_keys_list_click(self.task_word_key, self.word_acquire_data, x3=15,y3=5,delay_time=1)
            self.mouse_move_scope(926, 224, 1181, 551, delay_time=10)

        self.interface_closes()

    def handle_task(self):
        task_methods = {
            'task_任务领取人': self.task_任务领取人,
            "task_任务中" : self.task_任务中,
            "task_爵位领取": self.task_爵位领取,
        }
        if self.node_current in task_methods:
            task_methods[self.node_current]()

    def task_details(self):
        """
        self.ls_progress=None # 进度信息:task_finish,task_fail,task_error,task_wait,
        self.node_current=None #当前节点
        self.node_list= []  # 节点列表
        self.node_counter = 0 # 节点计数器
        self.queue_message({"word": {11: {"enable": False}}}) # 参数关闭
        函数写入这里
        """
        logger.success(f"任务详情:{self.__class__.__name__}")
        logger.success(f"节点信息:{self.node_current}")

        if self.find_data_from_keys_list_click(["你还可以","您已获取"],self.word_handle_data):
            pass

        if self.find_data_from_keys_list_click(["可以提升"],self.word_handle_data):
            if self.task_爵位领取()=="task_finish":
                return "task_finish"
        elif self.find_data_from_keys_list(self.task_word_key,self.task_info):
            self.task_任务中()
        else:
            if not self.node_current:#判断当前节点为空,这里写任务开始
                self.task_任务领取人()
            elif self.node_current: #继续任务节点
                self.handle_task()


camp_data={
    "word": {
        "快捷搜索": {
            "scope": (996, 559, 1080, 585),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "唐军任务领取人": {
            "scope": (581, 265, 838, 536),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "义军任务领取人": {
            "scope": (581, 265, 838, 536),
            "con": 0.8,
            "offset": (0, 0),
            "use": "系统设置",
            "unique": True,
            "enable": True,
        },
        "自动寻路": {
            "scope": (756,157,846,184),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },  # 阵营任务
        "可以提升":{
            "scope": (466,375,647,405),
            "con": 0.8,
            "offset": (232,73),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "领取": {
            "scope": (778, 700, 875, 751),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },  # 阵营任务
        "收藏":{
            "scope": (557, 207, 609, 232),
            "con": 0.8,
            "offset": (0, 0),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "寻路": {
            "scope": (570,520,670,573),
            "con": 0.8,
            "offset": (0, 0),
            "use": "悬赏任务",
            "unique": True,
            "enable": True,
        },  # 阵营任务
        "陪":{
            "scope": (406, 494, 524, 526),
            "con": 0.8,
            "offset": (0, 0),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "位":{
            "scope": ( 671, 635, 752, 664),
            "con": 0.8,
            "offset": (0, 0),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "确":{
            "scope": (688, 519, 777, 543),
            "con": 0.8,
            "offset": (0, 0),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "提升":{
            "scope": (552, 571, 705, 636),
            "con": 0.8,
            "offset": (0, 0),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "确定":{
            "scope": (629,426,779,494),
            "con": 0.8,
            "offset": (0, 0),
            "use": "阵营任务",
            "enable":True,
        },#阵营任务
        "你还可以": {
            "scope": (513, 366, 749, 416),
            "con": 0.8,
            "offset": (224,75),
            "use": "阵营任务",
            "enable": True,
        },  # 阵营任务
        "您已获取": {
            "scope": (593, 375, 882, 422),
            "con": 0.8,
            "offset": (134, 147),
            "use": "阵营任务",
            "enable": True,
        },  # 阵营任务
    },
    "image": {
        r"resource/images_info/camp_task/地图_npc.bmp":{
            "scope":(1088,563,1153,618),
            "con":0.8,
            "model":1,
            "enable":True,
            "unique": True,
        },#奖励图标
    },
}

