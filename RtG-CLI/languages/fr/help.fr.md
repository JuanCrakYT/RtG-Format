RtG-CLI — Aide
================

RtG-CLI est l'interface en ligne de commande de l'écosystème RtG-Format.
Elle permet de découvrir et d'exécuter des addons, de consulter les langues, d'afficher les règles et la version.

Utilisation
------------

  rtg [OPTIONS] <COMMANDE> [ARGUMENTS]

  Le premier argument identifie la commande ou l'addon à exécuter.

  Exemples:
    rtg image
    rtg preview
    rtg help image


Commandes système
------------------

  -h, --help        Affiche cette aide générale
  -v, --version     Affiche la version de RtG-CLI
  -l, --lang        Liste les langues disponibles dans RtG-CLI
  -r, --rules       Affiche les règles de RtG-CLI
  -c, --commands    Liste les commandes internes de RtG-CLI
  -a, --addons      Liste les addons avec documentation utilisateur
  -u, --usage       Affiche les informations d'utilisation courantes (nouveau)
  -u-<langue>       Affiche l'utilisation dans une langue spécifique (ex: -u-es, -u-en) (nouveau)
  --usage-<langue>  Affiche l'utilisation dans une langue spécifique (ex: --usage-es, --usage-en) (nouveau)
  -language <langue>  Définit la langue du texte de démarrage (void)

Commande: help
---------------

  rtg help                    # Aide générale (cet écran)
  rtg help <commande>         # Aide pour une commande/addon spécifique
  rtg help <commande> -<langue> # Aide en langue spécifique (ex: -es, -en)
  rtg help <commande> -lang     # Langues disponibles pour cette commande
  rtg help -u                  # Aide courante (nouveau)
  rtg help -u-<langue>         # Aide dans une langue spécifique (ex: -u-es) (nouveau)
  rtg help --usage             # Aide courante (nouveau)
  rtg help --usage-<langue>    # Aide dans une langue spécifique (ex: --usage-es) (nouveau)
  rtg help usage               # Aide courante (syntaxe alternative, nouveau)

  Exemples:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


Commande: version
------------------

  rtg -v
  rtg --version

  Affiche la version et le contenu de version dans toutes les langues disponibles.


Commande: rules
----------------

  rtg -r
  rtg --rules
  rtg -r -<langue>   # Règles en langue spécifique (ex: rtg -r -en)

  Par défaut utilise la première langue définie dans 'rules' (espagnol).


Commande: lang
---------------

  rtg -l
  rtg --lang

  Liste toutes les langues disponibles organisées par catégorie:
  Version, Rules, Help, Void, et par addon.


Commande: commands
--------------------

  rtg -c
  rtg --commands

  Liste exclusivement les commandes internes de RtG-CLI.
  N'inclut pas les commandes d'addons.


Commande: addons
-----------------

  rtg -a
  rtg --addons

  Liste les addons ayant une documentation/aide visible pour l'utilisateur.
  Un addon enregistré sans documentation n'apparaît pas ici.


Commande: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<langue>       # Utilisation dans une langue spécifique (ex: -u-es, -u-en) (nouveau)
  --usage-<langue>      Affiche l'utilisation dans une langue spécifique (ex: --usage-es, --usage-en) (nouveau)

  Affiche les informations d'utilisation courantes (void) dans la langue demandée.
  La langue doit exister dans 'void-language' de assets.json.


Commande: language
--------------------

  rtg -language <langue>

  Sélectionne la langue du texte de démarrage (void).
  La langue doit exister dans 'void-language' de assets.json.

  Exemple:
    rtg -language en


Addons disponibles
--------------------

  image      | RtG Image        - Convertisseur d'images
  preview    | RtG Preview      - Visualiseur 3D pour builds RtG-Format
  test-addon | RtG Test Addon   - Addon de test pour validation


Langues
--------

Les langues sont indiquées avec un trait d'union unique: -es, -en, -pt, etc.
La langue ne change pas le nom interne de la commande.

  rtg help image -es    # Aide en espagnol
  rtg help image -en    # Aide en anglais
  rtg -r -en            # Règles en anglais

  Pour voir les langues d'un addon:
    rtg help image -lang

  La signification de -lang dépend de sa position:
    rtg --lang          # Langues de RtG-CLI (avant l'addon)
    rtg image -lang     # Langues de l'addon (après l'addon)


Arguments d'addons
--------------------

Après l'identification d'un addon, les arguments sont classés par préfixe:

  sans trait d'union   -> addon        (ex: convert, fichier.png)
  --option             -> addon        (ex: --width 128)
  -option              -> RtG-CLI      (ex: -lang, -en)

Exemples:
  rtg image convert fichier.png     # convert, fichier.png -> addon
  rtg image --width 128             # --width 128 -> addon
  rtg image -lang                   # -lang -> RtG-CLI (langues de l'addon)
  rtg image -en                     # -en -> RtG-CLI (sélecteur de langue)


Arguments avec espaces
------------------------

Les arguments contenant des espaces doivent être entre guillemets:

  rtg image "mon image.png" "sortie.json"

RtG-CLI conserve l'ordre et passe les arguments tels quels à l'addon.


Plus d'informations
--------------------

  rtg help <commande>      # Aide détaillée d'un addon
  rtg help <commande> -lang  # Langues de cet addon
  rtg --addons             # Voir tous les addons documentés
  rtg --commands           # Voir les commandes internes