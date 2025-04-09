#!/bin/env python3
# -*- coding: UTF-8 -*-

import os
import pathlib
import tempfile
from configparser import ConfigParser

config = ConfigParser()
path = ''
conf_path = str(pathlib.Path(os.path.abspath(__file__)).parent.parent) + "/conf.cfg" if len(str(path)) == 0 else path
config.read(os.path.abspath(conf_path), encoding="UTF-8")


def get_temp_dir_from_config():
    """
    从配置中获取临时存储目录，如果没有配置则使用默认目录
    """
    temp_dir = config['App']['temp_dir']
    return temp_dir


class ApiConfig:
    """A ApiConfig Class"""
    oauth2_uri = config['API']['oauth2_uri']
    token = config['API']['token']
    project_id = config['API']['project_id']

    @classmethod
    def update_token(cls, new_token):
        """Update token"""
        if new_token:
            cls.token = new_token

    @classmethod
    def update_project_id(cls, new_project_id):
        """Update project_id"""
        if new_project_id:
            cls.project_id = new_project_id

    @classmethod
    def load_from_args(cls, token='', project_id=''):
        if token:
            cls.update_token(token)
        if project_id:
            cls.update_project_id(project_id)


class SSLConfig:
    """SSL证书校验"""
    verify = config['SSL']['verify']


class FILE_UPLOAD_TYPE:
    """FTP/SFTP UPLOAD_CHOOSE"""
    upload_choose = config['FILE_UPLOAD_TYPE']['upload_choose']
    file_protocol = 'FTP' if upload_choose.lower() == 'true' else "SFTP"

class BaseConfig:
    """A BaseConfig Class"""
    timezone = 'Asia/Shanghai'


class FTPConfig:
    namespace = config['FTP']['ftp_namespace']
    host = config['FTP']['ftp_host']
    user = config['FTP']['ftp_user']
    password = config['FTP']['ftp_password']
    port = config['FTP']['ftp_port']


class SFTPConfig:
    namespace = config['SFTP']['sftp_namespace']
    host = config['SFTP']['sftp_host']
    user = config['SFTP']['sftp_user']
    password = config['SFTP']['sftp_password']
    port = config['SFTP']['sftp_port']


class SaasConfig:
    uri = config['SAAS']['saas_uri']
    token = config['SAAS']['saas_token']
    uid = config['SAAS']['saas_uid']
