"""
BrandCraft Backend - FastAPI Implementation
Main application with AI orchestration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Initialize FastAPI app
app = FastAPI(title="BrandCraft API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class BrandInput(BaseModel):
    domain: str
    target_audience: str
    personality_traits: List[str]
    tone: str
    emotional_goals: List[str]
    additional_context: Optional[str] = None

class BrandNameRequest(BaseModel):
    context: BrandInput
    count: int = 10

class LogoRequest(BaseModel):
    brand_name: str
    context: BrandInput
    style_preferences: Optional[List[str]] = None

class ContentRequest(BaseModel):
    brand_name: str
    context: BrandInput
    content_type: str  # 'tagline', 'social_post', 'description'
    platform: Optional[str] = None
    topic: Optional[str] = None

# ==================== BRAND CONTEXT ENGINE ====================

class BrandContext:
    """
    Maintains shared brand memory for consistency
    """
    def __init__(self):
        self.profile = {
            'domain': None,
            'target_audience': None,
            'personality_traits': [],
            'tone': None,
            'visual_style': None,
            'emotional_goals': [],
            'generated_names': [],
            'selected_name': None,
            'logo_preferences': {},
            'content_history': [],
            'brand_colors': [],
            'created_at': datetime.now().isoformat()
        }
        self.embeddings_cache = {}
    
    def update(self, key: str, value):
        """Update brand context"""
        self.profile[key] = value
        return self.profile
    
    def get_context_prompt(self) -> str:
        """Generate context-aware prompt for AI models"""
        return f"""
