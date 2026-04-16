from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from pathlib import Path
from datetime import datetime, date
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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
            create_instruction(username=user_name,output=user_image_path)
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

scene_sentence = [
    "请在两分钟内", "请在一天的时间里", "在九十小时内", "请在一小时内", "今天之内必须",
    "请在睡前", "请从现在开始", "请在二十四小时内", "请在三十分钟内", "请立刻打开",
    "请在四小时内", "用你最顺手的方式", "在大街上当众", "请在空调房里",
    "请将手边的物品", "请在三小时内", "若你感觉被约束请", "请在晚上九点整",
    "在二十四小时内务必", "请在一分钟之内", "在冬天的户外", "在夏天的烈日下",
    "请在深夜里", "写作业的过程中", "请在两小时内", "请在今天结束前",
    "在十二小时三十七分钟二十四秒后"
]

action_sentence = [
    "对着镜子说八百遍我是正常人", "喝下一升的热牛奶",
    "开始三十分钟的剧烈运动", "只用右手写字吃饭和做所有事",
    "去往图书馆拿出一本任意的书", "戴上黑色面具找到一个陌生人",
    "对朋友说痛苦啊你就是我的唯一", "睡十分钟醒十分钟重复二十四小时",
    "举起一把刀对着墙面划下痕迹", "眨三次眼并用力点一次头",
    "找到任意白色液体并喝掉", "给见到的第一个熟人一拳",
    "工作十二小时后立刻下班休息", "在最痛苦的时候开怀大笑",
    "听完所有你最喜欢的音乐", "用橡皮当笔写完一次作业",
    "用叉子当筷子吃完一顿饭", "盯着镜子里的自己直到认不出",
    "学会一支简单的舞蹈并跳出来", "买五十六桶爆米花并全部打开",
    "吹一小时的冷气不许离开", "连续玩二十四小时的游戏不休息",
    "把这首哈基米音乐完整唱完", "流利说完二十六个英文字母",
    "模仿猫咪的样子让猫睡床你睡猫窝", "喝下一升的温牛奶",
    "写一篇短篇小说并分享给三个人", "站在垃圾桶上享用你的晚餐",
    "站在大街上淋一场完整的雨", "给自己放二十四小时的无理由假期",
    "让喜欢的人发现你最奇怪的小癖好", "看完所有你最喜欢的动漫",
    "学会游泳并前往湖边尝试", "免费拿到一颗鸡蛋并好好保存",
    "和朋友PK并一定要获得胜利", "向星星许愿并两小时内完成愿望",
    "展示一个你最拿手的后空翻", "把左手和右手的物品互换使用",
    "只吃一半煮好的面条剩下的倒掉", "打开空调调到最低温度",
    "打开暖气调到最高温度", "在街道垃圾桶旁品尝你的零食",
    "晒三十分钟的日光浴不遮挡", "在白墙上看出绿色的图案",
    "聆听自己的内心并前往想去的地方", "把任意视频的评论全部看完",
    "和朋友吵架直到他不再回怼", "刷完一套高考模拟试题并核对答案",
    "听mili的歌并三连", "在漆黑的下水道念出痛苦啊你便是我的唯一",
    "找到一个时长11分45秒的视频并看完", "向暗恋的人表白并向右跳一下",
    "假装自己是警察并对路人说你被逮捕了", "假装自己是明星并让路人找你签名",
    "找到一只山羊并骑在上面两小时", "把自己的内脏挂在家中的墙上，骨头部分可以不用处理。",
    "打开你最喜欢的游戏并给今天第一个登录的游戏充值任意金额。",
    "点一份外卖若超时就并且只给外卖员一块钱配送费。",
    "请前往附近的医院并跟医生坚持说自己有病并说出症状。",
    "在装满热牛奶的泳池中跳一支舞并把泳池里的牛奶喝完。",
    "打开边狱巴士并只用一次通关15牢。", "无视朋友发的所有信息"
]

