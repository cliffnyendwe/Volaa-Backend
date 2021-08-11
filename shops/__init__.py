
import re

from django.template.defaultfilters import slugify


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    slug_field = instance._meta.get_field(slug_field_name)

    slug_len = slug_field.max_length

    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]  # limit its len to max_length of slug field
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    if not queryset:
        queryset = instance.__class__.objects.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '-%s' % next
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator=None):
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        value = re.sub('%s+' % re_sep, separator, value)
    return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '',
                  value)  # removes the separator from the ned or start of the string
