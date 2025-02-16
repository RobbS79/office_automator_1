import json
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
from langchain_openai import ChatOpenAI

# Configure logging
logger = logging.getLogger(__name__)

class ConstructionActivityEstimator:
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.pricing_data = self.load_pricing_data()
        self.llm = self.initialize_llm()

    def load_pricing_data(self) -> List[Dict[str, Any]]:
        """Load pricing data from JSON file."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info("Pricing data successfully loaded")
            return data
        except Exception as e:
            logger.error(f"Error loading pricing data: {e}")
            return []

    def initialize_llm(self) -> ChatOpenAI:
        """Initialize ChatGPT model."""
        try:
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=os.getenv('OPENAI_API_KEY')
            )
        except Exception as e:
            logger.error(f"Failed to initialize ChatGPT: {e}")
            raise

    def estimate_construction_activities(self, project_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate construction activities for the project."""
        try:
            # Validate inputs
            self._validate_inputs(project_inputs)
            
            # Prepare prompt
            prompt = self._create_estimation_prompt(project_inputs)
            
            # Get estimation from LLM
            response = self.llm.invoke(prompt)
            
            # Parse and validate response
            estimation = self._parse_estimation(response.content)
            
            # Add pricing information
            estimation = self._add_pricing_info(estimation)
            
            return estimation

        except Exception as e:
            logger.error(f"Estimation error: {e}")
            return self._create_error_response(str(e))

    def _validate_inputs(self, inputs: Dict[str, Any]) -> None:
        """Validate project inputs."""
        required_fields = ['description', 'value', 'location', 'headline']
        if not all(field in inputs for field in required_fields):
            raise ValueError("Missing required fields")
        if not isinstance(inputs.get('value'), (int, float)):
            raise ValueError("Project value must be a number")

    def _create_estimation_prompt(self, inputs: Dict[str, Any]) -> str:
        """Create prompt for the LLM."""
        # Prepare examples of actual activities from our database
        example_activities = []
        for category, items in self.pricing_data.items():
            if items:  # Get first 2-3 activities from each category as examples
                category_examples = [
                    f"- {item['Popis práce']} ({item['mj']}) - {item['Kategorie']}"
                    for item in items[:3]
                    if 'Popis práce' in item and 'mj' in item and 'Kategorie' in item
                ]
                if category_examples:
                    example_activities.append(f"{category}:\n" + "\n".join(category_examples))

        return f"""
        
        Detaily projektu:
        - Název: {inputs['headline']}
        - Popis: {inputs['description']}
        - Lokalita: {inputs['location']}
        - Předpokládaná hodnota: {inputs['value']} Kč

        Get me a BoQ with price estimation of given construction based on 
        Detail projektu from above. For orientation in current market prices, 
        use online available statical data, or construction price lists of works
        and materials in Czechia. E.g. cesky staisticky urad, cennikremesel.cz, modra strecha, etc.

        Return only valid JSON object, in czech language of following structure:
        {{
            "activities": [
                {{
                    "activity_category": "přesný název kategorie z databáze",
                    "name": "přesný Popis práce z databáze",
                    "quantity": číslo (reálná výměra dle projektu),
                    "unit": "měrná jednotka dle databáze",
                    "estimated_price": číslo (respektující rozpočet),
                    "confidence": číslo (0-100)
                }}
            ],
            "total_price": číslo (nesmí výrazně překročit {inputs['value']} Kč),
            "total_confidence": číslo (0-100),
            "metadata": {{
                "project_type": "přesný typ stavby dle popisu",
                "complexity": "nízká/střední/vysoká",
                "estimation_notes": "důvody výběru položek a případné důležité poznámky"
            }}
        }}

        """

    def _parse_estimation(self, response: str) -> Dict[str, Any]:
        """Parse and validate LLM response."""
        try:
            # Extract JSON from response
            json_str = response.strip()
            if not json_str:
                raise ValueError("Empty response from LLM")

            # Parse JSON
            estimation = json.loads(json_str)
            
            # Validate structure
            if not estimation.get('activities'):
                raise ValueError("No activities in estimation")
                
            return estimation
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            raise ValueError("Invalid response format")

    def _add_pricing_info(self, estimation: Dict[str, Any]) -> Dict[str, Any]:
        """Add pricing information from pricing data."""
        try:
            activities = estimation.get('activities', [])
            if not activities:
                logger.warning("No activities found in estimation")
                return estimation

            # Get all available activities with their details
            available_activities = {}
            for category, items in self.pricing_data.items():
                for item in items:
                    if 'Popis práce' in item and 'Profese' in item:
                        # Create a unique key combining category, profession and work description
                        activity_key = f"{category}:{item['Profese']}:{item['Popis práce']}".lower().strip()
                        available_activities[activity_key] = {
                            'category': category,
                            'profession': item['Profese'],
                            'description': item['Popis práce'],
                            'data': item
                        }
            
            logger.info(f"Available activities loaded: {len(available_activities)}")

            for activity in activities:
                if 'name' not in activity:
                    logger.error("Activity missing 'name' field")
                    continue

                activity_name = activity['name'].lower().strip()
                
                # Try to find the best matching activity
                best_match = None
                best_match_score = 0
                
                for activity_key, activity_data in available_activities.items():
                    category, profession, description = activity_key.split(':', 2)
                    
                    # Check various matching conditions
                    description_match = (description in activity_name or 
                                      activity_name in description)
                    profession_match = (profession in activity_name or 
                                     activity_name in profession)
                    category_match = category in activity_name
                    
                    # Calculate match score
                    match_score = 0
                    if description_match:
                        match_score += 3  # Higher weight for description match
                    if profession_match:
                        match_score += 2  # Medium weight for profession match
                    if category_match:
                        match_score += 1  # Lower weight for category match
                        
                    # Additional scoring based on word overlap
                    activity_words = set(activity_name.split())
                    description_words = set(description.split())
                    common_words = activity_words & description_words
                    match_score += len(common_words)
                    
                    if match_score > best_match_score:
                        best_match = activity_data
                        best_match_score = match_score
                
                if best_match and best_match_score > 0:
                    price_info = best_match['data']
                    logger.info(f"Matched '{activity_name}' to:")
                    logger.info(f"  Category: {best_match['category']}")
                    logger.info(f"  Profession: {best_match['profession']}")
                    logger.info(f"  Description: {best_match['description']}")
                    
                    # Extract unit and base price
                    base_price = self._extract_price(price_info.get('mj', '0 Kč'))
                    activity['unit'] = price_info.get('Popis materiálu', 'm2')
                    activity['category'] = best_match['category']
                    activity['matched_description'] = best_match['description']
                    
                    # Calculate prices
                    contractor_price = self._extract_price(price_info.get('Cena práce pro řemeslníka', '0 Kč'))
                    company_markup = self._extract_price(price_info.get('Cena práce pro stavební firmu (+35%)', '0 Kč'))
                    material_cost = self._extract_price(price_info.get('Cena nákupu materiálu', '0 Kč'))
                    material_sale = self._extract_price(price_info.get('Cena prodeje materiálu (+15%)', '0 Kč'))
                    
                    # Calculate total price per unit
                    total_price_per_unit = max(base_price, contractor_price + company_markup + material_sale)
                    
                    # Set the values
                    activity['unit_price'] = total_price_per_unit
                    activity['estimated_price'] = total_price_per_unit * float(activity.get('quantity', 0))
                    activity['material_cost'] = material_cost
                    activity['contractor_price'] = contractor_price
                    activity['company_markup'] = company_markup
                    activity['material_markup'] = material_sale - material_cost if material_sale > 0 else 0
                    activity['matched_profession'] = best_match['profession']
                    activity['match_score'] = best_match_score
                    
                    logger.info(f"Calculated price: {activity['estimated_price']} (match score: {best_match_score})")
                else:
                    logger.warning(f"No matching activity found for: {activity_name}")
                    activity['estimated_price'] = activity.get('estimated_price', 0.0)
                    activity['unit_price'] = activity.get('unit_price', 0.0)
                    activity['unit'] = activity.get('unit', 'm2')
                    activity['category'] = 'unknown'
                    activity['matched_profession'] = None
                    activity['matched_description'] = None
                    activity['match_score'] = 0

            return estimation

        except Exception as e:
            logger.error(f"Error in _add_pricing_info: {str(e)}", exc_info=True)
            return self._create_error_response(str(e))

    def _extract_price(self, price_str: str) -> float:
        """Extract numeric price value from string with 'Kč'."""
        try:
            return float(price_str.replace(' Kč', '').replace(',', '.').strip() or 0)
        except (ValueError, AttributeError):
            return 0.0

    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response structure."""
        return {
            "activities": [],
            "total_price": 0,
            "total_confidence": 0,
            "metadata": {
                "error": error_message,
                "timestamp": datetime.now().isoformat()
            }
        }