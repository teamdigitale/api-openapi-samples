Un ecosistema API porta ad integrare fortemente sistemi server e client.
Per gestire i problemi ed evitare [fallimenti a cascata ](http://landing.google.com/sre/book/chapters/addressing-cascading-failures.html) bisogna scambiare informazioni stato dei servizi ed il carico supportato.

Esempio - Caso di sovraccarico: cittadino -&gt; banca -&gt; servizio di pagamento -&gt; comune

* Un cittadino vuole pagare la TARI tramite home-banking
* la banca si interfaccia con un servizio di pagamento che contatta il comune
* il comune espone un’API per il pagamento della TARI comunale
* nel giorno di scadenza della TARI, l’endpoint del comune va’ in sovraccarico e non riesce a gestire tutte le richieste:
  * parte delle richieste andranno in errore
  * altre supereranno il timeout impostato dal servizio di pagamento e/o dal sito della banca
  * una piccola parte verrà servita nei tempi stabiliti

**Vanno fatti quindi dei piani di emergenza per gestire le situazioni di errore e/o sovraccarico.**

Il protocollo HTTP mette a disposizione due strumenti semplici e potenti:

* gli stati di errore **[429 (too many requests) ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429)** e **[503 (service unavailable)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/503)**
* gli header **Retry-After** ed **X-RateLimit-** *

Per segnalare le politiche di throttling basta **inviare per ogni risposta i seguenti header** :

**X-RateLimit-Limit: limite massimo di richieste per un endpoint**
**X-RateLimit-Remaining: numero di richieste rimanenti fino al prossimo reset**
**X-RateLimit-Reset: il numero di secondi mancante al prossimo reset**

In questo modo i client potranno regolare il numero di richieste da inviare.

**ATTENZIONE: questi tre header, qui nella versione più diffusa, sono utilizzati anche con leggere variazioni. I client devono gestire queste variazioni, ma chi eroga in un Ecosistema API deve adottare una sintassi comune! **

Si possono segnalare problemi di sovraccarico ritornando HTTP 503 quando il sistema si accorge di non riuscire ad erogare il servizio secondo le deadline previste: [questo pattern si chiama Circuit-Breaker (in italiano: fusibile) ](https://docs.microsoft.com/it-it/azure/architecture/patterns/circuit-breaker).

Gli status che evidenziano un sovraccarico devono essere ritornati quanto prima:

* HTTP 429 (too many requests) se il rate limit viene superato
* HTTP 503 (service unavailable) in caso di servizio indisponibile (eg. in manutenzione) o di sovraccarico

Per differire le richieste, si dovrebbe sempre usare l’header

**- Retry-After: numero di secondi dopo i quali ripresentarsi**

anche implementando meccanismi di [exponential back-off](https://it.wikipedia.org/wiki/Algoritmo_di_backoff_esponenziale_binario).

A **Retry-After** e **X-RateLimit-Reset** vanno assegnati valori in secondi, eventualmente aggiungendo un po’ di [jitter](https://aws.amazon.com/it/blogs/architecture/exponential-backoff-and-jitter/) per evitare che [gruppi di client si presentino contemporaneamente](http://www.nurkiewicz.com/2015/02/retry-after-http-header-in-practice.html).

Si può anche pensare di “rimbalzare” le richieste in eccesso anche se il sistema non è sovraccarico: una lettura utile è [The Global Chubby Planned Outage ](https://landing.google.com/sre/book/chapters/service-level-objectives.html#xref_risk-management_global-chubby-planned-outage) dal libro [Google SRE ](https://landing.google.com/sre/)

L’utilizzo di header uniformi è importantissimo:

* semplifica lo sviluppo dei client, riducendo gli errori;
* evita di verificare l’esistenza di header sempre diversi.
