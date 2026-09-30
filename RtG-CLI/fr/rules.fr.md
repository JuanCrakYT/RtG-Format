# Règles de commandes RtG-CLI

## 1. Structure générale

Une commande RtG-CLI consiste en une commande principale et, optionnellement, des arguments.
Format général :

`rtg <commande> [<arguments>]`

Le premier argument après `rtg` détermine quelle commande ou addon sera exécuté.

Exemples :

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Commandes enregistrées

Les commandes principales doivent être enregistrées dans la configuration de RtG-CLI.
Une commande est identifiée par sa clé interne.

Exemple :

`image`

La clé `image` identifie l'addon correspondant, indépendamment du nom affiché à l'utilisateur.
Exemple :

`image` → `RtG Image`

`preview` → `RtG Preview`

Le nom affiché ne doit pas être utilisé comme identifiant de commande.

---

## 3. Commandes RtG-CLI et commandes des addons

RtG-CLI et les addons peuvent avoir leurs propres commandes et arguments.

Avant d'identifier un addon, les commandes et arguments appartiennent à RtG-CLI.
Après l'identification d'un addon, le préfixe détermine à qui appartient chaque argument :

- Sans trait d'union (`-`) → appartient à l'addon.
- Deux traits d'union (`--`) → appartient à l'addon.
- Un trait d'union (`-`) → appartient à RtG-CLI.

Exemple :

`rtg image convert`

- `image` → addon.
- `convert` → commande de l'addon.

Exemple :

`rtg image --width 128`

- `image` → addon.
- `--width` → argument de l'addon.
- `128` → valeur de l'argument de l'addon.

Exemple :

`rtg image -lang`

- `image` → addon.
- `-lang` → argument de RtG-CLI.

---

## 4. Arguments du système

Avant d'identifier un addon, RtG-CLI utilise ses propres règles de syntaxe.
Les options longues du système utilisent deux traits d'union :

`rtg --version`
`rtg --help`

Les abréviations du système utilisent un trait d'union :

`rtg -v`
`rtg -h`
`rtg -l`

Après l'identification d'un addon, une option commençant par un seul trait d'union (`-`) appartient à RtG-CLI.

Exemple :

`rtg image -lang`
`rtg image -en`

---

## 5. Arguments avant et après l'addon

Les arguments de RtG-CLI peuvent avoir une signification différente selon qu'ils apparaissent avant ou après l'identification de l'addon.

Avant d'identifier un addon, les arguments appartiennent à RtG-CLI.

Par exemple :

`rtg --lang`

Affiche les langues disponibles pour RtG-CLI.

Après l'identification d'un addon, les arguments sont interprétés selon les règles de propriété établies pour les addons.

Par exemple :

`rtg image -lang`

Interroge les langues disponibles pour l'addon `image`.

Ainsi, la position de l'argument détermine son contexte et évite de confondre les arguments globaux de RtG-CLI avec les arguments utilisés après l'identification d'un addon.

---

## 6. Position des arguments du système

Les arguments du système ne doivent pas apparaître avant la commande ou l'addon qu'ils affectent lorsque l'argument dépend de cette commande.

Exemple correct :

`rtg help image -en`

Exemple incorrect :

`rtg help -en image`

Dans ces deux exemples, la commande système `help` utilise cette structure, c'est pourquoi le second exemple est incorrect :
`help <target> <options>`

La position doit permettre de déterminer clairement quelle commande reçoit l'argument.

---

## 7. Commandes et arguments des addons

Les commandes sont écrites comme arguments individuels du terminal.
Une commande ne doit pas contenir d'espaces sauf si elle est entre guillemets.

Les arguments suivants peuvent être utilisés par l'addon selon sa propre interface.

Par exemple :

`rtg image convert image`

peut être interprété comme :

- `image` → addon
- `convert` → commande de l'addon
- `image` → argument de la commande

---

## 8. Utilisation des traits d'union dans les commandes d'addons

Après l'identification d'un addon :

- Les arguments sans trait d'union appartiennent à l'addon.
- Les arguments avec deux traits d'union ou plus (`--`) appartiennent à l'addon.
- Les arguments avec un seul trait d'union (`-`) appartiennent à RtG-CLI.

