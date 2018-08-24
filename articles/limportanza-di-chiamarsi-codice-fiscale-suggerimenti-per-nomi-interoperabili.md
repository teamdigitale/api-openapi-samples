> There are only two hard things in Computer Science:
> cache invalidation and naming things.
> Phil Karlton

Probabilmente l’engineer di Netscape pensava proprio alle variabili usate per il codice fiscale:

[cod_fisc ](https://github.com/fievelk/kmZeroSpring/blob/7f3107eee8dea28b0b766c66895d1af1d71c4b22/src/it/univaq/mwt/j2ee/kmZero/business/model/Seller.java#L34), [CF](https://gist.github.com/mahizsas/4347953#file-check-cfisc-js-L4), [cod_fiscale](https://github.com/NadiaCattari/DemyHelpMe/blob/3026c6bb2c459dcf9b625b033aebf5ba9bf30f5b/Credenziale.java#L10), [codiceFiscale](https://github.com/heavybeard/codice-fiscale/blob/775fdb3f767945ca58e7803c373209468d09d6a0/source/CodiceFiscale.js#L8), [codice_fiscale](https://github.com/ProfessioneIT/italian-rails/blob/master/lib/italian-rails/codice_fiscale.rb), [fiscalCode](https://gist.github.com/supix/97dfe1e2c4b804bd3721faf4bec1c573#file-checkcodicefiscale-cs-L4) , [cfiscale](https://github.com/link-it/GovPay/blob/907bbe3ed5dd3decefbfa59dd792c747576dcef6/govpay-core/src/main/java/it/govpay/core/utils/RptUtils.java#L167)

Quando queste - piccole - differenze si riflettono sulla codifica dei dati (eg. serializzazione/marshalling) impattano sui costi di interoperabilità ed anche di sviluppo.

Se due servizi serializzano differentemente i dati personali

```
Servizio A
{ 'nome_proprio': 'Mario',
  'cognome': 'Rossi',
  'codice_fiscale': 'RSSMRA30A01H501I'
}

Servizio B

{ 'nome': 'Mario',
  'cognome': 'Rossi'
  'cf': 'RSSMRA30A01H501I'
}
```

per interoperare ogni servizio deve aggiungere delle funzioni di conversione ed i relativi metodi di test.

Le [Linee Guida Nazionali per la Valorizzazione del Patrimonio Informativo Pubblico ](http://lg-patrimonio-pubblico.readthedocs.io/it/latest/index.html) forniscono una strategia per i nomi delle variabili e la serializzazione degli oggetti.

Ad esempio, [questo file definisce i campi di una persona ](https://github.com/italia/daf-ontologie-vocabolari-controllati/blob/master/Ontologie/CPV/latest/CPV-AP_IT.jsonld) e fornisce un riferimento parlante per i nomi dei campi sia in inglese che in italiano.

Di seguito alcuni esempi in camelCase e snake_case:

* [givenName, given_name ](https://github.com/italia/daf-ontologie-vocabolari-controllati/blob/882ca0cfdc17c188e00606bac68c7b306e88e6ec/Ontologie/CPV/latest/CPV-AP_IT.jsonld#L16), [nomeProprio, nome_proprio](https://github.com/italia/daf-ontologie-vocabolari-controllati/blob/882ca0cfdc17c188e00606bac68c7b306e88e6ec/Ontologie/CPV/latest/CPV-AP_IT.jsonld#L51)
* familyName, family_name, cognome, cognome
* dateOfBirth, date_of_birth, dataDiNascita, data_di_nascita
* taxCode, tax_code, codiceFiscale, codice_fiscale

Come suggerito in [Profilo metadatazione DCAT-AP_IT
](https://linee-guida-cataloghi-dati-profilo-dcat-ap-it.readthedocs.io/it/latest/catalogo_elementi_obbligatori.html#titolo-dct-title) vanno evitati acronimi ed abbreviazioni incomprensibili.

Ecco altre utili indicazioni per costruire servizi interoperabili:

* [utilizzare UTF-8](http://lg-patrimonio-pubblico.readthedocs.io/it/latest/riepilogoazioni.html#azione-11)
* utilizzare ISO4217:alpha-3 (eg. EUR, USD, GBP, …) per le monete, come in[ fatturaPA](http://www.fatturapa.gov.it/export/fatturazione/sdi/Specifiche_tecniche_del_formato_FatturaPA_v1.0.pdf)
* utilizzare ISO 3166-1-alpha2 (eg. IT, US, DE) per i paesi


