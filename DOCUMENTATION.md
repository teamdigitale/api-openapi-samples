A draft API documentation template.

#### Documentation
    Write here the documentation. You can use markdown. This is an 
    informative section.

      * what does this API do?
      * who can use it?
      * why is useful?

    Include the following informations:
    
    
    ##### Subsections
    You can create subsections, with sense.

    #### Notes

    Use this section for further disclaimer respect to `termsOfService`.

    #### Technical informations and examples
    
    Brief technical informations. Remember that `description` does not 
    replace the technical documentation, but should ease the execution of
    the first requests.


    ##### Authentication
    Explain here how to apply for authentication (eg. mutual tls, api key, …) or reference the appropriate page. The `securityScheme` openapi
    section should be compiled accordingly.
    
    ##### Authorization
    Explain here the various authorization level for your api or reference
    the appropriate page

    ##### Rate Limits and Service Availability
    Add here rate-limits informations and or algorithm. Consider that
    rate-limit may apply per-user so you always have to check 
    the `X-RateLimit-*` headers. On fault you always have to return 429
    with the `Retry-After`.

    ##### Versioning
    Explain your versioning model here. 
    All APIs should use [Semantic Versioning](semver.org), but we don't 
    enforce either URL or media-type versioning. 
