import asyncio

from nonebot import get_driver, logger
from nonebot.adapters import Bot

from . import config
from .config import config_manager
from .hook_manager import run_hooks

driver = get_driver()
__KERNEL_VERSION__ = "unknown"

@driver.on_bot_connect
async def onConnect(bot: Bot):
    logger.info(f"已连接 {bot.self_id} ，开始加载配置文件。")
    config_manager.load(bot.self_id)
    logger.info("配置文件加载完成。")
    logger.info(f"配置文件目录：{config_manager.config_dir}")
    logger.info(f"主要配置文件：{config_manager.toml_config}")
    logger.info(f"群聊记忆文件目录：{config_manager.group_memory}")
    logger.info(f"私聊记忆文件目录：{config_manager.private_memory}")
    logger.info(f"模型预设文件目录：{config_manager.custom_models_dir}")

    # 执行 hook 函数
    await run_hooks(bot)


@driver.on_startup
async def onEnable():
    global __KERNEL_VERSION__
    import subprocess
    import sys

    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pip",
            "show",
            "nonebot-plugin-suggarchat",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await process.communicate()
        try:
            __KERNEL_VERSION__ = stdout.decode("utf-8").split("\n")[1].split(": ")[1]
        except IndexError:
            __KERNEL_VERSION__ = "unknown"
    except subprocess.CalledProcessError:
        __KERNEL_VERSION__ = "unknown"
    except Exception:
        __KERNEL_VERSION__ = "unknown"
    config.__KERNEL_VERSION__ = __KERNEL_VERSION__
    logger.info(f"NONEBOT PLUGIN SUGGARCHAT {__KERNEL_VERSION__}")
    logger.info("Start successfully!Waitting for bot connection...")
