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
        url_rule = request.url_rule.rule
        apis_keys = [a[1:] for a in apis.keys()]
        url_rule_splitted = [a for a in url_rule.split("/") if a in apis_keys]
        blueprint = url_rule_splitted[-1]
        blueprint = "/" + blueprint

        controller_function = apis[blueprint].functions[url_rule]
        res, status = controller_function(args, kwargs, request=request)

    except Exception as exc:
        # TODO: log error
        print(exc)

        res['error'] = True
        status = 400

    return res, status
