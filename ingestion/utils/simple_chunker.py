from transformers import AutoTokenizer

class SimpleChunker:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        max_tokens: int = 300,
    ):
        self.max_tokens = max_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def create_chunks(self, text_content: str):
        paragraphs = [p.strip() for p in text_content.split("\n") if p.strip()]

        chunks = []
        current_chunk = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = len(self.tokenizer.encode(para, add_special_tokens=False))

            # Condição para verificar se cria um novo chunk ou incrementa em um existente (quando houver espaço)
            if current_tokens + para_tokens > self.max_tokens and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_tokens = para_tokens
            else:
                current_chunk.append(para)
                current_tokens += para_tokens

        # Se o chunk atual não estiver vazio, adiciona aos chunks
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks