#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Create Time: 2021/1/25 10:00
# Create User: NB-Dragon
import uuid
import urllib.parse
from tool.RuntimeOperator import RuntimeOperator
from schema.Downloader.HTTPDownloader import HTTPDownloader


class DownloadHelper(object):
    def __init__(self, message_receiver, runtime_operator: RuntimeOperator):
        self._runtime_operator = runtime_operator
        self._message_receiver = message_receiver

    def create_download_mission(self, mission_info: dict):
        uuid_description = "".join(str(uuid.uuid1()).split("-"))
        self._distribute_download_mission(uuid_description, mission_info, dict())

    def load_download_mission(self, mission_uuid, mission_info, download_info):
        self._distribute_download_mission(mission_uuid, mission_info, download_info)

    def _distribute_download_mission(self, mission_uuid, mission_info, download_info):
        link_parse_result = urllib.parse.urlparse(mission_info["download_link"])
        scheme = link_parse_result.scheme
        if scheme in ["https", "http"]:
            http_helper = HTTPDownloader(mission_uuid, mission_info, download_info, self._message_receiver)
            http_helper.start_download_mission()
        else:
            self._make_message_and_send(mission_uuid, "unknown scheme, please wait to support!", False)
        self._do_final_tips(mission_uuid)

    def _do_final_tips(self, uuid_description):
        final_donate_message = "赞助二维码图片路径为：{}".format(self._runtime_operator.get_static_donate_image_path())
        self._make_message_and_send(uuid_description, "任务结束", False)
        self._make_message_and_send(uuid_description, "如有帮助，请扫码给予赞助，感谢各位", False)
        self._make_message_and_send(uuid_description, final_donate_message, False)

    def _make_message_and_send(self, uuid_description, content, exception: bool):
        message_dict = dict()
        message_dict["action"] = "print"
        detail_info = {"sender": "DownloadHelper", "content": content, "exception": exception}
        message_dict["value"] = {"mission_uuid": uuid_description, "detail": detail_info}
        self._message_receiver.put(message_dict)
