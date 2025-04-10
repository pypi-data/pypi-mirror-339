import datetime
from django.apps import apps
from django.core.paginator import Paginator
from django.db.models import Manager, QuerySet

from ..orm.detacher import detach_props, save_detached
from ..orm.meta_loader import load_meta, load_view, load_meta_field
from ..models import VModel
from ..query import Query


def load_model(entity=None):
    mapping = {}
    for mod in apps.get_models():
        if issubclass(mod, VModel):
            path, name = mod.__module__, mod.__name__
            print(path)
            app = path.replace('.models', '').replace('src.valar.','')
            key = '%s.%s' % (app, name)
            verbose_name = mod._meta.verbose_name
            mapping[key] = [mod, verbose_name]
    return mapping.get(entity) if entity else mapping

class OrmDao:
    def __init__(self, entity):
        self.entity = entity
        param = load_model(entity)
        if param is None:
            raise Exception('no entity named %s' % entity)
        self.model = param[0]
        self.name: str = param[1]
        self.manager: Manager = self.model.objects
        self.meta_fields = {}
        self.model_fields = {}
        for field in self.model._meta.get_fields():
            _field = load_meta_field(field)
            prop = _field['prop']
            self.model_fields[prop] = field
            self.meta_fields[prop] = _field


    def save_one(self, item):
        _item = detach_props(item, self.meta_fields.values())
        _id = item.get('id',0)
        query_set = self.manager.filter(id=_id)
        if len(query_set):
            del item['id']
            item['modify_time'] = datetime.datetime.now()
            query_set.update(**item)
            bean = query_set.first()
        else:
            bean = self.manager.create(**item)
            bean.sort = bean.id
            bean.save()
        save_detached(bean, _item, self.model_fields)
        return bean

    def update_many(self, query: Query, template):
        self.find_many(query).update(**template)

    def delete_one(self, _id):
        self.manager.filter(id=_id).delete()

    def delete_many(self, query: Query):
        self.find_many(query)[0].delete()

    def find_one(self, _id):
        return self.manager.filter(id=_id).first()

    def find_many(self, query: Query, size=0, page=1)->[QuerySet, int]:
        includes, excludes = query.orm_conditions()
        query_set = self.manager.filter(includes).exclude(excludes).order_by(*query.orm_orders())
        total = query_set.count()
        if size:
            paginator = Paginator(query_set, size)
            query_set = paginator.page(page).object_list
        return query_set, total


    def meta(self, code:str = 'default'):
        omit = [ 'sort', 'create_time', 'modify_time', 'saved']
        fields = [ self.meta_fields[prop] for prop in self.meta_fields if prop not in omit]
        view =  load_view(self.entity, code, self.name, fields)
        return load_meta(view)



