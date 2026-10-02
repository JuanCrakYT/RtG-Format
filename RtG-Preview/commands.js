#!/usr/bin/env node
"use strict";

const fs = require('fs');
const path = require('path');

const PREVIEW_DIR = path.dirname(__filename);

function getCommands() {
    return ["open", "help", "version"];
}

function getHelp(command, lang) {
    const helpTexts = {
        "en": {
            "open": "Open RtG Preview in browser.\n\nUsage: rtg preview open [--file <build.json>] [--port <port>]\n\nOptions:\n  --file, -f    RtG build JSON file to preview\n  --port, -p    Port for local server (default: 8080)\n  --help        Show this help",
            "help": "Show help for commands.\n\nUsage: rtg preview help [command]",
            "version": "Show version information.\n\nUsage: rtg preview version",
        },
        "es": {
            "open": "Abrir RtG Preview en el navegador.\n\nUso: rtg preview open [--file <build.json>] [--port <puerto>]\n\nOpciones:\n  --file, -f    Archivo JSON de build RtG para previsualizar\n  --port, -p    Puerto para servidor local (por defecto: 8080)\n  --help        Mostrar esta ayuda",
            "help": "Muestra ayuda para comandos.\n\nUso: rtg preview help [comando]",
            "version": "Muestra información de versión.\n\nUso: rtg preview version",
        },
    };
    lang = lang || "en";
    if (!helpTexts[lang]) lang = "en";
    return helpTexts[lang][command] || null;
}

function showVersion() {
    const packageJson = path.join(PREVIEW_DIR, "package.json");
    let version = "0.7.8";
    if (fs.existsSync(packageJson)) {
        try {
            const pkg = JSON.parse(fs.readFileSync(packageJson, "utf-8"));
            version = pkg.version || version;
        } catch (e) {}
    }
    console.log(`RtG Preview v${version}`);
}

function openPreview(args) {
    const parsed = parseArgs(args);
    if (parsed.help) {
        console.log(getHelp("open", parsed.lang));
        return 0;
    }

    // For now, just show info about how to use the preview
    console.log("RtG Preview - Browser-based build viewer");
    console.log();
    console.log("To use RtG Preview:");
    console.log("1. Open preview.html in a web browser");
    console.log("2. Load your RtG build JSON file");
    console.log();
    console.log("Preview files are located in:");
    console.log(`  ${PREVIEW_DIR}`);
    console.log();
    console.log("For programmatic use, you can serve the preview directory:");
    console.log(`  npx serve ${PREVIEW_DIR} -p 8080`);
    console.log("Then open http://localhost:8080/preview.html");

    return 0;
}

function parseArgs(args) {
    const result = { help: false, lang: null, file: null, port: 8080 };
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === "--help" || arg === "-h") {
            result.help = true;
        } else if (arg === "--lang" && i + 1 < args.length) {
            result.lang = args[++i];
        } else if ((arg === "--file" || arg === "-f") && i + 1 < args.length) {
            result.file = args[++i];
        } else if ((arg === "--port" || arg === "-p") && i + 1 < args.length) {
            result.port = parseInt(args[++i], 10);
        }
    }
    return result;
}

function execute(args) {
    if (!args || args.length === 0) {
        console.log("RtG Preview - Browser-based RtG build viewer");
        console.log();
        console.log("Commands:");
        console.log("  open      Open preview (shows instructions)");
        console.log("  help      Show help");
        console.log("  version   Show version");
        console.log();
        console.log("Use 'rtg preview help <command>' for more information.");
        return 0;
    }

    const command = args[0];
    const cmdArgs = args.slice(1);

    switch (command) {
        case "help":
            if (cmdArgs.length > 0) {
                const help = getHelp(cmdArgs[0], null);
                if (help) console.log(help);
                else console.log(`No help available for '${cmdArgs[0]}'`);
            } else {
                console.log("RtG Preview - Browser-based RtG build viewer");
                console.log();
                console.log("Commands:");
                console.log("  open      Open preview (shows instructions)");
                console.log("  help      Show help");
                console.log("  version   Show version");
            }
            return 0;

        case "version":
            showVersion();
            return 0;

        case "open":
            return openPreview(cmdArgs);

        default:
            console.error(`Unknown command: ${command}`);
            console.error("Available commands: open, help, version");
            return 1;
    }
}

if (require.main === module) {
    process.exit(execute(process.argv.slice(2)));
}

module.exports = { execute, getCommands, getHelp };