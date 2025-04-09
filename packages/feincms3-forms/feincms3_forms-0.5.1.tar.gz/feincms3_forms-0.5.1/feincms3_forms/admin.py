from urllib.parse import quote as urlquote

from content_editor.admin import ContentEditor, ContentEditorInline
from django import forms
from django.contrib import messages
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


NO_CONTINUE_PARAMETERS = {"_addanother", "_save", "_saveasnew"}


class ConfiguredFormAdmin(ContentEditor):
    # Possible hook for validation, with stack hacking: _create_formsets

    def validate_configured_form(self, request, obj):
        opts = obj._meta
        obj_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_change",
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )
        if self.has_change_permission(request, obj):
            obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
        else:
            obj_repr = str(obj)

        if type := obj.type:
            if msgs := list(type.validate(obj)):
                messages.warning(
                    request,
                    format_html(
                        _('Validation of "{obj}" wasn\'t completely successful.'),
                        obj=obj_repr,
                    ),
                )
                for msg in msgs:
                    messages.add_message(request, msg.level, msg.message)
            else:
                messages.success(
                    request, format_html(_('"{obj}" has been validated.'), obj=obj_repr)
                )
        else:
            messages.warning(
                request,
                format_html(
                    _(
                        '"{obj}" could not be validated because'
                        " it seems to have an invalid type."
                    ),
                    obj=obj_repr,
                ),
            )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change=change)
        # Only validate if navigating away from this page. Otherwise validation
        # will happen in render_change_form anyway.
        if request.method == "POST" and any(
            key in request.POST for key in NO_CONTINUE_PARAMETERS
        ):
            self.validate_configured_form(request, form.instance)

    def render_change_form(self, request, context, *, obj, **kwargs):
        if obj and request.method == "GET":
            self.validate_configured_form(request, obj)
        return super().render_change_form(request, context, obj=obj, **kwargs)


class FormFieldInline(ContentEditorInline):
    core_fields = ["name", "label", "is_required"]
    advanced_fields = ["help_text"]

    def get_fieldsets(self, request, obj=None):
        return [
            (None, {"fields": self.core_fields + ["ordering", "region"]}),
            (_("Advanced"), {"fields": self.advanced_fields, "classes": ["collapse"]}),
        ]


class SimpleFieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.TYPE == self.instance.Type.SELECT:
            self["placeholder"].label = _("Empty choice label")


class SimpleFieldInline(FormFieldInline):
    form = SimpleFieldForm

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=self.model.TYPE)

    @classmethod
    def create(cls, model, **kwargs):
        type = model.Type
        if model.TYPE in {type.TEXT, type.TEXTAREA, type.EMAIL, type.URL}:
            kwargs.setdefault(
                "advanced_fields",
                ["help_text", "placeholder", "default_value", "max_length"],
            )

        elif model.TYPE in {type.DATE, type.INTEGER}:
            kwargs.setdefault(
                "advanced_fields", ["help_text", "placeholder", "default_value"]
            )

        elif model.TYPE in {type.CHECKBOX}:
            kwargs.setdefault("advanced_fields", ["help_text", "default_value"])

        elif model.TYPE in {type.SELECT}:
            kwargs.setdefault(
                "core_fields", ["name", "label", "is_required", "choices"]
            )
            kwargs.setdefault(
                "advanced_fields", ["help_text", "placeholder", "default_value"]
            )

        elif model.TYPE in {
            type.RADIO,
            type.SELECT_MULTIPLE,
            type.CHECKBOX_SELECT_MULTIPLE,
        }:
            kwargs.setdefault(
                "core_fields", ["name", "label", "is_required", "choices"]
            )
            kwargs.setdefault("advanced_fields", ["help_text", "default_value"])

        icons = {
            type.TEXT: "short_text",
            type.EMAIL: "alternate_email",
            type.URL: "link",
            type.DATE: "event",
            type.INTEGER: "looks_one",
            type.TEXTAREA: "notes",
            type.CHECKBOX: "check_box",
            type.SELECT: "arrow_drop_down_circle",
            type.RADIO: "radio_button_checked",
            type.SELECT_MULTIPLE: "check_box",
            type.CHECKBOX_SELECT_MULTIPLE: "check_box",
        }
        if icon := icons.get(model.TYPE):
            kwargs.setdefault("button", f'<span class="material-icons">{icon}</span>')

        return super().create(model, **kwargs)
