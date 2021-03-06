# -*- coding: utf-8 -*-
"""Group Controller"""
from tgext.crud import CrudRestController
from biorepo.lib.base import BaseController
from tg import expose, flash
from repoze.what.predicates import has_permission
from tg.controllers import redirect
#from biorepo.widgets.group import new_group_form, group_edit_form
from biorepo.model import DBSession, Group
from tg import app_globals as gl
__all__ = ['GroupController']


class GroupController(BaseController):
    allow_only = has_permission(gl.perm_admin)
    model = Group
    #edit_form = group_edit_form
    #new_form = new_group_form

    @expose('genshi:tgext.crud.templates.post_delete')
    def post_delete(self, *args, **kw):
        for id in args:
            group = DBSession.query(Group).filter(Group.id == id).first()
            if group.name == gl.group_admins:
                flash('Cannot delete admin group')
                redirect('/groups')
            if group.name == gl.group_users:
                flash('Cannot delete users group')
                redirect('/groups')
        return CrudRestController.post_delete(self, *args, **kw)
