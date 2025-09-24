from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import json
import pandas as pd
import io
import os
from datetime import datetime
import uuid
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import tiktoken
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Token tracking
token_usage = {
    'session_tokens': 0,
    'total_tokens': 0
}

# Load OpenAI API key from environment
openai_api_key = os.getenv('OPENAI_API_KEY', '')
openai.api_key = openai_api_key

# Validate API key on startup
if not openai_api_key:
    print("WARNING: OpenAI API key not found! Please check your .env file.")
    print("Make sure you have a .env file with OPENAI_API_KEY=your_key_here")
else:
    print(f"✅ OpenAI API key loaded: {openai_api_key[:10]}...{openai_api_key[-10:]}")

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count tokens in text using tiktoken"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback estimation
        return len(text.split()) * 1.3

def clean_openai_json_response(response_text):
    """Clean and fix common JSON issues in OpenAI responses"""
    import re
    
    # Remove markdown code blocks
    cleaned = response_text.strip()
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]
    elif cleaned.startswith('```'):
        cleaned = cleaned[3:]
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]
    
    cleaned = cleaned.strip()
    
    # Find JSON boundaries
    start_idx = cleaned.find('{')
    end_idx = cleaned.rfind('}') + 1
    
    if start_idx == -1 or end_idx == 0:
        raise ValueError("No valid JSON object found in response")
    
    json_content = cleaned[start_idx:end_idx]
    
    # Try to fix common issues with quotes in the content
    # This is a simple approach - we'll try to parse as-is first
    try:
        # Test if it parses correctly
        json.loads(json_content)
        return json_content
    except json.JSONDecodeError:
        # If it fails, try some basic fixes
        
        # Fix unescaped newlines in strings
        json_content = re.sub(r'(?<!\\)\n(?=.*"[^"]*$)', '\\n', json_content)
        
        # Try again
        try:
            json.loads(json_content)
            return json_content
        except json.JSONDecodeError:
            # Return as-is and let the caller handle the error
            return json_content

def attempt_json_repair(response_text):
    """Attempt more aggressive JSON repair strategies"""
    import re
    
    try:
        # Start with basic cleaning
        cleaned = clean_openai_json_response(response_text)
        
        # More aggressive repair strategies
        repair_strategies = [
            # Strategy 1: Fix newlines and control characters first
            lambda s: s.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t'),
            
            # Strategy 2: Fix unescaped quotes in code strings
            lambda s: re.sub(r'(:\s*")([^"]*)"([^"]*)"([^"]*)"', r'\1\2\\"\3\\"\4"', s),
            
            # Strategy 3: Fix trailing commas
            lambda s: re.sub(r',(\s*[}\]])', r'\1', s),
            
            # Strategy 4: Try to close unterminated strings
            lambda s: fix_unterminated_strings(s),
            
            # Strategy 5: Fix missing commas
            lambda s: re.sub(r'}(\s*)"', r'},\1"', s),
        ]
        
        current_json = cleaned
        
        for i, strategy in enumerate(repair_strategies):
            try:
                repaired = strategy(current_json)
                json.loads(repaired)  # Test if it parses
                print(f"JSON repair successful with strategy {i+1}")
                return repaired
            except (json.JSONDecodeError, Exception) as e:
                print(f"Strategy {i+1} failed: {e}")
                current_json = repaired if 'repaired' in locals() else current_json
                continue
        
        # If none work, return None
        return None
        
    except Exception as e:
        print(f"JSON repair attempt failed: {e}")
        return None

