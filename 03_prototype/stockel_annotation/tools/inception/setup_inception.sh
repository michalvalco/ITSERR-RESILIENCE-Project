#!/bin/bash
# INCEpTION Setup Script for Stöckel Annotation Project
#
# This script downloads and configures INCEpTION for the annotation work.
# Run this script on your local machine where you have internet access.
#
# Requirements:
# - Java 17+ (Java 21 recommended)
# - ~500MB disk space
# - Port 8080 available (or modify INCEPTION_PORT below)

set -e

INCEPTION_VERSION="39.4"
INCEPTION_JAR="inception-app-webapp-${INCEPTION_VERSION}-standalone.jar"
INCEPTION_URL="https://github.com/inception-project/inception/releases/download/inception-${INCEPTION_VERSION}/${INCEPTION_JAR}"
INCEPTION_HOME="${HOME}/.inception"
INCEPTION_PORT=8080

echo "=============================================="
echo "INCEpTION Setup for Stöckel Annotation Project"
echo "=============================================="
echo ""

# Check Java version
echo "Checking Java installation..."
if ! command -v java &> /dev/null; then
    echo "ERROR: Java is not installed. Please install Java 17 or later."
    echo "  Ubuntu/Debian: sudo apt install openjdk-21-jre"
    echo "  macOS: brew install openjdk@21"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "ERROR: Java 17 or later is required. Found: Java $JAVA_VERSION"
    exit 1
fi
echo "  Java version: OK ($(java -version 2>&1 | head -1))"

# Download INCEpTION if not present
if [ ! -f "$INCEPTION_JAR" ]; then
    echo ""
    echo "Downloading INCEpTION ${INCEPTION_VERSION}..."
    curl -L -o "$INCEPTION_JAR" "$INCEPTION_URL"
    echo "  Download complete: $INCEPTION_JAR"
else
    echo "  INCEpTION JAR already exists: $INCEPTION_JAR"
fi

# Create data directory
echo ""
echo "Creating INCEpTION home directory..."
mkdir -p "$INCEPTION_HOME"
echo "  Data directory: $INCEPTION_HOME"

# Create settings file
SETTINGS_FILE="${INCEPTION_HOME}/settings.properties"
if [ ! -f "$SETTINGS_FILE" ]; then
    echo ""
    echo "Creating settings file..."
    cat > "$SETTINGS_FILE" << EOF
# INCEpTION Settings for Stöckel Annotation Project
# Generated: $(date -Iseconds)

# Server configuration
server.port=${INCEPTION_PORT}

# Database (embedded H2 by default)
database.driver=org.h2.Driver
database.url=jdbc:h2:\${inception.home}/db/inception;MODE=MySQL
database.username=sa
database.password=

# Backup settings
backup.interval=0
backup.keep.number=0

# Disable telemetry
telemetry.enabled=false

# Annotation settings
annotation.default-preferences.scroll-page=true
annotation.default-preferences.editor=cwanno
EOF
    echo "  Settings file created: $SETTINGS_FILE"
else
    echo "  Settings file already exists: $SETTINGS_FILE"
fi

# Create startup script
echo ""
echo "Creating startup script..."
cat > start_inception.sh << 'EOF'
#!/bin/bash
# Start INCEpTION annotation server
# Access at: http://localhost:8080

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

JAR_FILE=$(ls inception-app-webapp-*-standalone.jar 2>/dev/null | head -1)
if [ -z "$JAR_FILE" ]; then
    echo "ERROR: INCEpTION JAR file not found. Run setup_inception.sh first."
    exit 1
fi

echo "Starting INCEpTION..."
echo "Access at: http://localhost:8080"
echo "Default credentials: admin / admin"
echo "Press Ctrl+C to stop the server."
echo ""

java -jar "$JAR_FILE"
EOF
chmod +x start_inception.sh
echo "  Startup script created: start_inception.sh"

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "To start INCEpTION:"
echo "  ./start_inception.sh"
echo ""
echo "Then open: http://localhost:${INCEPTION_PORT}"
echo "Default login: admin / admin"
echo ""
echo "Next steps:"
echo "  1. Start INCEpTION with ./start_inception.sh"
echo "  2. Log in as admin"
echo "  3. Create a new project for Stöckel corpus"
echo "  4. Import text files from ../data/normalized/"
echo "  5. Configure annotation layers (see ANNOTATION_SETUP.md)"
echo ""
