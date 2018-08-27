import zipfile
import rarfile
import json
import os
from schema import Schema, Optional, And
from werkzeug import secure_filename


class Archive(object):
    @staticmethod
    def _get_obj_method(suffix):
        """
        :param suffix: 文件后缀名
        :return: obj, method
        """
        d = {
            'rar': (rarfile, rarfile.RarFile),
            'zip': (zipfile, zipfile.ZipFile),
        }
        return d[suffix]

    @classmethod
    def validate(cls, file, suffix):
        """
        验证压缩包中内容是否与预期相符，防止用户恶意上传。
        :param file: request.file
        :param suffix: 后缀名
        :return: True or False
        """
        obj, method = cls._get_obj_method(suffix)
        result = []
        ora_file_name = {
            'sheet1': ('data_sheet1.json', ValidateORAFile.sheet1),
            'sheet2': ('data_sheet2.json', ValidateORAFile.sheet2),
            'sheet3': ('data_sheet3.json', ValidateORAFile.sheet3),
            'meta_info': ('metainfo.json', ValidateORAFile.meta_info),
        }
        try:
            archive = method(file, 'r')
            for k, v in ora_file_name.items():
                name, method = v
                data = json.loads(archive.read(name))
                result.append(method(data))
            return all(result)
        except:
            return False

    @staticmethod
    def rename(file_name, files_path):
        """
        过滤非法文件名，并判断本地是否有相同文件名的文件。
        如果有，那么则改成以下格式的新文件名:
            index_filename.rar
        并返回文件保存的绝对路径
        """
        file_name = secure_filename(file_name)
        index = 0
        path = os.path.join(files_path, file_name)
        while os.path.exists(path):
            if index == 0:
                index += 1
                file_name = '{}_{}'.format(index, file_name)
            else:
                file_name = file_name[len(str(index)) + 1:]
                index += 1
                file_name = '{}_{}'.format(index, file_name)
            path = os.path.join(files_path, file_name)
        return path


class ValidateORAFile(object):
    @staticmethod
    def sheet1(data):
        try:
            Schema([{
                'subject': {
                    'team': str,
                    'player': str,
                    'chara': str,
                },
                'object': {
                    'team': str,
                    'player': str,
                    'chara': str,
                },
                'assist': {
                    '1': {
                        Optional('hero'): str,
                        Optional('player'): str,
                    },
                    '2': {
                        Optional('hero'): str,
                        Optional('player'): str,
                    },
                    '3': {
                        Optional('hero'): str,
                        Optional('player'): str,
                    },
                    '4': {
                        Optional('hero'): str,
                        Optional('player'): str,
                    },
                    '5': {
                        Optional('hero'): str,
                        Optional('player'): str,
                    },
                },
                'time': str,
                'action': str,
                'ability': str,
                'critical kill': str,
                'comments': str,
            }]).validate(data)
            return True
        except:
            return False

    @staticmethod
    def sheet2(data):
        try:
            Schema(And([
                {
                    'team': str,
                    'team_status': str,
                    'players': And([
                        {
                            'index': int,
                            'name': str,
                            'starting lineup': str,
                            'final lineup': str,
                            'KDA': str,
                        }
                    ], lambda lt: len(lt) == 6)
                },
            ], lambda lt: len(lt) == 2)).validate(data)
            return True
        except:
            return False

    @staticmethod
    def sheet3(data):
        try:
            Schema([
                {
                    'time': str,
                    'players': And([
                        {
                            'chara': str,
                            'hps': int,
                            'ults': int,
                            'team': str,
                            'index': int,
                        },
                    ], lambda lt: len(lt) == 12)
                }
            ]).validate(data)
            return True
        except:
            return False

    @staticmethod
    def meta_info(data):
        try:
            Schema({
                "team_names": And([str], lambda lt: len(lt) == 2),
                "player_names": And([str], lambda lt: len(lt) == 12),
                "game_type": int,
                "game_version": int,
                "created_at": str,
            }).validate(data)
            return True
        except:
            return False

