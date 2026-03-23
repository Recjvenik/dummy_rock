#!/bin/bash
# Quick setup script for Learning Resources feature

echo "\ud83c\udf93 Setting up Learning Resources Feature..."
echo ""

cd "/home/ravi/latest project repo/RESREACH_PROJECTS/AL_ML_TECH_DASHBOARD"

echo "1\ufe0f\u20e3 Creating database migrations..."
python3 manage.py makemigrations modules

echo ""
echo "2\ufe0f\u20e3 Running migrations..."
python3 manage.py migrate

echo ""
echo "3\ufe0f\u20e3 Seeding curated learning resources..."
python3 manage.py seed_resources

echo ""
echo "\u2705 Setup complete!"
echo ""
echo "\ud83d\ude80 Next steps:"
echo "   1. Restart your Django server: ./start.sh"
echo "   2. Visit any module page (e.g., /learn/ai-basics/)"
echo "   3. Click the '\ud83c\udf93 Resources' tab"
echo ""
echo "\ud83d\udcda Students now have access to 28+ curated learning resources!"
