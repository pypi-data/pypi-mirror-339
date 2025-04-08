# coding=utf-8
from collections.abc import Iterator
from typing import Any

import os
import datetime
import glob
import pathlib
from string import Template
import re

from ka_uts_com.log import Log

TyArr = list[Any]
TyAoS = list[str]
TyAoA = list[TyArr]
TyDic = dict[Any, Any]
TyDoA = dict[Any, TyArr]
TyDoAoA = dict[Any, TyAoA]
TyDoInt = dict[str, int]
TyDoDoInt = dict[str, TyDoInt]
TyIntStr = int | str
TyPath = str
TyIterAny = Iterator[Any]
TyStr = str
TyTup = tuple[Any]

TnArr = None | TyArr
TnAoA = None | TyAoA
TnDic = None | TyDic
TnInt = None | int
TnStr = None | str
TnTup = None | TyTup


class Path:

    @classmethod
    def edit_path(cls, path: str, kwargs: TyDic) -> str:
        _d_edit = kwargs.get('d_out_path_edit', {})
        _prefix = kwargs.get('dl_out_file_prefix', '')
        _suffix = kwargs.get('dl_out_file_suffix', '.csv')
        _edit_from = _d_edit.get('from')
        _edit_to = _d_edit.get('to')
        if _edit_from is not None and _edit_to is not None:
            _path_out = path.replace(_edit_from, _edit_to)
        else:
            _path_out = path
        _dir_out = os.path.dirname(_path_out)
        cls.mkdir_from_path(_dir_out)
        _basename_out = os.path.basename(_path_out)
        if _prefix:
            _basename_out = str(f"{_prefix}{_basename_out}")
        if _suffix:
            _basename_out = os.path.splitext(_basename_out)[0]
            _basename_out = str(f"{_basename_out}{_suffix}")
        _path_out = os.path.join(_dir_out, _basename_out)
        return _path_out

    @staticmethod
    def mkdir(path: str) -> None:
        if not os.path.exists(path):
            # Create the directory
            os.makedirs(path)

    @staticmethod
    def mkdir_from_path(path: str) -> None:
        _dir = os.path.dirname(path)
        if not os.path.exists(_dir):
            # Create the directory
            os.makedirs(_dir)

    @staticmethod
    def sh_basename(path: str) -> str:
        """ Extracts basename of a given path.
            Should Work with any OS Path on any OS
        """
        raw_string = r'[^\\/]+(?=[\\/]?$)'
        basename = re.search(raw_string, path)
        if basename:
            return basename.group(0)
        return path

    @classmethod
    def sh_component(
            cls, path: str, d_ix: TyDic, separator: str = "-") -> TnStr:
        ix_start = d_ix.get("start")
        ix_add = d_ix.get("add", 0)
        if not ix_start:
            return None
        _a_dir: TyArr = cls.split_to_array(path)
        _ix_end = ix_start + ix_add + 1
        _component = separator.join(_a_dir[ix_start:_ix_end])
        _component = os.path.splitext(_component)[0]
        return _component

    @classmethod
    def sh_component_at_start(
            cls, path: str, d_path_ix: TyDoDoInt, field_name: str) -> TyStr:
        _d_ix: TyDoInt = d_path_ix.get(field_name, {})
        if not _d_ix:
            msg = f"field_name: {field_name} is not defined in dictionary: {d_path_ix}"
            raise Exception(msg)
        _start = _d_ix.get('start')
        if not _start:
            msg = f"'start' is not defined in dictionary: {_d_ix}"
            raise Exception(msg)
        _a_dir: TyAoS = cls.split_to_array(path)
        if _start < len(_a_dir):
            return _a_dir[_start]
        msg = f"index: {_start} is out of range of list: {_a_dir}"
        raise Exception(msg)

    # @classmethod
    # def sh_data_type(cls, path: str, kwargs: TyDic) -> TnStr:
    #     _d_in_path_ix: TyDoDoInt = kwargs.get("d_in_path_ix", {})
    #     _d_data_type_ix: TyDoInt = _d_in_path_ix.get("data_type", {})
    #     _data_type = cls.sh_component(path, _d_data_type_ix)
    #     return _data_type

    @staticmethod
    def sh_fnc_name(path: str) -> str:
        _purepath = pathlib.PurePath(path)
        dir_: str = _purepath.parent.name
        stem_: str = _purepath.stem
        return f"{dir_}-{stem_}"

    @classmethod
    def sh_last_component(cls, path: str) -> Any:
        a_dir: TyArr = cls.split_to_array(path)
        return a_dir[-1]

    @staticmethod
    def sh_os_fnc_name(path: str) -> str:
        split_ = os.path.split(path)
        dir_ = os.path.basename(split_[0])
        stem_ = os.path.splitext(split_[1])[0]
        return f"{dir_}-{stem_}"

    @classmethod
    def sh_path_by_pathnm(cls, pathnm: str, **kwargs) -> str:
        _path = kwargs.get(pathnm, '')
        _d_path = kwargs.get('d_path', {})
        _path = cls.sh_path_by_d_path(_path, _d_path)
        path = cls.sh_path_by_d_pathnmh2dttype(_path, pathnm, kwargs)
        return path

    @staticmethod
    def sh_path_by_d_path(path: str, d_path: TyDic) -> str:
        if not d_path:
            return path
        return Template(path).safe_substitute(d_path)

    @classmethod
    def sh_path_by_d_pathnmh2dttype(
            cls, path: str, pathnm: str, kwargs) -> str:
        _d_pathnm2dttype: TyDic = kwargs.get('d_pathnm2dttype', {})
        _dttype: TyDoA = _d_pathnm2dttype.get(pathnm, {})
        Log.Eq.debug("_path", path)
        Log.Eq.debug("_pathnm", pathnm)
        Log.Eq.debug("_d_pathnm2dttype", _d_pathnm2dttype)
        Log.Eq.debug("_dttype", _dttype)
        match _dttype:
            case 'last':
                path_new = cls.sh_path_last(path)
            case 'first':
                path_new = cls.sh_path_first(path)
            case 'now':
                path_new = cls.sh_path_now(path, **kwargs)
            case _:
                path_new = cls.sh_path(path)
        Log.Eq.debug("path_new", path_new)
        return path_new

    @staticmethod
    def sh_path(path: str) -> str:
        Log.Eq.debug("path", path)
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        if not _a_path:
            raise Exception(f"glob.glob find no paths for template: {path}")
        path_new: str = sorted(_a_path)[0]
        return path_new

    @staticmethod
    def sh_path_first(path: str) -> str:
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        if not _a_path:
            raise Exception(f"glob.glob find no paths for template: {path}")
        path_new: str = sorted(_a_path)[0]
        return path_new

    @staticmethod
    def sh_path_last(path: str) -> str:
        if not path:
            raise Exception("Argument 'path' is empty")
        _a_path: TyArr = glob.glob(path)
        if not _a_path:
            raise Exception(f"glob.glob find no paths for template: {path}")
        path_new: str = sorted(_a_path)[-1]
        return path_new

    @staticmethod
    def sh_path_now(path: str, **kwargs) -> str:
        now_var = kwargs.get('now_var', 'now')
        now_fmt = kwargs.get('now_fmt', '%Y%m%d')
        if not path:
            raise Exception("Argument 'path' is empty")
        _current_date: str = datetime.datetime.now().strftime(now_fmt)
        _dic = {now_var: _current_date}
        path_new: str = Template(path).safe_substitute(_dic)
        return path_new

    @staticmethod
    def split_to_array(path: str) -> TyArr:
        """ Convert path to normalized pyth
            Should Work with any OS Path on any OS
        """
        normalized_path = os.path.normpath(path)
        a_path: TyArr = normalized_path.split(os.sep)
        return a_path
