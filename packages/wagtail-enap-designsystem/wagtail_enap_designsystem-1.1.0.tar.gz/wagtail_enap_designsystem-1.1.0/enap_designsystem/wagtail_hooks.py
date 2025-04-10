import os
from wagtail import hooks
from django.utils.html import format_html
from django.templatetags.static import static
from django.conf import settings


def static_exists(path):
	return os.path.exists(os.path.join(settings.STATIC_ROOT or '', path))


@hooks.register('insert_global_admin_css')
def global_admin_css():
	styles = []
	if static_exists('css/main_layout.css'):
		styles.append('<link rel="stylesheet" href="{}">'.format(static('css/main_layout.css')))
	if static_exists('css/mid_layout.css'):
		styles.append('<link rel="stylesheet" href="{}">'.format(static('css/mid_layout.css')))
	return format_html(''.join(styles))


@hooks.register('insert_global_admin_js')
def global_admin_js():
	scripts = []
	if static_exists('js/main_layout.js'):
		scripts.append('<script src="{}"></script>'.format(static('js/main_layout.js')))
	if static_exists('js/mid_layout.js'):
		scripts.append('<script src="{}"></script>'.format(static('js/mid_layout.js')))
	return format_html(''.join(scripts))