Brand Context:
- Domain: {self.profile['domain']}
- Target Audience: {self.profile['target_audience']}
- Personality: {', '.join(self.profile['personality_traits'])}
- Tone: {self.profile['tone']}
- Emotional Goals: {', '.join(self.profile['emotional_goals'])}
- Brand Name: {self.profile.get('selected_name', 'Not yet selected')}
"""
    
    def to_dict(self) -> Dict:
        """Export brand context"""
        return self.profile


# ==================== NAME GENERATION ====================

class BrandNameGenerator:
    """
    Multi-strategy brand name generation with intelligent scoring
    """
    
    PERSONALITY_MODIFIERS = {
        'professional': ['Pro', 'Elite', 'Prime', 'Core', 'Peak'],
        'playful': ['Joy', 'Spark', 'Bounce', 'Fizz', 'Pop'],
        'innovative': ['Neo', 'Flex', 'Forge', 'Shift', 'Edge'],
        'trustworthy': ['True', 'Solid', 'Safe', 'Sure', 'Trust'],
        'creative': ['Art', 'Craft', 'Create', 'Design', 'Vision']
    }
    
    DOMAIN_KEYWORDS = {
        'technology': ['Tech', 'Digital', 'Smart', 'Cloud', 'Data', 'AI'],
        'fashion': ['Style', 'Wear', 'Mode', 'Chic', 'Trend'],
        'food': ['Taste', 'Flavor', 'Bite', 'Cook', 'Fresh'],
        'education': ['Learn', 'Skill', 'Know', 'Edu', 'Mind'],
        'health': ['Health', 'Vital', 'Fit', 'Well', 'Care'],
        'finance': ['Fund', 'Capital', 'Wealth', 'Pay', 'Coin']
    }
    
    def __init__(self):
        self.generated_cache = set()
    
    def generate_names(self, context: BrandContext, count: int = 10) -> List[Dict]:
        """
        Generate brand names using multiple strategies
        """
        candidates = []
        
        # Strategy 1: Descriptive names
        candidates.extend(self._generate_descriptive(context, count // 3))
        
        # Strategy 2: Abstract/Creative names
        candidates.extend(self._generate_abstract(context, count // 3))
        
        # Strategy 3: Portmanteau names
        candidates.extend(self._generate_portmanteau(context, count // 3))
        
        # Score all candidates
        scored_names = []
        for name in candidates:
            if name not in self.generated_cache:
                score = self._calculate_score(name, context)
                scored_names.append({
                    'name': name,
                    'score': score,
                    'memorability': self._calculate_memorability(name),
                    'uniqueness': self._calculate_uniqueness(name),
                    'relevance': self._calculate_relevance(name, context)
                })
                self.generated_cache.add(name)
        
        # Sort by score and return top results
        scored_names.sort(key=lambda x: x['score'], reverse=True)
        return scored_names[:count]
    
    def _generate_descriptive(self, context: BrandContext, count: int) -> List[str]:
        """Generate descriptive names: domain + modifier"""
        names = []
        domain = context.profile['domain'].lower()
        
        # Get domain keywords
        keywords = []
        for key, values in self.DOMAIN_KEYWORDS.items():
            if key in domain:
                keywords.extend(values)
        
        if not keywords:
            keywords = ['Smart', 'Pro', 'Plus', 'Hub', 'Zone']
        
        # Get personality modifiers
        modifiers = []
        for trait in context.profile['personality_traits']:
            trait_lower = trait.lower()
            if trait_lower in self.PERSONALITY_MODIFIERS:
                modifiers.extend(self.PERSONALITY_MODIFIERS[trait_lower])
        
        if not modifiers:
            modifiers = ['Pro', 'Plus', 'Prime']
        
        # Combine
        for keyword in keywords[:3]:
            for modifier in modifiers[:3]:
                names.append(f"{keyword}{modifier}")
                names.append(f"{modifier}{keyword}")
        
        return names[:count]
    
    def _generate_abstract(self, context: BrandContext, count: int) -> List[str]:
        """Generate abstract/creative names using phonetic patterns"""
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        consonants = ['b', 'c', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'x', 'z']
        
        names = []
        patterns = [
            'CVCV',    # e.g., Lyft
            'CVCCV',   # e.g., Stripe
            'CVCVC',   # e.g., Slack
            'VCVC',    # e.g., Uber
        ]
        
        for pattern in patterns:
            for _ in range(count // len(patterns)):
                name = ''
                for char in pattern:
                    if char == 'C':
                        name += np.random.choice(consonants)
                    else:
                        name += np.random.choice(vowels)
                names.append(name.capitalize())
        
        return names[:count]
    
    def _generate_portmanteau(self, context: BrandContext, count: int) -> List[str]:
        """Generate portmanteau names by blending words"""
        domain_words = context.profile['domain'].split()
        personality_words = context.profile['personality_traits']
        
        all_words = domain_words + personality_words
        names = []
        
        for i in range(len(all_words)):
            for j in range(i + 1, len(all_words)):
                word1 = all_words[i].lower()
                word2 = all_words[j].lower()
                
                if len(word1) >= 3 and len(word2) >= 3:
                    # Blend: first part of word1 + last part of word2
                    blend1 = word1[:len(word1)//2] + word2[len(word2)//2:]
                    blend2 = word1[:len(word1)//2 + 1] + word2[len(word2)//2 + 1:]
                    
                    names.append(blend1.capitalize())
                    names.append(blend2.capitalize())
        
        return names[:count]
    
    def _calculate_score(self, name: str, context: BrandContext) -> float:
        """
        Calculate comprehensive score for brand name
        """
        score = 0.0
        
        # Length score (shorter is better, 4-8 chars ideal)
        length = len(name)
        if 4 <= length <= 8:
            score += 30
        elif length < 4 or length > 12:
            score += 10
        else:
            score += 20
        
        # Memorability
        score += self._calculate_memorability(name) * 0.3
        
        # Uniqueness
        score += self._calculate_uniqueness(name) * 0.2
        
        # Relevance
        score += self._calculate_relevance(name, context) * 0.3
        
        # Pronounceability
        score += self._calculate_pronounceability(name) * 0.2
        
        return round(score, 2)
    
    def _calculate_memorability(self, name: str) -> float:
        """Score based on memorability factors"""
        score = 100.0
        
        # Penalize very long names
        if len(name) > 10:
            score -= (len(name) - 10) * 5
        
        # Reward simple syllable structure
        syllables = self._count_syllables(name)
        if syllables <= 3:
            score += 10
        
        return max(0, min(100, score))
    
    def _calculate_uniqueness(self, name: str) -> float:
        """Score based on uniqueness"""
        common_words = ['the', 'and', 'app', 'web', 'net', 'site', 'online']
        
        score = 100.0
        if name.lower() in common_words:
            score -= 50
        
        return score
    
    def _calculate_relevance(self, name: str, context: BrandContext) -> float:
        """Score based on relevance to domain"""
        score = 50.0  # Base score
        
        domain_words = context.profile['domain'].lower().split()
        name_lower = name.lower()
        
        # Check if any domain word is in the name
        for word in domain_words:
            if len(word) > 2 and word in name_lower:
                score += 25
        
        return min(100, score)
    
    def _calculate_pronounceability(self, name: str) -> float:
        """Score based on how easy it is to pronounce"""
        score = 100.0
        
        # Penalize consonant clusters
        consonant_cluster = 0
        for i in range(len(name) - 1):
            if name[i].lower() not in 'aeiou' and name[i+1].lower() not in 'aeiou':
                consonant_cluster += 1
        
        score -= consonant_cluster * 10
        
        return max(0, score)
    
    def _count_syllables(self, word: str) -> int:
        """Approximate syllable count"""
        vowels = 'aeiou'
        word = word.lower()
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        return max(1, count)


# ==================== LOGO GENERATION ====================

class LogoGenerator:
    """
    Logo generation coordinator
    In production, this would call Stable Diffusion API
    """
    
    PERSONALITY_VISUAL_MAP = {
        'professional': 'clean lines, corporate, structured, minimal, blue and gray tones',
        'playful': 'rounded shapes, bright colors, dynamic, fun, energetic',
        'innovative': 'geometric, futuristic, gradient, modern, tech-inspired',
        'trustworthy': 'solid, balanced, stable, blue tones, serif fonts',
        'creative': 'artistic, colorful, unique shapes, abstract, vibrant',
        'elegant': 'refined, sophisticated, gold accents, luxury, minimal',
        'bold': 'strong, impactful, high contrast, geometric, powerful'
    }
    
    DOMAIN_SYMBOLS = {
        'technology': 'circuit, chip, connection, digital',
        'fashion': 'clothing, thread, style, fabric',
        'food': 'plate, utensil, chef hat, ingredients',
        'education': 'book, graduation cap, lightbulb, pencil',
        'health': 'heart, pulse, wellness, leaf',
        'finance': 'coin, chart, growth, security'
    }
    
    def generate_logo_prompts(self, brand_name: str, context: BrandContext, 
                             styles: List[str] = None) -> List[Dict]:
        """
        Generate Stable Diffusion prompts for logos
        """
        if styles is None:
            styles = ['minimalist', 'modern', 'geometric', 'abstract']
        
        base_prompt = self._build_base_prompt(brand_name, context)
        
        logo_prompts = []
        for style in styles:
            prompt = f"{base_prompt}, {style} style, professional logo design, vector art, clean, scalable"
            negative_prompt = "text, letters, words, photo, realistic, cluttered, busy, complex, 3d render"
            
            logo_prompts.append({
                'style': style,
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'guidance_scale': 7.5,
                'steps': 50,
                'size': '512x512'
            })
        
        return logo_prompts
    
    def _build_base_prompt(self, brand_name: str, context: BrandContext) -> str:
        """Build base visual prompt from brand context"""
        visual_elements = []
        
        # Add personality-based visual descriptions
        for trait in context.profile['personality_traits']:
            trait_lower = trait.lower()
            if trait_lower in self.PERSONALITY_VISUAL_MAP:
                visual_elements.append(self.PERSONALITY_VISUAL_MAP[trait_lower])
        
        # Add domain symbols
        domain = context.profile['domain'].lower()
        for key, symbols in self.DOMAIN_SYMBOLS.items():
            if key in domain:
                visual_elements.append(symbols)
        
        visual_desc = ', '.join(visual_elements) if visual_elements else 'modern, professional'
        
        return f"Logo design for {brand_name}, {visual_desc}"
    
    def extract_color_palette(self, context: BrandContext) -> List[str]:
        """
        Extract color palette based on brand personality
        """
        personality_colors = {
            'professional': ['#1E3A8A', '#64748B', '#F8FAFC'],  # Blues and grays
            'playful': ['#F59E0B', '#EC4899', '#8B5CF6'],       # Bright colors
            'innovative': ['#06B6D4', '#8B5CF6', '#10B981'],    # Techy colors
            'trustworthy': ['#1E40AF', '#475569', '#FFFFFF'],   # Blues
            'creative': ['#EC4899', '#F59E0B', '#8B5CF6'],      # Vibrant
            'elegant': ['#000000', '#D4AF37', '#FFFFFF'],       # Black and gold
            'bold': ['#DC2626', '#000000', '#FFFFFF']           # Red and black
        }
        
        colors = []
        for trait in context.profile['personality_traits']:
            trait_lower = trait.lower()
            if trait_lower in personality_colors:
                colors.extend(personality_colors[trait_lower])
        
        # Return unique colors
        return list(set(colors))[:5] if colors else ['#1E3A8A', '#64748B', '#F8FAFC']


# ==================== CONTENT GENERATION ====================

class ContentGenerator:
    """
    Marketing content generation with brand voice consistency
    """
    
    PLATFORM_SPECS = {
        'twitter': {
            'max_length': 280,
            'style': 'concise, engaging, hashtag-friendly',
            'tone': 'conversational'
        },
        'linkedin': {
            'max_length': 1300,
            'style': 'professional, insightful, value-driven',
            'tone': 'authoritative yet approachable'
        },
        'instagram': {
            'max_length': 2200,
            'style': 'visual, story-driven, emotional',
            'tone': 'authentic and relatable'
        },
        'facebook': {
            'max_length': 500,
            'style': 'friendly, community-focused',
            'tone': 'warm and inclusive'
        }
    }
    
    def generate_taglines(self, brand_name: str, context: BrandContext, count: int = 5) -> List[Dict]:
        """
        Generate memorable taglines
        """
        taglines = []
        
        # Template-based generation (in production, use Gemini)
        templates = [
            f"Where {context.profile['domain']} meets excellence",
            f"Your {context.profile['personality_traits'][0] if context.profile['personality_traits'] else 'trusted'} {context.profile['domain']} partner",
            f"Empowering {context.profile['target_audience']} through {context.profile['domain']}",
            f"{', '.join(context.profile['personality_traits'][:2])} {context.profile['domain']} solutions",
            f"Transform your {context.profile['domain']} experience"
        ]
        
        for i, template in enumerate(templates[:count]):
            taglines.append({
                'tagline': template,
                'score': 85 - (i * 5),  # Decreasing scores
                'length': len(template.split()),
                'emotional_impact': self._analyze_emotional_impact(template, context)
            })
        
        return taglines
    
    def generate_social_content(self, brand_name: str, context: BrandContext, 
                               platform: str, topic: str) -> Dict:
        """
        Generate platform-specific social media content
        """
        if platform not in self.PLATFORM_SPECS:
            platform = 'twitter'
        
        spec = self.PLATFORM_SPECS[platform]
        
        # In production, this would call Gemini API with proper prompting
        # For now, generate template-based content
        
        content_templates = {
            'brand_launch': f"🚀 Excited to introduce {brand_name}! We're here to revolutionize {context.profile['domain']} for {context.profile['target_audience']}. Join us on this journey! #BrandLaunch #{brand_name}",
            'product_feature': f"💡 Discover what makes {brand_name} different: {', '.join(context.profile['personality_traits'])} approach to {context.profile['domain']}. Learn more → [link]",
            'customer_story': f"❤️ Nothing makes us happier than seeing {context.profile['target_audience']} succeed with {brand_name}. Your story is our story. #CustomerSuccess",
            'industry_insight': f"📊 The future of {context.profile['domain']} is {', '.join(context.profile['emotional_goals'])}. At {brand_name}, we're leading the way. What are your thoughts?",
            'behind_the_scenes': f"👋 Meet the team behind {brand_name}! We're passionate about bringing {', '.join(context.profile['personality_traits'])} solutions to {context.profile['target_audience']}."
        }
        
        content = content_templates.get(topic, content_templates['brand_launch'])
        
        # Ensure within platform limits
        if len(content) > spec['max_length']:
            content = content[:spec['max_length']-3] + '...'
        
        return {
            'platform': platform,
            'content': content,
            'hashtags': self._generate_hashtags(brand_name, context),
            'optimal_post_time': self._suggest_post_time(platform),
            'engagement_prediction': 'high'
        }
    
    def _analyze_emotional_impact(self, text: str, context: BrandContext) -> str:
        """Analyze emotional resonance of content"""
        # In production, use Hugging Face sentiment models
        target_emotions = context.profile['emotional_goals']
        
        if target_emotions:
            return f"Aligned with {target_emotions[0]}"
        return "Neutral"
    
    def _generate_hashtags(self, brand_name: str, context: BrandContext) -> List[str]:
        """Generate relevant hashtags"""
        hashtags = [
            f"#{brand_name.replace(' ', '')}",
            f"#{context.profile['domain'].replace(' ', '')}",
        ]
        
        for trait in context.profile['personality_traits'][:2]:
            hashtags.append(f"#{trait.replace(' ', '')}")
        
        return hashtags
    
    def _suggest_post_time(self, platform: str) -> str:
        """Suggest optimal posting time"""
        optimal_times = {
            'twitter': '12:00 PM - 1:00 PM',
            'linkedin': '8:00 AM - 10:00 AM',
            'instagram': '11:00 AM - 1:00 PM',
            'facebook': '1:00 PM - 3:00 PM'
        }
        return optimal_times.get(platform, '12:00 PM')


# ==================== SENTIMENT ANALYZER ====================

class SentimentAnalyzer:
    """
    Emotional intelligence and tone analysis
    In production, integrate Hugging Face models
    """
    
    EMOTION_KEYWORDS = {
        'joy': ['happy', 'excited', 'thrilled', 'delighted', 'wonderful'],
        'trust': ['reliable', 'confident', 'secure', 'dependable', 'honest'],
        'innovation': ['new', 'cutting-edge', 'revolutionary', 'advanced', 'future'],
        'calm': ['peaceful', 'serene', 'balanced', 'harmonious', 'gentle'],
        'energy': ['dynamic', 'vibrant', 'energetic', 'powerful', 'bold']
    }
    
    def analyze_content(self, text: str, target_emotions: List[str]) -> Dict:
        """
        Analyze emotional impact and alignment
        """
        # Detect emotions in text
        detected_emotions = self._detect_emotions(text)
        
        # Calculate alignment with target emotions
        alignment_score = self._calculate_alignment(detected_emotions, target_emotions)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            detected_emotions, 
            target_emotions, 
            alignment_score
        )
        
        return {
            'overall_sentiment': self._get_overall_sentiment(text),
            'detected_emotions': detected_emotions,
            'target_emotions': target_emotions,
            'alignment_score': alignment_score,
            'recommendations': recommendations
        }
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Detect emotions present in text"""
        text_lower = text.lower()
        detected = []
        
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if emotion not in detected:
                        detected.append(emotion)
                    break
        
        return detected if detected else ['neutral']
    
    def _get_overall_sentiment(self, text: str) -> str:
        """Get overall sentiment (positive/negative/neutral)"""
        positive_words = ['great', 'excellent', 'amazing', 'wonderful', 'best', 'love', 'excited']
        negative_words = ['bad', 'terrible', 'worst', 'hate', 'awful', 'poor']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'
    
    def _calculate_alignment(self, detected: List[str], target: List[str]) -> float:
        """Calculate alignment score (0-100)"""
        if not target:
            return 75.0  # Default score if no target
        
        matches = len(set(detected) & set(target))
        return (matches / len(target)) * 100
    
    def _generate_recommendations(self, detected: List[str], 
                                 target: List[str], score: float) -> List[str]:
        """Generate improvement recommendations"""
        if score >= 80:
            return ["✅ Content is well-aligned with brand emotions"]
        
        recommendations = []
        missing_emotions = set(target) - set(detected)
        
        for emotion in missing_emotions:
            if emotion in self.EMOTION_KEYWORDS:
                keywords = ', '.join(self.EMOTION_KEYWORDS[emotion][:3])
                recommendations.append(
                    f"💡 Try incorporating words like: {keywords} to evoke '{emotion}'"
                )
        
        if score < 50:
            recommendations.append(
                "⚠️ Consider revising the tone to better match brand personality"
            )
        
        return recommendations


