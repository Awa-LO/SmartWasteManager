# 🌍 SmartWasteManager 🌍

**SmartWasteManager** est une solution IoT innovante visant à révolutionner la gestion des déchets urbains. Grâce à des capteurs intelligents, cette poubelle surveille le niveau de remplissage, détecte les gaz toxiques et contrôle la qualité de l'air en temps réel. 🌱

## 🚀 Fonctionnalités principales :
- **Surveillance en temps réel** du niveau de remplissage grâce aux capteurs à ultrasons.
- **Contrôle de la qualité de l'air** avec le capteur MQ135.
- **Détection des gaz toxiques** dans les déchets pour garantir un environnement sain.
- **Gestion automatisée** de l'ouverture/fermeture du couvercle.
- **Sécurité des données** grâce à un système de gestion des rôles.

## 💡 Pourquoi ce projet ?
Au Sénégal et dans d'autres grandes villes, la gestion des déchets devient un défi majeur. Ce projet vise à apporter une réponse technologique avec une **poubelle intelligente** qui améliore l'efficacité du processus de collecte et contribue à un environnement plus sain.

## 🛠️ Technologies utilisées :
- **IoT** (Internet des Objets) : Communication entre les capteurs et le système.
- **Arduino** : Pour la gestion des capteurs.
- **MQ135** : Capteur de qualité de l'air et de détection des gaz.
- **Ultrasonic Sensors** : Pour mesurer le niveau de remplissage.
- **NGINX** : Serveur web qui fonctionne comme reverse proxy pour accéder à l'application via un domaine local.

## 🎯 Objectifs :
1. **Réduire la pollution** en surveillant en temps réel la qualité de l'air et les gaz toxiques.
2. **Optimiser la collecte des déchets** en offrant une gestion intelligente des poubelles.
3. **Fournir une solution éco-énergétique** avec des fonctionnalités comme l'intégration de panneaux solaires.

## ✨ Auteurs :
- **Awa Lo** 
- **Hawa Dembele** 

## 📢 Perspectives d'amélioration :
- Ajouter des **capteurs supplémentaires** pour surveiller plus de polluants.
- Implémenter des **notifications push** pour les alertes urgentes.
- Utiliser **l'IA** pour prédire les besoins de collecte.
- Intégrer un **système de tri automatique** des déchets.
- **Panneaux solaires** pour un système autonome et durable.

## 🚀 Lancer le projet localement :
1. Clonez ce dépôt.
2. Installez les dépendances nécessaires via `npm install`.
3. Lancez le serveur local avec `npm start`.
4. Ouvrez votre navigateur et accédez à `http://localhost:80` pour voir le site en action **si le reverse proxy avec NGINX est configuré**.

### 🌐 Configuration du nom de domaine local :
Si vous souhaitez accéder au site via `gestionsdesdechets` sur le même réseau local :
1. Configurez NGINX en tant que reverse proxy pour pointer vers votre application Django.
2. Ajoutez `gestionsdesdechets` à votre fichier `/etc/hosts` (sur les machines qui doivent y accéder) avec l'adresse IP du serveur local.
   Exemple d'entrée dans `/etc/hosts` :

   192.168.x.x  gestionsdesdechets

   Où `192.168.x.x` est l'adresse IP de la machine hébergeant le serveur.

3. **Important** : Assurez-vous que la machine où le projet est hébergé a l'IP correcte configurée dans `settings.py` de Django. Cela peut être fait en ajoutant l'IP de votre réseau local à `ALLOWED_HOSTS` dans Django.

   Exemple dans `settings.py` de Django :

   ALLOWED_HOSTS = ['gestionsdesdechets', 'localhost', '127.0.0.1']


4. Vous pouvez désormais accéder à l'application en utilisant l'URL `http://gestionsdesdechets` dans votre navigateur à partir de n'importe quelle machine sur le même réseau local.

## 📜 Licence :
Ce projet est sous licence **MIT**. Consultez le fichier `LICENSE` pour plus de détails.



### 🧑‍💻 Contribuer :
- Fork le projet, crée une branche et soumets une pull request pour de nouvelles fonctionnalités ou corrections de bugs.

**N'oubliez pas de contribuer et de rendre le monde plus propre et plus sain ! 🌎💚**