Exemples :

`rtg image convert`
`convert` → addon.

`rtg image --width 128`
`--width` → addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Interface de commandes des addons

Les commandes spécifiques à un addon sont définies par le programme de l'addon lui-même.
RtG-CLI utilise la configuration de l'addon pour localiser son interface de commandes via la propriété `program commands`.

Cette propriété contient les chemins vers les fichiers qui fournissent l'interface de commandes du programme.

Exemple :

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI peut utiliser cette interface pour découvrir ou exécuter les commandes disponibles de l'addon, mais ne doit pas en supposer ou modifier la signification interne.

Un addon peut définir des commandes supplémentaires qui ne sont pas directement enregistrées comme commandes propres de RtG-CLI.

L'implémentation interne du programme peut différer entre addons, tant qu'elle fournit une interface compatible avec les règles de RtG-CLI.

---

## 10. Langues

Les langues disponibles pour un addon sont définies via sa configuration.

Exemple :

`lang: ["es", "en"]`

Les textes traduits sont identifiés à l'aide du code de langue correspondant.

Exemple :

`content.fr`
`content.en`

Le sélecteur de langue utilisé par RtG-CLI doit être considéré comme un argument système.

Exemple :

`rtg help image -en`

---

## 11. Langue par défaut

Si `-<langue>` n'est pas spécifié, RtG-CLI utilisera la première langue définie dans `rules`.
Si `-<langue>` est spécifié, RtG-CLI utilisera cette langue si elle est disponible.

La première langue définie dans l'objet `rules` de `assets.json` est la langue par défaut pour les règles.

Lorsque l'utilisateur demande les règles sans spécifier de langue, RtG-CLI doit utiliser cette première langue.

Par exemple :

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

Dans ce cas :

`rtg -r`
et
`rtg --rules`

afficheront les règles en espagnol car `es` est la première langue définie.
Pour demander une autre langue, son sélecteur correspondant doit être utilisé :

`rtg -r -en`

L'ordre des langues dans `rules` détermine uniquement quelle langue est la langue par défaut. Il ne change pas les langues disponibles.

Cette règle s'applique également aux autres sélecteurs de langue comme :

`rtg help image -es`

---

## 12. La langue ne change pas la commande

Changer la langue ne modifie que le texte affiché par RtG-CLI.
Elle ne change pas le nom interne de la commande.

Exemple :

`rtg help image -es`

et

`rtg help image -en`

font toujours référence à la même commande :

`image`

---

## 13. Aide

L'aide générale s'obtient avec :

`rtg help`

L'aide pour une commande spécifique s'obtient avec :

`rtg help <commande>`

L'aide peut être demandée dans une langue spécifique :

`rtg help <commande> -<langue>`

Exemple :

`rtg help image -en`

---

## 14. Requête de langue

Les langues disponibles pour un addon peuvent être interrogées avec :

`rtg help <commande> -lang`

Exemple :

`rtg help image -lang`

Cette option appartient à RtG-CLI et non à l'addon.

---

## 15. Les addons ne doivent pas modifier les règles du système

Un addon peut définir ses propres commandes et arguments, mais ne peut pas redéfinir la signification des arguments réservés par RtG-CLI.

Par exemple, un addon ne doit pas utiliser `-h` pour donner une signification différente à l'aide système.
Les noms réservés par RtG-CLI ont la priorité sur les commandes des addons.
Les commandes et options réservées par RtG-CLI doivent être explicitement définies par l'interface CLI.
Un addon ne peut pas redéfinir le comportement d'une option réservée.

---

## 16. Séparation entre identifiant et nom

La clé interne d'un addon est utilisée pour l'identifier.
Le nom de l'addon n'est utilisé que comme information descriptive ou pour l'affichage à l'utilisateur.

Exemple :

`image` → identifiant interne

`RtG Image` → nom affiché

Il ne doit pas être supposé que le nom affiché peut être utilisé comme commande.

---

## 17. Les commandes doivent être déterministes

