from django import template
register = template.Library()


@register.tag
def make_list(parser, token):
    bits = list(token.split_contents())
    if len(bits) >= 4 and bits[-2] == "as":
        varname = bits[-1]
        items = bits[1:-2]
        return make_list_none(items, varname)
    else:
        raise template.TemplateSyntaxError(
            "%r expected format is 'item [item ...] as varname'" % bits[0])


class make_list_none(template.Node):

    def __init__(self, items, varname):
        self.items = map(template.Variable, items)
        self.varname = varname

    def render(self, context):
        context[self.varname] = [i.resolve(context) for i in self.items]
        return ""


@register.inclusion_tag('breadcrumbs.html', takes_context=False)
def breadcrumbs(list):
    return {'list': list}
