# Messaggi d'errore in JSON: lo standard rfc7807

In un sistema fortemente integrato come quello delle PA è utile avere una gestione degli errori uniforme.

Per le comunicazioni basate su JSON esiste [RFC7807](https://tools.ietf.org/html/rfc7807), che struttura i messaggi di errore con:

  - un campo obbligatorio (title)
  - una serie di campi opzionali (type, detail, status, instance)
  - ulteriori campi personalizzati, che possono essere aggiunti

```
    HTTP/1.1 500 Internal Error
    Content-Type: application/problem+json

    {
    "title": "Internal Server Error"
    "type": "http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html",
    "detail": "Status failed validation",
    "status": 500,
    }
```

Quando specificato, il campo `type` punta a una pagina che spiega l'errore: possiamo quindi referenziare la documentazione della piattaforma e velocizzare le iterazioni di sviluppo riportando  l'utente ad una fonte autoritativa per la gestione degli errori.

Un messaggio di errore[ deve sempre essere associato ad un http status descrittivo](http://zalando.github.io/restful-api-guidelines/index.html#150) (eg. 4xx o 5xx). Se c'è un errore non andrebbe mai restituito lo status 200.

Json+problem permette di indicare lo `status` HTTP. Questo permette di passare lo stato nella catena di trasmissione (eg. all'applicazione client).

Aggiungendo ulteriori campi possiamo descrivere meglio l'errore: in tal caso andrebbe documentato ulteriormente il comportamento dell'oggetto.

```
    HTTP/1.1 413 Payload Too Large
    Content-Type: application/problem+json

    {
    "title": "Payload Too Large"
    "type": "https://httpstatuses.com/413",
    "detail": "Request payload was larger than 1MB. See payload_size.",
    "status": 413,
    "payload_size": 10241024,
    }
```

Riferimenti:

  - https://tools.ietf.org/html/rfc7807
  - https://adidas-group.gitbooks.io/api-guidelines/content/message/error-reporting.html
  - http://zalando.github.io/restful-api-guidelines/index.html#176