RtG-CLI doit pouvoir déterminer si un argument appartient au système ou à l'addon sans dépendre du nom descriptif du programme.

L'interprétation doit être basée sur la structure et les règles de la commande.

Exemple :

`rtg help image -en`

doit toujours être interprété de la même manière :

`rtg` → CLI

`help` → commande CLI

`image` → addon

`-en` → option CLI

---

## 18. Arguments inconnus

Après l'identification d'un addon, RtG-CLI doit déterminer l'appartenance de chaque argument selon son préfixe.

* Un argument sans trait d'union appartient à l'addon.
* Un argument avec deux traits d'union ou plus (`--`) appartient à l'addon.
* Un argument avec un seul trait d'union (`-`) appartient à RtG-CLI.

Si RtG-CLI reçoit un argument système inconnu, il doit signaler que l'option n'existe pas.

Les arguments de l'addon doivent être transmis à l'addon sans que RtG-CLI n'essaie d'interpréter leur signification.

---

## 19. Ne pas supposer de commandes non enregistrées

RtG-CLI ne doit pas considérer une commande comme valide simplement parce qu'un dossier, fichier ou programme associé existe.

La commande doit être définie dans la configuration correspondante.

---

## 20. Compatibilité

Les addons doivent suivre les règles de syntaxe de RtG-CLI pour s'intégrer correctement.
Un addon peut avoir une implémentation interne complètement différente, mais son interface de commandes doit suivre les règles établies par RtG-CLI.

---

## 21. Règle de priorité

Après l'identification d'un addon, un seul trait d'union (`-`) est réservé pour RtG-CLI.
Un addon ne peut pas utiliser d'arguments commençant par un seul trait d'union.
Les arguments commençant par deux traits d'union ou plus (`--`) ou ne commençant pas par un trait d'union appartiennent à l'addon.

---

## 22. Arguments d'addon

Une fois l'addon identifié, RtG-CLI ne doit pas supposer la signification des arguments spécifiques à l'addon.

Les arguments appartenant à l'addon doivent être transmis au programme de l'addon pour qu'il les traite.

Exemple :

`rtg image --width 128`

RtG-CLI identifie `image` comme addon.

`--width 128` correspond à l'interface de RtG Image et doit être traitée par ledit addon.

---

## 23. Arguments avec espaces

Les arguments contenant des espaces doivent être écrits entre guillemets pour que le terminal les traite comme un argument unique.

Exemple :

`rtg image "C:\Users\User\Downloads\mon image.png" "C:\Users\User\Downloads\sortie.json"`

Le chemin complet doit être reçu comme un argument unique.

---

## 24. Les arguments d'addon doivent être conservés

RtG-CLI ne doit pas modifier, supprimer ou réinterpréter les arguments destinés à l'addon, sauf si une règle système explicite indique le contraire.

Les arguments doivent être livrés à l'addon dans l'ordre dans lequel ils ont été fournis par l'utilisateur.

---

## 25. Exemples complets

Commande d'addon :

`rtg image`

Aide :

`rtg help image`

Aide en anglais :

`rtg help image -en`

Interroger les langues :

`rtg help image -lang`

Version du CLI :

`rtg --version`

Aide du CLI :

`rtg --help`

Une option propre à l'addon :

`rtg image --width 128`

Une option propre à l'addon avec valeur :

`rtg image --output fichier.json`

Une combinaison :

`rtg image image.png --output sortie.json`

Dans cet exemple :

* `image` identifie l'addon.
* `image.png` est un argument de l'addon.
* `--output` est une option de l'addon.
* `sortie.json` est la valeur de cette option.
* Aucun de ces arguments ne doit être interprété comme une option système.

---

## 26. Langue du texte de démarrage

`rtg -language <langue>` sélectionne la langue du texte de démarrage affiché par RtG-CLI.

La langue doit exister dans `void-language`.

Exemple :

`rtg -language fr`

affiche le texte défini dans :

`void-language.fr`

Si `-language` n'est pas spécifié, RtG-CLI utilise `void`.

Si la langue demandée n'est pas disponible, RtG-CLI doit signaler que la langue n'est pas disponible.