RtG-CLI — Ajuda
=================

RtG-CLI é a interface de linha de comandos do ecossistema RtG-Format.
Permite descobrir e executar addons, consultar idiomas, ver regras e versão.

Uso
-----

  rtg [OPÇÕES] <COMANDO> [ARGUMENTOS]

  O primeiro argumento identifica o comando ou addon a executar.

  Exemplos:
    rtg image
    rtg preview
    rtg help image


Comandos do sistema
--------------------

  -h, --help        Mostra esta ajuda geral
  -v, --version     Mostra a versão do RtG-CLI
  -l, --lang        Lista os idiomas disponíveis no RtG-CLI
  -r, --rules       Mostra as regras do RtG-CLI
  -c, --commands    Lista os comandos internos do RtG-CLI
  -a, --addons      Lista os addons com documentação disponível
  -u, --usage       Mostra a informação de uso comum do sistema (novo)
  -u-<idioma>       Mostra o uso em um idioma específico (ex: -u-es, -u-en) (novo)
  --usage-<idioma>  Mostra o uso em um idioma específico (ex: --usage-es, --usage-en) (novo)
  -language <idioma>  Define o idioma do texto de início (void)

Comando: help
--------------

  rtg help                    # Ajuda geral (esta tela)
  rtg help <comando>          # Ajuda de um comando/addon específico
  rtg help <comando> -<idioma>  # Ajuda em idioma específico (ex: -es, -en)
  rtg help <comando> -lang      # Idiomas disponíveis para esse comando
  rtg help -u                  # Uso comum (novo)
  rtg help -u-<idioma>         # Uso em idioma específico (ex: -u-es) (novo)
  rtg help --usage             # Uso comum (novo)
  rtg help --usage-<idioma>    # Uso em idioma específico (ex: --usage-es) (novo)
  rtg help usage               # Uso comum (sintaxe alternativa, novo)

  Exemplos:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


Comando: version
-----------------

  rtg -v
  rtg --version

  Mostra a versão e o conteúdo da versão em todos os idiomas disponíveis.


Comando: rules
---------------

  rtg -r
  rtg --rules
  rtg -r -<idioma>   # Regras em idioma específico (ex: rtg -r -en)

  Por padrão usa o primeiro idioma definido em 'rules' (espanhol).


Comando: lang
--------------

  rtg -l
  rtg --lang

  Lista todos os idiomas disponíveis organizados por categoria:
  Version, Rules, Help, Void, e por cada addon.


Comando: commands
------------------

  rtg -c
  rtg --commands

  Lista exclusivamente os comandos internos do RtG-CLI.
  Não inclui comandos de addons.


Comando: addons
----------------

  rtg -a
  rtg --addons

  Lista os addons que têm documentação/ajuda visível para o usuário.
  Um addon registrado mas sem documentação não aparece aqui.


Comando: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<idioma>       # Uso em idioma específico (ex: -u-es, -u-en) (novo)
  --usage-<idioma>      # Uso em idioma específico (ex: --usage-es, --usage-en) (novo)

  Mostra a informação de uso comum do sistema (void) no idioma solicitado.
  O idioma deve existir em 'void-language' de assets.json.


Comando: language
------------------

  rtg -language <idioma>

  Seleciona o idioma do texto de início (void).
  O idioma deve existir em 'void-language' de assets.json.

  Exemplo:
    rtg -language en


Addons disponíveis
-------------------

  image      | RtG Image        - Conversor de imagens
  preview    | RtG Preview      - Visualizador 3D de builds RtG-Format
  test-addon | RtG Test Addon   - Addon de teste para validação


Idiomas
--------

Os idiomas são indicados com um único hífen: -es, -en, -pt, etc.
O idioma não muda o nome interno do comando.

  rtg help image -es    # Ajuda em espanhol
  rtg help image -en    # Ajuda em inglês
  rtg -r -en            # Regras em inglês

  Para ver idiomas de um addon:
    rtg help image -lang

  O significado de -lang depende de sua posição:
    rtg --lang          # Idiomas do RtG-CLI (antes do addon)
    rtg image -lang     # Idiomas do addon (depois do addon)


Argumentos de addons
---------------------

Após identificar um addon, os argumentos são classificados por prefixo:

  sem hífen       -> addon        (ex: convert, arquivo.png)
  --opção         -> addon        (ex: --width 128)
  -opção          -> RtG-CLI      (ex: -lang, -en)

Exemplos:
  rtg image convert arquivo.png     # convert, arquivo.png -> addon
  rtg image --width 128             # --width 128 -> addon
  rtg image -lang                   # -lang -> RtG-CLI (idiomas do addon)
  rtg image -en                     # -en -> RtG-CLI (seletor de idioma)


Argumentos com espaços
-----------------------

Argumentos com espaços devem ir entre aspas:

  rtg image "minha imagem.png" "saida.json"

RtG-CLI conserva a ordem e passa os argumentos tal qual ao addon.


Mais informações
-----------------

  rtg help <comando>      # Ajuda detalhada de um addon
  rtg help <comando> -lang  # Idiomas desse addon
  rtg --addons            # Ver todos os addons documentados
  rtg --commands          # Ver comandos internos