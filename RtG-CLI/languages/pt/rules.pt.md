# Regras de comandos do RtG-CLI

## 1. Estrutura geral

Um comando do RtG-CLI consiste em um comando principal e, opcionalmente, argumentos.
Formato geral:

`rtg <comando> [<argumentos>]`

O primeiro argumento após `rtg` determina qual comando ou addon será executado.

Exemplos:

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. Comandos registrados

Os comandos principais devem estar registrados na configuração do RtG-CLI.
Um comando é identificado pela sua chave interna.

Exemplo:

`image`

A chave `image` identifica o addon correspondente, independentemente do nome mostrado ao usuário.
Exemplo:

`image` → `RtG Image`

`preview` → `RtG Preview`

O nome mostrado não deve ser utilizado como identificador do comando.

---

## 3. Comandos do RtG-CLI e comandos dos addons

O RtG-CLI e os addons podem ter seus próprios comandos e argumentos.

Antes de identificar um addon, os comandos e argumentos pertencem ao RtG-CLI.
Após identificar um addon, o prefixo determina a quem pertence cada argumento:

- Sem hífen (`-`) → pertence ao addon.
- Dois hífens (`--`) → pertence ao addon.
- Um hífen (`-`) → pertence ao RtG-CLI.

Exemplo:

`rtg image convert`

- `image` → addon.
- `convert` → comando do addon.

Exemplo:

`rtg image --width 128`

- `image` → addon.
- `--width` → argumento do addon.
- `128` → valor do argumento do addon.

Exemplo:

`rtg image -lang`

- `image` → addon.
- `-lang` → argumento do RtG-CLI.

---

## 4. Argumentos do sistema

Antes de identificar um addon, o RtG-CLI utiliza suas próprias regras de sintaxe.
As opções longas do sistema utilizam dois hífens:

`rtg --version`
`rtg --help`

As abreviações do sistema utilizam um hífen:

`rtg -v`
`rtg -h`
`rtg -l`

Após identificar um addon, uma opção que começa com um único hífen (`-`) pertence ao RtG-CLI.

Exemplo:

`rtg image -lang`
`rtg image -en`

---

## 5. Argumentos antes e depois do addon

Os argumentos do RtG-CLI podem ter um significado diferente dependendo de se encontram antes ou depois de identificar o addon.

Antes de identificar um addon, os argumentos pertencem ao RtG-CLI.

Por exemplo:

`rtg --lang`

Mostra os idiomas disponíveis para o RtG-CLI.

Após identificar um addon, os argumentos são interpretados segundo as regras de propriedade estabelecidas para os addons.

Por exemplo:

`rtg image -lang`

Consulta os idiomas disponíveis para o addon `image`.

Desta forma, a posição do argumento determina o seu contexto e evita confundir os argumentos globais do RtG-CLI com os argumentos utilizados após identificar um addon.

---

## 6. Posição dos argumentos do sistema

Os argumentos do sistema não devem aparecer antes do comando ou addon a que afetam quando dito argumento depende desse comando.

Exemplo correto:

`rtg help image -en`

Exemplo incorreto:

`rtg help -en image`

Nestes dois exemplos, o comando do sistema `help` usa esta estrutura, e por isso o segundo está incorreto:
`help <target> <options>`

A posição deve permitir determinar claramente qual comando recebe o argumento.

---

## 7. Comandos e argumentos dos addons

Os comandos são escritos como argumentos individuais do terminal.
Um comando não deve conter espaços sem estar entre aspas.

Os argumentos posteriores podem ser utilizados pelo addon segundo a sua própria interface.

Por exemplo:

`rtg image convert image`

pode ser interpretado como:

- `image` → addon
- `convert` → comando do addon
- `image` → argumento do comando

---

## 8. Uso de hífens em comandos de addons

Após identificar um addon:

- Os argumentos sem hífen pertencem ao addon.
- Os argumentos com dois hífens ou mais (`--`) pertencem ao addon.
- Os argumentos com um único hífen (`-`) pertencem ao RtG-CLI.

Exemplos:

`rtg image convert`
`convert` → addon.

