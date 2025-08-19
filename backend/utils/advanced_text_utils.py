"""Advanced text utility functions"""
import re
import statistics
from typing import Dict, Any, List
from collections import Counter
import html

def text_statistics(text: str) -> Dict[str, Any]:
    """Get comprehensive text statistics"""
    if not text:
        return {"error": "No text provided"}
    
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]+', text)
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    
    # Word frequency
    word_freq = Counter(words)
    most_common = word_freq.most_common(10)
    
    # Sentence lengths
    sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if s.strip()]
    avg_sentence_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
    
    # Readability metrics (simplified)
    avg_word_length = statistics.mean([len(word) for word in words]) if words else 0
    
    return {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "total_sentences": len([s for s in sentences if s.strip()]),
        "total_paragraphs": len(paragraphs),
        "avg_sentence_length": round(avg_sentence_length, 2),
        "avg_word_length": round(avg_word_length, 2),
        "most_common_words": most_common,
        "longest_word": max(words, key=len) if words else "",
        "shortest_word": min(words, key=len) if words else "",
        "lexical_diversity": round(len(set(words)) / len(words), 3) if words else 0
    }

def find_replace(text: str, find: str, replace: str, case_sensitive: bool = True, whole_word: bool = False) -> Dict[str, Any]:
    """Find and replace text with options"""
    if not text or not find:
        return {"result": text, "replacements": 0}
    
    flags = 0 if case_sensitive else re.IGNORECASE
    
    if whole_word:
        pattern = r'\b' + re.escape(find) + r'\b'
    else:
        pattern = re.escape(find)
    
    result, count = re.subn(pattern, replace, text, flags=flags)
    
    return {
        "result": result,
        "replacements": count,
        "original_length": len(text),
        "new_length": len(result)
    }

def text_splitter(text: str, delimiter: str = "\n", max_length: int = None) -> Dict[str, Any]:
    """Split text by delimiter or length"""
    if not text:
        return {"parts": [], "count": 0}
    
    if max_length:
        # Split by length
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    else:
        # Split by delimiter
        if delimiter == "\\n":
            delimiter = "\n"
        elif delimiter == "\\t":
            delimiter = "\t"
        parts = text.split(delimiter)
    
    return {
        "parts": parts,
        "count": len(parts),
        "total_length": len(text),
        "avg_part_length": round(len(text) / len(parts), 2) if parts else 0
    }

def text_merger(texts: List[str], separator: str = "\n") -> Dict[str, str]:
    """Merge multiple texts with separator"""
    if separator == "\\n":
        separator = "\n"
    elif separator == "\\t":
        separator = "\t"
    
    result = separator.join(texts)
    
    return {
        "result": result,
        "parts_merged": len(texts),
        "total_length": len(result)
    }

def keyword_density(text: str, keywords: List[str] = None) -> Dict[str, Any]:
    """Calculate keyword density"""
    if not text:
        return {"error": "No text provided"}
    
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)
    word_freq = Counter(words)
    
    if keywords:
        # Calculate density for specific keywords
        densities = {}
        for keyword in keywords:
            count = word_freq.get(keyword.lower(), 0)
            density = (count / total_words) * 100 if total_words > 0 else 0
            densities[keyword] = {
                "count": count,
                "density": round(density, 2)
            }
        return {"keyword_densities": densities, "total_words": total_words}
    else:
        # Top 20 words with density
        top_words = word_freq.most_common(20)
        densities = {}
        for word, count in top_words:
            density = (count / total_words) * 100
            densities[word] = {
                "count": count,
                "density": round(density, 2)
            }
        return {"word_densities": densities, "total_words": total_words}

