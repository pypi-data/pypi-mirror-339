import json

from .query import Query
from .. import ValarResponse
from ..channels import ValarSocketSender
from ..channels.utils import execute_channel

from ..data.handlers import save_many_handler
from ..data.utils import get_dao, transform


async def save_many(request,db, entity):

    data = json.loads(request.body)
    handler = '%s/%s' % (db, entity)
    sender = ValarSocketSender(handler, request)
    await execute_channel(save_many_handler, data, sender)

    return ValarResponse(True)

def save_one (request,db, entity):
    item = json.loads(request.body)
    dao = get_dao(db, entity)
    bean = dao.save_one(item)
    return ValarResponse(transform(db,bean))


def update_many(request, db, entity):
    body = json.loads(request.body)
    query = Query(body['query'])
    item  = body['item']
    dao = get_dao(db, entity)
    dao.update_many(query, item)
    return ValarResponse(True)

def delete_one(request, db, entity):
    body = json.loads(request.body)
    _id = body['id']
    dao = get_dao(db, entity)
    dao.delete_one(_id)
    return ValarResponse(True)

def delete_many(request, db, entity):
    body = json.loads(request.body)
    query = Query(body)
    dao = get_dao(db, entity)
    dao.delete_many(query)
    return ValarResponse(True)

def find_one(request, db, entity):
    body = json.loads(request.body)
    _id = body['id']
    dao = get_dao(db, entity)
    bean = dao.find_one(_id)
    return ValarResponse(transform(db,bean))

def find_many(request, db, entity):
    body = json.loads(request.body)
    query = Query(body)
    dao = get_dao(db, entity)
    page = body.get('page', 1)
    size = body.get('size', 0)
    code = body.get('code')
    results, total = dao.find_many(query, size, page)
    return ValarResponse({
        'results': transform(db, results, code),
        'total': total
    })

def meta(request, db, entity ):
    body = json.loads(request.body)
    code = body.get('code')
    dao = get_dao(db, entity)
    view = dao.meta(code)
    return ValarResponse(view)

