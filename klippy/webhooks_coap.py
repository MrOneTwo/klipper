from libcoapy import CoapContext, CoapSession, CoapAsync, CoapResource, CoapPDURequest, CoapPDUResponse
import libcoapy.llapi as llapi
from util import jsonify_result


printer = None
webhooks = None
toolhead = None
bed_mesh = None

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

@jsonify_result
def toolhead_handler_print_time(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result['print_time']

@jsonify_result
def toolhead_handler_stalls(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result['stalls']

@jsonify_result
def toolhead_handler_estimated_print_time(resource, session, request, query, response):
    reactor = printer.get_reactor()

    result = toolhead.get_status(reactor.NOW)

    return result['estimated_print_time']


def coap_init_resources_bed_mesh(obj_printer, obj_bed_mesh):
    '''
    This function assumes webhooks object is already available.
    '''
    global webhooks
    global bed_mesh
    global printer
    webhooks = obj_printer.lookup_object('webhooks')
    bed_mesh = obj_bed_mesh
    printer = obj_printer

    path_root = "bed_mesh"

    if hasattr(bed_mesh, 'get_status'):
        webhooks.register_endpoint_read(f'{path_root}', bed_mesh_handler)
        webhooks.register_endpoint_read(f'{path_root}/profile_name', bed_mesh_handler_profile_name)
        webhooks.register_endpoint_read(f'{path_root}/mesh_min', bed_mesh_handler_mesh_min)
        webhooks.register_endpoint_read(f'{path_root}/mesh_max', bed_mesh_handler_mesh_max)
        webhooks.register_endpoint_read(f'{path_root}/profiles', bed_mesh_handler_profiles)

@jsonify_result
def bed_mesh_handler(resource, session, request, query, response):
    return bed_mesh.get_status(printer.get_reactor().NOW)

@jsonify_result
def bed_mesh_handler_profile_name(resource, session, request, query, response):
    result = bed_mesh.get_status(printer.get_reactor().NOW).get("profile_name", "")

    return result

@jsonify_result
def bed_mesh_handler_mesh_min(resource, session, request, query, response):
    result = bed_mesh.get_status(printer.get_reactor().NOW).get("mesh_min", None)

    return result

@jsonify_result
def bed_mesh_handler_mesh_max(resource, session, request, query, response):
    result = bed_mesh.get_status(printer.get_reactor().NOW).get("mesh_max", None)

    return result

@jsonify_result
def bed_mesh_handler_probed_matrix(resource, session, request, query, response):
    result = bed_mesh.get_status(printer.get_reactor().NOW).get("probed_matrix", [])

    return result

@jsonify_result
def bed_mesh_handler_mesh_matrix(resource, session, request, query, response):
    result = bed_mesh.get_status(printer.get_reactor().NOW).get("mesh_matrix", [])

    return result

@jsonify_result
def bed_mesh_handler_profiles(resource, session, request, query, response):
    which = None
    profile_data = None
    for el in query:
        if el.startswith('i='):
            try:
                which = int(el.split('=')[1])
                break
            except (IndexError, ValueError):
                response.code = llapi.coap_pdu_code_t.COAP_RESPONSE_CODE_BAD_REQUEST
                return None
        elif el.startswith('name='):
            try:
                which = el.split('=')[1]
                break
            except (IndexError, ValueError):
                response.code = llapi.coap_pdu_code_t.COAP_RESPONSE_CODE_BAD_REQUEST
                return None

    try:
        # profiles is a dictionary so it should be dereferenced by profile name.
        result = bed_mesh.get_status(printer.get_reactor().NOW)['profiles'][which]
    except (IndexError, KeyError):
        response.code = llapi.coap_pdu_code_t.COAP_RESPONSE_CODE_NOT_FOUND
        return None

    return result
