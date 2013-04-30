# -*- coding: utf-8 -*-

"""Posterous service"""
#
# Author: Wil Alvarez (aka Satanas)

import traceback

from libturpial.lib.interfaces.service import ServiceResponse
from libturpial.lib.services.media.upload.base import UploadService


class PosterousUploader(UploadService):
    def __init__(self):
        UploadService.__init__(self, "posterous.com", "/api2/upload.xml",
            "https://api.twitter.com/1/account/verify_credentials.json")

    def do_service(self, account, filepath, message):
        try:
            _image = self._open_file(filepath)
        except:
            return self._error_opening_file(filepath)

        files = (
            ('media', self._get_pic_name(filepath), _image),
        )

        fields = (
            ('message', message),
        )
        try:
            resp = self._upload_pic(account, fields, files)
            link = self._parse_xml('url', resp)
            return ServiceResponse(link)
        except Exception, error:
            self.log.debug("Error: %s\n%s" % (error, traceback.print_exc()))
            return ServiceResponse(err=True,
                                   err_msg='Problem uploading pic')
