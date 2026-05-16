from libcoapy import CoapContext, CoapSession, CoapAsync, CoapResource, CoapPDURequest, CoapPDUResponse
import libcoapy.llapi as llapi
from util import jsonify_result


printer = None
webhooks = None
toolhead = None

def coap_init_resources_toolhead(obj_printer, obj_toolhead):
    '''
    This function assumes webhooks object is already available.
    '''
    global webhooks
    global toolhead
    global printer
    webhooks = obj_printer.lookup_object('webhooks')
    toolhead = obj_toolhead
    printer = obj_printer

    if hasattr(toolhead, 'get_status'):
        webhooks.register_endpoint_read('toolhead', toolhead_handler)
        webhooks.register_endpoint_read('toolhead/print_time', toolhead_handler_print_time)
        webhooks.register_endpoint_read('toolhead/stalls', toolhead_handler_stalls)
        webhooks.register_endpoint_read('toolhead/estimated_print_time', toolhead_handler_estimated_print_time)

@jsonify_result
def toolhead_handler(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result

def toolhead_handler_print_time(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result['print_time']

def toolhead_handler_stalls(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result['stalls']

def toolhead_handler_estimated_print_time(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result['estimated_print_time']
