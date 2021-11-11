
#@app.errorhandler(404)
#def error_handler_api(e):
#    return redirect("https://error.redirect", code=302)
#
#@app.before_request
#def before_request_api():
#    session["start_time"] = time.time()
#
#@app.after_request
#def after_request_api(response):
#    start_time = session.get("start_time")
#    elapsed_time = time.time() - start_time
#
#    metadata = {}
#    for _key in REQUEST_KEYS:
#        metadata[_key] = str(getattr(request, _key))
#
#    metadata['elapsed_time'] = elapsed_time
#    metadata['status'] = response.status
#
#    if request.headers.has_key('Authorization'):
#        token = request.headers["Authorization"].split(',')[-1].split()[1]
#        stored_token = services.auth_service._get_token(token)
#        if stored_token != None:
#            decoded_token = jwt.decode(token,
#                                       stored_token['secret'],
#                                       stored_token['alg'])
#     
#            metadata['username'] = decoded_token['sub']
#
#    services.logging_service.register_request_log(metadata)
#
#    return response
