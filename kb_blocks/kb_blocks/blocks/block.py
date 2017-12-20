"""
kbuilds, LLC
"""


from ..common.serializer import KbBlocksSerializer
from ..common.deserializer import KbBlocksDeserializer

import django
from django.http import HttpResponse
from django.conf.urls import url
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.templatetags.static import get_static_prefix, get_media_prefix
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls import include
import base64

import markdown

import json
import string
import datetime
import decimal


class Block:

    #Options
    NAME = None
    AUTH = True
    #This block and all of its children will have this appended to the beginning of its name
    NAME_PREFIX = None

    CHILDREN = []
    FUNCTIONS = []
    LISTENERS = []

    TEMPLATE = None
    CONTAINER_TEMPLATE = "kb_blocks/block_container.html"
    SCRIPT_TEMPLATE = "kb_blocks/block_script.html"

    CSS_LIST = []
    JS_LIST = []

    SERIALIZER = KbBlocksSerializer()
    DESERIALIZER = KbBlocksDeserializer()


    #Types

    #HTTP methods

    HTTP_TYPE_GET = "GET"
    HTTP_TYPE_POST = "POST"
    HTTP_TYPES = [
        HTTP_TYPE_GET,
        HTTP_TYPE_POST,
        ]

    #HTTP statuses
    HTTP_STATUS_OK = 200
    HTTP_STATUS_NOT_FOUND = 404
    HTTP_STATUS_BAD_REQUEST = 400
    HTTP_STATUS_NOT_AUTHENTICATED = 401
    HTTP_STATUSES = [
        HTTP_STATUS_OK,
        HTTP_STATUS_NOT_FOUND,
        HTTP_STATUS_BAD_REQUEST,
        HTTP_STATUS_NOT_AUTHENTICATED,
        ]

    #Content types

    CONTENT_TYPE_HTML = "html"
    CONTENT_TYPE_JSON = "json"
    CONTENT_TYPES = [
        CONTENT_TYPE_HTML,
        CONTENT_TYPE_JSON,
        ]
    API_CONTENT_TYPES = [
        CONTENT_TYPE_JSON,
        ]

    #Exception types
    EXCEPTION_TYPE_USER = "user"
    EXCEPTION_TYPE_ARGUMENT = "argument"
    EXCEPTION_TYPE_NOT_AUTHENTICATED = "not_authenticated"
    EXCEPTION_TYPE_NOT_FOUND = "not_found"
    EXCEPTION_TYPES = [
        EXCEPTION_TYPE_USER,
        EXCEPTION_TYPE_ARGUMENT,
        EXCEPTION_TYPE_NOT_AUTHENTICATED,
        EXCEPTION_TYPE_NOT_FOUND,
        ]
    #Exception statuses
    EXCEPTION_STATUS_CODES = {
        EXCEPTION_TYPE_USER: HTTP_STATUS_OK,
        EXCEPTION_TYPE_ARGUMENT: HTTP_STATUS_BAD_REQUEST,
        EXCEPTION_TYPE_NOT_AUTHENTICATED: HTTP_STATUS_NOT_AUTHENTICATED,
        EXCEPTION_TYPE_NOT_FOUND: HTTP_STATUS_NOT_FOUND,
        }
    #Default exception messages
    EXCEPTION_MESSAGE_NOT_AUTHENTICATED = "user not authenticated in {block_name}"
    EXCEPTION_MESSAGE_NOT_FOUND = "not found in {block_name}"

    #Functions
    FUNCTION_NAME_GET = "get"


    def __init__(self,request=None,
                      parent_block=None,
                      content_type=CONTENT_TYPE_HTML):
        self.request = request
        self.parent_block = parent_block
        self.content_type = content_type

        self.child_index = 0
        self.kb_block_id = None
        self.content = None

    def __str__(self):
        if self.content is not None:
            return self.getContent()
        else:
            return super().__str__()


    #GETTERS

    def getNamePrefix(self):
        return self.NAME_PREFIX

    def getName(self):
        if self.NAME is not None:
            name = self.NAME
        else:
            name = self.__class__.__name__
        name = self.convertToUnderscoreCase(name)
        name_prefix = self.getNamePrefix()
        name_list = [name_prefix,name]
        name_list = [n for n in name_list if n is not None]
        name = "_".join(name_list)
        return name

    def getId(self):
        if self.kb_block_id is not None:
            return self.kb_block_id

        name = self.getName()

        if self.parent_block is None:
            return name

        parent_id = self.parent_block.getId()
        child_index = self.parent_block.getChildIndex()
        id = "__".join([parent_id,str(child_index),name])

        return id

    def getChildIndex(self):
        return self.child_index

    def getFunctions(self):
        if self.FUNCTION_NAME_GET in self.FUNCTIONS:
            raise Exception("'{0}' is a protected function. Please remove it from self.FUNCTIONS".format(self.FUNCTION_NAME_GET))
        return self.FUNCTIONS

    def getChildren(self):
        children = []
        for c in self.CHILDREN:
            if c in children:
                raise Exception("block, {0}, already a child of {1}".format(c,self.getName()))
            children.append(c)
        return children

    def getListeners(self):
        listeners = []
        for l in self.LISTENERS:
            if l in listeners:
                raise Exception("block, {0}, already has listener {1}".format(l,self.getName()))
            listeners.append(l)
        return listeners

    def getRequest(self):
        return self.request

    def getContentType(self):
        return self.content_type

    def getSelf(self):
        s = self
        s.id = self.getId()
        s.name = self.getName()
        return s

    def getContent(self):
        return self.content


    #SETTERS

    def addChild(self,child_block):
        if child_block in self.CHILDREN:
            return None
        self.CHILDREN = self.CHILDREN + [child_block]
        
    def addListener(self,listener):
        if listener in self.LISTENERS:
            return None
        self.LISTENERS = self.LISTENERS + [listener]

    def addFunction(self,function):
        if function in self.FUNCTIONS:
            return None
        self.FUNCTIONS = self.FUNCTIONS + [function]

    def addJs(self,js):
        if js in self.JS_LIST:
            return None
        self.JS_LIST = self.JS_LIST + [js]

    def addCss(self,css):
        if css in self.CSS_LIST:
            return None
        self.CSS_LIST = self.CSS_LIST + [css]


    #HTTP RESPONSE

    def getResponse(self,function_name):
        """
        The interface with the framework
        Takes a function name
        Distills request
        Executes proper function
        Serializes response data
        Renders response data (into template, json, etc)
        Returns http response
        """
        state,data,file_data = self.getRequestData()

        #Deserialize
        state = self.loadJsonValues(state)
        data = self.loadJsonValues(data)
        state = self.deserialize(state)
        data = self.deserialize(data)

        data.update(file_data)

        self.kb_block_id = data.pop("kb_block_id",None)

        context = {}
        status_code = self.HTTP_STATUS_OK
        exception = None
        exception_message = None

        try:
            context = self.getContext(state,data,function_name)

        except self.NotAuthenticatedException as e:
            #User is not authenticated
            exception = self.EXCEPTION_TYPE_NOT_AUTHENTICATED
            exception_message = e

        except self.NotFoundException as e:
            #Resource not found
            exception = self.EXCEPTION_TYPE_NOT_FOUND
            exception_message = e

        except self.ArgumentException as e:
            #The arguments passed to the a block were bad
            exception = self.EXCEPTION_TYPE_ARGUMENT
            exception_message = e

        except self.UserException as e:
            #The user entered something bad
            exception = self.EXCEPTION_TYPE_USER
            exception_message = e
            #Call the get function again to get the context
            context = self.getContext(state,data,None)

        #Add any exceptions to the context and state
        #Set the status code
        if exception is not None:
            context["exception"] = {exception: exception_message}
            status_code = self.EXCEPTION_STATUS_CODES[exception]
            if status_code != self.HTTP_STATUS_OK:
                state["exception"] = exception

        if exception_message is not None and self.getDebug():
            print(exception_message)

        #Check the context
        #If the context is not a dict, it should be returned directly
        if not isinstance(context,dict):
            return context

        #Render the content
        content = self.renderContent(state,context)
        self.content = content

        content_type = self.getContentType()

        if content_type in self.API_CONTENT_TYPES:
            content = self.SERIALIZER.serialize(content)

        if content_type == self.CONTENT_TYPE_JSON:
            content = json.dumps(content)

        #Pack the content
        #Get the response
        response = self.getHttpResponse(content)
        #Set the status code
        response = self.setHttpStatusCode(response,status_code)

        return response

    def render(self,state,data):
        context = self.getContext(state,data,None)
        self.content = self.renderContent(None,context)

        if self.getContentType() not in self.API_CONTENT_TYPES:
            self.content = self.renderContainer(self.content)

        return None
        

    #Content

    def renderContent(self,state,context):
        """
        Takes state and context
        Renders the context into the template
        Returns json or html
        """
        if not isinstance(context,dict):
            raise Exception("context in {0} was not a dict".format(self.getName()))

        content_type = self.getContentType()

        if content_type == self.CONTENT_TYPE_HTML:
            #Check to make sure that a template is defined
            if self.TEMPLATE is None:
                raise Exception("{0} does not define self.TEMPLATE".format(self.getName()))

            #Render to TEMPLATE
            context["self"] = self.getSelf()
            content = self.renderTemplate(self.TEMPLATE,context)
            content = self.renderScript(state,content)
            content = self.makeTemplateSafe(content)

        else:
            content = context

        return content

    def renderScript(self,state,content):
        """
        Renders kb_blocks functions calls in a script tag above the content
        Script is placed above the content so that the js references can be manipulated from any scripts in the content
        """
        listeners = self.makeTemplateSafe(json.dumps(self.getListeners()))
        if state is None:
            string_state = None
        else:
            string_state = {key:str(value) for key,value in state.items()}
        state = self.makeTemplateSafe(json.dumps(string_state))
        csrf_token = self.getCsrfToken()

        script_context = {
            "self": self.getSelf(),
            "content": content,
            "listeners": listeners,
            "state": state,
            "csrf_token": csrf_token,
            }
        content = self.renderTemplate(self.SCRIPT_TEMPLATE,
                                      script_context)
        return content

    def renderContainer(self,content):
        """
        Renders div container around content
        """
        container_context = {
            "self": self.getSelf(),
            "content": content,
            }
        content = self.renderTemplate(self.CONTAINER_TEMPLATE,
                                      container_context)
        return content


    #Execution

    def getContext(self,state,data,function_name):
        """
        Checks auth
        Gets the functon that needs to be called
        Calls the function using state and data
        If function returns something, such as a context or Redirect object, it is returned, otherwise the self.get() function is called and the context from that is returned
        """
        #Make sure that the user is authenticated and allowed to see this content
        self.checkAuth(state,data)

        #Call function is the function that needs to be called before the read function
        call_function = self.getCallFunction(function_name)

        if call_function is not None:
            call_result = call_function(state,data)
        else:
            call_result = None

        if call_result is not None:
            return call_result

        #Call the get function
        context = self.get(state,data)

        return context

    
    def getCallFunction(self,function_name):
        """
        Returns the function pointer of the with the name `function_name`
        Returns None if function name is None
        Raises Exception if block does not have the given function name
        """
        if function_name is None:
            return None

        if function_name not in self.getFunctions():
            raise Exception("block, {0}, does not have '{1}' in self.FUNCTIONS".format(self.getName(),
                                                                                       function_name))

        function = getattr(self,function_name,None)
        if function is None:
            raise Exception("block, {0}, does not have a function called {1}".format(self.getName(),
                                                                                     function_name))
        return function


    #Security

    def checkAuth(self,state,data):
        """
        Returns None if the block does not require auth
        Gets the user
        Checks to see if the user is authenticated
        Checks to see if the user is authroized
        Raises NotAuthenticatedException if the user is not authenticated
        Raises NotFoundException if the user is not authorized
        """
        if not self.AUTH:
            return None

        #Check that user is logged in
        user = self.getUser()
        if user is None:
            raise self.NotAuthenticatedException(self.EXCEPTION_MESSAGE_NOT_AUTHENTICATED.format(block_name=self.getName()))

        content_type = self.getContentType()

        if content_type in self.API_CONTENT_TYPES:
            authenticated = self.checkUserBasicHttpAuth(user)
        else:
            authenticated = self.checkUserAuthenticated(user)

        if not authenticated:
            raise self.NotAuthenticatedException(self.EXCEPTION_MESSAGE_NOT_AUTHENTICATED.format(block_name=self.getName()))

        #Check that the user is allowed to see this block
        authorized = self.authorize(state,data)
        if not authorized:
            raise self.NotFoundException(self.EXCEPTION_MESSAGE_NOT_FOUND.format(block_name=self.getName()))


    #Exposed functions

    def get(self,state,data):
        return {}

    def authorize(self,state,data):
        """
        Developer can determine whether or not the user is authorized
        """
        return True

    def getDocs(self,state,data):
        context = {
            "functions": self.FUNCTIONS,
            }
        return context


    #User helpers

    def initBlock(self,child_block):
        """
        Shortcut for developer to get a block instance that is ready to be rendered
        """
        if not issubclass(child_block,Block):
            raise Exception("'{0}' is not a block".format(child_block))
        if child_block not in self.getChildren():
            raise Exception("'{0}' not a child of block, '{1}'".format(child_block,
                                                                       self.getName()))

        request = self.getRequest()
        content_type = self.getContentType()

        block = child_block(request=request,
                            parent_block=self,
                            content_type=content_type)

        self.child_index += 1

        return block

    def renderBlock(self,block,state,data):
        block = self.initBlock(block)
        block.render(state,data)
        return block

    def getMarkdown(self,text):
        html = markdown.markdown(text)
        html = self.makeTemplateSafe(html)
        return html

    
    #Init helpers

    def getRoutes(self):
        routes = []

        #Make the routes for this block
        name = self.getName()
        for content_type in self.CONTENT_TYPES:
            #Get the default route
            path = "{0}/{1}$".format(content_type,name)
            view_function = self.getView(content_type,None)
            if content_type != self.CONTENT_TYPE_HTML:
                view_function = self.makeViewCsrfExempt(view_function)
            route = self.getRoute(path,view_function)
            routes.append(route)

            for function_name in self.getFunctions():
                path = "{0}/{1}/{2}$".format(content_type,name,function_name)
                view_function = self.getView(content_type,function_name)
                if content_type != self.CONTENT_TYPE_HTML:
                    view_function = self.makeViewCsrfExempt(view_function)
                route = self.getRoute(path,view_function)
                routes.append(route)

        #Make the routes for the children of this block
        for child in self.getChildren():
            child = self.initBlock(child)
            child.NAME_PREFIX = self.NAME_PREFIX
            routes += child.getRoutes()

        return routes

    def getCssList(self):
        css_list = [css for css in self.CSS_LIST]

        for child in self.getChildren():
            child = self.initBlock(child)
            css_list += child.getCssList()

        return self.getUniqueList(css_list)

    def getJsList(self):
        js_list = [js for js in self.JS_LIST]

        for child in self.getChildren():
            child = self.initBlock(child)
            js_list += child.getJsList()

        return self.getUniqueList(js_list)


    #Data methods

    def serialize(self,obj):
        return self.SERIALIZER.serialize(obj)

    def deserialize(self,obj):
        return self.DESERIALIZER.deserialize(obj)

    def loadJsonValues(self,d):
        """
        Takes a dict
        Tries to load each value as a json object
        """
        for key,value in d.items():
            try:
                value = json.loads(value)
            except (ValueError, TypeError):
                pass
            d[key] = value
        return d


    #Internal helpers
    #TODO: move to KBDE

    def getUrl(self,data):
        """
        Takes a dictionary
        Returns a url querystring
        """
        arg_list = ["{0}={1}".format(key,data[key]) for key in data]
        url = "&".join(arg_list)
        return url

    def getUniqueList(self,l):
        """
        Returns a version of list
        Preserves order of items
        """
        unique_list = []
        for item in l:
            if item in unique_list:
                continue
            unique_list.append(item)

        return unique_list

    def convertToUnderscoreCase(self,string):
        new_string = ""
        string_len = len(string)
        for index,char in enumerate(string):

            if index < string_len - 1:
                #We are not on the last string
                next_char = string[index+1]
            else:
                next_char = None

            converted = False

            if char.isupper():
                char = char.lower()
                converted = True

            if char.isdigit() and \
               next_char is not None and \
               not next_char.isdigit():
                converted = True

            if converted and new_string:
                char = "_" + char

            new_string += char

        return new_string

    def getFunctionArgSpec(self,function):
        return inspect.getfullargspec(function) 

    #Exceptions

    class UserException(Exception):
        """
        Issues caused by user interactions
        """
        pass

    class ArgumentException(Exception):
        """
        Issues caused by the worng arguments being provided
        """
        pass

    class NotFoundException(Exception):
        """
        We looked for it, and it wasn't there
        """
        pass

    class NotAuthenticatedException(Exception):
        """
        Exceptions caused by not knowing who the user is
        """
        pass


    #Framework-specific functions

    def getHttpResponse(self,content):
        """
        Takes the content
        Returns the framework-specific http response object
        """
        return HttpResponse(content)

    def setHttpStatusCode(self,http_response,status_code):
        http_response.status_code = status_code
        return http_response

    def getHttpMethod(self):
        """
        Returns a string, representing the request type
        Examples: POST, GET, PUT, DELETE
        """
        request = self.getRequest()
        return request.method

    def renderTemplate(self,template_path,context):
        """
        Takes template_path, and context
        returns rendered html, with the context rendered into the template
        """
        html = render_to_string(template_path,context)
        return html

    def getRequestData(self):
        """
        Distills the request parameters into state, data, and other_data
        state should contain all GET parameters in the request
        data should contain all deserializable data from the request body
        other_data should contain all non-deserializable data, such as files and images
        returns state, data, other_data
        """
        request = self.getRequest()

        get = request.GET
        state = {key:get[key] for key in get}

        post = request.POST
        data = {key:post[key] for key in post}

        files = request.FILES
        file_data = {key:files[key] for key in files}

        return state,data,file_data

    def getUser(self):
        """
        Returns a user object
        """
        username = self.getBasicHttpUsername()
        if username is not None:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                pass
        return self.getRequest().user

    def checkUserAuthenticated(self,user):
        """
        Takes a user object
        Returns True/False representing if the user is authenticated
        """
        return user.is_authenticated()

    def checkUserBasicHttpAuth(self):
        """
        Returns True/False representing if the user is authenticated via BasicHttpAuth
        """
        username = self.getBasicHttpUsername()
        if username is None:
            return False
        password = self.getBasicHttpPassword()
        user = authenticate(username=username,password=password)
        if user is None:
            return False
        return True

    def getRoute(self,path,view_function_ptr,**kwargs):
        """
        Takes a path string and a function pointer to the view function
        Makes a route from path to view_function_ptr, and returns it
        """
        regex = r"^{0}".format(path)
        route = url(regex,view_function_ptr,kwargs)
        return route

    def makeViewCsrfExempt(self,view):
        """
        Returns the view after being made CSRF-exempt
        """
        return csrf_exempt(view)

    def getView(self,content_type,function_name):
        """
        Defines a view function for the framework being used
        returns a pointer to that view function
        """
        def view(request):
            block = type(self)(request=request,
                               parent_block=None,
                               content_type=content_type)
            return block.getResponse(function_name)
        return view

    def getBasicHttpUsername(self):
        result = self.getBasicHttpAuthenticationData()
        if result is None:
            return None
        else:
            return result[0]

    def getBasicHttpPassword(self):
        result = self.getBasicHttpAuthenticationData()
        if result is None:
            return None
        else:
            return result[1]

    def makeTemplateSafe(self,string):
        """
        Returns a string that can be placed into a template without being escaped
        """
        return mark_safe(string)

    def getCsrfToken(self):
        """
        Returns a valid csrf token
        """
        request = self.getRequest()
        return django.middleware.csrf.get_token(request)

    def getDebug(self):
        """
        Returns True or False depending on whether or not the server is running in debug mode
        """
        return settings.DEBUG

    def getAdminView(self):
        """
        Returns the view for the admin panel
        """
        return include(admin.site.urls)

    def getAdminUrl(self):
        """
        Gets the admin url from the settings
        If not found, return None
        """
        if hasattr(settings,"ADMIN_URL"):
            return settings.ADMIN_URL

    def getMediaView(self):
        return serve

    def getMediaRoot(self):
        """
        Gets the media root
        Meda root is the location on the server at which meda files are kept
        If not found, return None
        """
        if hasattr(settings,"MEDIA_ROOT"):
            return settings.MEDIA_ROOT

    def getMediaUrl(self):
        """
        Gets the media url
        Meda url is the url beginning that will route to the media files
        If not found, return None
        """
        if hasattr(settings,"MEDIA_URL"):
            return settings.MEDIA_URL

    def getStaticUrl(self):
        if hasattr(settings,"STATIC_URL"):
            return settings.STATIC_URL

    #Framework-specific helpers

    def getBasicHttpAuthenticationData(self):
        """
        returns the username and password required for BasicHttpAuth
        not part of the API; this is a helper
        """
        request = self.getRequest()
        if "HTTP_AUTHORIZATION" not in request.META:
            return None

        auth = request.META["HTTP_AUTHORIZATION"].split()
        if len(auth) != 2:
            return None

        if auth[0].lower() != "basic":
            return None

        auth = base64.b64decode(auth[1])
        auth = auth.decode("utf-8")
        username, password = auth.split(':', 1)
        return username, password