# ==================== API ENDPOINTS ====================

# Global instances
brand_contexts = {}  # In production, use database
name_generator = BrandNameGenerator()
logo_generator = LogoGenerator()
content_generator = ContentGenerator()
sentiment_analyzer = SentimentAnalyzer()

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "BrandCraft API",
        "version": "1.0.0"
    }

@app.post("/api/brand/create")
async def create_brand_context(brand_input: BrandInput):
    """Create a new brand context"""
    context = BrandContext()
    context.update('domain', brand_input.domain)
    context.update('target_audience', brand_input.target_audience)
    context.update('personality_traits', brand_input.personality_traits)
    context.update('tone', brand_input.tone)
    context.update('emotional_goals', brand_input.emotional_goals)
    
    # Generate unique ID
    brand_id = f"brand_{datetime.now().timestamp()}"
    brand_contexts[brand_id] = context
    
    return {
        "brand_id": brand_id,
        "context": context.to_dict(),
        "message": "Brand context created successfully"
    }

@app.post("/api/brand/{brand_id}/names")
async def generate_names(brand_id: str, count: int = 10):
    """Generate brand names"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    names = name_generator.generate_names(context, count)
    
    # Update context
    context.update('generated_names', [n['name'] for n in names])
    
    return {
        "brand_id": brand_id,
        "names": names,
        "total": len(names)
    }

@app.post("/api/brand/{brand_id}/select-name")
async def select_brand_name(brand_id: str, name: str):
    """Select a brand name"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    context.update('selected_name', name)
    
    return {
        "brand_id": brand_id,
        "selected_name": name,
        "message": "Brand name selected"
    }

