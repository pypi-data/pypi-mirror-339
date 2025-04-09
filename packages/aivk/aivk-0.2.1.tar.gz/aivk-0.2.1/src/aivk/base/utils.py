"""AIVK 工具函数模块"""
import asyncio
import logging
import importlib
import subprocess
import os
from asyncio.subprocess import Process
from dataclasses import dataclass
from typing import Dict, Any, Literal, Optional, Union, List, Tuple
from datetime import datetime

@dataclass
class AivkExecResult:
    """命令执行结果数据类"""
    returncode: int
    stdout: str
    stderr: str
    success: bool
    command: str

class AivkExecuter:
    """AIVK 命令执行器
    
    提供同步和异步命令执行功能，并记录执行统计信息
    """
    
    # 元数据类变量
    _total_execs = 0  # 执行总数
    _failed_execs = 0  # 失败数
    _last_exec = None  # 最后执行的命令
    _exec_history = []  # 执行历史
    _start_time = None  # 开始执行时间
    
    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """获取执行统计信息
        
        Returns:
            Dict[str, Any]: 包含总数、失败数、成功率等统计信息的字典
        """
        return {
            "total_execs": cls._total_execs,
            "failed_execs": cls._failed_execs,
            "success_rate": (cls._total_execs - cls._failed_execs) / cls._total_execs if cls._total_execs > 0 else 0,
            "last_exec": cls._last_exec,
            "history": cls._exec_history
        }

    @classmethod
    def _update_stats(cls, result: AivkExecResult) -> None:
        """更新执行统计信息
        
        Args:
            result: 命令执行结果
        """
        cls._total_execs += 1
        if not result.success:
            cls._failed_execs += 1
        cls._last_exec = result.command
        cls._exec_history.append({
            "command": result.command,
            "success": result.success,
            "timestamp": datetime.now().isoformat()
        })
    
    @staticmethod
    async def _process_output(process: Process, encoding: str = 'utf-8') -> Tuple[str, str]:
        """处理进程输出"""
        stdout, stderr = await process.communicate()
        return (stdout.decode(encoding) if stdout else "",
                stderr.decode(encoding) if stderr else "")

    @classmethod
    async def aexec(cls, command: Union[str, List[str]], 
                   working_dir: Optional[str] = None,
                   env: Optional[Dict[str, str]] = None,
                   timeout: Optional[float] = None,
                   encoding: str = 'utf-8',
                   check: bool = True,
                   shell: bool = True) -> AivkExecResult:
        """异步执行命令
        
        Args:
            command: 要执行的命令(字符串或列表)
            working_dir: 工作目录
            env: 环境变量字典
            timeout: 超时时间(秒)
            encoding: 输出编码
            check: 失败时是否抛出异常
            shell: 是否通过shell执行
            
        Returns:
            AivkExecResult: 命令执行结果
            
        Raises:
            TimeoutError: 命令执行超时
            subprocess.CalledProcessError: 命令执行失败且check=True
        """
        logger = logging.getLogger("aivk.executor")
        working_dir = working_dir or os.getcwd()
        env = env or os.environ.copy()
        cls._start_time = datetime.now()
        
        if isinstance(command, list):
            command = " ".join(command)
            
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=env,
                shell=shell
            ) if shell else await asyncio.create_subprocess_exec(
                *command.split(),
                stdout=asyncio.subprocess.PIPE, 
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=env
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    cls._process_output(process, encoding),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                raise TimeoutError(f"命令执行超时: {command}")
                
            await process.wait()
            success = process.returncode == 0
            
            if check and not success:
                raise subprocess.CalledProcessError(
                    process.returncode, command, stdout.encode(), stderr.encode()
                )
                
            result = AivkExecResult(
                returncode=process.returncode,
                stdout=stdout,
                stderr=stderr,
                success=success,
                command=command
            )
            cls._update_stats(result)
            return result
            
        except Exception as e:
            logger.error(f"命令执行失败: {e}")
            raise

    @classmethod
    def exec(cls, command: Union[str, List[str]],
            working_dir: Optional[str] = None,
            env: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None,
            encoding: str = 'utf-8',
            check: bool = True,
            shell: bool = True) -> AivkExecResult:
        """同步执行命令
        
        Args:
            command: 要执行的命令(字符串或列表)
            working_dir: 工作目录
            env: 环境变量字典
            timeout: 超时时间(秒)
            encoding: 输出编码
            check: 失败时是否抛出异常
            shell: 是否通过shell执行
            
        Returns:
            AivkExecResult: 命令执行结果
            
        Raises:
            TimeoutError: 命令执行超时
            subprocess.CalledProcessError: 命令执行失败且check=True
        """
        logger = logging.getLogger("aivk.executor")
        working_dir = working_dir or os.getcwd()
        env = env or os.environ.copy()
        cls._start_time = datetime.now()

        try:
            if isinstance(command, list):
                command = " ".join(command)

            process = subprocess.run(
                command,
                shell=shell,
                cwd=working_dir,
                env=env,
                timeout=timeout,
                capture_output=True,
                text=True,
                encoding=encoding,
                check=check
            )
            
            result = AivkExecResult(
                returncode=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
                success=process.returncode == 0,
                command=command
            )
            cls._update_stats(result)
            return result
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"命令执行超时: {command}")
        except Exception as e:
            logger.error(f"命令执行失败: {e}")
            raise

async def aivk_on(action_str: Literal["load", "unload", "install", "uninstall", "update","cli"] | str, 
                 id: str,
                 **kwargs: Dict[str, Any]
                ) -> any:
    """AIVK 统一操作接口

    Args:
        action_str: 动作字符串，可以是预定义动作或自定义动作
        id: 模块 ID
        **kwargs: 附加参数

    Returns:
        any: 操作结果
    """
    logger = logging.getLogger("aivk.utils")
    
    # 构造导入路径
    if id.startswith("aivk-"):
        pypi_id = id
    else:
        pypi_id = f"aivk-{id}"
        
    if action_str == "cli":
        try:
            # 动态导入模块的 cli 组
            # e.g. from aivk-fs.cli import cli
            cli_module = importlib.import_module(f"{pypi_id}.cli")
            cli_group = getattr(cli_module, "cli")
            
            # 获取 AIVK 主命令组
            try:
                from ..cli import cli as aivk_cli
            except ImportError:
                from aivk.cli import cli as aivk_cli
                
            # 添加为子命令组
            aivk_cli.add_command(cli_group, name=id)
            logger.info(f"成功导入命令组: {id}")
            return True
            
        except ImportError as e:
            logger.error(f"无法导入模块 {id} 的命令组: {e}")
            return False
        except AttributeError as e:
            logger.error(f"模块 {id} 缺少 cli 命令组: {e}")
            return False
    
    pypi_onAction_str = f"{pypi_id}.on{action_str.capitalize()}"
    
    try:
        # 尝试导入并执行模块中的函数
        onAction = importlib.import_module(pypi_onAction_str)
        action : callable = getattr(onAction, action_str)
        
        if asyncio.iscoroutinefunction(action):
            await action(**kwargs)
        else:
            action(**kwargs)
            
    except ImportError as e:
        logger.error(f"无法导入模块 {id}: {e}")
        return False
    except AttributeError as e:
        logger.error(f"模块 {id} 没有 {action_str} 函数: {e}")
        return False
    except Exception as e:
        logger.error(f"执行 {action_str} 操作失败: {e}")
        return False
        
    return True

__all__ = [
    "aivk_on",
    "AivkExecuter",
    "AivkExecResult"
]
