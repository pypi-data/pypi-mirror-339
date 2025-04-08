import traceback
import time
from functools import wraps
from typing import Dict, List, Set, Any, Union, Optional, Callable, Awaitable
import asyncio

from nonebot import get_driver, on_command, on_message, on_keyword
import nonebot.log
from nonebot.log import default_filter as original_default_filter # 导入并重命名原始过滤器
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, GroupMessageEvent, MessageEvent, Message
from nonebot.rule import Rule, to_me
from nonebot.plugin import PluginMetadata
from nonebot import require, logger
from nonebot.matcher import Matcher
from nonebot.exception import FinishedException


# 先导入依赖
require("nonebot_plugin_localstore")
from .config import Config, get_plugin_config
from .data_manager import MessageRecorder

# 然后定义插件元数据
__plugin_meta__ = PluginMetadata(
    name="whoasked",
    description="查询谁@了你或引用了你的消息",
    usage="发送 谁问我了 即可查询",
    type="application",
    homepage="https://github.com/enKl03B/nonebot-plugin-whoasked",
    supported_adapters={"~onebot.v11"},
    config=Config,
    extra={
        "unique_name": "whoasked",
        "example": "谁问我了",
        "author": "enKl03B",
        "version": "0.2.1",
        "repository": "https://github.com/enKl03B/nonebot-plugin-whoasked"
    }
)

# --- 全局关闭状态标志 ---
_is_shutting_down = False

# --- 定义新的组合过滤器 ---
def custom_whoasked_filter(record):
    """
    自定义日志过滤器：
    1. 应用原始的 NoneBot 默认过滤器。
    2. 额外过滤掉来自 nonebot logger 的、特定模块的 message 类型 matcher 的完成日志。
    """
    if not original_default_filter(record):
        return False

    # record 是 loguru 的 record 字典
    if record["name"] == "nonebot" and record["level"].name == "INFO":
        log_message = record["message"]
        # 检查关键部分是否存在，而不是完整的结构和行号
        if "Matcher(type='message'," in log_message and \
           "module='nonebot_plugin_whoasked'" in log_message and \
           log_message.endswith("running complete"):
            return False  # 过滤掉这条日志
    return True


# 全局配置
global_config = get_driver().config

# 修改消息记录器初始化
message_recorder = None

async def init_message_recorder():
    global message_recorder
    if message_recorder is None: # 避免重复初始化
        message_recorder = MessageRecorder()
        logger.info("消息记录器初始化完成")

# --- 定义关闭感知的 Rule ---
async def shutdown_aware_rule() -> bool:
    """如果程序正在关闭，则返回 False"""
    return not _is_shutting_down

# 在插件加载时初始化
from nonebot import get_driver
driver = get_driver()

@driver.on_startup
async def _startup():
    """插件启动时的操作"""
    global _is_shutting_down
    _is_shutting_down = False # 确保启动时标志为 False
    # 初始化消息记录器
    await init_message_recorder()

    # --- 应用新的过滤器 ---
    # 检查是否已经被 patch 过，防止重复 patch (例如在 reload 插件时)
    if getattr(nonebot.log.default_filter, "__name__", None) != 'custom_whoasked_filter':
        logger.debug("应用自定义日志过滤器以隐藏 record_msg 完成日志。")
        # 使用我们的函数替换 nonebot.log.default_filter
        nonebot.log.default_filter = custom_whoasked_filter
    else:
        logger.debug("自定义日志过滤器已应用。")


@driver.on_shutdown
async def shutdown_hook():
    """在驱动器关闭时调用"""
    global _is_shutting_down
    logger.info("检测到关闭信号，设置关闭标志...")
    _is_shutting_down = True # 立即设置关闭标志

    # 等待一小段时间，让事件循环有机会处理完当前正在执行的任务
    # 并让 Rule 生效，阻止新的 Matcher 运行
    await asyncio.sleep(0.1) 

    if message_recorder:
        await message_recorder.shutdown() # 然后再执行数据保存等清理操作

