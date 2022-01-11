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
* Faire le lien Kibana-Elasticsearch en définissant l'index pattern prédéfinit dans le code consumer.py sous le nom *electionsfrance*.

![](https://lh3.googleusercontent.com/js90EkEqU6CnytK9yasxn3tKjMrvEqvx-ULaNHziZLw5IRX6czmCTl9bCQS69xNK5EyoHxH_xfcpfVu25Jr9XA8U70_xjTamIjKAZZd0VvGmo-QaTx8NLIg6V2h4bI-DVtSnf8CvHfk7sPbERYRIe5Y0T_0t5KSTbo_kx3CHxBr_PCXp9cdEDXtJhetI4fAjhkZqw_HhfUU1mZMIiHmfVmLhCxSM66_ShUM55obWifmCXjZEto-Za_8s4TvX6NIQCu3jPSLF4JyzlYVrZ1IL73PnxjUicmsB3xHIi_uz7oawZeOyPA1A_lk28TKPJSMUaW4KZp_X0PPRSngjYqNKCUfiqtjL3dIOgI4a0umkKORjwtmHQSah9waky6SMRfBYfFYXeJJLnZ_8Vaykf6sVCybUs7f4cuukGPxBPFa9vKonEucfuXXF6cRh1g3wwPLTxhi0_eKq-2s-torESWWoEF4pmsh7BuNSJuPGWbV36lu3PLU2RM3aSO608Wgw1al-KULeJ2dUCPifhpMXdX-jXu-1sa5pMHCWXHPnl3h1I5Zx202SMtEZ7I7k7szxCLfzY4JfA9ntkBOvizkpQ55L5j-Ctu8ODIB5eFqXIokbjj-Oq3y-h_f9felTFezUd8VQXYh9izH_1D6aNvk7sYadwFHMk830mGMGbFBvPYlzBs-HSBpG0yAbSPImpoTbXthTVCGOGuyLqNuPwMyEzzzYqPE=w610-h209-no?authuser=0)

* Création des visualisations telles que pour chaque condidat est associé un  bar vertical contenant le nombre des avis négatifs, positifs et neutres.
* Création d'un dashboard avec les visualisations créées.

![](https://lh3.googleusercontent.com/6pQi_w1q8r-mV2tEt9ujxBwhQBn3y5uuJefLoGHNGhQAowfczNjegmOeQm80yvDO-2ZS_Ms_9LSb6pru410ULD9S8eKsbWGupf6XnbO839LgEVlosFoDSkLygF6it_vrZSYguI4cxtiiCg4gbV0mMCLKFl1rbaI85ElMx64fnCw8mv65TedbevPEoWUz64WIBvQDJOTIm8NiAPEk32aFv7Pk-s64vmuT7DeWz-DTiixZCcZOxALSduZ8eLJkZ4jhI6Kqjg7H6O56pK-IMJ9FnKjVnc-0rZ85fAsB0jEKs3PMxEzE7djwOaFHo1psOLQrdjvLOakju-u_riccyu2F_Hi15x97VS1HvWYDjFLinqx9DpVkfQP9jrHCPeYzMg3wsW4ozxCu0rhRIs4fv_5_mtPAwQitMvGhVxBlx0dbb55IEGdNNya1SmqhnEiyENwwmCnFHPufKC9FZnQZu1TtBjLPDex5ZcIUIk2S_sEZCDo1uXgsReIPxW2uzaU59YlYjhwhf2rwuiWLcvvv6UlhmjwsQs9OiHP8d4EGHyb0XT4fpQAlmqMdPcs06PX4u2MXTS6xedBMzQoA5J4Bf33dQgTAvzxe4e8cx4ugAaY2hHxWWEfNiz5k78d_h2zrPTyp-5r0auUsciDAUDhs1oN3VozeYZtObs3wrhGHMDbuFCQapEQrAq3VFdRIgIAihyLFgWop1RUFzMoA9bdxGoYtwiI=w845-h403-no?authuser=0)

