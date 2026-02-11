from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import random
import re

app = FastAPI(title="BrandCraft API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENHANCED DATA MODELS ====================

class BrandInput(BaseModel):
    domain: str
    target_audience: str
    personality_traits: List[str]
    tone: str
    emotional_goals: List[str]
    industry_context: Optional[str] = None
    unique_value: Optional[str] = None
    company_size: Optional[str] = None
    budget_range: Optional[str] = None
    target_market: Optional[str] = None

# ==================== ENHANCED BRAND CONTEXT ====================

class BrandContext:
    def __init__(self):
        self.profile = {
            'domain': None,
            'target_audience': None,
            'personality_traits': [],
            'tone': None,
            'emotional_goals': [],
            'industry_context': None,
            'unique_value': None,
            'company_size': None,
            'budget_range': None,
            'target_market': None,
            'selected_name': None,
            'brand_story': None,
            'mission_statement': None,
            'vision_statement': None,
            'core_values': [],
            'value_proposition': None,
            'brand_voice_guide': {},
            'created_at': datetime.now().isoformat()
        }
    
    def update(self, key: str, value):
        self.profile[key] = value
        return self.profile
    
    def get_context_prompt(self) -> str:
        return f"""
Brand Profile:
- Name: {self.profile.get('selected_name', 'Not selected')}
- Domain: {self.profile['domain']}
- Target Audience: {self.profile['target_audience']}
- Company Size: {self.profile.get('company_size', 'Not specified')}
- Target Market: {self.profile.get('target_market', 'Global')}
- Personality: {', '.join(self.profile['personality_traits'])}
- Tone: {self.profile['tone']}
- Emotional Goals: {', '.join(self.profile['emotional_goals'])}
- Unique Value: {self.profile.get('unique_value', 'Innovation and quality')}
"""
    
    def to_dict(self) -> Dict:
        return self.profile

# ==================== ULTRA-ADVANCED NAME GENERATOR ====================

class UltraBrandNameGenerator:
    """Ultra-advanced name generation with deep linguistic intelligence"""
    
    DOMAIN_KEYWORDS = {
        'technology': ['Tech', 'Digital', 'Cyber', 'Data', 'Cloud', 'AI', 'Smart', 'Nexus', 'Quantum', 'Neural', 'Flux', 'Pixel', 'Logic', 'Binary'],
        'tech': ['Tech', 'Digital', 'Cyber', 'Data', 'Cloud', 'Code', 'Bit', 'Flux', 'Node', 'Core'],
        'software': ['Soft', 'Code', 'Logic', 'Flow', 'Stack', 'Build', 'Deploy', 'Launch', 'Dev', 'App'],
        'saas': ['Cloud', 'Stack', 'Flow', 'Sync', 'Hub', 'Suite', 'Connect', 'Link'],
        'fashion': ['Vogue', 'Style', 'Chic', 'Mode', 'Luxe', 'Couture', 'Thread', 'Weave', 'Silk', 'Trend'],
        'food': ['Flavor', 'Taste', 'Spice', 'Zest', 'Fresh', 'Savory', 'Bistro', 'Plate', 'Chef', 'Gourmet'],
        'beverage': ['Brew', 'Pour', 'Blend', 'Sip', 'Drip', 'Cup', 'Bean', 'Roast'],
        'health': ['Vital', 'Life', 'Pure', 'Zen', 'Bloom', 'Thrive', 'Pulse', 'Natura', 'Well', 'Care'],
        'fitness': ['Fit', 'Peak', 'Vigor', 'Power', 'Strong', 'Pulse', 'Active', 'Gym', 'Train'],
        'education': ['Learn', 'Bright', 'Wisdom', 'Scholar', 'Insight', 'Skill', 'Know', 'Teach', 'Study'],
        'finance': ['Capital', 'Wealth', 'Mint', 'Vault', 'Prosper', 'Fund', 'Asset', 'Coin', 'Pay'],
        'consulting': ['Sage', 'Apex', 'Prime', 'Insight', 'Catalyst', 'Summit', 'Advisor', 'Guide'],
        'marketing': ['Brand', 'Reach', 'Impact', 'Buzz', 'Engage', 'Amplify', 'Social', 'Growth'],
        'design': ['Canvas', 'Pixel', 'Craft', 'Studio', 'Vision', 'Form', 'Create', 'Art'],
        'ecommerce': ['Shop', 'Cart', 'Market', 'Store', 'Trade', 'Buy', 'Sell', 'Commerce'],
        'real estate': ['Estate', 'Home', 'Property', 'Land', 'Realty', 'House', 'Space'],
        'automotive': ['Auto', 'Drive', 'Motor', 'Car', 'Wheel', 'Road', 'Speed'],
        'travel': ['Journey', 'Travel', 'Voyage', 'Explore', 'Wander', 'Trek', 'Quest'],
        'entertainment': ['Play', 'Fun', 'Show', 'Stage', 'Star', 'Scene', 'Act'],
        'hospitality': ['Stay', 'Host', 'Guest', 'Welcome', 'Suite', 'Lodge'],
    }
    
    POWER_WORDS = {
        'professional': ['Pro', 'Elite', 'Prime', 'Core', 'Apex', 'Peak', 'Sterling', 'Ascent', 'Premier', 'Master'],
        'innovative': ['Neo', 'Flux', 'Forge', 'Shift', 'Nova', 'Vanguard', 'Pioneer', 'Evolve', 'Future', 'Next'],
        'trustworthy': ['True', 'Anchor', 'Pillar', 'Haven', 'Shield', 'Beacon', 'Loyal', 'Trust', 'Solid'],
        'creative': ['Craft', 'Studio', 'Atelier', 'Canvas', 'Muse', 'Vision', 'Palette', 'Art', 'Create'],
        'playful': ['Joy', 'Spark', 'Fizz', 'Bounce', 'Whimsy', 'Gleam', 'Pop', 'Fun', 'Happy'],
        'bold': ['Blaze', 'Surge', 'Thunder', 'Impact', 'Force', 'Titan', 'Fierce', 'Power', 'Mighty'],
        'elegant': ['Luxe', 'Grace', 'Refined', 'Prestige', 'Noble', 'Opulent', 'Silk', 'Velvet', 'Pearl']
    }
    
    PREFIXES = ['Next', 'True', 'Pure', 'Quick', 'Smart', 'Super', 'Ultra', 'Meta', 'Alpha', 'Beta']
    SUFFIXES = ['ly', 'ify', 'io', 'hub', 'lab', 'co', 'ai', 'works', 'studio', 'group', 'app', 'spot']
    
    def __init__(self):
        self.generated_cache = set()
    
    def generate_names(self, context: BrandContext, count: int = 20) -> List[Dict]:
        """Generate diverse, intelligent brand names with advanced algorithms"""
        candidates = []
        
        # Strategy 1: Domain Intelligence (30%)
        candidates.extend(self._generate_domain_intelligent(context, int(count * 0.3)))
        
        # Strategy 2: Linguistic Patterns (25%)
        candidates.extend(self._generate_linguistic(context, int(count * 0.25)))
        
        # Strategy 3: Smart Blends (25%)
        candidates.extend(self._generate_smart_blends(context, int(count * 0.25)))
        
        # Strategy 4: Prefix/Suffix Combinations (20%)
        candidates.extend(self._generate_affixed(context, int(count * 0.2)))
        
        # Score and rank with advanced metrics
        scored_names = []
        for name in candidates:
            if name not in self.generated_cache and len(name) >= 3 and len(name) <= 15:
                scores = self._ultra_advanced_scoring(name, context)
                scored_names.append({
                    'name': name,
                    'score': scores['total'],
                    'memorability': scores['memorability'],
                    'uniqueness': scores['uniqueness'],
                    'relevance': scores['relevance'],
                    'pronounceability': scores['pronounceability'],
                    'brandability': scores['brandability'],
                    'marketability': scores['marketability'],
                    'category': scores['category']
                })
                self.generated_cache.add(name)
        
        scored_names.sort(key=lambda x: x['score'], reverse=True)
        return scored_names[:count]
    
    def _generate_domain_intelligent(self, context: BrandContext, count: int) -> List[str]:
        names = []
        domain_lower = context.profile['domain'].lower()
        
        domain_keywords = []
        for key, words in self.DOMAIN_KEYWORDS.items():
            if key in domain_lower:
                domain_keywords.extend(words)
        
        if not domain_keywords:
            domain_keywords = ['Smart', 'Prime', 'Core', 'Hub', 'Pro']
        
        power_words = []
        for trait in context.profile['personality_traits']:
            if trait.lower() in self.POWER_WORDS:
                power_words.extend(self.POWER_WORDS[trait.lower()])
        
        if not power_words:
            power_words = ['Pro', 'Plus', 'Core', 'Prime']
        
        for kw in domain_keywords[:6]:
            for pw in power_words[:6]:
                names.append(kw + pw)
                names.append(pw + kw)
                if random.random() > 0.6:
                    names.append(kw.lower() + random.choice(self.SUFFIXES))
        
        return names[:count * 3]
    
    def _generate_linguistic(self, context: BrandContext, count: int) -> List[str]:
        names = []
        vowels = ['a', 'e', 'i', 'o', 'u']
        strong_consonants = ['b', 'd', 'g', 'k', 'p', 't', 'v', 'z', 'x']
        soft_consonants = ['f', 'l', 'm', 'n', 'r', 's', 'w', 'y', 'h']
        
        if 'bold' in [t.lower() for t in context.profile['personality_traits']]:
            consonants = strong_consonants
        else:
            consonants = soft_consonants + strong_consonants[:4]
        
        patterns = [
            ['C', 'V', 'C', 'V'],           # Zara, Nike
            ['C', 'V', 'C', 'C', 'V'],      # Pepsi
            ['C', 'V', 'C', 'V', 'C'],      # Adidas
            ['V', 'C', 'V', 'C'],           # Uber
            ['C', 'C', 'V', 'C'],           # Slack
        ]
        
        for pattern in patterns:
            for _ in range(count * 2):
                name = ''
                for char_type in pattern:
                    if char_type == 'V':
                        name += random.choice(vowels)
                    else:
                        name += random.choice(consonants)
                names.append(name.capitalize())
        
        return names[:count * 3]
    
    def _generate_smart_blends(self, context: BrandContext, count: int) -> List[str]:
        names = []
        
        source_words = context.profile['domain'].split() + \
                      context.profile['personality_traits'] + \
                      context.profile['emotional_goals']
        
        for trait in context.profile['personality_traits']:
            if trait.lower() in self.POWER_WORDS:
                source_words.extend(self.POWER_WORDS[trait.lower()][:3])
        
        for i in range(len(source_words)):
            for j in range(i + 1, min(i + 5, len(source_words))):
                word1 = source_words[i].lower()
                word2 = source_words[j].lower()
                
                if len(word1) >= 3 and len(word2) >= 3:
                    # Multiple blending techniques
                    blend1 = word1[:len(word1)//2] + word2[len(word2)//2:]
                    blend2 = word1[:int(len(word1)*0.6)] + word2[int(len(word2)*0.4):]
                    blend3 = word1[:3] + word2[-3:]
                    
                    names.extend([blend1.capitalize(), blend2.capitalize(), blend3.capitalize()])
        
        return names[:count * 3]
    
    def _generate_affixed(self, context: BrandContext, count: int) -> List[str]:
        names = []
        domain_lower = context.profile['domain'].lower()
        
        keywords = []
        for key, words in self.DOMAIN_KEYWORDS.items():
            if key in domain_lower:
                keywords.extend(words[:3])
        
        if not keywords:
            keywords = ['Smart', 'Core', 'Hub']
        
        for kw in keywords:
            for prefix in self.PREFIXES[:5]:
                names.append(prefix + kw)
            for suffix in self.SUFFIXES[:5]:
                names.append(kw.lower() + suffix)
        
        return names[:count * 3]
    
    def _ultra_advanced_scoring(self, name: str, context: BrandContext) -> Dict[str, float]:
        scores = {}
        
        scores['memorability'] = self._score_memorability(name)
        scores['uniqueness'] = self._score_uniqueness(name)
        scores['relevance'] = self._score_relevance(name, context)
        scores['pronounceability'] = self._score_pronounceability(name)
        scores['brandability'] = self._score_brandability(name)
        scores['marketability'] = self._score_marketability(name, context)
        
        # Determine category
        scores['category'] = self._categorize_name(name, context)
        
        # Weighted total
        scores['total'] = round(
            scores['memorability'] * 0.25 +
            scores['uniqueness'] * 0.15 +
            scores['relevance'] * 0.20 +
            scores['pronounceability'] * 0.15 +
            scores['brandability'] * 0.15 +
            scores['marketability'] * 0.10
        , 2)
        
        return scores
    
    def _score_memorability(self, name: str) -> float:
        score = 100.0
        length = len(name)
        
        if 4 <= length <= 7:
            score += 25
        elif 3 <= length <= 9:
            score += 15
        elif length < 3:
            score -= 30
        else:
            score -= (length - 9) * 4
        
        syllables = self._count_syllables(name)
        if 1 <= syllables <= 2:
            score += 20
        elif syllables == 3:
            score += 10
        
        if len(set(name.lower())) / len(name) > 0.7:
            score += 10
        
        return max(0, min(100, score))
    
    def _score_uniqueness(self, name: str) -> float:
        score = 100.0
        
        common_words = ['app', 'web', 'net', 'site', 'tech', 'digital', 'online', 
                       'cloud', 'smart', 'the', 'and', 'pro', 'plus', 'new']
        
        name_lower = name.lower()
        if name_lower in common_words:
            score -= 60
        
        for word in common_words:
            if word in name_lower:
                score -= 15
        
        return max(0, min(100, score))
    
    def _score_relevance(self, name: str, context: BrandContext) -> float:
        score = 50.0
        name_lower = name.lower()
        
        domain_words = context.profile['domain'].lower().split()
        for word in domain_words:
            if len(word) > 2 and word in name_lower:
                score += 20
        
        for trait in context.profile['personality_traits']:
            if trait.lower()[:3] in name_lower:
                score += 12
        
        return min(100, score)
    
    def _score_pronounceability(self, name: str) -> float:
        score = 100.0
        
        consonant_cluster = 0
        prev_consonant = False
        
        for char in name.lower():
            is_consonant = char not in 'aeiou'
            if is_consonant and prev_consonant:
                consonant_cluster += 1
            prev_consonant = is_consonant
        
        score -= consonant_cluster * 12
        
        return max(0, min(100, score))
    
    def _score_brandability(self, name: str) -> float:
        score = 100.0
        
        if len(name) <= 12 and not any(char.isdigit() for char in name):
            score += 20
        
        if len(name) <= 10:
            score += 15
        
        if name.isalpha():
            score += 15
        
        return min(100, score)
    
    def _score_marketability(self, name: str, context: BrandContext) -> float:
        score = 75.0
        
        if context.profile.get('target_market') == 'global':
            if len(name) <= 8 and name.isalpha():
                score += 25
        
        return min(100, score)
    
    def _categorize_name(self, name: str, context: BrandContext) -> str:
        if any(kw in name.lower() for kw in ['tech', 'digital', 'cyber', 'data']):
            return 'Tech-focused'
        elif len(name) <= 5:
            return 'Short & Punchy'
        elif any(char in name for char in self.SUFFIXES):
            return 'Modern Suffix'
        else:
            return 'Creative Blend'
    
    def _count_syllables(self, word: str) -> int:
        vowels = 'aeiou'
        word = word.lower()
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        if word.endswith('e') and count > 1:
            count -= 1
        
        return max(1, count)

# ==================== ULTRA-ADVANCED CONTENT GENERATOR ====================

class UltraContentGenerator:
    """Ultra-advanced professional content generation"""
    
    def generate_brand_story(self, brand_name: str, context: BrandContext) -> str:
        """Generate compelling, professional brand story"""
        templates = [
            f"In a world where {context.profile['domain']} often feels impersonal, {brand_name} was founded on a simple belief: "
            f"{context.profile['target_audience']} deserve experiences that inspire {', '.join(context.profile['emotional_goals'][:2])}. "
            f"What started as a vision has evolved into a {', '.join(context.profile['personality_traits'][:2])} movement. "
            f"Every day, we work tirelessly to {context.profile.get('unique_value', 'create exceptional value')}, "
            f"proving that {context.profile['domain']} can be both {context.profile['personality_traits'][0]} and deeply human. "
            f"This is more than business—it's our calling.",
            
            f"The story of {brand_name} begins with a question: What if {context.profile['domain']} could be different? "
            f"What if {context.profile['target_audience']} had a partner who truly understood their needs? "
            f"Founded on principles of {', '.join(context.profile['emotional_goals'][:2])}, we've built something remarkable. "
            f"Our {', '.join(context.profile['personality_traits'][:2])} approach isn't just a strategy—it's who we are. "
            f"With {context.profile.get('unique_value', 'innovation at our core')}, we're not just serving {context.profile['target_audience']}; "
            f"we're revolutionizing how {context.profile['domain']} connects with the people who matter most.",
            
            f"{brand_name} emerged from a powerful insight: {context.profile['target_audience']} needed more than just another "
            f"{context.profile['domain']} solution. They needed a {', '.join(context.profile['personality_traits'][:2])} partner "
            f"who would stand beside them, championing {', '.join(context.profile['emotional_goals'][:2])} at every turn. "
            f"Today, we're proud to deliver on that promise. Our commitment to {context.profile.get('unique_value', 'excellence')} "
            f"drives everything we do, from strategy to execution. This is {brand_name}—where vision meets action, and where "
            f"{context.profile['target_audience']} find their perfect match."
        ]
        
        return random.choice(templates)
    
    def generate_mission_statement(self, brand_name: str, context: BrandContext) -> str:
        """Generate powerful mission statement"""
        templates = [
            f"To empower {context.profile['target_audience']} with {', '.join(context.profile['personality_traits'][:2])} "
            f"{context.profile['domain']} solutions that consistently deliver {', '.join(context.profile['emotional_goals'][:2])}, "
            f"while championing {context.profile.get('unique_value', 'innovation and excellence')} in everything we do.",
            
            f"Our mission is to transform {context.profile['domain']} for {context.profile['target_audience']} through "
            f"unwavering dedication to {', '.join(context.profile['personality_traits'][:2])} excellence, ensuring every interaction "
            f"creates {', '.join(context.profile['emotional_goals'][:2])} and lasting value.",
            
            f"We exist to revolutionize {context.profile['domain']} by providing {context.profile['target_audience']} with "
            f"{', '.join(context.profile['personality_traits'][:2])} experiences that inspire {', '.join(context.profile['emotional_goals'][:2])}, "
            f"driven by our commitment to {context.profile.get('unique_value', 'making a difference')}."
        ]
        
        return random.choice(templates)
    
    def generate_vision_statement(self, brand_name: str, context: BrandContext) -> str:
        """Generate inspiring vision statement"""
        templates = [
            f"To become the world's most {context.profile['personality_traits'][0]} {context.profile['domain']} partner, "
            f"setting new standards for {', '.join(context.profile['emotional_goals'][:2])} and transforming how "
            f"{context.profile['target_audience']} experience excellence.",
            
            f"A future where every {context.profile['target_audience'].lower()} has access to {', '.join(context.profile['personality_traits'][:2])} "
            f"{context.profile['domain']} that delivers {', '.join(context.profile['emotional_goals'][:2])}, "
            f"creating lasting impact and meaningful change worldwide.",
            
            f"To redefine {context.profile['domain']} by making it universally {', '.join(context.profile['personality_traits'][:2])}, "
            f"accessible, and transformative for {context.profile['target_audience']} across {context.profile.get('target_market', 'all markets')}."
        ]
        
        return random.choice(templates)
    
    def generate_value_proposition(self, brand_name: str, context: BrandContext) -> str:
        """Generate compelling value proposition"""
        return (
            f"For {context.profile['target_audience']} seeking {', '.join(context.profile['emotional_goals'][:2])}, "
            f"{brand_name} is the {', '.join(context.profile['personality_traits'][:2])} {context.profile['domain']} solution "
            f"that delivers {context.profile.get('unique_value', 'exceptional results')}. "
            f"Unlike traditional alternatives, we combine {context.profile['personality_traits'][0]} excellence with "
            f"deep understanding of your needs, ensuring every experience exceeds expectations."
        )
    
    def generate_core_values(self, context: BrandContext) -> List[Dict]:
        """Generate comprehensive core values"""
        value_pool = {
            'Innovation': 'We constantly push boundaries, embracing cutting-edge ideas and technologies to stay ahead of the curve.',
            'Integrity': 'We operate with unwavering honesty and transparency, building trust through every action we take.',
            'Excellence': 'We pursue the highest standards in everything we do, never settling for anything less than exceptional.',
            'Customer-First': f'We place {context.profile["target_audience"]} at the center of every decision, ensuring their success is our success.',
            'Collaboration': 'We believe in the transformative power of teamwork, achieving more together than we ever could alone.',
            'Sustainability': 'We build for the long term, making decisions that create lasting positive impact for future generations.',
            'Agility': 'We adapt swiftly to change, viewing challenges as opportunities and remaining flexible in dynamic markets.',
            'Empowerment': f'We enable {context.profile["target_audience"]} to unlock their full potential and achieve their most ambitious goals.',
            'Quality': 'We never compromise on quality, delivering superior results that stand the test of time.',
            'Trust': 'We build lasting relationships founded on reliability, respect, and consistent delivery on our promises.',
            'Creativity': 'We foster imaginative thinking and bold ideas, celebrating innovation in all its forms.',
            'Accountability': 'We take full ownership of our commitments, holding ourselves to the highest standards of responsibility.'
        }
        
        trait_value_map = {
            'professional': ['Excellence', 'Integrity', 'Quality', 'Accountability'],
            'innovative': ['Innovation', 'Agility', 'Empowerment', 'Creativity'],
            'trustworthy': ['Trust', 'Integrity', 'Customer-First', 'Accountability'],
            'creative': ['Innovation', 'Creativity', 'Excellence', 'Agility'],
            'bold': ['Innovation', 'Excellence', 'Agility', 'Empowerment'],
            'playful': ['Innovation', 'Customer-First', 'Collaboration', 'Creativity'],
            'elegant': ['Excellence', 'Quality', 'Integrity', 'Trust']
        }
        
        values_set = set()
        for trait in context.profile['personality_traits']:
            if trait.lower() in trait_value_map:
                values_set.update(trait_value_map[trait.lower()])
        
        if not values_set:
            values_set = {'Excellence', 'Innovation', 'Integrity', 'Customer-First'}
        
        selected_values = []
        for value_name in list(values_set)[:5]:
            selected_values.append({
                'value': value_name,
                'description': value_pool[value_name]
            })
        
        return selected_values
    
    def generate_taglines(self, brand_name: str, context: BrandContext, count: int = 10) -> List[Dict]:
        """Generate professional, diverse taglines"""
        templates = [
            (f"Elevating {context.profile['domain']}, empowering {context.profile['target_audience']}", "empowerment"),
            (f"{', '.join(context.profile['personality_traits'][:2]).title()} {context.profile['domain']} for tomorrow", "forward"),
            (f"Where {context.profile['domain']} meets {context.profile['personality_traits'][0]} excellence", "excellence"),
            (f"Your {context.profile['personality_traits'][0]} partner in {context.profile['domain']}", "partnership"),
            (f"Transforming {context.profile['domain']}, one {context.profile['target_audience'].split()[0]} at a time", "transformation"),
            (f"{context.profile['domain']} that inspires {context.profile['emotional_goals'][0]}", "inspiration"),
            (f"Redefining excellence in {context.profile['domain']}", "excellence"),
            (f"The {context.profile['personality_traits'][0]} choice for {context.profile['domain']}", "choice"),
            (f"Beyond {context.profile['domain']}, building {context.profile['emotional_goals'][0]}", "vision"),
            (f"Experience {context.profile['domain']} differently", "experience"),
            (f"{brand_name}: {', '.join(context.profile['personality_traits'][:2])} by design", "identity"),
            (f"Your journey to {context.profile['emotional_goals'][0]} starts here", "journey")
        ]
        
        taglines = []
        for template, style in templates[:count]:
            taglines.append({
                'tagline': template,
                'style': style,
                'score': random.randint(82, 98),
                'length': len(template.split()),
                'emotional_impact': f"Evokes {context.profile['emotional_goals'][0]}",
                'target_resonance': 'High'
            })
        
        return taglines
    
    def generate_brand_voice_guide(self, brand_name: str, context: BrandContext) -> Dict:
        """Generate comprehensive brand voice guidelines"""
        tone_guides = {
            'formal': {
                'do': ['Use professional language', 'Maintain respectful distance', 'Structure clearly'],
                'dont': ['Use slang', 'Be overly casual', 'Use emojis'],
                'example': 'We are pleased to present our comprehensive solution.'
            },
            'casual': {
                'do': ['Be conversational', 'Use contractions', 'Keep it friendly'],
                'dont': ['Be too stiff', 'Over-complicate', 'Use jargon'],
                'example': "We've got exactly what you need!"
            },
            'friendly': {
                'do': ['Be warm and approachable', 'Show empathy', 'Use inclusive language'],
                'dont': ['Be distant', 'Sound corporate', 'Over-formalize'],
                'example': "We're here to help you succeed!"
            },
            'authoritative': {
                'do': ['Demonstrate expertise', 'Be confident', 'Provide insights'],
                'dont': ['Sound arrogant', 'Be condescending', 'Over-promise'],
                'example': 'Based on our industry expertise, we recommend...'
            },
            'inspiring': {
                'do': ['Be motivational', 'Paint vision', 'Encourage action'],
                'dont': ['Be preachy', 'Sound unrealistic', 'Over-hype'],
                'example': 'Together, we can achieve extraordinary things.'
            }
        }
        
        tone = context.profile['tone']
        return tone_guides.get(tone, tone_guides['friendly'])

    def generate_elevator_pitch(self, brand_name: str, context: BrandContext) -> str:
        """Generate compelling 30-second pitch"""
        return (
            f"{brand_name} is a {', '.join(context.profile['personality_traits'][:2])} {context.profile['domain']} company "
            f"revolutionizing how {context.profile['target_audience']} achieve {', '.join(context.profile['emotional_goals'][:2])}. "
            f"Through our commitment to {context.profile.get('unique_value', 'excellence')}, we deliver solutions that don't just meet expectations—they redefine them. "
            f"In {context.profile.get('target_market', 'today\'s market')}, we stand as the {context.profile['personality_traits'][0]} choice for those who demand more."
        )
    
    def generate_social_content(self, brand_name: str, context: BrandContext, 
                               platform: str, content_type: str) -> Dict:
        """Generate platform-optimized social content with best practices"""
        
        content_templates = {
            'launch': {
                'short': f"🚀 Introducing {brand_name}! The {context.profile['personality_traits'][0]} way to experience {context.profile['domain']}. Join us!",
                'medium': f"Big news! {brand_name} is here to transform {context.profile['domain']} for {context.profile['target_audience']}. Our {', '.join(context.profile['personality_traits'][:2])} approach delivers {', '.join(context.profile['emotional_goals'][:2])} like never before. Ready to experience the difference?",
                'long': f"Today marks an exciting milestone! We're thrilled to introduce {brand_name}, a revolutionary {context.profile['domain']} solution built specifically for {context.profile['target_audience']}. Our journey began with a simple question: What if {context.profile['domain']} could inspire {', '.join(context.profile['emotional_goals'][:2])}? Through {', '.join(context.profile['personality_traits'][:2])} innovation and unwavering commitment to {context.profile.get('unique_value', 'excellence')}, we've created something truly special. Join us in redefining what's possible!"
            },
            'value': {
                'short': f"💡 What sets {brand_name} apart? Our {', '.join(context.profile['personality_traits'][:2])} approach to {context.profile['domain']}.",
                'medium': f"Why {brand_name}? Because {context.profile['target_audience']} deserve more than ordinary {context.profile['domain']}. We deliver {', '.join(context.profile['emotional_goals'][:2])} through {', '.join(context.profile['personality_traits'][:2])} solutions that actually work. Experience the difference today.",
                'long': f"Let's talk about what makes {brand_name} different. In a crowded {context.profile['domain']} marketplace, we stand out by putting {context.profile['target_audience']} first. Every solution we create is designed to inspire {', '.join(context.profile['emotional_goals'][:2])} and deliver real results. Our {', '.join(context.profile['personality_traits'][:2])} approach isn't just marketing speak—it's embedded in everything we do, from strategy to execution. Ready to partner with a team that truly understands your needs?"
            },
            'testimonial': {
                'short': f"❤️ '{brand_name} transformed how we approach {context.profile['domain']}.' - Happy Customer",
                'medium': f"Client success story: '{brand_name}'s {context.profile['personality_traits'][0]} team delivered beyond our expectations. Their deep understanding of {context.profile['domain']} made all the difference.' This is what we live for!",
                'long': f"We're honored to share this testimonial: 'Working with {brand_name} has been transformative. Their {', '.join(context.profile['personality_traits'][:2])} approach to {context.profile['domain']} not only met our needs but exceeded them in ways we didn't think possible. The team's commitment to {', '.join(context.profile['emotional_goals'][:2])} shows in every interaction. If you're looking for a partner who truly cares, look no further.' Stories like these remind us why we do what we do."
            },
            'insight': {
                'short': f"📊 {context.profile['domain']} is evolving. Are you ready?",
                'medium': f"Industry insight: The future of {context.profile['domain']} belongs to those who embrace {', '.join(context.profile['personality_traits'][:2])} innovation. At {brand_name}, we're not just following trends—we're setting them. Here's what {context.profile['target_audience']} need to know...",
                'long': f"Let's discuss the future of {context.profile['domain']}. As industry leaders, we're seeing a clear shift toward {', '.join(context.profile['emotional_goals'][:2])}-driven approaches. {context.profile['target_audience']} are demanding more {', '.join(context.profile['personality_traits'][:2])} solutions, and companies that fail to adapt will be left behind. At {brand_name}, we've been ahead of this curve from day one. Our {context.profile.get('unique_value', 'innovative approach')} positions us—and our partners—for long-term success. Want to know where your industry is headed? Let's talk."
            },
            'team': {
                'short': f"👋 Meet the minds behind {brand_name}!",
                'medium': f"Behind every great brand is an exceptional team. At {brand_name}, we're passionate about bringing {', '.join(context.profile['emotional_goals'][:2])} to {context.profile['target_audience']} through {', '.join(context.profile['personality_traits'][:2])} {context.profile['domain']} solutions. Want to join us?",
                'long': f"Culture spotlight: What makes {brand_name} special? It's our people. Every team member shares a passion for transforming {context.profile['domain']} and empowering {context.profile['target_audience']}. Our {', '.join(context.profile['personality_traits'][:2])} culture isn't just about delivering results—it's about making a genuine impact. From our collaborative workspace to our commitment to {context.profile.get('unique_value', 'innovation')}, we've built something remarkable. Interested in joining our mission? We're always looking for talented individuals who share our vision."
            }
        }
        
        platform_specs = {
            'twitter': {'style': 'short', 'max_hashtags': 2},
            'linkedin': {'style': 'long', 'max_hashtags': 3},
            'instagram': {'style': 'medium', 'max_hashtags': 5},
            'facebook': {'style': 'medium', 'max_hashtags': 3}
        }
        
        spec = platform_specs.get(platform, platform_specs['twitter'])
        content = content_templates.get(content_type, content_templates['launch'])[spec['style']]
        
        hashtags = [
            f"#{brand_name.replace(' ', '')}",
            f"#{context.profile['domain'].replace(' ', '')}",
        ]
        
        for trait in context.profile['personality_traits'][:spec['max_hashtags']-2]:
            hashtags.append(f"#{trait.capitalize()}")
        
        return {
            'platform': platform,
            'content': content,
            'content_type': content_type,
            'hashtags': hashtags[:spec['max_hashtags']],
            'optimal_time': self._get_optimal_time(platform),
            'engagement_tips': self._get_engagement_tips(platform),
            'cta': self._generate_cta(content_type, platform)
        }
    
    def _get_optimal_time(self, platform: str) -> str:
        times = {
            'twitter': '12:00 PM - 1:00 PM & 5:00 PM - 6:00 PM (Weekdays)',
            'linkedin': '7:30 AM - 8:30 AM & 12:00 PM - 1:00 PM (Tuesday-Thursday)',
            'instagram': '11:00 AM - 1:00 PM & 7:00 PM - 9:00 PM (Wednesday-Friday)',
            'facebook': '1:00 PM - 3:00 PM (Wednesday-Friday)'
        }
        return times.get(platform, '12:00 PM')
    
    def _get_engagement_tips(self, platform: str) -> List[str]:
        tips = {
            'twitter': [
                'Keep it concise and punchy',
                'Use 1-2 relevant hashtags',
                'Include visuals for 3x engagement',
                'Ask questions to encourage replies'
            ],
            'linkedin': [
                'Lead with value and insights',
                'Tag relevant companies and people',
                'Post during business hours',
                'Share actionable takeaways'
            ],
            'instagram': [
                'Use all available hashtags',
                'Post carousel content for higher reach',
                'Respond to comments within 1 hour',
                'Include clear call-to-action'
            ],
            'facebook': [
                'Keep initial text under 80 characters',
                'Use native video for maximum reach',
                'Post when your audience is most active',
                'Encourage shares and tags'
            ]
        }
        return tips.get(platform, ['Engage authentically with your audience'])
    
    def _generate_cta(self, content_type: str, platform: str) -> str:
        ctas = {
            'launch': 'Learn more at [link] | Join our community today',
            'value': 'Discover the difference at [link] | Book a demo',
            'testimonial': 'See more success stories at [link] | Start your journey',
            'insight': 'Read the full article at [link] | Subscribe for more insights',
            'team': 'View open positions at [link] | Connect with us'
        }
        return ctas.get(content_type, 'Visit us at [link]')

# ==================== ENHANCED LOGO GENERATOR ====================

class UltraLogoGenerator:
    """Ultra-advanced logo prompt generation"""
    
    def generate_logo_prompts(self, brand_name: str, context: BrandContext) -> List[Dict]:
        """Generate comprehensive, professional logo prompts"""
        
        primary_trait = context.profile['personality_traits'][0].lower() if context.profile['personality_traits'] else 'professional'
        
        style_guides = {
            'professional': {
                'visual': 'clean geometric shapes, structured layout, minimal design, corporate aesthetic',
                'colors': 'navy blue, charcoal gray, white, subtle gold accents',
                'mood': 'confidence, authority, reliability, sophistication'
            },
            'innovative': {
                'visual': 'abstract geometric forms, dynamic angles, futuristic elements, modern shapes',
                'colors': 'electric blue, cyan, vibrant gradients, tech-inspired palette',
                'mood': 'forward-thinking, cutting-edge, transformative, progressive'
            },
            'trustworthy': {
                'visual': 'solid shapes, balanced composition, classic elements, stable foundation',
                'colors': 'deep blue, forest green, warm gray, traditional tones',
                'mood': 'stability, dependability, security, lasting quality'
            },
            'creative': {
                'visual': 'artistic flourishes, unique shapes, expressive elements, imaginative forms',
                'colors': 'vibrant multi-color palette, artistic combinations, bold contrasts',
                'mood': 'imagination, originality, inspiration, artistic excellence'
            },
            'playful': {
                'visual': 'rounded shapes, dynamic movement, friendly forms, energetic design',
                'colors': 'bright primary colors, cheerful palette, warm tones',
                'mood': 'joy, energy, approachability, fun engagement'
            },
            'bold': {
                'visual': 'strong geometric forms, high contrast design, impactful shapes, powerful presence',
                'colors': 'red, black, white, gold accents, dramatic contrasts',
                'mood': 'power, strength, confidence, commanding presence'
            },
            'elegant': {
                'visual': 'refined lines, sophisticated forms, balanced luxury, timeless design',
                'colors': 'black, gold, white, navy, luxury palette',
                'mood': 'sophistication, prestige, timelessness, refined excellence'
            }
        }
        
        style_guide = style_guides.get(primary_trait, style_guides['professional'])
        
        logo_types = [
            {
                'name': 'Wordmark Logo',
                'description': 'Typography-focused design using the brand name as the primary visual element',
                'use_case': 'Perfect for website headers, business cards, letterheads, and professional documents',
                'prompt_base': f"Professional wordmark logo design for '{brand_name}', {style_guide['visual']}, "
                              f"modern sophisticated typography, {style_guide['colors']}, minimalist lettermark, "
                              f"{style_guide['mood']}, premium quality",
                'techniques': 'Custom lettering, unique ligatures, balanced kerning'
            },
            {
                'name': 'Iconic Symbol',
                'description': 'Abstract symbol representing core brand values and personality',
                'use_case': 'Ideal for app icons, social media avatars, merchandise, and standalone branding',
                'prompt_base': f"Abstract iconic logo symbol for {brand_name}, {style_guide['visual']}, "
                              f"{style_guide['colors']}, memorable distinctive symbol, {style_guide['mood']}, "
                              f"{context.profile['domain']} industry relevant",
                'techniques': 'Negative space usage, symbolic representation, scalable design'
            },
            {
                'name': 'Combination Mark',
                'description': 'Integrated symbol and wordmark creating a complete brand identity',
                'use_case': 'Versatile for all applications, recommended as primary logo across all touchpoints',
                'prompt_base': f"Combination mark logo design, '{brand_name}' text integrated with icon symbol, "
                              f"{style_guide['visual']}, {style_guide['colors']}, balanced composition, "
                              f"professional layout, {style_guide['mood']}",
                'techniques': 'Harmonious integration, flexible layout, brand cohesion'
            },
            {
                'name': 'Emblem Badge',
                'description': 'Badge-style enclosed design with traditional appeal',
                'use_case': 'Excellent for premium packaging, certificates, official documents, and heritage branding',
                'prompt_base': f"Emblem badge logo for {brand_name}, {style_guide['visual']}, "
                              f"{style_guide['colors']}, circular or shield shape, premium feel, "
                              f"traditional meets modern aesthetic",
                'techniques': 'Enclosed composition, detailed elements, classic appeal'
            },
            {
                'name': 'Monogram',
                'description': 'Stylized initials creating an elegant brand mark',
                'use_case': 'Perfect for luxury branding, fashion, and sophisticated business applications',
                'prompt_base': f"Elegant monogram logo design using initials of '{brand_name}', "
                              f"{style_guide['visual']}, {style_guide['colors']}, refined typography, "
                              f"luxury brand aesthetic, {style_guide['mood']}",
                'techniques': 'Interlocking letters, elegant curves, timeless design'
            }
        ]
        
        prompts = []
        for logo_type in logo_types:
            prompts.append({
                'type': logo_type['name'],
                'description': logo_type['description'],
                'use_case': logo_type['use_case'],
                'prompt': logo_type['prompt_base'] + f", {context.profile['domain']} industry context, vector art, "
                         f"clean professional lines, infinitely scalable design, print and digital ready",
                'negative_prompt': "photo realistic, 3d render, gradient mesh, drop shadow effects, lens flare, "
                                  "complex textures, cluttered design, text effects, bevels, emboss",
                'style_notes': style_guide['mood'],
                'color_palette': style_guide['colors'],
                'design_techniques': logo_type['techniques'],
                'file_formats': 'AI, EPS, SVG, PNG (transparent), PDF'
            })
        
        return prompts
    
    def extract_color_palette(self, context: BrandContext) -> List[Dict]:
        """Generate comprehensive color palette with usage guidelines"""
        trait = context.profile['personality_traits'][0].lower() if context.profile['personality_traits'] else 'professional'
        
        palettes = {
            'professional': [
                {'hex': '#1E3A8A', 'name': 'Corporate Blue', 'usage': 'Primary - Main brand color', 'psychology': 'Trust, professionalism, stability'},
                {'hex': '#64748B', 'name': 'Slate Gray', 'usage': 'Secondary - Supporting color', 'psychology': 'Balance, sophistication, neutrality'},
                {'hex': '#F8FAFC', 'name': 'Cloud White', 'usage': 'Background - Light surfaces', 'psychology': 'Clarity, openness, simplicity'},
                {'hex': '#0F172A', 'name': 'Deep Navy', 'usage': 'Text - Primary text color', 'psychology': 'Authority, depth, formality'},
                {'hex': '#3B82F6', 'name': 'Bright Blue', 'usage': 'Accent - CTAs and highlights', 'psychology': 'Action, engagement, trust'}
            ],
            'innovative': [
                {'hex': '#06B6D4', 'name': 'Cyan', 'usage': 'Primary - Innovation indicator', 'psychology': 'Technology, freshness, advancement'},
                {'hex': '#8B5CF6', 'name': 'Purple', 'usage': 'Secondary - Creative accent', 'psychology': 'Creativity, luxury, imagination'},
                {'hex': '#10B981', 'name': 'Emerald', 'usage': 'Accent - Success states', 'psychology': 'Growth, harmony, vitality'},
                {'hex': '#0F172A', 'name': 'Dark Slate', 'usage': 'Text - High contrast', 'psychology': 'Depth, sophistication, focus'},
                {'hex': '#F0F9FF', 'name': 'Ice Blue', 'usage': 'Background - Light mode', 'psychology': 'Clarity, freshness, innovation'}
            ],
            'creative': [
                {'hex': '#EC4899', 'name': 'Vibrant Pink', 'usage': 'Primary - Creative energy', 'psychology': 'Creativity, passion, boldness'},
                {'hex': '#F59E0B', 'name': 'Amber Gold', 'usage': 'Secondary - Warmth accent', 'psychology': 'Optimism, energy, warmth'},
                {'hex': '#8B5CF6', 'name': 'Purple', 'usage': 'Accent - Artistic flair', 'psychology': 'Imagination, luxury, creativity'},
                {'hex': '#1F2937', 'name': 'Charcoal', 'usage': 'Text - Strong contrast', 'psychology': 'Grounding, sophistication, stability'},
                {'hex': '#FFFFFF', 'name': 'Pure White', 'usage': 'Background - Clean canvas', 'psychology': 'Simplicity, purity, openness'}
            ],
            'trustworthy': [
                {'hex': '#1E40AF', 'name': 'Royal Blue', 'usage': 'Primary - Trust foundation', 'psychology': 'Trust, loyalty, dependability'},
                {'hex': '#059669', 'name': 'Forest Green', 'usage': 'Secondary - Growth signal', 'psychology': 'Stability, growth, reliability'},
                {'hex': '#FFFFFF', 'name': 'Pure White', 'usage': 'Background - Clarity', 'psychology': 'Honesty, transparency, purity'},
                {'hex': '#1F2937', 'name': 'Deep Gray', 'usage': 'Text - Professional tone', 'psychology': 'Seriousness, formality, depth'},
                {'hex': '#3B82F6', 'name': 'Sky Blue', 'usage': 'Accent - Friendly touch', 'psychology': 'Openness, clarity, accessibility'}
            ],
            'playful': [
                {'hex': '#F59E0B', 'name': 'Sunny Orange', 'usage': 'Primary - Energy burst', 'psychology': 'Joy, enthusiasm, energy'},
                {'hex': '#EC4899', 'name': 'Bubblegum Pink', 'usage': 'Secondary - Fun accent', 'psychology': 'Playfulness, youth, excitement'},
                {'hex': '#8B5CF6', 'name': 'Grape Purple', 'usage': 'Accent - Creative pop', 'psychology': 'Fun, imagination, uniqueness'},
                {'hex': '#000000', 'name': 'Black', 'usage': 'Text - Contrast anchor', 'psychology': 'Grounding, readability, definition'},
                {'hex': '#FEF3C7', 'name': 'Cream', 'usage': 'Background - Soft warmth', 'psychology': 'Comfort, warmth, approachability'}
            ],
            'bold': [
                {'hex': '#DC2626', 'name': 'Power Red', 'usage': 'Primary - Strong impact', 'psychology': 'Power, passion, action'},
                {'hex': '#000000', 'name': 'Bold Black', 'usage': 'Secondary - Strong base', 'psychology': 'Authority, sophistication, power'},
                {'hex': '#FFFFFF', 'name': 'Crisp White', 'usage': 'Background - High contrast', 'psychology': 'Clarity, boldness, directness'},
                {'hex': '#1F2937', 'name': 'Charcoal', 'usage': 'Text - Professional edge', 'psychology': 'Strength, stability, confidence'},
                {'hex': '#F59E0B', 'name': 'Gold Accent', 'usage': 'Accent - Premium touch', 'psychology': 'Excellence, prestige, success'}
            ],
            'elegant': [
                {'hex': '#000000', 'name': 'Luxury Black', 'usage': 'Primary - Sophistication', 'psychology': 'Elegance, luxury, timelessness'},
                {'hex': '#D4AF37', 'name': 'Antique Gold', 'usage': 'Secondary - Premium accent', 'psychology': 'Luxury, prestige, quality'},
                {'hex': '#FFFFFF', 'name': 'Pure White', 'usage': 'Background - Refined base', 'psychology': 'Sophistication, purity, elegance'},
                {'hex': '#1F2937', 'name': 'Graphite', 'usage': 'Text - Elegant contrast', 'psychology': 'Refinement, depth, sophistication'},
                {'hex': '#6B7280', 'name': 'Silver Gray', 'usage': 'Accent - Subtle luxury', 'psychology': 'Elegance, balance, understated luxury'}
            ]
        }
        
        return palettes.get(trait, palettes['professional'])

# ==================== API INSTANCES ====================

brand_contexts = {}
name_generator = UltraBrandNameGenerator()
content_generator = UltraContentGenerator()
logo_generator = UltraLogoGenerator()

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "BrandCraft Ultra API",
        "version": "3.0.0",
        "features": [
            "Ultra-advanced name generation (20+ names)",
            "Professional content with 6 metrics",
            "Comprehensive brand voice guidelines",
            "Enhanced social media strategies",
            "Advanced logo system with 5 types",
            "Detailed color psychology"
        ]
    }

@app.post("/api/brand/create")
async def create_brand_context(brand_input: BrandInput):
    context = BrandContext()
    context.update('domain', brand_input.domain)
    context.update('target_audience', brand_input.target_audience)
    context.update('personality_traits', brand_input.personality_traits)
    context.update('tone', brand_input.tone)
    context.update('emotional_goals', brand_input.emotional_goals)
    context.update('industry_context', brand_input.industry_context)
    context.update('unique_value', brand_input.unique_value)
    context.update('company_size', brand_input.company_size)
    context.update('budget_range', brand_input.budget_range)
    context.update('target_market', brand_input.target_market)
    
    brand_id = f"brand_{datetime.now().timestamp()}"
    brand_contexts[brand_id] = context
    
    return {
        "brand_id": brand_id,
        "context": context.to_dict(),
        "message": "Advanced brand context created successfully"
    }

@app.post("/api/brand/{brand_id}/names")
async def generate_names(brand_id: str, count: int = 20):
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    names = name_generator.generate_names(context, count)
    context.update('generated_names', [n['name'] for n in names])
    
    return {
        "brand_id": brand_id,
        "names": names,
        "total": len(names),
        "generation_strategy": "Ultra-advanced multi-algorithm approach"
    }

@app.post("/api/brand/{brand_id}/select-name")
async def select_brand_name(brand_id: str, name: str):
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    context.update('selected_name', name)
    
    story = content_generator.generate_brand_story(name, context)
    mission = content_generator.generate_mission_statement(name, context)
    vision = content_generator.generate_vision_statement(name, context)
    values = content_generator.generate_core_values(context)
    value_prop = content_generator.generate_value_proposition(name, context)
    voice_guide = content_generator.generate_brand_voice_guide(name, context)
    elevator_pitch = content_generator.generate_elevator_pitch(name, context)
    
    context.update('brand_story', story)
    context.update('mission_statement', mission)
    context.update('vision_statement', vision)
    context.update('core_values', values)
    context.update('value_proposition', value_prop)
    context.update('brand_voice_guide', voice_guide)
    
    return {
        "brand_id": brand_id,
        "selected_name": name,
        "brand_story": story,
        "mission": mission,
        "vision": vision,
        "core_values": values,
        "value_proposition": value_prop,
        "brand_voice_guide": voice_guide,
        "elevator_pitch": elevator_pitch
    }

@app.post("/api/brand/{brand_id}/complete")
async def get_complete_brand(brand_id: str):
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    brand_name = context.profile.get('selected_name')
    
    if not brand_name:
        names = name_generator.generate_names(context, 20)
        brand_name = names[0]['name']
        context.update('selected_name', brand_name)
    
    taglines = content_generator.generate_taglines(brand_name, context, 10)
    elevator_pitch = content_generator.generate_elevator_pitch(brand_name, context)
    logo_prompts = logo_generator.generate_logo_prompts(brand_name, context)
    color_palette = logo_generator.extract_color_palette(context)
    
    social_content = {}
    content_types = ['launch', 'value', 'testimonial', 'insight', 'team']
    
    for platform in ['twitter', 'linkedin', 'instagram', 'facebook']:
        social_content[platform] = []
        for content_type in content_types:
            post = content_generator.generate_social_content(
                brand_name, context, platform, content_type
            )
            social_content[platform].append(post)
    
    return {
        "brand_id": brand_id,
        "brand_name": brand_name,
        "brand_story": context.profile.get('brand_story'),
        "mission": context.profile.get('mission_statement'),
        "vision": context.profile.get('vision_statement'),
        "core_values": context.profile.get('core_values'),
        "value_proposition": context.profile.get('value_proposition'),
        "brand_voice_guide": context.profile.get('brand_voice_guide'),
        "elevator_pitch": elevator_pitch,
        "taglines": taglines,
        "logo_prompts": logo_prompts,
        "color_palette": color_palette,
        "social_content": social_content,
        "context": context.to_dict(),
        "message": "Ultra-advanced brand package generated successfully"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
