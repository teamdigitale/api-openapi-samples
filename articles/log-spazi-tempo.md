Il formato del timestamping nei log è una delle cose più bistrattate dell'IT.

A specifiche estremamente liberali come ISO8601 si affiancano il timestamping in formato unix, i fusi orari e i cambi d'ora.
Nei log di sistema troviamo stringhe come:

```
lug 15 14:04:50                 # mese in italiano, senza anno ne timezone
mag-06 18:58:50                 # con separatore
Aug 02 18:43:47                 # in inglese
mer  9 mag 08:45:37 CEST 2018   # sempre in italiano, ora legale
Fri May 05 08:45:37 IST         # in inglese,
2018-May-08 10:06:25 AM         # in inglese, intervallo 00-12
2018-05-08T10:06:25Z            # RFC 3339
```

L'[RFC3339](https://tools.ietf.org/html/rfc3339) fa un po' d'ordine:

  - è un sottoinsieme di ISO8601 per le date dopo Cristo
  - data ed ora sono ordinate lessicograficamente (dall'anno 1000 al 9999) ;)
  - i separatori sono obbligatori
  - le timezone sono indicate con la distanza da UTC

Ecco alcuni esempi:

```
1985-04-12T23:20:50Z 	   # UTC: 
1985-04-12T23:20:50.52Z    # UTC con frazioni di secondo: 
1996-12-19T16:39:57-08:00  # non UTC, con offset:    
```

Utilizzando per tutti i log `RFC 3339 in UTC`:

  - è più facile aggregare i tracciati ed individuare i problemi, anche tra piattaforme diverse;
  - si evita la gestione della timezone, obbligatoria durante i cambi d'ora;
  - si traccia sempre l'anno: le righe di log divengono autocontenute;
  - si velocizza il parsing (identificare il formato dell'ora lo rallenta significativamente
    (nel micro-benchmark di esempio il rapporto è almeno di 2:1);
  - si possono usare librerie standard invece che parser custom;

Di seguito un micro-benchmark tra due librerie di parsing:

  - una che individua il formato della data, eventualmente localizzato (min: 2120 µs)

```
from dateparser import parse as parse_hint

%timeit parse_hint('Fri, 12 Dec 2014 10:55:50')
# 2.31 ms ± 18.7 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit parse_hint('Ven, 12 Dic 2014 10:55:50')
# 2.64 ms ± 44.5 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit parse_hint('2014-10-21T10:55:50Z')  
# 2.12 ms ± 15.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

```

 - una che ignora la localizzazione e senza supporto per il locale (min: 856 µs)

```
from dateutil.parser import parse

%timeit parse('Fri, 12 Dec 2014 10:55:50')
# 104 µs ± 1.5 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)

%timeit parse('2014-12-12T10:55:50Z')
# 85.6 µs ± 663 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```