@app.post("/api/brand/{brand_id}/logos")
async def generate_logos(brand_id: str, styles: Optional[List[str]] = None):
    """Generate logo prompts"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    brand_name = context.profile.get('selected_name')
    
    if not brand_name:
        raise HTTPException(status_code=400, detail="Please select a brand name first")
    
    logo_prompts = logo_generator.generate_logo_prompts(brand_name, context, styles)
    color_palette = logo_generator.extract_color_palette(context)
    
    return {
        "brand_id": brand_id,
        "brand_name": brand_name,
        "logo_prompts": logo_prompts,
        "color_palette": color_palette,
        "message": "Use these prompts with Stable Diffusion API"
    }

@app.post("/api/brand/{brand_id}/taglines")
async def generate_taglines(brand_id: str, count: int = 5):
    """Generate brand taglines"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    brand_name = context.profile.get('selected_name', 'Your Brand')
    
    taglines = content_generator.generate_taglines(brand_name, context, count)
    
    return {
        "brand_id": brand_id,
        "brand_name": brand_name,
        "taglines": taglines
    }

@app.post("/api/brand/{brand_id}/social-content")
async def generate_social_content(brand_id: str, platform: str, topic: str = "brand_launch"):
    """Generate social media content"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    brand_name = context.profile.get('selected_name', 'Your Brand')
    
    content = content_generator.generate_social_content(brand_name, context, platform, topic)
    
    return {
        "brand_id": brand_id,
        "content": content
    }

@app.post("/api/analyze/sentiment")
async def analyze_sentiment(text: str, target_emotions: List[str]):
    """Analyze sentiment and emotional impact"""
    analysis = sentiment_analyzer.analyze_content(text, target_emotions)
    
    return {
        "text": text,
        "analysis": analysis
    }

@app.get("/api/brand/{brand_id}")
async def get_brand(brand_id: str):
    """Get complete brand package"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    
    return {
        "brand_id": brand_id,
        "brand_package": context.to_dict()
    }

@app.post("/api/brand/{brand_id}/complete")
async def get_complete_brand(brand_id: str):
    """Get complete brand with all assets"""
    if brand_id not in brand_contexts:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    context = brand_contexts[brand_id]
    brand_name = context.profile.get('selected_name')
    
    if not brand_name:
        # Generate names if not selected
        names = name_generator.generate_names(context, 10)
        brand_name = names[0]['name']
        context.update('selected_name', brand_name)
    
    # Generate all assets
    taglines = content_generator.generate_taglines(brand_name, context, 5)
    logo_prompts = logo_generator.generate_logo_prompts(brand_name, context)
    colors = logo_generator.extract_color_palette(context)
    
    social_content = {}
    for platform in ['twitter', 'linkedin', 'instagram']:
        social_content[platform] = content_generator.generate_social_content(
            brand_name, context, platform, 'brand_launch'
        )
    
    return {
        "brand_id": brand_id,
        "brand_name": brand_name,
        "context": context.to_dict(),
        "taglines": taglines,
        "logo_prompts": logo_prompts,
        "color_palette": colors,
        "social_content": social_content,
        "message": "Complete brand package generated"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