# 关键词集合
QUERY_KEYWORDS = {"谁问我了"}

# 修改错误处理装饰器
def catch_exception(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FinishedException:
            raise
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行出错: {str(e)}")
            logger.error(traceback.format_exc())
            if len(args) > 0 and hasattr(args[0], "finish"):
                try:
                    await args[0].finish(f"处理命令时出错: {str(e)[:100]}")
                except FinishedException:
                    raise
    return wrapper

# --- 修改消息记录器注册，加入 Rule ---
record_msg = on_message(rule=shutdown_aware_rule, priority=1, block=False) # 添加 rule
@record_msg.handle() # 现在日志中看到的行号可能是这里
async def _handle_record_msg(bot: Bot, event: MessageEvent):
    """记录所有消息"""
    # 无需在此处再次检查 _is_shutting_down，因为 Rule 已经阻止了它
    if message_recorder is None:
        logger.warning("尝试记录消息时，MessageRecorder 未初始化。")
        return
    try:
        # 注意：即使 Rule 阻止了新的匹配，如果 handle 在 Rule 检查前已被调用，
        # 这里的 shutdown 检查仍然是有意义的，防止并发问题。
        if message_recorder._shutting_down:
             logger.debug("MessageRecorder 正在关闭，跳过内部记录逻辑")
             return
        await message_recorder.record_message(bot, event)
    except Exception as e:
        logger.error(f"记录消息失败: {e}")
        logger.error(traceback.format_exc())

# 修改命令处理器
who_at_me = on_command("谁问我了", priority=50, block=True)
@who_at_me.handle()
@catch_exception
async def handle_who_at_me(bot: Bot, event: GroupMessageEvent):
    """处理查询@消息的指令"""
    if message_recorder is None:
        await who_at_me.finish("消息记录器未初始化，请稍后再试")
        return
        
    logger.info(f"收到谁@我命令，来自用户 {event.user_id}，群 {event.group_id}")
    await process_query(bot, event, who_at_me)

# 修改查询处理函数
async def process_query(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    """处理查询@消息的请求"""
    user_id = str(event.user_id)
    current_group_id = str(event.group_id)
    
    try:
        async with asyncio.timeout(10):  # 增加10秒超时控制
            user_id = str(event.user_id)
            current_group_id = str(event.group_id)
        # 添加性能监控
        start_time = time.time()
        
        messages = await message_recorder.get_at_messages(user_id)
        
        if not messages:
            await matcher.finish("最近没人问你")
            return
        
        # 使用生成器表达式优化内存使用
        filtered_messages = (
            msg for msg in messages
            if msg.get("group_id") == current_group_id and
               (user_id in msg.get("at_list", []) or
               (msg.get("is_reply", False) and msg.get("reply_user_id") == user_id))
        )
        
        # 转换为列表并检查是否为空
        filtered_messages = list(filtered_messages)
        if not filtered_messages:
            await matcher.finish("最近在本群没有人问你")
            return
        
        # 构建转发消息
        forward_messages = [{
            "type": "node",
            "data": {
                "name": event.sender.card or event.sender.nickname,
                "uin": user_id,
                "content": str(event.get_message())
            }
        }]
        
        # 使用列表推导式优化
        forward_messages.extend({
            "type": "node",
            "data": {
                "name": msg_data["sender_name"],
                "uin": msg_data["user_id"],
                "content": f"【{'引用了你的消息' if msg_data.get('is_reply', False) else '@了你'}】\n{msg_data['raw_message']}"
            }
        } for msg_data in filtered_messages)
        
        # 添加性能日志
        logger.info(f"处理查询请求耗时: {time.time() - start_time:.2f}秒")
        
        await bot.call_api(
            "send_group_forward_msg",
            group_id=event.group_id,
            messages=forward_messages
        )
    except FinishedException:
        raise
    except Exception as e:
        logger.error(f"处理查询请求失败: {e}")
        logger.error(traceback.format_exc())
        try:
            await matcher.finish("查询失败，请稍后再试")
        except FinishedException:
            raise