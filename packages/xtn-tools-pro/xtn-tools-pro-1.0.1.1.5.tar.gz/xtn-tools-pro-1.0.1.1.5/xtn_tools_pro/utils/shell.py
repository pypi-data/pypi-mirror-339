#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 说明：
#    服务器批量操作
# History:
# Date          Author    Version       Modification
# --------------------------------------------------------------------------------------------------
# 2025/4/2    xiatn     V00.01.000    新建
# --------------------------------------------------------------------------------------------------
import os

from fabric import Connection, Config
from xtn_tools_pro.utils.log import Log


class ShellPro:
    def __init__(self, server_info_list):
        self.server_info_list = server_info_list
        self.__logger = Log('shell', './xxx.log', log_level='DEBUG', is_write_to_console=True,
                            is_write_to_file=False,
                            color=True, mode='a', save_time_log_path='./logs')

        for _ in range(len(self.server_info_list)):
            ip, pwd, tips = self.server_info_list[_]["ip"], \
                            self.server_info_list[_]["pwd"], \
                            self.server_info_list[_]["tips"]
            self.__logger.info(f"{tips} 正在连接...")
            config = Config(overrides={'sudo': {'password': pwd}})
            conn = Connection(
                host=ip,
                user="root",  # 根据实际情况修改用户名
                connect_kwargs={"password": pwd},
                config=config
            )
            self.server_info_list[_]["conn"] = conn
            self.__logger.info(f"{tips} 连接成功!!!")

    def run_shell(self, conn, cmd, warn=False, hide=True, tips=""):
        """
            传入conn和命令执行
        :param conn:
        :param cmd:
        :param warn:
        :param hide: 隐藏命令输出（减少控制台噪音）
        :param tips: 备注信息
        :return:
        """
        conn.run(cmd, warn=warn, hide=hide)
        self.__logger.info(f"{tips} {cmd}")

    def update_file(self, local_file, remote_file, mkdir=False):
        """
            覆盖远程文件
        :param local_file: 本地文件
        :param remote_file: 远程文件
        :param mkdir: 是否先在远程创建该路径的文件夹
        :return:
        """
        for server_item in self.server_info_list:
            ip = server_item["ip"]
            tips = server_item["tips"]
            conn = server_item["conn"]
            if mkdir:
                remote_dir = os.path.dirname(remote_file)
                cmd = f"mkdir -p {remote_dir}"
                self.run_shell(conn, cmd=cmd, warn=True, tips=tips)
            conn.put(local_file, remote_file)
            self.__logger.info(f"{tips}-{ip} 覆盖远程文件成功!!!")


if __name__ == '__main__':
    server_info_list = [
        {"ip": "xxx.xxx.xx.xxx", "pwd": "123456", "tips": "服务器_01"},
    ]
    sh = ShellPro(server_info_list=server_info_list)
