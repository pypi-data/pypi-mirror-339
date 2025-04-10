import json
import os.path
from io import BytesIO
from pathlib import Path
import urllib.parse

from nwebclient import util
from nwebclient import base as b
import base64
import uuid

class Img:
    CHIP = '/static/img/chip.png'
    CHART = '/static/img/chart.png'
    GIS = '/static/img/gis.png'
    TEST = '/static/img/test.png'
    DATA = '/static/img/data.png'
    APP = '/static/img/app.png'

class CSS:
    UL_MENU = 'nx_menu'

def ql(params, newps, remove_keys=[]) -> str:
    """
    :return: Query String z.B. "?a=42"
    """
    ps = {**params, **newps}
    for key in remove_keys:
        if key in ps:
            ps.pop(key)
    return '?' + urllib.parse.urlencode(ps)

def htmlentities(text):
    t = str(text)
    return t.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace('\'', '&#39;').replace('"', '&#34;')

def css_parse_dict(v: dict):
    res = ''
    for k, v in v.items():
        # TODO key anpassen aus margin_left margin-left
        res += k + ': ' + v + '; '
    return res


def tag(tag_name, content, **kw):
    a = ''
    if '_class' in kw:
        kw['class'] = kw['_class']
        kw.pop('_class', None)
    for k in kw.keys():
        if k == 'style' and isinstance(kw[k], dict):
            a += ' ' + k + '="' + css_parse_dict(kw[k]) + '"'
        else:
            a += ' ' + k + '="' + str(kw[k]) + '"'
    return '<'+tag_name+a+'>'+str(content)+'</'+tag_name+'>'


def a(content, href):
    if isinstance(href, str):
        return tag('a', content, href=href)
    else:
        return tag('a', content, **href)


def pre(content, **kw):
    return tag('pre', content, **kw)


def div(content, **kw):
    return tag('div', content, **kw)


def span(content, **kw):
    return tag('span', content, **kw)


def tt(content, **kw):
    return tag('tt', content, **kw)


def input(name, **attrs):
    attrs['name'] = name
    return tag('input', '', **attrs)


def hidden(name, val):
    return input(name, type='hidden', value=val)


def combo(name, values, **attrs):
    options = ''
    attrs['name'] = name
    if isinstance(values, list):
        for v in values:
            options += f'<option value="{v}">{v}</option>'
    elif isinstance(values, dict):
        for k, v in values.items():
            options += f'<option value="{v}">{k}</option>'
    return tag('select', options, **attrs)


def textarea(content, **kwargs):
    return tag('textarea', content, **kwargs)


def submit(title="Senden", **kwargs):
    return input(value=title, type='submit', **kwargs)


def script(js):
    if js.startswith('/') or js.startswith('http'):
        return '<script src="'+js+'"></script>'
    else:
        return f'<script>{js}</script>'


def img(src):
    return f'<img src="{src}" />'


def img_j64(binary_data):
    if isinstance(binary_data, BytesIO):
        binary_data = binary_data.getvalue()
    base64_utf8_str = base64.b64encode(binary_data).decode('utf-8')
    url = f'data:image/jpg;base64,{base64_utf8_str}'
    return img(url)


def table(content, **kw):
    s = '<table>'
    if isinstance(content, list):
        for rows in content:
            s += '<tr>'
            for cell in rows:
                s += '<td>'+str(cell)+'<td>'
            s += '</tr>'
    else:
        s += content
    s += '</table>'
    return s


