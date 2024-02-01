python cg_comparison_fix.py --user_request "Move the numpad above totals in the rightmost column, move the basket to the middle column, and make the middle column twice as wide as the side columns." --screenshot_url "http://localhost:3000/pos" --comp_path "./working/POS.png" --code_path "../packages/web-app/src/pages/POS/POS.tsx"

python cg_update_fix.py --user_request "Move the numpad above totals in the rightmost column, move the basket to the middle column, and make the middle column twice as wide as the side columns." --screenshot_url "http://localhost:3000/rxs" --code_path "../packages/web-app/src/pages/Rxs/Rxs.tsx"

python cg_orchestrate_update.py --user_request "Review the Prescription controls and the rxs.tsx page, integrate them together intelligently. The rxs page should make use of the prescription list, the prescription list should make use of prescription details and prescription form for adding and editing. Ensure state is wired properly and order your updates locgically." --screenshot_url "http://localhost:3000/rxs"
python cg_update_fix.py --user_request "" --screenshot_url "http://localhost:3000/rxs" --code_path "../packages/web-app/src/pages/Rxs/Rxs.tsx"