`rtg image --width 128`
`--width` → addon.

`rtg image -lang`
`-lang` → RtG-CLI.

---

## 9. Interface de comandos dos addons

Os comandos específicos de um addon são definidos pelo próprio programa do addon.

O RtG-CLI utiliza a configuração do addon para localizar a sua interface de comandos mediante a propriedade `program commands`.

Esta propriedade contém as rotas dos arquivos que fornecem a interface de comandos do programa.

Exemplo:

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

O RtG-CLI pode utilizar esta interface para conhecer ou executar os comandos disponíveis do addon, mas não deve assumir nem modificar o significado dos seus comandos internos.

O addon pode definir comandos adicionais que não estejam registrados diretamente como comandos próprios do RtG-CLI.

A implementação interna do programa pode ser diferente entre addons, sempre que forneça uma interface compatível com as regras do RtG-CLI.

---

## 10. Idiomas

Os idiomas disponíveis de um addon definem-se mediante a sua configuração.

Exemplo:

`lang: ["es", "en"]`

Os textos traduzidos identificam-se mediante o código correspondente ao idioma.

Exemplo:

`content.pt`
`content.en`

O seletor de idioma utilizado pelo RtG-CLI deve considerar-se um argumento do sistema.

Exemplo:

`rtg help image -en`

---

## 11. Idioma predeterminado

Se não se especifica `-<idioma>`, o RtG-CLI utilizará o primeiro idioma definido em `rules`.
Se se especifica `-<idioma>`, o RtG-CLI utilizará esse idioma se estiver disponível.

O primeiro idioma definido no objeto `rules` do `assets.json` é o idioma predeterminado das regras.

Quando o usuário solicite as regras sem especificar um idioma, o RtG-CLI deve utilizar esse primeiro idioma.

Por exemplo:

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

Neste caso:

`rtg -r`
e
`rtg --rules`

mostrarão as regras em espanhol, porque `es` é o primeiro idioma definido.
Para solicitar outro idioma deve-se utilizar o seu seletor correspondente:

`rtg -r -en`

A ordem dos idiomas dentro de `rules` determina unicamente qual será o idioma predeterminado. Não muda os idiomas disponíveis.

Esta regra também se aplica para outros seletores de idioma como:

`rtg help image -es`

---

## 12. O idioma não muda o comando

Mudar o idioma somente modifica o texto mostrado pelo RtG-CLI.
Não muda o nome interno do comando.

Exemplo:

`rtg help image -es`

e

`rtg help image -en`

seguem fazendo referência ao mesmo comando:

`image`

---

## 13. Ajuda

A ajuda geral obtém-se mediante:

`rtg help`

A ajuda de um comando específico obtém-se mediante:

`rtg help <comando>`

A ajuda pode solicitar-se em um idioma específico:

`rtg help <comando> -<idioma>`

Exemplo:

`rtg help image -en`

---

## 14. Consulta de idiomas

Os idiomas disponíveis para um addon podem consultar-se mediante:

`rtg help <comando> -lang`

Exemplo:

`rtg help image -lang`

Esta opção pertence ao RtG-CLI e não ao addon.

---

## 15. Os addons não devem modificar as regras do sistema

Um addon pode definir seus próprios comandos e argumentos, mas não pode redefinir o significado dos argumentos reservados pelo RtG-CLI.

Por exemplo, um addon não deve utilizar `-h` para dar um significado diferente à ajuda do sistema.
Os nomes reservados pelo RtG-CLI têm prioridade sobre os comandos dos addons.
Os comandos e opções reservados pelo RtG-CLI devem estar definidos explicitamente pela interface do CLI.
Um addon não pode redefinir o comportamento de uma opção reservada.

---

## 16. Separação entre identificação e nome

A chave interna do addon é utilizada para identificá-lo.
O nome do addon somente se utiliza como informação descritiva ou para mostrá-lo ao usuário.

Exemplo:

`image` → identificador interno

`RtG Image` → nome mostrado

Não deve assumir-se que o nome mostrado pode utilizar-se como comando.

---

## 17. Os comandos devem ser determinísticos

