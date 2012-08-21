from pystache.context   import ContextStack
from pystache           import Renderer
from pyramid.path       import AssetResolver
from pyramid.i18n       import get_localizer
from pyramid.i18n       import TranslationStringFactory

import re

_ = TranslationStringFactory('pyramid_mustache')

class MustacheContextStack(ContextStack):
    """ Context stack that makes renderering match with mustache.js """

    def get_value(self, context, key):
        value = super(MustacheContextStack, self)._get_value(context, key)

        if value == None:
            return ''
        else:
            return value

class MustacheRendererFactory(object):
    def __init__(self, info):
        self.info = info

    def route_path(self, data):
        split_data = data.split(' ')
        name = split_data[0]

        kwargs = {}

        if len(split_data) > 1:
            arguments = split_data[1]

            kv_pairs = [x.strip().split('=') for x in arguments.split(',')]

            for key, value in kv_pairs:
                kwargs[key.strip()] = value.strip()

        return self.request.route_path(name, **kwargs)

    def translate(self, text):
        if self.request.localizer:
            localizer = self.request.localizer
        else:
            localizer = get_localizer(self.request)

        if self.request.translate:
            translate = self.request.translate
        else:
            translate = _

        translated = localizer.translate(translate(text))

        return translated

    def lorem_ipsum(self, number):
        lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Fusce nulla felis, semper id aliquam vel, condimentum sed libero.
        Sed volutpat iaculis pellentesque. Cras dui lectus, pretium vel 
        fermentum pretium, faucibus non tellus. Morbi semper auctor diam id 
        molestie. Maecenas aliquam aliquam ultricies. Nam ut turpis mi, 
        scelerisque aliquet odio. Proin in nulla a diam pretium ornare. Donec 
        ipsum justo, egestas ac semper non, blandit ac mauris. Nulla ultrices, 
        neque non egestas adipiscing, massa velit volutpat tellus, sit amet 
        fermentum tellus risus id quam. Vivamus hendrerit fringilla egestas. 
        Nunc sit amet arcu id erat interdum dictum vitae quis risus. Sed 
        porttitor dui vel elit pharetra ut hendrerit lorem ornare. Mauris id 
        augue augue, sit amet facilisis justo.
        """

        data = []
        for i in xrange(int(number.strip())):
            data.append(lorem)

        return "<br />".join(data)

    def render_template(self, name):
        full_path = AssetResolver(None).resolve(name).abspath()
        template_fh = open(full_path)
        template_stream = template_fh.read()
        template_fh.close()

        partials = {}

        if hasattr(self.request, 'mustache_partials'):
            partials = self.request.mustache_partials

#TODO: Get the patch merged and deployed to pypi so we can do this
#        renderer = Renderer(context_class=MustacheContextStack)
        renderer = Renderer(partials=partials)

        return renderer.render(template_stream, self.value, partials)

    def __call__(self, value, system):
        self.request = system['req']
        self.value = value

        value['_'] = self.translate
        value['lorem'] = self.lorem_ipsum
        value['route_path'] = self.route_path

        return self.render_template(self.info.name)


def extract_mustache(fileobj, keywords, comment_tags, options):
    """Extract messages from mustache files.
    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: a list of keywords (i.e. function names) that should
                     be recognized as translation functions
    :param comment_tags: a list of translator tags to search for and
                         include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``
    """
    tag_re = "\{\{\#_\}\}(.+)\{\{\/_\}\}"
    p = re.compile(tag_re, flags=re.DOTALL | re.MULTILINE)

    content = fileobj.read()

    final_matches = []

    for line_no, line in enumerate(content.split('\n')):
        matches = p.findall(line)
        for match in matches:
            final_matches.append((line_no, match))

    for line, text in final_matches:
        yield (line, '_', text, '')
