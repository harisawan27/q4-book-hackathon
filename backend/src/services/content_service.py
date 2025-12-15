"""
Content transformation service for personalization and translation.
"""
from typing import Optional
import google.generativeai as genai
from src.core.config import get_settings
from src.core.logging import logger
from src.models.auth import UserBackground

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_skill_description(level: str) -> str:
    """Convert skill level to descriptive text."""
    descriptions = {
        'none': 'no prior experience',
        'beginner': 'basic understanding',
        'intermediate': 'working knowledge',
        'advanced': 'expert-level understanding'
    }
    return descriptions.get(level, 'some experience')


def get_role_description(role: str) -> str:
    """Convert role to descriptive text."""
    descriptions = {
        'student': 'a student learning these concepts',
        'professional': 'a working professional',
        'hobbyist': 'a hobbyist exploring these topics',
        'researcher': 'an academic researcher'
    }
    return descriptions.get(role, 'someone interested in these topics')


async def personalize_content(
    content: str,
    chapter_title: str,
    background: UserBackground
) -> str:
    """
    Personalize chapter content based on user background.

    Args:
        content: The original chapter content (markdown)
        chapter_title: Title of the chapter
        background: User's background information

    Returns:
        Personalized content maintaining the same structure
    """
    software_desc = get_skill_description(background.software_skills)
    hardware_desc = get_skill_description(background.hardware_skills)
    role_desc = get_role_description(background.experience_level)

    system_prompt = f"""You are an expert technical writer who adapts educational content for different audiences.
Your task is to personalize the following chapter content for a specific reader.

READER PROFILE:
- Role: {role_desc}
- Software/Programming Skills: {software_desc}
- Hardware/Robotics Skills: {hardware_desc}

CRITICAL RULES:
1. PRESERVE ALL TECHNICAL ACCURACY - Never change facts, formulas, code, or technical details
2. PRESERVE MARKDOWN STRUCTURE - Keep all headings, code blocks, lists, and formatting intact
3. ADAPT EXPLANATIONS based on reader's background:
   - For beginners: Add brief clarifications for jargon, use analogies
   - For advanced readers: Skip basic explanations, focus on nuances
   - For students: Emphasize learning objectives and key takeaways
   - For professionals: Highlight practical applications
4. MAINTAIN THE SAME LENGTH - Don't significantly expand or reduce content
5. DO NOT ADD NEW INFORMATION - Only rephrase existing content
6. DO NOT REMOVE ANY SECTIONS - All original sections must remain

OUTPUT FORMAT:
Return ONLY the personalized markdown content. No explanations, no meta-commentary."""

    user_prompt = f"""Chapter: {chapter_title}

Original Content:
{content}

Personalize this content for the reader profile described above. Return only the personalized markdown."""

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=system_prompt
        )

        response = model.generate_content(user_prompt)

        # Check if response has valid parts
        if response.parts:
            return response.text.strip()
        elif response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            # Check finish reason for debugging
            if response.candidates:
                finish_reason = response.candidates[0].finish_reason
                logger.warning(f"Response finish_reason: {finish_reason}")
            logger.error("Empty response from personalization model")
            return content  # Return original on failure

    except Exception as e:
        logger.error(f"Personalization error: {str(e)}")
        raise RuntimeError(f"Failed to personalize content: {str(e)}")


async def translate_content(
    content: str,
    chapter_title: str,
    source_language: str = "English",
    target_language: str = "Urdu"
) -> str:
    """
    Translate chapter content to target language.

    Args:
        content: The original chapter content (markdown)
        chapter_title: Title of the chapter
        source_language: Source language (default: English)
        target_language: Target language (default: Urdu)

    Returns:
        Translated content maintaining the same structure
    """
    system_prompt = f"""You are an expert translator specializing in technical and educational content.
Your task is to translate the following chapter from {source_language} to {target_language}.

CRITICAL RULES:
1. PRESERVE ALL TECHNICAL TERMS - Keep code, variable names, function names, and technical keywords in English
2. PRESERVE MARKDOWN STRUCTURE - Keep all headings, code blocks, lists, links, and formatting intact
3. TRANSLATE ONLY THE EXPLANATORY TEXT - Translate descriptions, explanations, and prose
4. MAINTAIN TECHNICAL ACCURACY - Ensure translations accurately convey the original meaning
5. USE APPROPRIATE TECHNICAL {target_language} VOCABULARY - Use established technical terms where they exist
6. DO NOT TRANSLATE:
   - Code snippets and commands
   - File names and paths
   - URLs and links
   - Mathematical formulas
   - Variable names and identifiers
7. FORMAT FOR RTL (Right-to-Left) if applicable to target language

OUTPUT FORMAT:
Return ONLY the translated markdown content. No explanations, no meta-commentary."""

    user_prompt = f"""Chapter: {chapter_title}

Original Content ({source_language}):
{content}

Translate this content to {target_language}. Return only the translated markdown."""

    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=system_prompt
        )

        response = model.generate_content(user_prompt)

        # Check if response has valid parts
        if response.parts:
            return response.text.strip()
        elif response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            # Check finish reason for debugging
            if response.candidates:
                finish_reason = response.candidates[0].finish_reason
                logger.warning(f"Response finish_reason: {finish_reason}")
            logger.error("Empty response from translation model")
            return content  # Return original on failure

    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise RuntimeError(f"Failed to translate content: {str(e)}")
