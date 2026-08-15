#!/bin/bash
# Docker validation script for PyAuthService
# Checks configuration and runs basic tests

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 PyAuthService Docker Validation${NC}\n"

# 1. Check Docker installation
echo -e "${BLUE}1. Checking Docker installation...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}✅ $DOCKER_VERSION${NC}"
else
    echo -e "${RED}❌ Docker not installed${NC}"
    exit 1
fi

# 2. Check Docker Compose
echo -e "${BLUE}2. Checking Docker Compose...${NC}"
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    echo -e "${GREEN}✅ $COMPOSE_VERSION${NC}"
else
    echo -e "${RED}❌ Docker Compose not installed${NC}"
    exit 1
fi

# 3. Check required files
echo -e "${BLUE}3. Checking required files...${NC}"
REQUIRED_FILES=("Dockerfile" "docker-compose.yml" ".dockerignore" "entrypoint.sh" ".env.example")
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file missing${NC}"
        exit 1
    fi
done

# 4. Check .env file
echo -e "${BLUE}4. Checking environment configuration...${NC}"
if [[ -f ".env" ]]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found, copying from .env.example${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Edit .env with your configuration before running${NC}"
fi

# 5. Check Docker daemon
echo -e "${BLUE}5. Checking Docker daemon...${NC}"
if docker ps &> /dev/null; then
    echo -e "${GREEN}✅ Docker daemon running${NC}"
else
    echo -e "${RED}❌ Docker daemon not accessible${NC}"
    exit 1
fi

# 6. Build Docker image
echo -e "${BLUE}6. Building Docker image...${NC}"
if docker-compose build --quiet; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker image build failed${NC}"
    exit 1
fi

# 7. Syntax check on docker-compose.yml
echo -e "${BLUE}7. Validating docker-compose.yml...${NC}"
if docker-compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✅ docker-compose.yml is valid${NC}"
else
    echo -e "${RED}❌ docker-compose.yml has syntax errors${NC}"
    exit 1
fi

# 8. Check image size
echo -e "${BLUE}8. Checking image size...${NC}"
IMAGE_SIZE=$(docker images | grep pyauthservice | awk '{print $7}')
if [[ -n "$IMAGE_SIZE" ]]; then
    echo -e "${GREEN}✅ Image size: $IMAGE_SIZE${NC}"
else
    echo -e "${YELLOW}⚠️  Could not determine image size${NC}"
fi

# 9. Summary
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ All Docker checks passed!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Customize .env if needed: nano .env"
echo "  2. Start services: docker-compose up -d"
echo "  3. View logs: docker-compose logs -f app"
echo "  4. Access admin: http://localhost:8000/admin"
echo ""
echo -e "${YELLOW}💡 Tip: Use 'make docker-help' to see all available commands${NC}"
echo ""
