from django.db.models import (ManyToOneRel, ForeignKey, ManyToManyRel, ManyToManyField, OneToOneField, CharField,
                              OneToOneRel, IntegerField, BooleanField, FloatField, FileField, JSONField, DateField,
                              TextField,DateTimeField, TimeField)

from ..orm.meta import field_props
from ..models import Meta, MetaView, VModel, MetaField





def __save_model(model):
    model.save()
    model.sort = model.id
    model.save()



def load_view(entity, code, name, fields):
    meta = Meta.objects.filter(entity=entity).first()
    if meta is None:
        meta = Meta(entity=entity, name=name)
        __save_model(meta)
    view = MetaView.objects.filter(meta__entity=entity, code=code).first()
    if view is None:
        view = MetaView(meta=meta, code=code, view_name=code.upper())
        __save_model(view)
    if view.metafield_set.count() == 0:
        t, p = field_props.get(entity, {}).get(code,('omit',[]))
        _fields = [f for f in fields if f['prop'] not in p] if t=='omit' else [f for f in fields if f['prop']  in p]
        for f in _fields:
            f['view'] = view
            field = MetaField.objects.create(**f)
            __save_model(field)
    return view

def load_meta(view):
    _view = view.full
    _meta = _view['meta']
    _fields = _view['metafield_set']
    clear_item(_view, 'meta_id', 'metafield', 'metafield_set', 'meta')
    _view['meta_name'] = _meta['name']
    _view['entity'] = _meta['entity']
    _view['fields'] = {}
    for _field in _fields:
        clear_item(_field, 'view_id')
        prop = _field['prop']
        _view['fields'][prop] = _field
    return _view



def clear_item(item, *keys):
    del item['saved']
    del item['sort']
    del item['id']
    del item['create_time']
    del item['modify_time']
    for key in keys:
        del item[key]



def get_refer(model, multiple = False):
    module, name = model.__module__, model.__name__
    entity = '%s.%s' % (module.replace('.models', '').split('.')[-1], name)
    return {
        "entity": entity,
        "value": "id", "label": 'name', "display": "id",
        "strict": False, "remote": False, "multiple": multiple,
        "includes": {}, "excludes": {}, "root": 0,
    }

def get_align(clazz):
    if clazz in [FloatField, IntegerField, ManyToManyRel, ManyToManyField, ManyToOneRel]:
        return 'right'
    elif clazz in [BooleanField,FileField,JSONField,DateField,DateTimeField,TimeField]:
        return 'center'
    return 'left'

def get_format(field):
    clazz = type(field)
    if clazz == CharField:
        return {'maxlength': field.max_length, "type": "text"}
    if clazz == TextField:
        return {'maxlength': None, "type": "textarea"}
    elif clazz == FloatField:
        return {'min': None, 'max': None, 'step': 1, 'precision': None, 'step_strictly': False}
    elif clazz == IntegerField:
        return {'min': None, 'max': None, 'step': 1, 'precision': 0, 'step_strictly': True}
    elif clazz == FileField:
        return {'max': 5, 'accept': "*", "width": "800px", "height": "auto", 'locked': False}
    else:
        return {}



def load_meta_field(field):
    clazz = type(field)
    if clazz in [ManyToOneRel, ManyToManyField, ManyToManyRel]:
        prop = field.name
        domain = clazz.__name__
        model: VModel= field.related_model
        label = model._meta.verbose_name
        refer = get_refer(model, True)
    elif clazz in [ForeignKey]:
        prop = field.name + "_id"
        domain = field.get_internal_type()
        model: VModel = field.related_model
        label = field.verbose_name
        refer = get_refer(model)
    elif clazz in [OneToOneRel, OneToOneField]:
        prop = field.name + "_id"
        domain = clazz.__name__
        model: VModel = field.related_model
        label = model._meta.verbose_name
        refer = get_refer(model)
    else:
        prop = field.name
        domain = field.get_internal_type()
        label = field.verbose_name
        refer = {}
    not_null = not field.null
    align = get_align(clazz)
    _format = get_format(field)
    return {
        "prop": prop,
        "label":label,
        "name":label,
        "domain":domain,
        "refer":refer,
        "format":_format,
        "not_null":not_null,
        "align":align,
    }
