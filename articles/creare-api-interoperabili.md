Così vuoi creare un’API e non sai da dove iniziare.

Qui trovi un [api-starter-kit ](https://github.com/teamdigitale/api-starter-kit) che, partendo da un openapi-v3:

* descrive un microservizo che ritorna un timestamp in formato RFC5424
* genera un server stub in python
* serve il microservizio in https

Sappiamo che molti generatori di codice supportano solo le vecchie specifiche swagger-2. Che fare allora?

* innanzitutto verificate che non siano stati rilasciati nuovi code-generator (lo sviluppo su questo fronte è molto attivo)

* se non lo avete trovato, potete comunque scrivere le specifiche in openapi v3 e convertirle in v2 con [api-spec-converter ](https://lucybot-inc.github.io/api-spec-converter/), che è stato patchato di recente per supportare meglio alcuni casi. Ovviamente la v3 ha delle feature in più - che possiamo conservare a livello di specifica.

* se avete specifiche in swagger-2 invece potete:

  * convertirle in openapi-3
  * arricchirle con tutte le opzioni in più messe a disposizione dalla nuova specifica
  * ricondurvi al caso precedente :wink:

Leggete poi [i tanti post sull’interoperabilità ](https://forum.italia.it/c/piano-triennale/interoperabilita) che sono su questo forum!