O RtG-CLI deve poder determinar se um argumento pertence ao sistema ou ao addon sem depender do nome descritivo do programa.

A interpretação deve basear-se na estrutura e nas regras do comando.

Exemplo:

`rtg help image -en`

deve interpretar-se sempre da mesma maneira:

`rtg` → CLI

`help` → comando do CLI

`image` → addon

`-en` → opção do CLI

---

## 18. Argumentos desconhecidos

Após identificar um addon, o RtG-CLI deve determinar a propriedade de cada argumento segundo o seu prefixo.

- Um argumento sem hífen pertence ao addon.
- Um argumento com dois hífens ou mais (`--`) pertence ao addon.
- Um argumento com um só hífen (`-`) pertence ao RtG-CLI.

Se o RtG-CLI recebe um argumento próprio do sistema que não reconhece, deve informar que a opção não existe.

Os argumentos do addon devem ser entregues ao addon sem que o RtG-CLI tente interpretar o seu significado.

---

## 19. Não assumir comandos que não estejam registrados

O RtG-CLI não deve considerar válido um comando somente porque exista uma pasta, arquivo ou programa relacionado.

O comando deve estar definido na configuração correspondente.

---

## 20. Compatibilidade

Os addons devem respeitar as regras de sintaxe do RtG-CLI para poder integrar-se corretamente.
Um addon pode ter uma implementação interna completamente diferente, mas a sua interface de comandos deve respeitar as regras estabelecidas pelo RtG-CLI.

---

## 21. Regra de prioridade

Após identificar um addon, um só hífen (`-`) está reservado para o RtG-CLI.
Um addon não pode utilizar argumentos que comecem com um só hífen.
Os argumentos que comecem com dois ou mais hífens (`--`) ou que não comecem com hífen pertencem ao addon.

---

## 22. Argumentos do addon

Uma vez identificado o addon, o RtG-CLI não deve assumir o significado dos argumentos específicos do addon.
Os argumentos que pertencem ao addon devem ser entregues ao programa do addon para que este os processe.

Exemplo:

`rtg image --width 128`

O RtG-CLI identifica `image` como addon.
`--width 128` corresponde à interface de RtG Image e deve ser processado por dito addon.

---

## 23. Argumentos com espaços

Os argumentos que contenham espaços devem escrever-se entre aspas para que o terminal os trate como um único argumento.

Exemplo:

`rtg image "C:\Users\User\Downloads\minha imagem.png" "C:\Users\User\Downloads\saida.json"`

A rota completa deve receber-se como um único argumento.

---

## 24. Os argumentos do addon devem conservar-se

O RtG-CLI não deve modificar, eliminar nem reinterpretar argumentos destinados ao addon, salvo quando uma regra explícita do sistema indique o contrário.
Os argumentos devem entregar-se ao addon na ordem em que foram proporcionados pelo usuário.

---

## 25. Exemplos completos

Comando de addon:

`rtg image`

Ajuda:

`rtg help image`

Ajuda em inglês:

`rtg help image -en`

Consultar idiomas:

`rtg help image -lang`

Versão do CLI:

`rtg --version`

Ajuda do CLI:

`rtg --help`

Uma opção própria do addon:

`rtg image --width 128`

Uma opção própria do addon com valor:

`rtg image --output arquivo.json`

Uma combinação:

`rtg image arquivo.png --output arquivo.json`

Neste exemplo:

* `image` identifica o addon.
* `arquivo.png` é um argumento do addon.
* `--output` é uma opção do addon.
* `arquivo.json` é o valor dessa opção.
* Nenhum desses argumentos deve ser interpretado como uma opção do sistema.

---

## 26. Idioma do texto de início

`rtg -language <idioma>` seleciona o idioma do texto de início mostrado pelo RtG-CLI.
O idioma deve existir dentro de `void-language`.

Exemplo:

`rtg -language pt`

mostra o texto definido em:
`void-language.pt`

Se não se especifica `-language`, o RtG-CLI utiliza `void`.
Se o idioma solicitado não está disponível, o RtG-CLI deve informar que esse idioma não está disponível.