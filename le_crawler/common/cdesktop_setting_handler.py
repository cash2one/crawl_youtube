#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

from ..common.settings_base import SettingsBase
class CDesktopSettingHandler(SettingsBase):
  def __init__(self, module_path):
    SettingsBase.__init__(self, module_path)
    self.meta_dict_ = self.settings.getdict('META_PATH', {})

  def get_meta_dict(self, )