def fix_unterminated_strings(json_str):
    """Try to fix unterminated strings in JSON"""
    import re
    
    # This is a simple heuristic approach
    # Look for patterns like: "key": "value with unterminated string
    lines = json_str.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Check if line has an unterminated string (odd number of unescaped quotes after colon)
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key_part = parts[0]
                value_part = parts[1].strip()
                
                # Count unescaped quotes in value part
                unescaped_quotes = 0
                i = 0
                while i < len(value_part):
                    if value_part[i] == '"' and (i == 0 or value_part[i-1] != '\\'):
                        unescaped_quotes += 1
                    i += 1
                
                # If odd number of quotes and line doesn't end with quote, try to close it
                if unescaped_quotes % 2 == 1 and not value_part.rstrip().endswith('"'):
                    line = line.rstrip() + '"'
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def parse_structured_response(response_text):
    """Parse structured text response into replica data"""
    import re
    try:
        # Extract theme
        theme_match = re.search(r'THEME:\s*(.+)', response_text)
        raw_theme = theme_match.group(1).strip() if theme_match else "Untitled Theme"
        
        # Clean up theme - remove any "Replica X" text and ensure it's a clean title
        theme = re.sub(r'\s*-?\s*Replica\s*\d*\s*', '', raw_theme, flags=re.IGNORECASE).strip()
        if not theme:
            theme = "Custom Theme"
        
        # Extract HTML
        html_match = re.search(r'HTML_START\s*(.*?)\s*HTML_END', response_text, re.DOTALL)
        html_code = html_match.group(1).strip() if html_match else ""
        
        # Extract CSS  
        css_match = re.search(r'CSS_START\s*(.*?)\s*CSS_END', response_text, re.DOTALL)
        css_code = css_match.group(1).strip() if css_match else ""
        
        # Extract JavaScript
        js_match = re.search(r'JS_START\s*(.*?)\s*JS_END', response_text, re.DOTALL)
        js_code = js_match.group(1).strip() if js_match else ""
        
        # Extract question
        question_match = re.search(r'QUESTION_START\s*(.*?)\s*QUESTION_END', response_text, re.DOTALL)
        question_text = question_match.group(1).strip() if question_match else ""
        
        # Extract test cases
        tests_match = re.search(r'TESTS_START\s*(.*?)\s*TESTS_END', response_text, re.DOTALL)
        test_cases = tests_match.group(1).strip() if tests_match else ""
        
        # Return structured data
        return {
            "short_text": theme,
            "html_code": html_code,
            "css_code": css_code,
            "js_code": js_code,
            "question_text": question_text,
            "test_cases": test_cases,
            "html_solution": html_code,  # Same as html_code
            "css_solution": css_code,    # Same as css_code
            "js_solution": js_code,      # Same as js_code
            "subtopic": "",
            "course": "",
            "module": "",
            "unit": ""
        }
        
    except Exception as e:
        print(f"Error parsing structured response: {e}")
        return None

