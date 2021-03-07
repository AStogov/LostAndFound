import json
import operator
from functools import reduce

from django.contrib import admin

# Register your models here.
from django.contrib.admin.utils import lookup_needs_distinct
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.utils.html import format_html

from item.models import Item, TYPE_DICT
from lib.client import rpc


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    def get_search_results(self, request, queryset, search_term):
        """
                Return a tuple containing a queryset to implement the search
                and a boolean indicating if the results may contain duplicates.
                """

        # Apply keyword searches.
        def remove_head(search_term):
            search_term = search_term[1:]
            id = 0
            for ch in search_term:
                if ch != ' ':
                    break
                id += 1
            search_term = search_term[id:]
            return search_term

        if len(search_term) > 1:
            if search_term[0] == '&':
                operator_fc = operator.and_
                search_term = remove_head(search_term)

            elif search_term[0] == '|':
                operator_fc = operator.or_
                search_term = remove_head(search_term)
            else:
                operator_fc = operator.or_

        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            # Use field_name if it includes a lookup.
            opts = queryset.model._meta
            lookup_fields = field_name.split(LOOKUP_SEP)
            # Go through the fields, following all relations.
            prev_field = None
            for path_part in lookup_fields:
                if path_part == 'pk':
                    path_part = opts.pk.name
                try:
                    field = opts.get_field(path_part)
                except FieldDoesNotExist:
                    # Use valid query lookups.
                    if prev_field and prev_field.get_lookup(path_part):
                        return field_name
                else:
                    prev_field = field
                    if hasattr(field, 'get_path_info'):
                        # Update opts to follow the relation.
                        opts = field.get_path_info()[-1].to_opts
            # Otherwise, use the field with icontains.
            return "%s__icontains" % field_name

        use_distinct = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator_fc, or_queries))
            use_distinct |= any(lookup_needs_distinct(self.opts, search_spec) for search_spec in orm_lookups)

        return queryset, use_distinct

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.categories = None

    def type2str(self, obj):
        return TYPE_DICT[obj.status]

    list_display = (
        'id',
        'openid',
        'type2str',
        'goods',
        'area',
        'address',
        'type',
        'time',
        'descr',
        'created_at',
        'visible',
        'qq',
        'phone',
        'wxid'
    )
    search_fields = ('id', 'openid', 'type', 'status', 'goods', 'area', 'address', 'time', 'descr', 'visible', 'name',
                     'phone', 'wxid')
