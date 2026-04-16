from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from pathlib import Path
from datetime import datetime, date
import instruction

@register("astrbot_plugin_instruction", "指令之意", "获取每日的指令", "1.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.command("instruction")
    async def get_instruction(self, event: AstrMessageEvent):
        """获取指令图片并发送"""
        user_name = event.get_sender_name()
        user_id = event.get_sender_id()
        user_image_path = f"data/plugin_data/astrbot_plugin_instruction/image/{user_id}.png"
        if is_created_today(user_image_path):
            yield event.image_result(user_image_path)
        else:
            instruction.create_instruction(username=user_name,output=user_image_path)
            yield event.image_result(user_image_path)

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

def is_created_today(path: str) -> bool:
    """判断文件是否是今天创建的"""
    file_path = Path(path)
    if not file_path.exists():
        return False
    
    ctime_timestamp = file_path.stat().st_birthtime 
    created_date = datetime.fromtimestamp(ctime_timestamp).date()
    return created_date == date.today()