supplement_sentence = [
    "然后若无其事的离开现场", "选择棕色头发的为优",
    "并且全程不让任何人发现", "骨头部分可以不用处理", "全程保持面无表情不说话",
    "做完之后抬头数十分钟的星星", "优先选择黑色头发的",
    "做这件事时无需有任何犹豫", "完成后一定要拍照留念记录", "不许借助任何的工具和外力",
    "直到完整完成这件事再停止", "整个过程不能被任何人察觉", "一定要自然不刻意",
    "全程保持沉默一句话也不说", "完成后要向我汇报结果", "必须独自一人完成不能找人帮忙",
    "做这件事时要放着哈基米音乐", "完成后把结果发布到你的社交平台"
]

easter_eggs = [
    "不念完自然常数e就不要回家。",
    "请在自己生日当天的凌晨零点，准时祝自己生日快乐。",
    "向你最喜欢的女生表白，直到她明确同意或者拒绝为止。",
    "现在去喝一口水",
    "关闭屏幕",
    "染上黑发并改名，然后找到一位伴侣，白色头发为优。",
    "告诉您所遇到的第34个人，自然常数其实是个整数。",
    "煽动31只蝴蝶的翅膀。",
    "用摄影机记录14区后巷居民的日常生活。",
    "在任意工坊购买一把长度大于12英寸的短剑。",
    "不要去执行任何所谓的指令。",
    "在路口转14个弯，并直走12m",
    "将有生命的画杀死",
    "在屋顶撑伞，并将伞扔到下面人头上",
    "将你路上遇到的第三片树叶放在头上3秒",
    "俯瞰天空13秒",
    "走到最近的十字路口，向对面方向遇见的第三个人挥手。",
    "在向母亲说过晚安以后，数完圆周率然后在十分钟内睡着。",
    "同时向前后分别移动十米",
    "屏住呼吸30!秒",
    "背诵圆周率倒数第六到第七百一十二位，结束之前不准饮水",
    "两分钟内按照完全向北的直线移动一千米",
    "在十二小时三十七分钟二十四秒后，完成一本针织的书",
]

NEON_BLUE = (0, 240, 255)
BRIGHT_WHITE = (255, 255, 255)
DARK_BG = (0, 0, 0)

def get_content():
    """生成指令文本"""
    if random.random() < 0.15:
        return random.choice(easter_eggs)
    return f"{random.choice(scene_sentence)}{random.choice(action_sentence)}{random.choice(supplement_sentence)}"


def _text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _wrap_lines(text, font, max_w):
    tmp = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    avg = _text_width(d, "测", font) or font.size * 0.65
    cpl = max(1, int(max_w / avg))
    rough = textwrap.wrap(text, width=cpl)
    lines = []
    for line in rough:
        if _text_width(d, line, font) <= max_w:
            lines.append(line)
        else:
            cur = ""
            for ch in line:
                t = cur + ch
                if _text_width(d, t, font) <= max_w:
                    cur = t
                else:
                    if cur: lines.append(cur)
                    cur = ch
            if cur: lines.append(cur)
    return lines or [text]


def _draw_bold(draw, xy, text, font, fill):
    """9方向偏移绘制模拟粗体"""
    x, y = xy
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            draw.text((x + dx, y + dy), text, font=font, fill=fill)


def _char_glow_layer(width, height, chars_pos, color, font, blur_radius):
    """
    每个字符单独绘制 → 单独blur → 合成一个光晕层
    这样每个字的发光量和范围完全相同，不会因为字距密集而叠加变亮
    """
    layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    for (ch, x, y) in chars_pos:
        # 每个字单独一个小图层
        char_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        d = ImageDraw.Draw(char_layer)
        _draw_bold(d, (x, y), ch, font, (*color, 255))
        char_layer = char_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        layer = Image.alpha_composite(layer, char_layer)

    return layer


