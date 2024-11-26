#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Compteurs globaux
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Compteurs par catégorie
declare -A CATEGORY_TESTS
declare -A CATEGORY_PASSED
declare -A CATEGORY_FAILED

# Configuration
export HBNB_MYSQL_USER="hbnb_dev"
export HBNB_MYSQL_PWD="hbnb_dev_pwd"
export HBNB_MYSQL_HOST="localhost"
export HBNB_MYSQL_DB="hbnb_dev_db"
export HBNB_TYPE_STORAGE="db"

# Fonctions helper
log_test() {
   local category=$1
   local description=$2
   local status=$3
   local response=$4
   local expected=$5

   ((TESTS_TOTAL++))
   ((CATEGORY_TESTS[$category]++))

   if [ $status -eq 0 ]; then
       ((TESTS_PASSED++))
       ((CATEGORY_PASSED[$category]++))
       echo -e "${GREEN}✓ $description${NC}"
   else
       ((TESTS_FAILED++))
       ((CATEGORY_FAILED[$category]++))
       echo -e "${RED}✗ $description${NC}"
       echo -e "${RED}Response: $response${NC}"
       if [ ! -z "$expected" ]; then
           echo -e "${RED}Expected: $expected${NC}"
       fi
   fi
}

test_endpoint() {
   local category=$1
   local description=$2
   local command=$3
   local expected_code=$4
   local expected_response=$5

   echo -e "\n${BLUE}Testing: $description${NC}"
   response=$(eval $command)
   status_code=$?

   if [ "$status_code" -eq "$expected_code" ] && 
      { [ -z "$expected_response" ] || [[ "$response" == *"$expected_response"* ]]; }; then
       log_test "$category" "$description" 0 "$response" "$expected_response"
       return 0
   else
       log_test "$category" "$description" 1 "$response" "$expected_response"
       return 1
   fi
}

cleanup_db() {
   echo -e "${YELLOW}Nettoyage base de données...${NC}"
   mysql -u$HBNB_MYSQL_USER -p$HBNB_MYSQL_PWD $HBNB_MYSQL_DB -e "
       SET FOREIGN_KEY_CHECKS = 0;
       TRUNCATE TABLE reviews;
       TRUNCATE TABLE place_amenity;
       TRUNCATE TABLE places;
       TRUNCATE TABLE cities;
       TRUNCATE TABLE states;
       TRUNCATE TABLE users;
       TRUNCATE TABLE amenities;
       SET FOREIGN_KEY_CHECKS = 1;
   " 2>/dev/null
}

print_category_report() {
   local category=$1
   local total=${CATEGORY_TESTS[$category]}
   local passed=${CATEGORY_PASSED[$category]}
   local failed=${CATEGORY_FAILED[$category]}
   local coverage=0

   if [ $total -gt 0 ]; then
       coverage=$(( passed * 100 / total ))
   fi

   echo -e "${PURPLE}=== $category ===${NC}"
   echo -e "Tests: $total"
   echo -e "Réussis: ${GREEN}$passed${NC}"
   echo -e "Échoués: ${RED}$failed${NC}"
   echo -e "Couverture: ${YELLOW}$coverage%${NC}\n"
}

# Début des tests
echo -e "${BLUE}=== Début des tests HBNB complets ===${NC}\n"
cleanup_db

# 1. Tests de base
test_endpoint "Base" "Status API" "curl -s http://0.0.0.0:5000/api/v1/status" 0 '{"status":"OK"}'
test_endpoint "Base" "Statistiques" "curl -s http://0.0.0.0:5000/api/v1/stats" 0

# 2. Tests User
echo -e "\n${BLUE}=== Tests User ===${NC}"
USER_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/users \
   -H "Content-Type: application/json" \
   -d '{
       "email": "test@test.com",
       "password": "test123",
       "first_name": "Test",
       "last_name": "User"
   }')
USER_ID=$(echo $USER_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

test_endpoint "User" "Création utilisateur valide" "echo '$USER_CREATE'" 0 "id"
test_endpoint "User" "Email invalide" "curl -s -X POST http://0.0.0.0:5000/api/v1/users -H 'Content-Type: application/json' -d '{\"email\":\"invalid\",\"password\":\"test\"}'" 0 "error"
test_endpoint "User" "Password manquant" "curl -s -X POST http://0.0.0.0:5000/api/v1/users -H 'Content-Type: application/json' -d '{\"email\":\"test@test.com\"}'" 0 "Missing password"
# 3. Tests State et City
echo -e "\n${BLUE}=== Tests State et City ===${NC}"
STATE_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/states \
   -H "Content-Type: application/json" \
   -d '{"name": "California"}')
