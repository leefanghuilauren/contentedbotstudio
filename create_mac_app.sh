#!/bin/bash
APP_PATH="$HOME/Desktop/VideoAgent [Studio.app](https://Studio.app)"
PROJECT_DIR="/Users/leefanghui/Desktop/ContentedBot"

mkdir -p "$APP_PATH/Contents/MacOS"
mkdir -p "$APP_PATH/Contents/Resources"

cat > "$APP_PATH/Contents/MacOS/VideoAgent Studio" << INNER
#!/bin/bash
cd "$PROJECT_DIR"
if ! curl -sf http://localhost:11434 > /dev/null 2>&1; then
    ollama serve &
    sleep 3
fi
open http://localhost:8501
streamlit run "$PROJECT_DIR/app.py" --server.port 8501 --server.headless true
INNER

chmod +x "$APP_PATH/Contents/MacOS/VideoAgent Studio"

cat > "$APP_PATH/Contents/Info.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key><string>VideoAgent Studio</string>
    <key>CFBundleDisplayName</key><string>VideoAgent Studio</string>
    <key>CFBundleIdentifier</key><string>com.videoagent.studio</string>
    <key>CFBundleVersion</key><string>1.0</string>
    <key>CFBundleExecutable</key><string>VideoAgent Studio</string>
    <key>LSMinimumSystemVersion</key><string>11.0</string>
</dict>
</plist>
PLIST

echo "✅ VideoAgent Studio icon created on your Desktop!"
echo "Right-click it → Open → Open (first time only)"
