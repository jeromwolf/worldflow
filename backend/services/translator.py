"""
AI Translation Service - OpenAI & Anthropic integration
Supports chunk-based translation with context preservation
"""
from typing import List, Optional, Dict, Any
from enum import Enum
import re
import openai
from anthropic import Anthropic
from loguru import logger
from core.config import settings


class AIProvider(str, Enum):
    """AI Provider options"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class TranslationService:
    """AI translation service with multiple provider support"""

    def __init__(self):
        self.provider = AIProvider(settings.AI_PROVIDER)
        self.mock_mode = False

        if self.provider == AIProvider.OPENAI:
            if settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                self.model = "gpt-4"
                logger.info("Using OpenAI GPT-4 for translation")
            else:
                self.mock_mode = True
                logger.warning("OPENAI_API_KEY not set - using mock translation")

        elif self.provider == AIProvider.ANTHROPIC:
            if settings.ANTHROPIC_API_KEY:
                self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                self.model = "claude-3-opus-20240229"
                logger.info("Using Anthropic Claude for translation")
            else:
                self.mock_mode = True
                logger.warning("ANTHROPIC_API_KEY not set - using mock translation")

    def translate_text(
        self,
        text: str,
        source_lang: str = "ko",
        target_lang: str = "en",
        context: Optional[str] = None,
        glossary: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Translate text with AI

        Args:
            text: Text to translate
            source_lang: Source language code (ko, en, ja, etc)
            target_lang: Target language code
            context: Previous context for coherence
            glossary: Custom terminology dictionary

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""

        # Mock mode: return text with translation prefix
        if self.mock_mode:
            return f"[MOCK TRANSLATION {source_lang}→{target_lang}]\n\n{text}"

        # Build prompt
        prompt = self._build_translation_prompt(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            context=context,
            glossary=glossary
        )

        # Call AI provider
        if self.provider == AIProvider.OPENAI:
            return self._translate_with_openai(prompt, source_lang, target_lang)
        else:
            return self._translate_with_anthropic(prompt)

    def translate_markdown(
        self,
        markdown: str,
        source_lang: str = "ko",
        target_lang: str = "en",
        glossary: Optional[Dict[str, str]] = None,
        chunk_size: int = 2000
    ) -> str:
        """
        Translate Markdown document in chunks with context preservation

        Args:
            markdown: Full markdown text
            source_lang: Source language
            target_lang: Target language
            glossary: Custom terminology
            chunk_size: Characters per chunk

        Returns:
            Translated markdown
        """
        # Split into chunks by paragraphs
        chunks = self._split_markdown_chunks(markdown, chunk_size)

        translated_chunks = []
        context = None

        for i, chunk in enumerate(chunks):
            logger.info(f"Translating chunk {i+1}/{len(chunks)}")

            # Translate with context from previous chunk
            translated = self.translate_text(
                text=chunk,
                source_lang=source_lang,
                target_lang=target_lang,
                context=context,
                glossary=glossary
            )

            translated_chunks.append(translated)

            # Update context (last 200 chars of translated text)
            context = translated[-200:] if len(translated) > 200 else translated

        return "\n\n".join(translated_chunks)

    def _build_translation_prompt(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str],
        glossary: Optional[Dict[str, str]]
    ) -> str:
        """Build translation prompt with instructions"""

        lang_names = {
            "ko": "Korean",
            "en": "English",
            "ja": "Japanese",
            "zh": "Chinese"
        }

        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)

        # Build a clean prompt - detailed instructions are in system message
        prompt_parts = []

        # Add glossary if provided
        if glossary:
            prompt_parts.append("Custom terminology:")
            for src_term, tgt_term in glossary.items():
                prompt_parts.append(f"  {src_term} = {tgt_term}")
            prompt_parts.append("")

        # Add context if provided
        if context:
            prompt_parts.append(f"[Context from previous section: {context}]")
            prompt_parts.append("")

        # Add the text to translate (just the text, no labels)
        prompt_parts.append(text)

        return "\n".join(prompt_parts)

    def _clean_translation_output(self, text: str) -> str:
        """
        Remove unwanted headers and labels from translation output

        Removes common AI-added headers like:
        - "English translation:"
        - "Korean translation:"
        - "Translation:"
        - "Translated text:"
        """
        # Common header patterns to remove
        header_patterns = [
            r"^English translation:\s*\n?",
            r"^Korean translation:\s*\n?",
            r"^Japanese translation:\s*\n?",
            r"^Chinese translation:\s*\n?",
            r"^Translation:\s*\n?",
            r"^Translated text:\s*\n?",
            r"^Here is the translation:\s*\n?",
            r"^Here's the translation:\s*\n?",
            # Korean equivalents
            r"^한글 번역:\s*\n?",
            r"^영어 번역:\s*\n?",
            r"^번역:\s*\n?",
            r"^번역 결과:\s*\n?",
        ]

        cleaned = text
        for pattern in header_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.MULTILINE)

        return cleaned.strip()

    def _translate_with_openai(self, prompt: str, source_lang: str = "en", target_lang: str = "ko") -> str:
        """Translate using OpenAI GPT-4"""

        lang_names = {
            "ko": "Korean",
            "en": "English",
            "ja": "Japanese",
            "zh": "Chinese"
        }
        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a professional translator translating from {source_name} to {target_name}.

CRITICAL RULES:
1. Translate EVERY word and sentence - skip NOTHING
2. Translate ALL text including Lorem ipsum, placeholder text, Latin/dummy text
3. For meaningless text like "Lorem ipsum", provide phonetic {target_name} translation
4. Output ONLY the translated text - no explanations, no labels, no headers
5. Preserve Markdown formatting (# * - etc.) but do not translate code blocks (```)
6. Maintain the same structure and line breaks as the original"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000
            )

            translated = response.choices[0].message.content.strip()

            # Remove any unwanted headers that may have been added
            translated = self._clean_translation_output(translated)

            return translated

        except Exception as e:
            logger.error(f"OpenAI translation failed: {str(e)}")
            raise ValueError(f"Translation failed: {str(e)}")

    def _translate_with_anthropic(self, prompt: str) -> str:
        """Translate using Anthropic Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                system="You are a professional translator specializing in technical and educational content.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            translated = response.content[0].text.strip()

            # Remove any unwanted headers that may have been added
            translated = self._clean_translation_output(translated)

            return translated

        except Exception as e:
            logger.error(f"Anthropic translation failed: {str(e)}")
            raise ValueError(f"Translation failed: {str(e)}")

    def _split_markdown_chunks(self, markdown: str, chunk_size: int) -> List[str]:
        """
        Split Markdown into chunks by sections (headers) for better context preservation

        Args:
            markdown: Full markdown text
            chunk_size: Max characters per chunk (soft limit for sections)

        Returns:
            List of markdown chunks
        """
        # First, try to split by markdown headers for better semantic chunking
        sections = self._split_by_sections(markdown)

        # If no sections found, fall back to paragraph-based splitting
        if len(sections) <= 1:
            return self._split_by_paragraphs(markdown, chunk_size)

        # Group sections into chunks based on size
        chunks = []
        current_chunk = []
        current_size = 0

        for section in sections:
            section_size = len(section)

            # If single section exceeds chunk size, add it separately
            if section_size > chunk_size:
                # Add current chunk if exists
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = []
                    current_size = 0

                # Add large section as its own chunk
                chunks.append(section)

            # If adding this section exceeds chunk size, start new chunk
            elif current_size + section_size > chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [section]
                current_size = section_size

            # Otherwise, add to current chunk
            else:
                current_chunk.append(section)
                current_size += section_size

        # Add remaining chunk
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    def _split_by_sections(self, markdown: str) -> List[str]:
        """
        Split markdown by headers (# ## ### etc.)

        Returns:
            List of sections (each starting with a header or content before first header)
        """
        lines = markdown.split("\n")
        sections = []
        current_section = []

        for line in lines:
            # Check if line is a header
            if re.match(r"^#{1,6}\s+", line):
                # Save previous section if exists
                if current_section:
                    sections.append("\n".join(current_section))
                # Start new section with this header
                current_section = [line]
            else:
                current_section.append(line)

        # Add last section
        if current_section:
            sections.append("\n".join(current_section))

        return sections

    def _split_by_paragraphs(self, markdown: str, chunk_size: int) -> List[str]:
        """
        Fallback: Split markdown by paragraphs when no sections found

        Args:
            markdown: Full markdown text
            chunk_size: Max characters per chunk

        Returns:
            List of markdown chunks
        """
        # Split by double newlines (paragraphs)
        paragraphs = markdown.split("\n\n")

        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_size = len(para)

            # If single paragraph exceeds chunk size, split it
            if para_size > chunk_size:
                # Add current chunk if exists
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = []
                    current_size = 0

                # Split large paragraph by sentences
                sentences = para.split(". ")
                for sentence in sentences:
                    if current_size + len(sentence) > chunk_size:
                        if current_chunk:
                            chunks.append("\n\n".join(current_chunk))
                        current_chunk = [sentence]
                        current_size = len(sentence)
                    else:
                        current_chunk.append(sentence)
                        current_size += len(sentence)

            # Normal paragraph
            elif current_size + para_size > chunk_size:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size

        # Add remaining chunk
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks


# Singleton instance
translator_service = TranslationService()
