# DRAFT: How to conform API specs?

To conform your API to the specs, just start creating
an openapi-v3 specification file.

## Expose OpenAPI v3 specs

### If you don't use swagger

Check the API samples and write your own specs.

### If you use swagger

Add as much informations as possible to swagger v2 specs, and we'll convert to v3 after
with swaggerhub or mermade.

```
https://mermade.org.uk/api/v1/convert?url=$YOUR_SWAGGER_URL
```

### Required informations

We expect every API specifies

```
info:
  version: "0.0.1"
  title: |
    Just an API
  description: |
    A short description of the application.
    [CommonMark](http://spec.commonmark.org/) syntax
    *MAY* be used for rich text representation.

    The `x-api-id` MUST be an [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier).
  termsOfService: 'https://en.wikipedia.org/wiki/Terms_of_service'
  contact:
    email: robipolli@gmail.com
    name: Roberto Polli
    url: 'https://twitter.com/ioggstream'
  x-audience: |
    Definire qui l'audience delle API
  x-api-id: b9ec7026-5da5-4db6-a959-fce72db5de64
  license:
    name: Apache 2.0
    url: 'http://www.apache.org/licenses/LICENSE-2.0.html'

```

## Use Problem.Json for errors

Every error should be packed in a [RFC7807](https://tools.ietf.org/html/rfc7807) object

The schema is defined here https://teamdigitale.github.io/openapi/schemas/problem.yaml
and can be referenced directly by your API. Eg.

```
components:
  schemas:
    Problem:
      $ref: 'https://teamdigitale.github.io/openapi/schemas/problem.yaml#Problem'

```

## Throttle clients

Your API should throttle clients always returning the following headers.

```
  headers:
    # Headers conform to http://zalando.github.io/restful-api-guidelines/index.html#132
    X-RateLimit-Limit:
      $ref: 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Limit'
    X-RateLimit-Remaining:
      $ref: 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Remaining'
    X-RateLimit-Reset:
      $ref: 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Reset'

```

You can use the pre-built responses in errors.

```
# https://teamdigitale.github.io/openapi/responses/v3.yaml#/429TooManyRequests
429TooManyRequests:
  description: Too many requests
  headers:
    X-RateLimit-Limit:
      $ref: 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Limit'
    X-RateLimit-Remaining:
      $ref: 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Remaining'
    X-RateLimit-Reset:
      $ref: 'https://teamdigitale.github.io/openapi/headers/v3.yaml#/X-RateLimit-Reset'
  content:
    application/problem+json:
      schema:
        $ref: 'https://teamdigitale.github.io/openapi/schemas/problem.yaml#Problem'

```



