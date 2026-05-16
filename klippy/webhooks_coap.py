from libcoapy import CoapContext, CoapSession, CoapAsync, CoapResource, CoapPDURequest, CoapPDUResponse
import libcoapy.llapi as llapi


#wh = self.printer.lookup_object('webhooks')

obj_toolhead = None

def coap_init_resources_toolhead(webhooks):
    global obj_toolhead
    obj_toolhead = self.printer.lookup_object('toolhead')

    webhooks.register_endpoint_read('toolhead', toolhead_handler)
    webhooks.register_endpoint_read('toolhead/print_time', toolhead_handler_print_time)
    webhooks.register_endpoint_read('toolhead/stalls', toolhead_handler_stalls)
    webhooks.register_endpoint_read('toolhead/estimated_print_time', toolhead_handler_estimated_print_time)

def toolhead_handler(resource, session, request, query, response):
    reactor = self.printer.get_reactor()

    if hasattr(obj_toolhead, 'get_status'):
        result = obj_toolhead.get_status(reactor.NOW)

    return result

def toolhead_handler_print_time(resource, session, request, query, response):
    reactor = self.printer.get_reactor()

    if hasattr(obj_toolhead, 'get_status'):
        result = obj_toolhead.get_status(reactor.NOW)

    return result['print_time']

def toolhead_handler_stalls(resource, session, request, query, response):
    reactor = self.printer.get_reactor()

    if hasattr(obj_toolhead, 'get_status'):
        result = obj_toolhead.get_status(reactor.NOW)

    return result['stalls']

def toolhead_handler_estimated_print_time(resource, session, request, query, response):
    reactor = self.printer.get_reactor()

    if hasattr(obj_toolhead, 'get_status'):
        result = obj_toolhead.get_status(reactor.NOW)

    return result['estimated_print_time']
