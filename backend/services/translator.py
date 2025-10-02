"""
AI Translation Service - OpenAI & Anthropic integration
Supports chunk-based translation with context preservation
"""
from typing import List, Optional, Dict, Any
from enum import Enum
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

        if self.provider == AIProvider.OPENAI:
            openai.api_key = settings.OPENAI_API_KEY
            self.model = "gpt-4"
            logger.info("Using OpenAI GPT-4 for translation")

        elif self.provider == AIProvider.ANTHROPIC:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = "claude-3-opus-20240229"
            logger.info("Using Anthropic Claude for translation")

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
            return self._translate_with_openai(prompt)
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

        prompt_parts = [
            f"Translate the following {source_name} text to {target_name}.",
            "",
            "Guidelines:",
            "- Preserve Markdown formatting (headers, lists, tables, links)",
            "- Maintain technical terminology accurately",
            "- Keep natural and fluent expression",
            "- Preserve line breaks and spacing",
            "- Do not translate code blocks",
        ]

        # Add glossary
        if glossary:
            prompt_parts.append("")
            prompt_parts.append("Use these custom terms:")
            for src_term, tgt_term in glossary.items():
                prompt_parts.append(f"- {src_term} → {tgt_term}")

        # Add context
        if context:
            prompt_parts.append("")
            prompt_parts.append(f"Previous context: {context}")

        prompt_parts.append("")
        prompt_parts.append(f"{source_name} text:")
        prompt_parts.append("---")
        prompt_parts.append(text)
        prompt_parts.append("---")
        prompt_parts.append("")
        prompt_parts.append(f"{target_name} translation:")

        return "\n".join(prompt_parts)

    def _translate_with_openai(self, prompt: str) -> str:
        """Translate using OpenAI GPT-4"""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator specializing in technical and educational content."
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
            return translated

        except Exception as e:
            logger.error(f"Anthropic translation failed: {str(e)}")
            raise ValueError(f"Translation failed: {str(e)}")

    def _split_markdown_chunks(self, markdown: str, chunk_size: int) -> List[str]:
        """
        Split Markdown into chunks by paragraphs

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
