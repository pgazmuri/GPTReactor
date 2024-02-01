@echo off
setx /M AZURE_OPENAI_KEY c454ae3711e64a1d968cd5d4378d7bc2
setx /M AZURE_OPENAI_ENDPOINT https://pgazmurioai-west.openai.azure.com/

# Correct the import paths for Basket.css and BasketItemCard.css or create them if they don't exist
python ./cg_error_fix.py --user_request "Error: Can't resolve './Basket.css' and './BasketItemCard.css'. Ensure these files exist and the import paths are correct." --code_path ../packages/web-app/src/components/POS/Basket.tsx
python ./cg_error_fix.py --user_request "Error: Can't resolve './BasketItemCard.css'. Ensure this file exists and the import path is correct." --code_path ../packages/web-app/src/components/POS/BasketItemCard.tsx

# Update the usage of the <Totals /> component to include all required props according to its type definition
python ./cg_error_fix.py --user_request "Fix the error" --code_path ../packages/web-app/src/pages/POS/POS.tsx