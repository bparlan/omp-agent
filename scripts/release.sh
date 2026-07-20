#!/bin/bash
# OMP AEF Release Script
# Syncs verified dev skills and templates to the consumer production root

echo "Initiating OMP AEF Release..."

# 1. Sync Skills (Delete old files in consumer that no longer exist in dev)
rsync -av --delete ~/devcode/aef/agent/skills/ ~/devcode/aef/skills/

# 2. Sync Templates
rsync -av --delete ~/devcode/aef/agent/templates/ ~/devcode/aef/templates/

# 3. Fix Pathing for Consumer Context
# Re-paths the consumer skills to point to the consumer templates folder
find ~/devcode/aef/skills -type f -name "*.md" -exec sed -i '' 's|devcode/aef/agent/templates|devcode/aef/templates|g' {} +
find ~/devcode/aef/skills -type f -name "*.md" -exec sed -i '' 's|devcode/aef/agent/skills|devcode/aef/skills|g' {} +

echo "Release complete. Consumer projects can now access the latest framework."
