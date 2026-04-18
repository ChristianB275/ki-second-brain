#!/usr/bin/env bash
# KI OS Sync — liest alle Workspace status.yaml und vergleicht mit KI-OS Stubs
# Aufruf: bash scripts/sync-brain.sh
# Wird automatisch bei /start ausgefuehrt

WORKSPACES_DIR="/Users/christian/Desktop/Claude/workspaces"
KIOS_DIR="/Users/christian/Desktop/Claude/ki_second_brain"
STUBS_DIR="$KIOS_DIR/04-projects"

echo ""
echo "=== KI OS Sync Check — $(date '+%Y-%m-%d %H:%M') ==="
echo ""

DRIFT_COUNT=0
SYNC_COUNT=0

for WORKSPACE in "$WORKSPACES_DIR"/claude-workspace-*/; do
    # Vorlage ueberspringen
    [[ "$WORKSPACE" == *"vorlage"* ]] && continue

    STATUS_FILE="$WORKSPACE/status.yaml"
    WS_NAME=$(basename "$WORKSPACE")

    if [ ! -f "$STATUS_FILE" ]; then
        echo "  FEHLT  $WS_NAME — keine status.yaml"
        DRIFT_COUNT=$((DRIFT_COUNT + 1))
        continue
    fi

    # YAML-Felder parsen (nur grep + awk — kein Python, kein yq)
    PROJEKT=$(grep "^projekt:" "$STATUS_FILE" | awk -F': ' '{print $2}' | tr -d '"' | tr -d "'" | xargs)
    WS_STATUS=$(grep "^status:" "$STATUS_FILE" | awk -F': ' '{print $2}' | tr -d '"' | tr -d "'" | xargs)
    FORTSCHRITT=$(grep "^fortschritt:" "$STATUS_FILE" | awk -F': ' '{print $2}' | tr -d '"' | tr -d "'" | xargs)
    LETZTES_UPDATE=$(grep "^letztes-update:" "$STATUS_FILE" | awk -F': ' '{print $2}' | tr -d '"' | tr -d "'" | xargs)
    NAECHSTER=$(grep "^naechster-schritt:" "$STATUS_FILE" | sed "s/naechster-schritt: //" | tr -d '"' | xargs)

    if [ -z "$PROJEKT" ]; then
        echo "  FEHLER $WS_NAME — kein 'projekt:' Feld in status.yaml"
        DRIFT_COUNT=$((DRIFT_COUNT + 1))
        continue
    fi

    # Passenden Stub finden (sucht in allen README-Dateien nach projekt: <name>)
    STUB_FILE=$(grep -rl "^projekt: $PROJEKT" "$STUBS_DIR" 2>/dev/null | head -1)

    if [ -z "$STUB_FILE" ]; then
        echo "  NEU    $PROJEKT — kein Stub in 04-projects/ vorhanden"
        echo "         Workspace: $WS_STATUS / $FORTSCHRITT% (Stand: $LETZTES_UPDATE)"
        DRIFT_COUNT=$((DRIFT_COUNT + 1))
        continue
    fi

    # Stub-Status lesen (aus YAML-Frontmatter)
    STUB_STATUS=$(grep "^status:" "$STUB_FILE" | head -1 | awk -F': ' '{print $2}' | tr -d '"' | tr -d "'" | xargs)
    STUB_FORTSCHRITT=$(grep "^fortschritt:" "$STUB_FILE" | head -1 | awk -F': ' '{print $2}' | tr -d '"' | tr -d "'" | xargs)

    # Vergleich
    if [ "$WS_STATUS" = "$STUB_STATUS" ] && [ "$FORTSCHRITT" = "$STUB_FORTSCHRITT" ]; then
        echo "  OK     $PROJEKT — $WS_STATUS / $FORTSCHRITT% (Stand: $LETZTES_UPDATE)"
        SYNC_COUNT=$((SYNC_COUNT + 1))
    else
        echo "  DRIFT  $PROJEKT"
        echo "         Workspace: $WS_STATUS / $FORTSCHRITT% | Stub: $STUB_STATUS / $STUB_FORTSCHRITT%"
        echo "         Naechster Schritt: $NAECHSTER"
        DRIFT_COUNT=$((DRIFT_COUNT + 1))
    fi
done

echo ""
if [ "$DRIFT_COUNT" -eq 0 ]; then
    echo "Alle $SYNC_COUNT Projekte synchron. ✓"
else
    echo "$SYNC_COUNT synchron — $DRIFT_COUNT Abweichung(en) gefunden."
    echo "Stubs werden von Claude bei /start automatisch aktualisiert."
fi
echo ""
