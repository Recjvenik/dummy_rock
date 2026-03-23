#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Activate virtualenv
source venv/bin/activate

echo "══════════════════════════════════════════"
echo "  🧠  AI Lab — Interactive Learning Platform"
echo "══════════════════════════════════════════"

# Run migrations if needed
echo "→ Checking migrations..."
python manage.py migrate --run-syncdb 2>&1 | grep -v "No migrations"

# Seed data if no modules exist
MODULE_COUNT=$(echo "from modules.models import Module; print(Module.objects.count())" | python manage.py shell 2>/dev/null | tail -1)
if [ "$MODULE_COUNT" = "0" ] || [ -z "$MODULE_COUNT" ]; then
    echo "→ Seeding database with AI modules..."
    python manage.py seed_data
fi

# Collect static files
echo "→ Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo ""
echo "✅ Starting AI Lab on http://localhost:8000"
echo "   Admin: http://localhost:8000/admin/ (admin / admin123)"
echo "   Press Ctrl+C to stop"
echo ""

# Start Daphne ASGI server (WebSocket support)
daphne -b 0.0.0.0 -p 8000 ailab.asgi:application