def text_cleaner(text: str, options: Dict[str, bool] = None) -> Dict[str, str]:
    """Clean text with various options"""
    if not text:
        return {"result": ""}
    
    result = text
    operations = []
    
    if not options:
        options = {
            "remove_extra_spaces": True,
            "remove_line_breaks": False,
            "remove_tabs": False,
            "remove_punctuation": False,
            "remove_numbers": False,
            "remove_special_chars": False
        }
    
    if options.get("remove_extra_spaces", False):
        result = re.sub(r'\s+', ' ', result)
        operations.append("Removed extra spaces")
    
    if options.get("remove_line_breaks", False):
        result = result.replace('\n', ' ').replace('\r', ' ')
        operations.append("Removed line breaks")
    
    if options.get("remove_tabs", False):
        result = result.replace('\t', ' ')
        operations.append("Removed tabs")
    
    if options.get("remove_punctuation", False):
        result = re.sub(r'[^\w\s]', '', result)
        operations.append("Removed punctuation")
    
    if options.get("remove_numbers", False):
        result = re.sub(r'\d+', '', result)
        operations.append("Removed numbers")
    
    if options.get("remove_special_chars", False):
        result = re.sub(r'[^a-zA-Z0-9\s]', '', result)
        operations.append("Removed special characters")
    
    result = result.strip()
    
    return {
        "result": result,
        "operations_performed": operations,
        "original_length": len(text),
        "cleaned_length": len(result)
    }

def html_stripper(text: str) -> Dict[str, str]:
    """Remove HTML tags from text"""
    if not text:
        return {"result": ""}
    
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    clean = html.unescape(clean)
    
    # Clean up extra whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return {
        "result": clean,
        "original_length": len(text),
        "cleaned_length": len(clean),
        "tags_removed": len(re.findall(r'<[^>]+>', text))
    }

def regex_tester(text: str, pattern: str, flags: str = "") -> Dict[str, Any]:
    """Test regex patterns against text"""
    if not text or not pattern:
        return {"error": "Text and pattern are required"}
    
    try:
        # Parse flags
        flag_map = {
            'i': re.IGNORECASE,
            'm': re.MULTILINE,
            's': re.DOTALL,
            'x': re.VERBOSE
        }
        
        regex_flags = 0
        for flag in flags.lower():
            if flag in flag_map:
                regex_flags |= flag_map[flag]
        
        # Compile pattern
        compiled = re.compile(pattern, regex_flags)
        
        # Find all matches
        matches = []
        for match in compiled.finditer(text):
            matches.append({
                "match": match.group(),
                "start": match.start(),
                "end": match.end(),
                "groups": match.groups()
            })
        
        # Test if pattern matches
        is_match = bool(compiled.search(text))
        
        return {
            "is_match": is_match,
            "matches": matches,
            "match_count": len(matches),
            "pattern": pattern,
            "flags": flags
        }
    
    except re.error as e:
        return {"error": f"Invalid regex pattern: {str(e)}"}

def language_detector(text: str) -> Dict[str, Any]:
    """Detect language of text (basic implementation)"""
    if not text:
        return {"error": "No text provided"}
    
    # Simple language detection based on common words
    # This is a basic implementation - in production you'd use a proper library
    
    common_words = {
        'english': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with'],
        'spanish': ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no'],
        'french': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
        'german': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'],
        'italian': ['il', 'di', 'che', 'e', 'la', 'per', 'in', 'un', 'è', 'non']
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return {"language": "unknown", "confidence": 0}
    
    scores = {}
    for lang, common in common_words.items():
        score = sum(1 for word in words if word in common)
        scores[lang] = score / len(words) * 100
    
    detected_lang = max(scores, key=scores.get)
    confidence = scores[detected_lang]
    
    return {
        "language": detected_lang,
        "confidence": round(confidence, 2),
        "all_scores": {lang: round(score, 2) for lang, score in scores.items()}
    }

def text_sentiment(text: str) -> Dict[str, Any]:
    """Basic sentiment analysis"""
    if not text:
        return {"error": "No text provided"}
    
    # Simple sentiment analysis using word lists
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
        'love', 'like', 'happy', 'joy', 'pleased', 'satisfied', 'perfect', 'best'
    ]
    
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry',
        'disappointed', 'frustrated', 'worst', 'annoying', 'stupid', 'useless'
    ]
    
    words = re.findall(r'\b\w+\b', text.lower())
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    
    total_sentiment_words = positive_count + negative_count
    
    if total_sentiment_words == 0:
        sentiment = "neutral"
        score = 0
    elif positive_count > negative_count:
        sentiment = "positive"
        score = (positive_count - negative_count) / len(words) * 100
    elif negative_count > positive_count:
        sentiment = "negative"
        score = (negative_count - positive_count) / len(words) * 100
    else:
        sentiment = "neutral"
        score = 0
    
    return {
        "sentiment": sentiment,
        "score": round(score, 2),
        "positive_words": positive_count,
        "negative_words": negative_count,
        "total_words": len(words)
    }