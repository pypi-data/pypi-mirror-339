mf_common = ['prop','name','domain']

field_props = {
    'data.Meta': {
        'default': ('pick', ['entity','name']),
    },
    'data.MetaView': {
        'list': ('pick', ['meta_id','code','view_name']),
        'control':('omit', ['name','meta_id', 'code', 'view_name', 'metafield'])
    },
    'data.MetaField': {
        'tool': ('pick',[*mf_common,'tool','refer','format']),
        'rest': ('pick',[*mf_common,'not_null','read_only','unit','sortable','allow_search','allow_download','allow_upload','allow_update']),
        'table': ('pick',[*mf_common,'column_width','fixed','align','edit_on_table','hide_on_table','header_color','cell_color']),
        'form': ('pick',[*mf_common,'hide_on_form','hide_on_form_insert','hide_on_form_edit','hide_on_form_branch','hide_on_form_leaf','span']),
    }
}


field_default = {
    'data.MetaField':{

    }
}