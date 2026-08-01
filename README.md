# Checklist

A small GTK4 + Libadwaita checklist application.

## Packaging notes

- Application ID: `com.misterg.checklist`
- Desktop launcher: `com.misterg.checklist.desktop`
- App metadata: `com.misterg.checklist.metainfo.xml`
- Placeholder icon: `assets/com.misterg.checklist.svg`

Persistent tasks are stored in the standard XDG user data directory:

- `~/.local/share/Checklist/tasks.json`

On first launch, the app will automatically import an existing legacy `tasks.json` from the old project-local location if one is present.
