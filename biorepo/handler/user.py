# -*- coding: utf-8 -*-
"""user handler"""
from biorepo.model.auth import User, Permission
from biorepo.model import DBSession
from tg import abort, redirect, url
from sqlalchemy import and_


def get_user_in_session(request):
    '''
    Get the user that is performing the current request
    @param request: the web request
    @type request: a WebOb
    '''

    if not 'repoze.who.identity' in request.environ:
        print "############### abort in handler/user ################"
        abort(401)
    identity = request.environ['repoze.who.identity']
    email = identity['repoze.who.userid']
    user = DBSession.query(User).filter(User.email == email).first()
    return user


def get_user(key, mail):
    '''
    Get the user with the the given mail,
    with the given key.
    '''
    print key, "------------ key given"
    print mail, " ---------- mail given"
    return DBSession.query(User).filter(and_(User.email == mail, User.key == key)).first()

#TODO
#def isAdmin(user.id):

    #return the user permission

    #pass
    #return DBSession.query(User.id)
