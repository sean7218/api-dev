//kbuilds,LLC

"use strict"

//Requires jQuery

var KbBlocks = (function(){
    //Main module
    var kb_blocks = {}

    //Static
    kb_blocks.HTTP_TYPE_GET = "GET"
    kb_blocks.HTTP_TYPE_POST = "POST"

    kb_blocks.HTTP_STATUS_OK = 200
    kb_blocks.HTTP_STATUS_NOT_FOUND = 404
    kb_blocks.HTTP_STATUS_BAD_REQUEST = 400
    kb_blocks.HTTP_STATUS_NOT_AUTHENTICATED = 401
    kb_blocks.HTTP_STATUSES = [
        kb_blocks.HTTP_STATUS_OK,
        kb_blocks.HTTP_STATUS_NOT_FOUND,
        kb_blocks.HTTP_STATUS_BAD_REQUEST,
        kb_blocks.HTTP_STATUS_NOT_AUTHENTICATED,
        ]
    kb_blocks.HTTP_NON_ERROR_STATUS_CODES = [
        kb_blocks.HTTP_STATUS_OK,
        kb_blocks.HTTP_STATUS_NOT_FOUND,
        kb_blocks.HTTP_STATUS_NOT_AUTHENTICATED,
        ]

    kb_blocks.page_id = null
    kb_blocks.state = null
    kb_blocks.tracker_list = null
    kb_blocks.errorFunction = null

    kb_blocks.blocks = {} //Keys are block_ids, values are blocks

    kb_blocks.request_registry = {}
    kb_blocks.request_count = 0

    kb_blocks.html_base_path = "/html"
    kb_blocks.block_loading_opacity = .5


    kb_blocks.updateBlock = function(block){
        //If not block state, assign it from the current state
        if (block.state === null){
            block.state = $.extend({},kb_blocks.state)
            }
        //Creates the block in the block registry
        kb_blocks.blocks[block.id] = block
        //Update the state obj
        kb_blocks.setState(block.state,false)
        }

    kb_blocks.changeState = function(state_change,push_state){
        var current_state = $.extend({},kb_blocks.state)
        var new_state = $.extend(current_state,state_change)
        kb_blocks.setState(new_state,push_state)
        }

    kb_blocks.setState = function(new_state,push_state){
        //Keep track if keys that have been changed so that we can update blocks that listen to the keys

        //Collect all keys that we care about
        var current_state = $.extend({},kb_blocks.state)
        var all_keys = []
        for (var key in new_state){
            if (all_keys.indexOf(key) > -1){
                continue
                }
            all_keys.push(key)
            }
        for (var key in current_state){
            if (all_keys.indexOf(key) > -1){
                continue
                }
            all_keys.push(key)
            }

        var changed_keys = []
        //Collect the keys that are different
        for (var index in all_keys){
            var key = all_keys[index]
            var current_value = kb_blocks.state[key]
            var new_value = new_state[key]
            if (current_value === new_value){
                continue
                }
            changed_keys.push(key)
            }

        kb_blocks.state = $.extend({},new_state)

        //Check to see if there are differences
        if (changed_keys.length > 0){
            //Update the url
            kb_blocks.setUrl(kb_blocks.state,push_state)
            //Update the links in the page
            kb_blocks.updateLinks()
            //Reload any blocks that need to be reloaded
            kb_blocks.reloadBlocks(changed_keys)
            }
        }

    kb_blocks.reloadBlocks = function(changed_keys){
        //Updates all blocks that need to be updated
        //Takes a list of state keys that have changed

        //Remove all blocks that are no longer in the DOM
        var new_blocks = {}
        for (var block_id in kb_blocks.blocks){
            var block = kb_blocks.blocks[block_id]
            var block_element = kb_blocks.getBlockElement(block)
            if (block_element.length){
                //This block is still in the DOM
                //Add it to the new_blocks
                new_blocks[block_id] = kb_blocks.blocks[block_id]
                }
            }
        kb_blocks.blocks = new_blocks
        
        //Gather blocks that need to be updated
        var reload_blocks = []
        for (var block_id in kb_blocks.blocks){
            var block = kb_blocks.blocks[block_id]
            for (var listener_index in block.listeners){
                var listener = block.listeners[listener_index]
                if (changed_keys.indexOf(listener) > -1){
                    //This block may need to be reloaded

                    //Blocks are expected to make sure that the state that they send back are up to date with the content in those blocks
                    //Blocks should not be reloaded, ever, if they are the one which introduced the change in state

                    //Check to make sure that the block's state is out of date
                    //Reload the block if the state is out of date
                    if (block.state[listener] != kb_blocks.state[listener]){
                        reload_blocks.push(block)
                        break
                        }
                    }
                }
            }

        //Remove blocks that will be updated within their parent
        var filtered_reload_blocks = []
        for (var index in reload_blocks){
            var block = reload_blocks[index]
            var block_element = kb_blocks.getBlockElement(block)
            var has_parent = false
            for (var parent_index in reload_blocks){
                var parent_block = reload_blocks[parent_index]
                //Check to see if the parent contains the block
                if (block_element.parents("#"+parent_block.id).length){
                    has_parent = true
                    break
                    }
                }
            if (!has_parent){
                //It has no parent
                //Add it to the filtered_reload_blocks
                filtered_reload_blocks.push(block)
                }
            }

        //Update the gathered blocks
        for (var index in filtered_reload_blocks){
            var block = filtered_reload_blocks[index]
            kb_blocks.callFunction(block)
            }
        }

    kb_blocks.callFunction = function(block,function_name,args){
        if (args === undefined){
            args = {}
            }

        //Start with html base
        var url = kb_blocks.html_base_path
        //Add the block name
        url += "/" + block.name
        //Add the block name if there is one given
        if (function_name !== undefined){
            url += "/" + function_name
            }
        //Add the get data from the state
        url += "?" + kb_blocks.makeUrl(kb_blocks.state)
        
        //Add the block id to the args
        args["kb_block_id"] = block.id

        kb_blocks.request(block,"POST",url,args)
        }

    kb_blocks.request = function(block,request_type,url,data){
        //Register the request
        var request_id = kb_blocks.registerRequest(block)
        
        //Add the block id to the request
        if (data instanceof FormData){
            data.append("kb_block_id",block.id)
            }
        else {
            data["kb_block_id"] = block.id
            }

        //Change the block to look like it's loading
        kb_blocks.setBlockLoadingOn(block)

        var ajax_obj = {
            type: request_type,
            url: url,
            data: data,
            error: kb_blocks.handleError,
            complete: function(jq_xhr){
                //Do nothing if there was a status that is not in HTTP_NON_ERROR_STATUS_CODES
                if (kb_blocks.HTTP_NON_ERROR_STATUS_CODES.indexOf(jq_xhr.status)=== -1){
                    return
                    }
                //Check to make sure that this is the response to the latest request
                if (!kb_blocks.checkRegisteredRequest(block,request_id)){
                    return
                    }
                kb_blocks.setHtml(block,jq_xhr.responseText)
                kb_blocks.setBlockLoadingOff(block)
                }
            }
        if (data instanceof FormData){
            ajax_obj.cache = false
            ajax_obj.contentType = false
            ajax_obj.processData = false
            }
        if (request_type === "POST"){
            var headers = ajax_obj.headers || {}
            headers["X-CSRFToken"] = kb_blocks.getCookie("csrftoken")
            ajax_obj.headers = headers
            }
        $.ajax(ajax_obj)
        }

    kb_blocks.registerRequest = function(block){
        kb_blocks.request_count += 1
        var request_id = kb_blocks.request_count
        kb_blocks.request_registry[block.id] = request_id
        return request_id
        }

    kb_blocks.checkRegisteredRequest = function(block,request_id){
        return kb_blocks.request_registry[block.id] === request_id
        }

    kb_blocks.getCookie = function(name){
        var cookie_value = null
        if (document.cookie && document.cookie !== ''){
            var cookies = document.cookie.split(';')
            for (var i = 0; i < cookies.length; i++){
                var cookie = jQuery.trim(cookies[i])
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookie_value;
        }

    kb_blocks.setHtml = function(block,html){
        if (!html){
            return
            }
        var block_element = kb_blocks.getBlockElement(block)
        block_element.html(html)
        //New HTML in the DOM
        //Update links
        kb_blocks.updateLinks()
        }

    kb_blocks.setBlockLoadingOn = function(block){
        }

    kb_blocks.setBlockLoadingOff = function(block){
        }

    kb_blocks.updateLinks = function(){
        //Assigns the proper anchor hrefs to all anchor tags in the page
        var anchor_tags = kb_blocks.getInternalElements("a")
        anchor_tags.each(function(index,element){
            var element = $(element)
            kb_blocks.setAnchorHref(element)
            })
        }

    kb_blocks.setAnchorHref = function(a){
        //Takes an <a> tag element
        //Sets its href value based on
        //state attribute
        //change attribute
        //remove attribute
        
        //Check the current href. Make sure that it needs to be modified
        var state_value = a.attr("state")
        var change_value = a.attr("change")
        var remove_value = a.attr("remove")

        if ((state_value !== undefined) ||
            (change_value !== undefined) ||
            (remove_value !== undefined)){
            //Need to adjust the href
            var state = $.extend({},kb_blocks.state)

            if (state_value !== undefined){
                state = kb_blocks.makeUrlObj(state_value)
                }
            else {
                if (change_value){
                    change_value = kb_blocks.makeUrlObj(change_value)
                    state = $.extend(state,change_value)
                    }
                if (remove_value){
                    remove_value = kb_blocks.makeUrlObj(remove_value)
                    for (var key in state){
                        if (key in remove_value){
                            delete state[key]
                            }
                        }
                    }
                }
            var url = kb_blocks.makeUrl(state)
            url = "/?"+url
            a.attr("href",url)

            return null
            }

        var function_name = a.attr("function")

        if (function_name){
            a.attr("href","#")
            return null
            }
        }


    kb_blocks.setUrl = function(data,push_state){
        if (push_state === undefined){
            push_state = true
            }

        var url = kb_blocks.makeUrl(data)
        url = "/?" + url
        var new_data = $.extend({},data)
        if (push_state){
            window.history.pushState(new_data,"",url)
            for (var index in kb_blocks.tracker_list){
                var tracker = kb_blocks.tracker_list[index]
                ga(tracker.name+'.set', 'page', url)
                ga(tracker.name+'.send', 'pageview')
                }
            }
        else {
            window.history.replaceState(new_data,"",url)
            }
        }

    kb_blocks.makeUrlObj = function(url){
        //Takes a url string and returns an object with the keys and values
        var url_list = url.split("&")
        if (!url_list[0]){
            return {}
            }
        var data = {}
        for (var index in url_list){
            var arg = url_list[index]
            var arg_split = arg.split("=")
            var value = arg_split[1]
            data[arg_split[0]] = value
            }
        return data
        }

    kb_blocks.makeUrl = function(obj){
        //Takes an obj and reutrns it represented as a url querystring
        var param_list = []
        for (var key in obj){
            var value = obj[key]
            if (value === undefined){
                value = null
                }
            if (value === null){
                continue
                }
            var param = key+"="+value
            param_list.push(param)
            }
        var url = param_list.join("&")
        return url
        }

    kb_blocks.getInternalElements = function(query){
        //Returns all matching elements, bound within the page element
        var results = $("#"+kb_blocks.page_id+" "+query)
        return results
        }

    kb_blocks.getBlockElement = function(block){
        return $("#"+block.id)
        }
        
    kb_blocks.getParentBlock = function(element){
        //Get the parent of the element
        element = $(element)
        var parent = element.parent()[0]
        if (!parent){
            return null
            }
        if (!parent.id){
            return kb_blocks.getParentBlock(parent)
            }
        if (parent.id in kb_blocks.blocks){
            return kb_blocks.blocks[parent.id]
            }
        return kb_blocks.getParentBlock(parent)
        }

    kb_blocks.initTrackers = function(){
        for (var index in kb_blocks.tracker_list){
            var tracker = kb_blocks.tracker_list[index]
            ga('create', tracker.id, 'auto', tracker.name);
            ga(tracker.name+'.send', 'pageview');
            }
        }

    kb_blocks.initClickHandler = function(){
        $("#"+kb_blocks.page_id).on("click","a",function(){
            var anchor_tag = this
            var a = $(anchor_tag)
            if (a.attr("change") === undefined &&
                a.attr("state") === undefined &&
                a.attr("remove") === undefined &&
                a.attr("function") === undefined) {
                //This is not a tag that we care about
                return
                }

            if (!a.attr("function")){
                //This link should modifiy the state

                //Read the url into an object
                if (!anchor_tag.search){
                    var new_state = {}
                    }
                else {
                    var search = anchor_tag.search
                    search = search.slice(1,search.length)
                    new_state = kb_blocks.makeUrlObj(search)
                    }
                kb_blocks.setState(new_state)
                }

            else {
                //This link should call a function
                //Get the block that contains this link
                var block = kb_blocks.getParentBlock(a)

                var function_full = a.attr("function")
                var split_function = function_full.split("?")
                var function_name = split_function[0]
                var function_args = split_function[1]
                if (function_args){
                    function_args = kb_blocks.makeUrlObj(function_args)
                    }
                else{
                    function_args = {}
                    }

                kb_blocks.callFunction(block,function_name,function_args)
                }

            return false
            })
        }

    kb_blocks.initBackButton = function(){
        window.onpopstate = function(e){
            var new_state = $.extend({},e.state)
            window.kb_blocks.setState(new_state,false)
            }
        }

    kb_blocks.handleError = function(jq_xhr,text_status,error_thrown){
        if (kb_blocks.HTTP_NON_ERROR_STATUS_CODES.indexOf(jq_xhr.status) === -1){
            kb_blocks.errorFunction(jq_xhr)
            }
        }

    kb_blocks.errorFunction = function(jq_xhr){
        alert("Something went wrong")
        }

    kb_blocks.assert = function(condition,exception_message){
        if (!condition){
            var error_message = "Assertion Error"
            if (exception_message !== undefined){
                error_message += ": "+exception_message
                }
            throw new Error(error_message)
            }
        }

    //Make sure that jQuery is present
    kb_blocks.assert(window.jQuery)

    //Constructor
    var init = function(page_id,
                        initial_state,
                        tracker_list){
        //Set up kb_blocks js
        kb_blocks.page_id = page_id
        kb_blocks.state = initial_state
        kb_blocks.tracker_list = tracker_list

        kb_blocks.updateLinks()
        kb_blocks.initClickHandler()
        kb_blocks.initBackButton()
        kb_blocks.initTrackers()

        window.kb_blocks = kb_blocks
        }

    return init
    })()