def svg_inline(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            while len(lines) > 0:
                if lines[0].startswith('<svg'):
                    break
                lines.pop(0)
            return "\n".join(lines)
    else:
        return '<!-- NON EXISTING -->'


def js_ready(js):
    return 'document.addEventListener("DOMContentLoaded", function() { '+str(js)+' }, false);';


def js_fn(name, args, code=[]):
    if isinstance(code, str):
        body = code
    else:
        body = '\n'.join(code)
    return 'function '+name+'('+','.join(args)+') {\n'+body+'\n}\n\n'


def js_interval(t=1000, js='console.log("ping")'):
    return 'setInterval(function() { '+js+' }, '+str(t)+');'


def js_add_event_for_id(id, event_js):
    return 'document.getElementById("'+id+'").addEventListener("click", function(e) {\n '+event_js+' \n});\n'


def button_js(title:str, js_action, css_class=None):
    id = 'btn' + str(uuid.uuid4()).replace('-', '')
    jsa = 'document.getElementById("'+id+'").innerHTML = "Processing..."; '
    title = title.replace('"', "")
    jsa += 'setTimeout(function() { document.getElementById("'+id+'").innerHTML = "'+title+'"; }, 3000);'
    jsa += js_action
    js = js_ready(js_add_event_for_id(id, jsa))
    attr = ''
    if css_class is not None:
        attr += ' class="'+css_class+'"'
    res = '<button id="'+id+'"'+attr+'>'+str(title)+'</button><script type="text/javascript">'+js+'</script>'
    return res


def alert_error(msg=' '):
    m = str(msg)
    return f'<div style="border-left: #900 5px solid; background-color: #b77; color: #000;padding:4px;">{m}</div>'

def alert_success(msg=' '):
    m = str(msg)
    return f'<div style="border-left: #090 5px solid; background-color: #7b7; color: #000;padding:4px;">{m}</div>'

def alert_info(msg=' '):
    m = str(msg)
    return f'<div style="border-left: #009 5px solid; background-color: #77b; color: #000;padding:4px;">{m}</div>'


def js_base_url_exp():
    # (location.port==""?"":":"+location.port)+
    return 'location.protocol+"//"+location.host+"/"'


def route_root(web, root):
    web.add_url_rule('/pysys/root', 'r_root', view_func=lambda: root.getHtmlTree())
    res = NwFlaskRoutes()
    res.addTo(web)
    return res


class WebRoute(b.Base, b.WebPage):
    def __init__(self, route, name, func):
        self.route = route
        self.name = name
        self.func = func
    def page(self, params={}):
        return self.func()

def all_params():
    from flask import request
    requestdata = {**request.args.to_dict(), **request.form.to_dict()}
    for name in request.files.to_dict().keys():
        f = request.files[name]
        requestdata[name] = base64.b64encode(f.read())
    return requestdata

class NwFlaskRoutes(b.Base):
    """
        Definition on /nw und /nws
    """

    routes = {}

    routes_added = False

    def __init__(self, childs=[]):
        super().__init__()
        self.app = None
        for child in childs:
            self.addChild(child)

    def requestParams(self):
        from flask import request
        data = {}
        for tupel in request.files.items():
            name = tupel[0]
            f = tupel[1]
            #print(str(f))
            data[name] = base64.b64encode(f.read()).decode('ascii')
        params = {
            **request.cookies.to_dict(),
            **request.args.to_dict(), 
            **request.form.to_dict(),
            **data,
            **{'request_url': request.url}}
        return params
    def addTo(self, app):
        self.web = app
        if self.routes_added is True:
            return
        self.routes_added = True
        app.add_url_rule('/nw/<path:p>', 'nw', lambda p: self.nw(p), methods=['GET', 'POST'])
        app.add_url_rule('/nws/', 'nws', self.nws)
    def nws(self):
        p = b.Page().h1("Module")
        for e in b.Plugins('nweb_web'):
            p.div('<a href="{0}" title="Plugin">{1}</a>'.format('/nw/'+e.name, e.name))
        for e in self.childs():
            p.div('<a href="{0}" title="Object">{1}</a>'.format('/nw/' + e.name, e.name))
        return p.simple_page()

    def add_url_rule(self, route, name, view_func):
        print("Route" + route + " via add_url_rule")
        self.routes[route] = view_func
        self.addChild(WebRoute(route, name, view_func))

    def load_flask_blueprints(self, app):
        for e in b.Plugins('flask_blueprints'):
            blueprint = util.load_class(e)
            app.register_blueprint(blueprint)


    def nw(self, path):
        params = self.requestParams()
        n = path.split('/')[0]
        if self.hasName(n):
            return self.getChildByName(n).page(params)
        plugin = b.Plugins('nweb_web')[n]
        if plugin is not None:
            obj = util.load_class(plugin.value, create=True)
            w = self.addChild(b.WebObject(obj, {**{'path': path}, **params}))
            w.name = n
            return w.page(params)
        else:
            return "Error: 404 (NwFlaskRoutes)"

    def handleRoute(self, path, request):
        # add and serv via error404
        return "Route " + str(path), 200

    def error404(self):
        from flask import Flask, request
        if request.path in self.routes.keys():
            return self.handleRoute(request.path, request)
        else:
            status = 404
            return "Error: 404 Not Found, nwebclient.web:NwFlaskRoutes", status

    def create_app(self):
        from flask import Flask, request
        self.app = Flask(__name__)
        self.app.register_error_handler(404, lambda: self.error404())
        # @app.route('/')
        self.addTo(self.app)

    def serv(self, args={},  port=8080):
        self.create_app()
        self.run(port=port)

    def redirect_static(self):
        from flask import Flask, request, redirect
        route = '/static/<path:p>'
        self.app.add_url_rule(route, 'static', lambda p: redirect('https://bsnx.net' + request.path), methods=['GET', 'POST'])
        # AssertionError -> dann gibt es die static route schon

    def serv_dir(self, route, path):
        from flask import send_file
        e = route.replace('/', '')
        p = route + '<path:filename>'
        kwa = {}
        kwa['static_url_path'] = route
        kwa['static_folder'] = path
        #self.app.add_url_rule(p, endpoint=e, view_func=lambda **kwa: self.app.send_static_file(**kwa))  #
        self.app.add_url_rule(p, endpoint=e, view_func=lambda filename: send_file(path + filename))

    def run(self, app=None, port=8080):
        print('NwFlaskRoutes::run(...) in ' + os.getcwd())
        if app is not None:
            self.app = app
        kw = {}
        if os.path.isdir('../app'):  # Debug
            self.serv_dir('/app/', os.getcwd() + '/../app/')
        if os.path.isdir('../static'): # Debug
            self.serv_dir('/static/', os.getcwd()+'/../static/')
        elif os.path.isdir(str(Path.home() / "static")):
            self.serv_dir('/static/', str(Path.home() / "static") + '/')
        elif os.path.isdir(str(Path.home() / "dev" / "static")):
            self.serv_dir('/static/', str(Path.home() / "dev" / "static") + '/')
        elif os.path.isdir('/var/www/html/static'):
            # git@gitlab.com:bsalgert/static.git
            # https://gitlab.com/bsalgert/static.git
            # https://gitlab.com/bsalgert/static/-/archive/main/static-main.zip
            self.serv_dir('/static/', '/var/www/html/static/')
            #kwa = {}
            #kwa['static_url_path'] = '/static'
            #kwa['static_folder'] = '/var/www/html/static'
            #self.app.add_url_rule(f"/static/<path:filename>", endpoint="static", view_func=lambda **kwa: self.app.send_static_file(**kwa))  #
        else:
            self.redirect_static()
        self.app.run(host='0.0.0.0', port=int(port), **kw)




class LiteGraph:
    """

    """

    node_classes = []

    def __init__(self):
        from nwebclient import visual
        self.width = '1024'
        self.height = '768'
        self.visual = visual
        self.node_classes = []
        self.items = visual.Items()
        self.item_name = lambda item: item.name

    def create_custom_node(self, class_name, title):
        self.node_classes.append(class_name)
        res = 'function '+class_name+'() {'
        #    this.addInput("A", "number");
        #this.addInput("B", "number");
        #this.addOutput("A+B", "number");
        # this.addWidget("text", "Text", "edit me", function(v) {}, {} );
        #this.properties = {precision: 1};
        res += '}'

        # name to show
        res += class_name+'.title = "'+title+'";'

        # function to call when the node is executed
        res += class_name + '.prototype.onExecute = function() {}'

        # register in the system
        res += 'LiteGraph.registerNodeType("basic/nx", '+class_name+');'
        return res

    def create_node(self, name, node_type='basic/string', pos=(100, 100), size=(100, 150), value=None):
        res = 'var '+name+' = LiteGraph.createNode("'+node_type+'");'
        res += name+'.pos = ['+str(pos[0])+', '+str(pos[1])+'];'
        res += 'this.size = ['+str(size[0])+', '+str(size[1])+'];'
        res += 'graph.add('+name+');'
        if node_type == 'basic/const' and value is not None:
            res += name+'.setValue('+value+');'
        if node_type == 'basic/string' and value is not None:
            res += name+'.setValue("'+value+'");'
        return res

    def create_connection(self, name_a, name_b):
        return name_a + '.connect(0, '+name_b+', 0);'

    def head(self):
        return """
            <link rel="stylesheet" type="text/css" href="/static/js/litegraph.js/litegraph.css">
	        <script type="text/javascript" src="/static/js/litegraph.js/litegraph.js"></script>
        """

    def name_for(self, item):
        res = self.item_name(item)
        if res is None:
            res = 'id' + str(id(item)) # type(x).__name__
        return res

    def create_script(self):
        res = 'var graph = new LGraph(); var canvas = new LGraphCanvas("#graph", graph);'
        for item in self.items:
            name = self.name_for(item)
            res += self.create_node(name, pos=item.pos, value=name)
        res += 'graph.start();'
        return res

    def html(self):
        html = "<canvas id='graph' width='"+str(self.width)+"' height='"+str(self.height)+"' style='border: 1px solid'></canvas>"
        html += "<script>" + self.create_script() + "</script>"
        return html

    def add_to(self, p: b.Page):
        p.add_meta(self.head())
        p(self.html())


class Canvas:
    """
        @seealso php ...
    """

    def __init__(self):
        from nwebclient import visual
        self.visual = visual
        self.items = visual.Items()

    def add(self, elem):
        self.items.append(self.visual.Box(elem))

    def map_item(self, item):
        return div(div(str(item), _class="header")+div(''), _class="Canvas_Box")

    def head(self):
        return """
            <script src="/static/js/jquery/jquery-ui.js"></script>
            <link rel="stylesheet" type="text/css" href="/static/js/jquery/ui.css">
        """ + script(self.js())

    def js(self):
        return js_ready(
            '$(".Canvas_Box").draggable({ handle: ".header" });'
        )

    def html(self):
        return div("\n".join(map(self.map_item, self.items)), _class="python Canvas")

    def add_to(self, p: b.Page):
        p.add_meta(self.head())
        p(self.html())

class Grid:

    def __init__(self, rows, cols=[]):
        self.hid = 'grid_' + str(uuid.uuid4()).replace('-', '')
        self.rows = rows
        self.cols = cols

    @staticmethod
    def col(key, title=None, sortable=False, width=None, type=None):
        c = {'field': key}
        if title is not None:
            c['title'] = title
        if sortable is True:
            c['sortable'] = True
        if width is not None:
            c['width'] = width
        if type is not None:
            c['type'] = type
        return c

    def add_col(self, *args, **kwargs):
        c = self.col(*args, **kwargs)
        self.cols.append(c)

    def data_json_str(self):
        return json.dumps(self.rows)

    def config(self):
        return {
            'dataSource': self.rows,
            'columns':  self.cols,
            'pager': {'limit': 5}
        }

    def js(self):
        return "var grid = $('#"+self.hid+"').grid("+json.dumps(self.config())+");"

    def add_to(self, p: b.Page):
        p.script('/static/jquery.js')
        p.style('/static/js/gijgo/m.css')
        p.script('/static/js/gijgo/m.js')
        p(f'<table id="{self.hid}"></table>')
        p.js_ready(self.js())