STATE_ID=$(echo $STATE_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

test_endpoint "State" "Création State" "echo '$STATE_CREATE'" 0 "id"

if [ ! -z "$STATE_ID" ]; then
   CITY_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/states/$STATE_ID/cities \
       -H "Content-Type: application/json" \
       -d '{"name": "San Francisco"}')
   CITY_ID=$(echo $CITY_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
   
   test_endpoint "City" "Création City" "echo '$CITY_CREATE'" 0 "id"
   test_endpoint "City" "Get cities d'un state" "curl -s http://0.0.0.0:5000/api/v1/states/$STATE_ID/cities" 0
fi

# 4. Tests Place
echo -e "\n${BLUE}=== Tests Place ===${NC}"
if [ ! -z "$CITY_ID" ] && [ ! -z "$USER_ID" ]; then
   PLACE_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/cities/$CITY_ID/places \
       -H "Content-Type: application/json" \
       -d "{
           \"user_id\": \"$USER_ID\",
           \"name\": \"Beautiful House\",
           \"description\": \"Nice view\",
           \"number_rooms\": 3,
           \"number_bathrooms\": 2,
           \"max_guest\": 6,
           \"price_by_night\": 100
       }")
   PLACE_ID=$(echo $PLACE_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
   
   test_endpoint "Place" "Création Place" "echo '$PLACE_CREATE'" 0 "id"
   
   # Test mise à jour
   if [ ! -z "$PLACE_ID" ]; then
       test_endpoint "Place" "Update Place" "curl -s -X PUT http://0.0.0.0:5000/api/v1/places/$PLACE_ID -H 'Content-Type: application/json' -d '{\"name\":\"Updated House\"}'" 0
   fi
fi

# 5. Tests Amenity et Many-to-Many
echo -e "\n${BLUE}=== Tests Amenity et Relations ===${NC}"
AMENITY1_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/amenities \
   -H "Content-Type: application/json" \
   -d '{"name": "WiFi"}')
AMENITY1_ID=$(echo $AMENITY1_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

AMENITY2_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/amenities \
   -H "Content-Type: application/json" \
   -d '{"name": "Pool"}')
AMENITY2_ID=$(echo $AMENITY2_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")

test_endpoint "Amenity" "Création Amenity1" "echo '$AMENITY1_CREATE'" 0 "id"
test_endpoint "Amenity" "Création Amenity2" "echo '$AMENITY2_CREATE'" 0 "id"

if [ ! -z "$PLACE_ID" ] && [ ! -z "$AMENITY1_ID" ]; then
   test_endpoint "Relations" "Link Amenity-Place" "curl -s -X POST http://0.0.0.0:5000/api/v1/places/$PLACE_ID/amenities/$AMENITY1_ID" 0
   test_endpoint "Relations" "Get Place Amenities" "curl -s http://0.0.0.0:5000/api/v1/places/$PLACE_ID/amenities" 0
fi

# 6. Tests Review
echo -e "\n${BLUE}=== Tests Review ===${NC}"
if [ ! -z "$PLACE_ID" ] && [ ! -z "$USER_ID" ]; then
   REVIEW_CREATE=$(curl -s -X POST http://0.0.0.0:5000/api/v1/places/$PLACE_ID/reviews \
       -H "Content-Type: application/json" \
       -d "{
           \"user_id\": \"$USER_ID\",
           \"text\": \"Amazing place!\"
       }")
   REVIEW_ID=$(echo $REVIEW_CREATE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
   
   test_endpoint "Review" "Création Review" "echo '$REVIEW_CREATE'" 0 "id"
   test_endpoint "Review" "Get Reviews" "curl -s http://0.0.0.0:5000/api/v1/places/$PLACE_ID/reviews" 0
fi

# 7. Tests Search
echo -e "\n${BLUE}=== Tests Search ===${NC}"
test_endpoint "Search" "Search simple" "curl -s -X POST http://0.0.0.0:5000/api/v1/places_search -H 'Content-Type: application/json' -d '{}'" 0

if [ ! -z "$STATE_ID" ] && [ ! -z "$CITY_ID" ] && [ ! -z "$AMENITY1_ID" ]; then
   test_endpoint "Search" "Search avec filtres" "curl -s -X POST http://0.0.0.0:5000/api/v1/places_search -H 'Content-Type: application/json' -d '{\"states\":[\"$STATE_ID\"],\"cities\":[\"$CITY_ID\"],\"amenities\":[\"$AMENITY1_ID\"]}'" 0
fi

# 8. Tests Cascade Delete
echo -e "\n${BLUE}=== Tests Delete Cascade ===${NC}"
if [ ! -z "$STATE_ID" ]; then
   test_endpoint "Delete" "Delete State" "curl -s -X DELETE http://0.0.0.0:5000/api/v1/states/$STATE_ID" 0 "{}"
fi

# Rapport final détaillé
echo -e "\n${PURPLE}=== Rapport Final Détaillé ===${NC}\n"

# Rapport par catégorie
for category in "Base" "User" "State" "City" "Place" "Amenity" "Relations" "Review" "Search" "Delete"; do
   if [ ${CATEGORY_TESTS[$category]+_} ]; then
       print_category_report "$category"
   fi
done

# Synthèse globale
echo -e "${BLUE}=== Synthèse Globale ===${NC}"
echo -e "Total tests exécutés: ${YELLOW}$TESTS_TOTAL${NC}"
echo -e "Tests réussis: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests échoués: ${RED}$TESTS_FAILED${NC}"
coverage=$(( TESTS_PASSED * 100 / TESTS_TOTAL ))
echo -e "Couverture globale: ${YELLOW}$coverage%${NC}\n"

# Liste des endpoints non testés ou échoués
if [ $TESTS_FAILED -gt 0 ]; then
   echo -e "${RED}Endpoints à vérifier :${NC}"
   for category in "${!CATEGORY_FAILED[@]}"; do
       if [ ${CATEGORY_FAILED[$category]} -gt 0 ]; then
           echo -e "- $category: ${CATEGORY_FAILED[$category]} échecs"
       fi
   done
fi

# Nettoyage final
cleanup_db
echo -e "\n${YELLOW}Nettoyage final effectué${NC}"

exit $TESTS_FAILED