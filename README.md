# Djinns ジン

*Djinss* is a tool in which you specify your API and, magically, you can go straight to implementing the business logic for your endpoints.

This might be useful for you because you can save time with coding and documentation as the API is specified.

This project is a wrapper around the [Flask](https://github.com/pallets/flask) that has automations for code and docs generation.

# Quickstart

1. Change the `api_spec.json` and the `apis/` folder with the definition of the endpoints/paths of your API.
2. Create your application code and invoke the Djinns as explained in the snippet below.

```
from djinns.main import Djinns


djinns = Djinns(apispec_file="api_spec.json")
djinns.invoke()
```

Obs: You can change the `entrypoint.py` code with your own procedure. The changes will be applied to all endpoints, like provides a database object for API controller functions.

# TODO

1. Implement documentation generation from **api_spec.json** file.
