from django.contrib import admin


class ReadOnlyAdminMixin:
    def _get_link_fields(self):
        if not hasattr(self, 'link_fields') or not self.link_fields:
            return []
        return self.link_fields

    def _get_readonly_exception_fields(self, request, obj=None):
        return []

    def _must_be_readonly(self, request, obj=None):
        return True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return False
        return not self._must_be_readonly(request, obj)

    def get_fields_readonly_in_add(self, request, obj=None):
        return self.readonly_fields or []

    def get_readonly_fields(self, request, obj=None):
        def filter_fields(input_value):
            if not input_value:
                return []
            link_fields = self._get_link_fields()
            exception_fields = list(self._get_readonly_exception_fields(request, obj)) + list(
                self.get_exclude(request, obj) or [])
            result = []
            for field in input_value:
                field_str = field if isinstance(field, str) else field.name
                if field_str in link_fields or field_str in exception_fields:
                    continue
                result.append(field_str)
            return result or []

        if not obj:
            return self.get_fields_readonly_in_add(request, obj)
        if not self._must_be_readonly(request, obj):
            return self.readonly_fields or []
        return list(
            set(
                filter_fields(self.opts.local_fields) +
                filter_fields(self.opts.local_many_to_many) +
                filter_fields(self.readonly_fields or [])))


class AddForbiddenBaseAdminMixin:
    """Keep these permission mixins before BaseAdmin or its subclasses"""
    def has_add_permission(self, request, obj=None):
        return False


class DeleteForbiddenBaseAdminMixin:
    """Keep these permission mixins before BaseAdmin or its subclasses"""
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class NeitherAddNorDeleteAdmin(AddForbiddenBaseAdminMixin, DeleteForbiddenBaseAdminMixin,
                               admin.ModelAdmin):
    pass
