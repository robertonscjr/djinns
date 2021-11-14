from flask import request


def view_function(*args, **kwargs):
    """
        This function is the entrypoint for all requests
        and it forwards the processing for the right API path.

        You can change the behavior according to your needs.
        For example: you can create a database object and pass it
        as a parameter to the API controller function
    """

    res = {}
    status = 200

    try:
        from apis import apis
        import pdb; pdb.set_trace()
        url_rule = request.url_rule.rule
        blueprint = "/{}".format(request.blueprint.split("/")[-1])
        controller_function = apis[blueprint].functions[url_rule]
        res, status = controller_function(args, kwargs, request=request)

    except Exception as exc:
        # TODO: log error

        res['error'] = True
        status = 400

    return res, status