def load_prompt_template():
    """Load the webcoding-replication-prompt.md file"""
    try:
        with open('../webcoding-replicas-prompt.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
# HTML/CSS/JS Replica Generation Prompt

You are an expert web developer tasked with creating **{{N}}** unique replicas of provided HTML/CSS/JS code. Each replica must maintain identical functionality while featuring distinct visual themes and contextual content.

## Input Placeholders:
```
ORIGINAL_HTML_CODE: {{original_html}}
ORIGINAL_CSS_CODE: {{original_css}}
ORIGINAL_JS_CODE: {{original_js}}
SHORT_TEXT: {{short_description}}
QUESTION_TEXT: {{problem_statement}}
TEST_CASES: {{test_scenarios}}
NUMBER_OF_REPLICAS: {{N}}
```

## Core Requirements:

### 🔧 Structural Preservation
- **Maintain identical layout structure** and DOM hierarchy
- **Preserve all JavaScript functionality** and event handlers
- **Keep responsive design** breakpoints and behavior
- **Maintain accessibility** features and ARIA attributes

### 🎨 Visual Transformation (Required Changes)
- **Color Schemes**: Primary/secondary colors, backgrounds, gradients
- **Typography**: Font families, sizes, weights, line heights
- **Visual Effects**: Shadows, borders, border-radius, opacity
- **Spacing**: Margins, padding, gaps (within 20% variance)
- **Animations**: Transition effects, durations, easing functions
- **UI Components**: Button styles, form elements, cards, icons

### 📝 Content Adaptation
- **Domain Context**: Transform theme (e.g., e-commerce → education → healthcare)
- **Terminology**: Update labels, headings, descriptions while preserving meaning
- **Placeholder Content**: Change examples, sample data, mock text
- **Maintain Logic**: New content must make semantic sense in context

### 🏷️ Technical Updates
- **HTML IDs**: Update to reflect new content context
- **CSS Classes**: Modify class names to match new theme
- **JavaScript Selectors**: Update all DOM selectors to match new IDs/classes
- **Variable Names**: Rename JavaScript variables for consistency
- **Comments**: Update code comments to reflect changes

## Output Format:

**CRITICAL JSON RULES - FOLLOW EXACTLY**:

1. Return ONLY valid JSON - no text, no markdown, no explanations
2. ALL code must be on single lines with \\n for line breaks
3. ALL quotes in code must be escaped as \\"
4. ALL backslashes must be doubled as \\\\
5. Remove ALL comments from code
6. Minify ALL code (no extra spaces)

**REQUIRED JSON FORMAT:**
{
"replica_1": {
"short_text": "Theme name (no quotes)",
"html_code": "Complete HTML (escaped and minified)",
"css_code": "Complete CSS (escaped and minified)",
"js_code": "Complete JavaScript (escaped and minified)",
"question_text": "Brief modified question (under 300 chars)",
"test_cases": "Test case 1\\nTest case 2\\nTest case 3",
"html_solution": "Same as html_code",
"css_solution": "Same as css_code", 
"js_solution": "Same as js_code",
"subtopic": "",
"course": "",
"module": "",
"unit": ""
}
}

**EXAMPLE ESCAPING:**
- HTML: `<div class="test">` becomes `<div class=\\"test\\">`
- CSS: `.class { color: red; }` becomes `.class { color: red; }`
- JS: `console.log("hello");` becomes `console.log(\\"hello\\");`

Generate **1** replica with a unique theme while preserving exact functionality.
"""

@app.route('/api/health', methods=['GET'])
def health_check():
    api_key_status = "configured" if os.getenv('OPENAI_API_KEY', '') else "not_configured"
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "openai_api_key": api_key_status
    })

@app.route('/api/test-json', methods=['POST'])
def test_json_parsing():
    """Test endpoint to verify JSON parsing works"""
    test_json = '''
    {
        "replica_1": {
            "short_text": "Test Replica",
            "html_code": "<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Hello</h1></body></html>",
            "css_code": "body { font-family: Arial; background: #f0f0f0; }",
            "js_code": "console.log('Hello World');",
            "question_text": "This is a test question",
            "test_cases": "Test case 1: Should work\\nTest case 2: Should also work",
            "html_solution": "Same as html_code",
            "css_solution": "Same as css_code", 
            "js_solution": "Same as js_code",
            "subtopic": "",
            "course": "",
            "module": "",
            "unit": ""
        }
    }
    '''
    
    try:
        cleaned_json = clean_openai_json_response(test_json)
        parsed = json.loads(cleaned_json)
        return jsonify({"success": True, "parsed": parsed})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/token-usage', methods=['GET'])
def get_token_usage():
    return jsonify(token_usage)

@app.route('/api/generate-replicas', methods=['POST'])
def generate_replicas():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['question_text', 'short_text', 'solutions_metadata', 'test_cases', 'replica_type', 'num_replicas']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Extract code from solutions_metadata
        solutions = data['solutions_metadata'][0] if data['solutions_metadata'] else {}
        code_details = solutions.get('code_details', [])
        
        html_code = ""
        css_code = ""
        js_code = ""
        
        for code_detail in code_details:
            if code_detail.get('language') == 'HTML':
                html_code = code_detail.get('code_data', '')
            elif code_detail.get('language') == 'CSS':
                css_code = code_detail.get('code_data', '')
            elif code_detail.get('language') == 'JAVASCRIPT':
                js_code = code_detail.get('code_data', '')
        
        # Format test cases
        test_cases_text = ""
        for test_case in data.get('test_cases', []):
            test_cases_text += f"Test Case {test_case.get('order', '')}: {test_case.get('display_text', '')}\n"
            test_cases_text += f"Criteria: {test_case.get('criteria', '')}\n\n"
        
        # Load and format prompt template
        prompt_template = load_prompt_template()
        
        # Replace placeholders in prompt
        formatted_prompt = prompt_template.replace('{{original_html}}', html_code)
        formatted_prompt = formatted_prompt.replace('{{original_css}}', css_code)
        formatted_prompt = formatted_prompt.replace('{{original_js}}', js_code)
        formatted_prompt = formatted_prompt.replace('{{short_description}}', data['short_text'])
        formatted_prompt = formatted_prompt.replace('{{problem_statement}}', data['question_text'])
        formatted_prompt = formatted_prompt.replace('{{test_scenarios}}', test_cases_text)
        formatted_prompt = formatted_prompt.replace('{{N}}', str(data['num_replicas']))
        
        # Count input tokens
        input_tokens = count_tokens(formatted_prompt)
        
        # Call OpenAI API
        current_api_key = os.getenv('OPENAI_API_KEY', '')
        if not current_api_key:
            print("ERROR: OpenAI API key not found in environment!")
            return jsonify({"error": "OpenAI API key not configured"}), 500

        print(f"Making OpenAI API call with key: {current_api_key[:10]}...")

        # Define diverse themes for each replica with context-specific content
        themes =[
  "Coffee Shop Manager", "Pizza Restaurant", "Bakery Counter", "Grocery Store",
  "Bookstore Inventory", "Game Store", "Electronics Shop", "Fashion Boutique",
  "Pet Store Manager", "Flower Shop", "Music Store", "Art Gallery",
  "Sports Equipment", "Candy Store", "Toy Shop", "Pharmacy Counter",
  "Hardware Store", "Car Rental", "Hotel Booking", "Travel Agency",
  "Fitness Gym", "Restaurant Menu", "Library System", "Movie Theater",
  "School Supplies", "Photography Studio", "Beauty Salon", "Laundromat",
  "Ice Cream Parlor", "Juice Bar", "Bike Rental", "Camping Gear",
  "Wedding Planner", "Food Truck", "Antique Shop", "Craft Store",
  "Supermarket Chain", "Farmers Market", "Butcher Shop", "Seafood Market",
  "Book Café", "Tattoo Studio", "Barbershop", "Nail Salon",
  "Daycare Center", "E-learning Platform", "Music Academy", "Dance Studio",
  "Driving School", "Language School", "Martial Arts Dojo", "Cooking Class",
  "Event Venue", "Conference Center", "Coworking Space", "Startup Incubator",
  "Real Estate Agency", "Property Rental", "Interior Design Studio", "Furniture Store",
  "Home Decor Shop", "Lighting Store", "Appliance Store", "Mattress Shop",
  "Garden Center", "Plant Nursery", "Organic Store", "Wine Shop",
  "Brewery Taproom", "Sports Bar", "Nightclub Manager", "Concert Hall",
  "Theater Playhouse", "Amusement Park", "Zoo Management", "Aquarium Center",
  "Theme Park", "Arcade Center", "Escape Room", "Bowling Alley",
  "Skating Rink", "Golf Course", "Tennis Club", "Soccer Academy",
  "Hospital Management", "Clinic Reception", "Dental Office", "Veterinary Clinic",
  "Pharmaceutical Store", "Optical Shop", "Hearing Aid Center", "Rehab Center",
  "Courier Service", "Logistics Hub", "Airline Booking", "Shipping Company",
  "Taxi Service", "Ride Sharing", "Parking Garage", "Fuel Station",
  "Tech Repair Shop", "Mobile Store", "Laptop Store", "Watch Boutique",
  "Jewelry Store", "Perfume Shop", "Handbag Boutique", "Shoe Store",
  "Surf Shop", "Diving Center", "Ski Resort", "Snowboard Shop",
  "Mountain Guide", "Hiking Supplies", "Fishing Store", "Hunting Shop",
  "Board Game Café", "VR Arcade", "Esports Arena", "Streaming Studio",
  "Podcast Studio", "Radio Station", "TV Channel Manager", "Film Production",
  "Animation Studio", "Advertising Agency", "Consulting Firm", "HR Platform",
  "Payroll Service", "Law Firm", "Notary Office", "Insurance Agency",
  "Bank Branch", "Stock Brokerage", "Investment Firm", "Cryptocurrency Exchange",
  "Charity Organization", "NGO Manager", "Volunteer Center", "Community Center",
  "Religious Organization", "Church Management", "Mosque Administration", "Temple Management",
  "Resort Manager", "Holiday Park", "Hostel Manager", "Bed and Breakfast",
  "Vacation Rentals", "Timeshare Service", "RV Rental", "Yacht Rental",
  "Cruise Line", "Train Service", "Metro Station", "Bus Depot",
  "Trucking Company", "Warehousing Hub", "Cold Storage", "Freight Forwarding",
  "Drone Delivery", "Postal Service", "Bike Courier", "Farmland Manager",
  "Dairy Farm", "Poultry Farm", "Fishery Farm", "Aquaponics Farm",
  "Greenhouse Farming", "Hydroponics Farm", "Crop Trading", "Fertilizer Shop",
  "Seed Store", "Tractor Rental", "Mining Operations", "Oil Refinery",
  "Solar Energy Plant", "Wind Farm", "Hydropower Plant", "Recycling Plant",
  "Construction Firm", "Architecture Studio", "Cement Factory", "Steel Plant",
  "Clothing Store", "Streetwear Shop", "Sports Apparel", "Tailor Shop",
  "Textile Factory", "Leather Goods", "Accessories Store", "Cap Store",
  "Restaurant Chain", "Buffet Restaurant", "Fine Dining", "Fast Food Outlet",
  "Burger Joint", "Sandwich Shop", "Steakhouse", "Seafood Restaurant",
  "Vegan Café", "Salad Bar", "Soup Kitchen", "Catering Service",
  "Ramen Shop", "Sushi Bar", "Dim Sum Place", "Mexican Cantina",
  "French Bistro", "Greek Taverna", "Turkish Kebab Shop", "Caribbean Restaurant",
  "Cupcake Store", "Donut Shop", "Chocolate Boutique", "Crepe Stand",
  "Pancake House", "Waffle Bar", "Coffee Roastery", "Bubble Tea Shop",
  "Gaming Café", "Internet Café", "Makerspace", "Electronics Repair",
  "Drone Store", "Smart Home Store", "AR Experience Center", "Tech Museum",
  "Airport Duty Free", "Railway Station Shop", "Pop-Up Shop", "Music Festival Manager",
  "Conference Organizer", "Sports League Manager", "Basketball Team", "Baseball Team",
  "Football Club", "Olympics Committee", "Circus Show", "Comedy Club",
  "Medical Research Lab", "Biotech Startup", "Pharma Manufacturing", "Health Insurance",
  "Yoga Studio", "Meditation Center", "Spa Resort", "Ayurveda Clinic",
  "News Agency", "Book Publisher", "Printing Press", "Stationery Shop",
  "Souvenir Shop", "Gift Wrapping Service", "Party Supplies", "Costume Rental",
  "Photo Booth", "DJ Service", "Karaoke Bar", "Open Mic Café",
  "Software Company", "Web Design Agency", "Game Development Studio", "Cloud Hosting",
  "Robotics Startup", "IoT Platform", "Blockchain Startup", "Metaverse Hub",
  "Wildlife Sanctuary", "National Park", "Botanical Garden", "Heritage Site",
  "Science Center", "Planetarium", "Space Observatory", "Rocket Launch Center",
  "City Hall", "Post Office", "Police Department", "Fire Department",
  "Ambulance Service", "Disaster Relief", "Customs Office", "Immigration Service",
  "Military Base", "Airport Security", "Playground", "Water Park",
  "Laser Tag Arena", "Go-Kart Track", "Horse Riding School", "Animal Shelter",
  "Dog Grooming", "Cat Café",
  "Elder Care Home", "Retirement Community", "Boarding School", "University Campus",
  "Student Housing", "Scholarship Fund", "Exam Prep Center", "Research Institute",
  "IT Training Center", "Coding Bootcamp", "Virtual Classroom", "MOOC Platform",
  "Job Portal", "Freelance Marketplace", "Gig Economy Platform", "Remote Work Hub",
  "Interior Landscaping", "Pool Maintenance", "Roofing Company", "Home Renovation",
  "Carpentry Workshop", "Plumbing Services", "Electrical Services", "Solar Installer",
  "Moving Company", "Cleaning Services", "Pest Control", "Security Services",
  "CCTV Store", "Alarm Installation", "Locksmith Services", "Smart Security Hub",
  "Baby Store", "Maternity Shop", "Toy Rental", "Kids Party Planner",
  "Children’s Bookstore", "Comic Convention", "Cosplay Shop", "Boarding Kennel",
  "Pet Daycare", "Pet Hotel", "Exotic Pet Store", "Aquarium Fish Shop",
  "Bird Store", "Reptile Shop", "Pet Grooming School", "Dog Training Center",
  "Organic Bakery", "Gluten-Free Store", "Keto Café", "Protein Bar",
  "Smoothie Shop", "Vegan Market", "Ethnic Grocery", "Spice Shop",
  "Olive Oil Shop", "Cheese Store", "Butcher Deli", "Farm-to-Table Restaurant",
  "Artisan Coffee Roaster", "Craft Brewery", "Whiskey Distillery", "Gin Bar",
  "Cigar Lounge", "Shisha Café", "Hookah Bar", "Wine Tasting Room",
  "Luxury Spa", "Thermal Baths", "Hot Spring Resort", "Detox Center",
  "Pilates Studio", "CrossFit Gym", "Boxing Club", "Climbing Gym",
  "Skateboard Shop", "Roller Rink", "Parkour Gym", "Adventure Park",
  "Drone Racing Arena", "RC Car Track", "Model Train Store", "LEGO Store",
  "3D Printing Service", "Makers Lab", "Prototype Studio", "Electronics Lab",
  "AR Gaming Arena", "Mixed Reality Studio", "Digital Art Gallery", "NFT Marketplace",
  "Crypto Mining Farm", "Token Exchange", "DeFi Platform", "Metaverse Land Agency",
  "Virtual Fashion Boutique", "VR Fitness Studio", "Online Casino", "Sports Betting",
  "Horse Racing Track", "Dog Racing Arena", "Lottery Kiosk", "Bingo Hall",
  "Community Radio", "Indie Film Studio", "Streaming Platform", "Music Label",
  "Talent Scout", "Modeling Agency", "Casting Studio", "Script Writing Agency",
  "Translation Service", "Subtitling Service", "Voiceover Studio", "Dubbing Studio",
  "Content Creation Hub", "Influencer Agency", "Social Media Agency", "SEO Firm",
  "Data Analytics Firm", "AI Consultancy", "ML Research Lab", "Cloud AI Service",
  "Drone Photography", "Aerial Mapping", "Survey Company", "GIS Mapping",
  "Real Estate Drone Tours", "Property Management", "Condominium Manager", "HOA Manager",
  "Urban Planning Firm", "Smart City Platform", "Transport Authority", "Highway Management",
  "Port Authority", "Shipyard", "Harbor Management", "Fisherman’s Wharf",
  "Luxury Car Dealer", "Used Car Dealer", "Motorcycle Shop", "Scooter Rental",
  "EV Charging Station", "EV Rental", "Battery Swap Station", "Green Energy Store",
  "Charcoal Shop", "BBQ Supplies", "Kitchen Equipment Store", "Cooking Oil Shop",
  "Packaging Supplies", "Paper Mill", "Printing Ink Store", "Label Printing",
  "Advertising Print Shop", "Merchandise Store", "Souvenir Kiosk", "Festival Booth",
  "Holiday Decor Store", "Halloween Shop", "Christmas Market", "Fireworks Stand",
  "Gift Basket Store", "Luxury Gifting Service", "Diamond Store", "Gemstone Boutique",
  "Goldsmith", "Silversmith", "Engraving Shop", "Watch Customization",
  "Vintage Car Rental", "Classic Car Restoration", "Motor Garage", "Auto Parts Shop",
  "Tire Shop", "Car Wash", "Detailing Center", "Tow Truck Service",
  "Scrapyard", "Metal Recycling", "E-waste Recycling", "Battery Recycling",
  "Eco-Friendly Products", "Zero Waste Store", "Thrift Shop", "Second-Hand Store",
  "Pawn Broker", "Consignment Store", "Auction House", "Art Auction",
  "Collector’s Shop", "Stamp Shop", "Coin Shop", "Antique Bookstore",
  "Rare Vinyl Store", "Vintage Clothing Shop", "Retro Arcade", "Classic Game Shop"
]

        
        # Shuffle themes to avoid predictable patterns across multiple generations
        import random
        shuffled_themes = themes.copy()
        random.shuffle(shuffled_themes)
        
        # For now, let's generate replicas one at a time to avoid JSON parsing issues
        num_replicas = int(data['num_replicas'])
        all_replicas = {}
        total_output_tokens = 0
        
        for i in range(1, num_replicas + 1):
            # Get a unique theme for this replica
            theme_index = (i - 1) % len(themes)
            selected_theme = themes[theme_index]
            theme_suffix = selected_theme.lower().replace(' ', '-').replace('store', '').replace('shop', '').replace('manager', '').strip('-')
            
            # Create a prompt for just one replica with specific theme
            single_replica_prompt = formatted_prompt.replace(f'**{num_replicas}**', '**1**')
            single_replica_prompt = single_replica_prompt.replace('Generate **{N}** replicas', 'Generate **1** replica')
            
            try:
                # Use a structured text format instead of JSON to avoid parsing issues
                structured_prompt = f"""
Create a web coding replica with the following format:

THEME: {selected_theme}
HTML_START
[complete HTML code with unique IDs based on theme "{theme_suffix}"]
HTML_END
CSS_START
[complete CSS code with matching selectors]  
CSS_END
JS_START
[complete JavaScript code with matching getElementById calls]
JS_END
QUESTION_START
[modified question text with new theme context for "{selected_theme}"]
QUESTION_END
TESTS_START
[test cases separated by newlines, adapted for "{selected_theme}" context]
TESTS_END

CRITICAL REQUIREMENTS FOR "{selected_theme}" THEME:
1. Use theme suffix "{theme_suffix}" in ALL IDs (e.g., calculate-{theme_suffix}, total-{theme_suffix})
2. Transform ALL text content to match "{selected_theme}" context
3. Change labels, headings, and descriptions to fit the theme
4. ALL HTML IDs must match ALL JavaScript getElementById calls exactly
5. Make the UI text contextually relevant to "{selected_theme}"

Example transformations for "{selected_theme}":
- Original: "Calculate Total" -> New: "Calculate {selected_theme} Total"
- Original: id="calculate" -> New: id="calculate-{theme_suffix}"
- Original: "Items" -> New: contextual items for {selected_theme}
- Original: getElementById('total') -> New: getElementById('total-{theme_suffix}')

Original content to transform:
{single_replica_prompt}

Generate exactly ONE replica with "{selected_theme}" theme and consistent ID naming using "{theme_suffix}" suffix.
"""
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"""You are a web developer who creates themed code replicas with completely unique contexts.

MANDATORY REQUIREMENTS FOR "{selected_theme}" THEME:
1. Transform ALL text content to match "{selected_theme}" context exactly
2. Use ONLY IDs with "{theme_suffix}" suffix (e.g., 'calculate-{theme_suffix}', 'total-{theme_suffix}')
3. ALL HTML element IDs must use the "{theme_suffix}" suffix consistently  
4. ALL JavaScript getElementById calls must match HTML IDs exactly
5. Replace ALL labels, headings, and UI text to fit "{selected_theme}" context
6. Make the entire interface contextually relevant to "{selected_theme}"

CONTENT TRANSFORMATION RULES:
- Change "Calculate" to "Calculate for {selected_theme}"
- Change "Items" to contextual items (e.g., "Products", "Books", "Coffees")
- Change "Total" to "{selected_theme} Total" 
- Adapt all text to be meaningful in "{selected_theme}" context

ID CONSISTENCY RULES:
- HTML: id="calculate-{theme_suffix}"
- JavaScript: getElementById('calculate-{theme_suffix}')
- NO generic IDs, ALL must use "{theme_suffix}" suffix

Use the THEME/HTML_START/HTML_END format exactly. Do not use JSON. Make this replica completely unique with "{selected_theme}" context."""},
                        {"role": "user", "content": structured_prompt}
                    ],
                    max_tokens=2500,
                    temperature=0.7
                )
                
                # Parse this single replica
                response_content = response.choices[0].message.content
                total_output_tokens += count_tokens(response_content)
                
                print(f"Replica {i} response length: {len(response_content)}")
                
                try:
                    # Parse the structured text response
                    replica_data = parse_structured_response(response_content)
                    
                    if replica_data:
                        all_replicas[f'replica_{i}'] = replica_data
                        print(f"Successfully generated replica {i}")
                    else:
                        all_replicas[f'replica_{i}'] = {
                            "error": f"Failed to parse structured response for replica {i}",
                            "raw_response": response_content[:500]
                        }
                    
                except Exception as e:
                    print(f"Parsing error for replica {i}: {str(e)}")
                    all_replicas[f'replica_{i}'] = {
                        "error": f"Failed to parse replica {i}: {str(e)}",
                        "raw_response": response_content[:500]
                    }
                
            except Exception as api_error:
                print(f"OpenAI API Error for replica {i}: {str(api_error)}")
                all_replicas[f'replica_{i}'] = {
                    "error": f"API Error: {str(api_error)}"
                }

        # Calculate total tokens
        total_request_tokens = input_tokens + total_output_tokens

        # Update token tracking
        token_usage['session_tokens'] += total_request_tokens
        token_usage['total_tokens'] += total_request_tokens

        # Set generated_replicas to our collected replicas
        generated_replicas = all_replicas
        
        # Add metadata to each replica
        subtopic = data.get('subtopic', '')
        course = data.get('course', '')
        module = data.get('module', '')
        unit = data.get('unit', '')
        
        for replica_key in generated_replicas:
            if isinstance(generated_replicas[replica_key], dict):
                generated_replicas[replica_key].update({
                    'subtopic': subtopic,
                    'course': course,
                    'module': module,
                    'unit': unit
                })
        
        return jsonify({
            "success": True,
            "replicas": generated_replicas,
            "token_usage": {
                "input_tokens": input_tokens,
                "output_tokens": total_output_tokens,
                "total_tokens": total_request_tokens
            },
            "session_usage": token_usage
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download-excel', methods=['POST'])
def download_excel():
    try:
        data = request.json
        replicas = data.get('replicas', {})
        
        # Prepare data for Excel
        excel_data = []
        
        for replica_key, replica_data in replicas.items():
            if isinstance(replica_data, dict):
                # Format test cases as string
                test_cases_str = ""
                if isinstance(replica_data.get('test_cases'), list):
                    for tc in replica_data.get('test_cases', []):
                        test_cases_str += f"{tc}\n"
                else:
                    test_cases_str = str(replica_data.get('test_cases', ''))
                
                excel_data.append({
                    'Short_Text': replica_data.get('short_text', ''),
                    'HTML_Code': replica_data.get('html_code', ''),
                    'CSS_Code': replica_data.get('css_code', ''),
                    'Js_Code': replica_data.get('js_code', ''),
                    'Question_text': replica_data.get('question_text', ''),
                    'Test_cases': test_cases_str,
                    'HTML_Solution': replica_data.get('html_solution', ''),
                    'CSS_Solution': replica_data.get('css_solution', ''),
                    'JS_Solution': replica_data.get('js_solution', ''),
                    'Subtopic': replica_data.get('subtopic', ''),
                    'Course': replica_data.get('course', ''),
                    'Module': replica_data.get('module', ''),
                    'Unit': replica_data.get('unit', '')
                })
        
        # Create DataFrame and Excel file
        df = pd.DataFrame(excel_data)
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Replicas', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'web_coding_replicas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download-json', methods=['POST'])
def download_json():
    try:
        data = request.json
        
        # Create JSON file in memory
        output = io.StringIO()
        json.dump(data, output, indent=2)
        output.seek(0)
        
        # Convert to bytes
        json_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            json_bytes,
            mimetype='application/json',
            as_attachment=True,
            download_name=f'web_coding_replicas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)