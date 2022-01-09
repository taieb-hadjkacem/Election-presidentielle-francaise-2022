# Élection présidentielle française 2022

## Description
Il s'agit d'un pipeline qui rassemble les differentes technologies: kafka, spark, elasticsearch et kibana afin d'analyser en temps réel les avis des Français concernant les élections présidentielles 2022.

## Documentation technique
### Comment installer le projet ?

1. Lancer kafka en initialisant zookeeper et kafka server avec les commandes suivantes
```bash
./bin/zookeeper-server-start.sh ./config/zookeeper.properties
```

```bash
./bin/kafka-server-start.sh ./config/server.properties
```
2. Créer un topic sous le nom *election*
```bash
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic election
```
3. Lancer Elasticsearch et Kibana en éxécutant les commandes suivantes
```bash
bin\elasticsearch.bat
```

```bash
bin\kibana.bat
```
4. Exécuter les deux programmes python `producer.py` puis `consumer.py
`

### producer.py
* Authentification auprès de l'API *tweepy* avec les *creadentials* obtenus avec le compte *twitter developper elevated acces*.
* Filtration des tweets selon les *hastags* des quatres condidats ayant plus de chance à passer au second tour, selon les sondages. 
* Envoi des donnnées pour la partie consumer.
### consumer.py
* Réception des tweets.
* Association de chaque tweet au condidat correspondant : comparaison des hashtags avec les noms des condidats, en utlisant la fonction *fuzz.ratio* de la bibliothèque *fuzzywuzzy*.
* Intégration des tweets dans un dataframe Pyspark avec les colonnes hastags, tweet, name_user, created_at.
* Nettoyage des tweets des caractères spéciaux.
* Classification des tweets (propos négatifs, positifs ou neutres) avec le module NLP *TextBlob*.
* Indexation des tweets, des données liés ainsi que les scores d’analyse de sentiment dans Elasticksearch.
### Visualisation avec Kibana
* Accès à Kibana via le port 5601.
* Création des visualisations telles que pour chaque condidat est associé un  bar vertical contenant le nombre des avis négatifs, positifs et neutres.
* Création d'un dashboard avec les visualisations créées.

![](https://lh3.googleusercontent.com/aQ7ROAQzlwoxR0M6LMm8_ufFCijvi5w4KGv3bfRWuDCbcW6885C4uri17wODs4ULhweV1HtcJrn6blnlap_ZiQReIdoCaSYdVhjG_mjnzfD-DIr_r4NuWgk20P0GTak-lWATe3zTOo_MyyR2jJZkJrUErGXGBgasVkvaKC7ztNY_w3ZTuRpagggHwlTFC_f8Igy0lDCGXL-D4OFcJrR43fNAvFy7HezRIARMwC5Tc2ETVwsz_RgortGXXsdVxUi9YrhFTxjOoUpPFVl-EqU9-83689hbCLunah7KRAzvIaZQwFm89k8Q68MuDp4OsZWlVdUvIvA1OqIC9903mp3YSPQykCIJm-tmwLwgHll0SINBY6mNZXZgZxRq_9zkc7GWHdyHik89vP2meVt8a4zQJx-OjVeyaeNjNUOXNMR2AmSNcP9hlg-4PzXIg6m37X39uRsAE9D1qF9qJWLWQ-1Zl6bMcOb6AH452NLWJ0_2U-4NYlyLT0dO06h8LVHVRBpb_YbonGPs4_9vNs8GuToaA5JvcPV47AsqrHRYJNQgM-D9hbM6VCOqtdguf_xb9CI7A1l-p7oHfnqAG0qX7x6aXJuMpfQvN0wYu1LBeQ7iZNY4Wgj1pg6iBSBldAoM_IaEGKdEytmxl4MY7xzzEUs3F7E9JvCidq-bftovilv5CYbLviHPZHDVlJfvHmQSwS69xx-C4oK2qy0cd8gYS_BUUlE=w845-h403-no?authuser=0)

