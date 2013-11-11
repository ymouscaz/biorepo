# -*- coding: utf-8 -*-
"""Trackhubs Controller"""
from biorepo.lib.base import BaseController
from biorepo import handler
from repoze.what.predicates import has_any_permission
import os
from tg import request, session, expose
from tg import app_globals as gl
from tg.decorators import with_trailing_slash
from biorepo.lib import util
from biorepo.lib.constant import trackhubs_path
from biorepo.widgets.datagrids import TrackhubGrid

__all__ = ['TrackhubController']


class TrackhubController(BaseController):
    allow_only = has_any_permission(gl.perm_admin, gl.perm_user)

    @with_trailing_slash
    @expose('biorepo.templates.list_no_new')
    def index(self, *args, **kw):
        user = handler.user.get_user_in_session(request)
        user_lab = session.get("current_lab", None)
        mail = user.email
        mail_tmp = mail.split("@")
        mail_final = mail_tmp[0] + "AT" + mail_tmp[1]
        user_TH_path = trackhubs_path() + "/" + user_lab + "/" + mail_final
        trackhubs = {}
        if os.path.exists(user_TH_path):
            list_trackhubs = os.listdir(user_TH_path)
            for t in list_trackhubs:
                th_path = user_TH_path + "/" + t
                #the only one directory into at this th level is named by the assembly used for it
                for i in os.listdir(th_path):
                    if os.path.isdir(i):
                        assembly = i
                hub_url = th_path + "/hub.txt"
                trackhubs[t] = 'http://genome.ucsc.edu/cgi-bin/hgTracks?hubUrl=' + hub_url + "&db=" + assembly

        else:
            #local test, TODO : delete it when the bug will be fixed
            trackhubs = {"name_test": "http://toto.com", "name2222_Tetssss": "http://google.com"}

        all_trackhubs = [util.to_datagrid(TrackhubGrid(), trackhubs, " UCSC's Trackhub(s)", len(trackhubs) > 0)]

        return dict(page='trackhubs', model=trackhubs, items=all_trackhubs, value=kw)
