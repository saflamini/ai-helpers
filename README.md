# Some helpful AI functions and patterns for audio data + embeddings

The recommended method for working with audio data and LLMs is AssemblyAI's LeMUR: https://www.assemblyai.com/blog/lemur-early-access/

This folder is useful in the event that you want to embed your audio data by semantically related chapters or 'sections' as opposed to using arbitrary character splitting.

`assembly_chapters.py` - example of transcribing an audio file with auto_chapters enabled
`chapter_helpers.py` - splits the transcript by chapter and includes the full text of each chapter in each section. 
`assembly_embed_by_chapter.py` - use chroma + openai embeddings to embed each section of the transcript and do similarity search