def create_instruction(username, output="instruction.png",
                         width=900, font_size=32, header_img_path="data/plugins/astrbot_plugin_instruction/logo.png"):
    content = get_content()
    full_text = f"致{username}：{content}"

    font = ImageFont.truetype('data/plugins/astrbot_plugin_instruction/LXGWWenKai-Regular.ttf', font_size)
    pad_x, pad_x_top = 40, 40
    max_w = width - 2 * pad_x

    lines = _wrap_lines(full_text, font, max_w)
    line_h = font_size + 18

    # ---- 加载顶部图片 ----
    header_img = None
    header_h = 0
    try:
        header_img = Image.open(header_img_path).convert('RGBA')
        # 自适应缩放：宽度不超过画布50%，保持比例
        max_header_w = width // 2
        if header_img.width > max_header_w:
            ratio = max_header_w / header_img.width
            header_img = header_img.resize(
                (max_header_w, int(header_img.height * ratio)),
                Image.LANCZOS
            )
        header_h = header_img.height + 20  # 图片下方留20px间距
    except (OSError, IOError):
        pass  # 没找到图片就跳过

    # ---- 计算画布高度 ----
    tmp = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    dt = ImageDraw.Draw(tmp)
    lw = [_text_width(dt, l, font) for l in lines]
    text_block_h = len(lines) * line_h
    text_top = header_h + 40  # 文字区顶部 = 图片+间距+上方留白
    height = text_top + text_block_h + 60  # 下方留白60

    # ---- 黑色底图 ----
    base = Image.new('RGBA', (width, height), (*DARK_BG, 255))

    # ---- 放置顶部图片 ----
    if header_img:
        hx = (width - header_img.width) // 2
        hy = 20  # 距画布顶部20px
        base = Image.alpha_composite(base, header_img) if hx == 0 and hy == 0 else _paste_rgba(base, header_img, hx, hy)

    # ---- 计算每个字符的坐标 ----
    chars_pos = []
    for i, line in enumerate(lines):
        x_start = (width - lw[i]) // 2
        y = text_top + i * line_h
        cx = x_start
        for ch in line:
            ch_w = _text_width(dt, ch, font)
            chars_pos.append((ch, cx, y))
            cx += ch_w

    # ---- 蓝色光晕：逐字单独blur，保证均匀 ----
    # 外层大光晕 4遍 × blur22
    for _ in range(5):
        layer = _char_glow_layer(width, height, chars_pos, NEON_BLUE, font, blur_radius=35)
        base = Image.alpha_composite(base, layer)

    # 中层光晕 4遍 × blur22
    for _ in range(4):
        layer = _char_glow_layer(width, height, chars_pos, NEON_BLUE, font, blur_radius=22)
        base = Image.alpha_composite(base, layer)

    # 内层光晕 3遍 × blur12
    for _ in range(3):
        layer = _char_glow_layer(width, height, chars_pos, NEON_BLUE, font, blur_radius=12)
        base = Image.alpha_composite(base, layer)

    # 近层光晕 2遍 × blur6
    for _ in range(2):
        layer = _char_glow_layer(width, height, chars_pos, NEON_BLUE, font, blur_radius=6)
        base = Image.alpha_composite(base, layer)

    # ---- 清晰粗体白字 ----
    d = ImageDraw.Draw(base)
    for i, line in enumerate(lines):
        x = (width - lw[i]) // 2
        y = text_top + i * line_h
        _draw_bold(d, (x, y), line, font, (*BRIGHT_WHITE, 255))

    base.convert('RGB').save(output, quality=95)
    return output


def _paste_rgba(base, overlay, x, y):
    """在指定坐标粘贴RGBA图片到base上"""
    # 创建一个全尺寸临时图层，把overlay放到正确位置
    tmp = Image.new('RGBA', (base.width, base.height), (0, 0, 0, 0))
    tmp.paste(overlay, (x, y), overlay)  # 第三个参数是mask，用overlay自身的alpha
    return Image.alpha_composite(base, tmp)
