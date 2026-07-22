import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove datalist block
html = re.sub(r'\s*<!-- Datalist for Dose Autocomplete -->\s*<datalist id="dose-options">.*?</datalist>', '', html, flags=re.DOTALL)

# 2. Update dose input in buildHTML
target_input = """<div class="w-full">
                                    <label class="block text-xs font-semibold text-slate-600 mb-1">Dose (Amount/Unit)</label>
                                    <input type="text" id="med-dose-" list="dose-options" value="" class="w-full border border-slate-300 rounded p-2 focus:border-teal-500 outline-none bg-white" placeholder="e.g. 1 tab, 5ml, apply locally">
                                </div>"""

replacement_input = """<div class="w-full relative">
                                    <label class="block text-xs font-semibold text-slate-600 mb-1">Dose (Amount/Unit)</label>
                                    <input type="text" id="med-dose-" onfocus="handleLocalSuggestions('med-dose-', 'dose-suggestions-', 'doses')" oninput="handleLocalSuggestions('med-dose-', 'dose-suggestions-', 'doses')" value="" class="w-full border border-slate-300 rounded p-2 focus:border-teal-500 outline-none bg-white" placeholder="e.g. 1 tab, 5ml, apply locally" autocomplete="off">
                                    <div id="dose-suggestions-" class="hidden absolute left-0 right-0 top-full bg-white border border-slate-200 rounded-b-lg shadow-lg max-h-40 overflow-y-auto z-50 text-xs font-medium divide-y divide-slate-100"></div>
                                </div>"""
html = html.replace(target_input, replacement_input)


# 3. Add doses array to suggestionLists (let's add it at the top of suggestionLists)
target_sug_list = """        const suggestionLists = {"""
replacement_sug_list = """        const suggestionLists = {
            doses: [
                "1 tab",
                "2 tabs",
                "1/2 tab",
                "1 capsule",
                "2 capsules",
                "2.5 ml",
                "5 ml",
                "10 ml",
                "15 ml",
                "1 drop",
                "2 drops",
                "1 puff",
                "2 puffs",
                "1 sachet",
                "1 injection",
                "Apply locally",
                "Apply thin layer",
                "As directed"
            ],"""
html = html.replace(target_sug_list, replacement_sug_list)

# 4. Modify handleLocalSuggestions to show all if empty
target_handle = """            const query = input.value.trim().toLowerCase();
            if (!query) {
                menu.innerHTML = '';
                menu.classList.add('hidden');
                return;
            }

            // Filter array items containing the typed substring characters
            const matches = suggestionLists[listKey].filter(item =>
                item.toLowerCase().includes(query)
            );

            if (matches.length === 0) {"""
replacement_handle = """            const query = input.value.trim().toLowerCase();
            let matches = [];
            
            if (!query) {
                matches = suggestionLists[listKey];
            } else {
                matches = suggestionLists[listKey].filter(item =>
                    item.toLowerCase().includes(query)
                );
            }

            if (!matches || matches.length === 0) {"""
html = html.replace(target_handle, replacement_handle)

# 5. Add clickaway for dose-suggestions
target_clickaway = """            appState.rx.forEach((_, index) => {
                const menu = document.getElementById(med-suggestions-);
                const input = document.getElementById(med-name-);
                if (menu && input && !input.contains(e.target) && !menu.contains(e.target)) {
                    menu.classList.add('hidden');
                }
            });"""
replacement_clickaway = """            appState.rx.forEach((_, index) => {
                const menu = document.getElementById(med-suggestions-);
                const input = document.getElementById(med-name-);
                if (menu && input && !input.contains(e.target) && !menu.contains(e.target)) {
                    menu.classList.add('hidden');
                }
                
                const doseMenu = document.getElementById(dose-suggestions-);
                const doseInput = document.getElementById(med-dose-);
                if (doseMenu && doseInput && !doseInput.contains(e.target) && !doseMenu.contains(e.target)) {
                    doseMenu.classList.add('hidden');
                }
            });"""
html = html.replace(target_clickaway, replacement_clickaway)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Changes applied!")
