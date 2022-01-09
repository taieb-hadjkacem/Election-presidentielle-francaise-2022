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
* Réception des tweets
* Association de chaque tweet au condidat correspondant : comparaison des hashtags avec les noms des condidats, en utlisant la fonction *fuzz.ratio* de la bibliothèque *fuzzywuzzy*
* Intégration des tweets dans un dataframe Pyspark avec les colonnes hastags, tweet, name_user, created_at
* Nettoyage des tweets des caractères spéciaux.
* Classification des tweets (propos négatifs, positifs ou neutres) avec le module NLP *TextBlob*.
* Indexation des tweets, des données liés ainsi que les scores d’analyse de sentiment dans Elasticksearch.
### Visualisation avec Kibana
* Création des visualisations telles que pour chaque condidat est associé un  bar vertical contenant le nombre des avis négatifs, positifs et neutres.
* Création d'un dashboard avec les visualisations créées

![](https://photos.app.goo.gl/8rzZAW5HTgGtoZQq9)

