RtG-CLI — Help
===============

RtG-CLI is the command-line interface for the RtG-Format ecosystem.
It allows discovering and executing addons, querying languages, viewing rules and version.

Usage
-----

  rtg [OPTIONS] <COMMAND> [ARGUMENTS]

  The first argument identifies the command or addon to execute.

  Examples:
    rtg image
    rtg preview
    rtg help image


System Commands
----------------

  -h, --help        Show this general help
  -v, --version     Show RtG-CLI version
  -l, --lang        List available languages in RtG-CLI
  -r, --rules       Show RtG-CLI rules
  -c, --commands    List RtG-CLI internal commands
  -a, --addons      List addons with user-visible documentation
  -language <lang>  Set the startup (void) text language

Command: help
--------------

  rtg help                    # General help (this screen)
  rtg help <command>          # Help for a specific command/addon
  rtg help <command> -<lang>  # Help in specific language (e.g. -es, -en)
  rtg help <command> -lang      # Available languages for that command

  Examples:
    rtg help image
    rtg help image -en
    rtg help image -lang


Command: version
-----------------

  rtg -v
  rtg --version

  Shows version and version content in all available languages.


Command: rules
---------------

  rtg -r
  rtg --rules
  rtg -r -<lang>   # Rules in specific language (e.g. rtg -r -en)

  Defaults to first language defined in 'rules' (Spanish).


Command: lang
--------------

  rtg -l
  rtg --lang

  Lists all available languages organized by category:
  Version, Rules, Help, Void, and per addon.


Command: commands
------------------

  rtg -c
  rtg --commands

  Lists exclusively RtG-CLI internal commands.
  Does not include addon commands.


Command: addons
----------------

  rtg -a
  rtg --addons

  Lists addons that have user-visible documentation/help.
  A registered addon without documentation does not appear here.


Command: language
------------------

  rtg -language <language>

  Selects the language of the startup (void) text.
  The language must exist in 'void-language' in assets.json.

  Example:
    rtg -language en


Available Addons
-----------------

  image      | RtG Image        - Image converter
  preview    | RtG Preview      - 3D viewer for RtG-Format builds
  test-addon | RtG Test Addon   - Test addon for CLI validation


Languages
----------

Languages are indicated with a single hyphen: -es, -en, -pt, etc.
The language does not change the internal command name.

  rtg help image -es    # Help in Spanish
  rtg help image -en    # Help in English
  rtg -r -en            # Rules in English

  To view languages for an addon:
    rtg help image -lang

  The meaning of -lang depends on its position:
    rtg --lang          # RtG-CLI languages (before addon)
    rtg image -lang     # Addon languages (after addon)


Addon Arguments
----------------

After identifying an addon, arguments are classified by prefix:

  no hyphen       -> addon        (e.g. convert, file.png)
  --option        -> addon        (e.g. --width 128)
  -option         -> RtG-CLI      (e.g. -lang, -en)

Examples:
  rtg image convert file.png     # convert, file.png -> addon
  rtg image --width 128          # --width 128 -> addon
  rtg image -lang                # -lang -> RtG-CLI (addon languages)
  rtg image -en                  # -en -> RtG-CLI (language selector)


Arguments with Spaces
----------------------

Arguments containing spaces must be quoted:

  rtg image "my image.png" "output.json"

RtG-CLI preserves argument order and passes them as-is to the addon.


More Information
-----------------

  rtg help <command>      # Detailed help for an addon
  rtg help <command> -lang  # Languages for that addon
  rtg --addons            # View all documented addons
  rtg --commands          # View internal commands