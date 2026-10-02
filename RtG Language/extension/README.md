# RtG-Language VS Code Extension

This extension provides language support for **RtG-Language 2.0** (.rtg files) in Visual Studio Code.

## Features

- **Syntax Highlighting** - Full syntax highlighting for RtG-Language 2.0
- **Snippets** - Ready-to-use snippets for common RtG-Language constructs
- **Language Configuration** - Auto-closing pairs, brackets, comments
- **File Icon** - Custom icon for .rtg files

## Supported Syntax

The extension supports the RtG-Language 2.0 syntax as defined in the [RtG Language Specification](https://github.com/JuanCrakYT/RtG-Format/tree/main/RtG%20Language/docs).

### Keywords
- `rtg` - Version declaration
- `schema` - Schema import
- `object` - Object section
- `instance` - Instance declaration
- `as` - Instance alias
- `connect` - Connection declaration
- `localType` - Connection local type
- `point` - Connection point
- `uuid` - UUID reference
- `properties` - Properties block
- `attachment` - Ephemeral attachment
- `on` - Attachment parent
- `partName` - Attachment part name
- `cframe` - CFrame transformation
- `output` - Output declaration
- `source` - Schema/output source
- `file` - Output file path

### Snippets

| Prefix | Description |
|--------|-------------|
| `rtg` | Complete RtG-Language 2.0 file template |
| `instance` | Instance declaration |
| `connect` | Connection declaration |
| `attachment` | Attachment declaration |

## Installation

### From VSIX (Recommended)

1. Download the latest `.vsix` from the [GitHub Releases](https://github.com/JuanCrakYT/RtG-Format/releases)
2. In VS Code, open the Command Palette (`Ctrl+Shift+P`)
3. Run `Extensions: Install from VSIX...`
4. Select the downloaded `.vsix` file

### From Source

```bash
cd RtG Language/extension
npm install
vsce package
code --install-extension rtg-language-0.1.0.vsix
```

## Requirements

- Visual Studio Code 1.80.0 or higher

## License

GPL-3.0-only - See [LICENSE](https://github.com/JuanCrakYT/RtG-Format/blob/main/LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](https://github.com/JuanCrakYT/RtG-Format/blob/main/CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](https://github.com/JuanCrakYT/RtG-Format/blob/main/RtG%20Language/CHANGELOG.md) for release history.