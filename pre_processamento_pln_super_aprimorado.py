import re
import nltk
from nltk.corpus import stopwords
from nltk import ngrams
import spacy
import sys

def carregar_recursos():
    nlp_spacy = None
    palavras_de_parada = None
    try:
        nlp_spacy = spacy.load("pt_core_news_sm")
    except OSError:
        print("Modelo 'pt_core_news_sm' do spaCy não encontrado.")
        print("Por favor, execute 'python3.12 -m spacy download pt_core_news_sm' no seu terminal.")
        print("Consulte o README.md para mais instruções de configuração do ambiente.")
        sys.exit(1)
    
    try:
        palavras_de_parada = stopwords.words("portuguese")
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        print("Recursos 'stopwords' ou 'punkt' do NLTK não encontrados.")
        print("Por favor, execute os seguintes comandos no Python após ativar o ambiente virtual:")
        print("import nltk")
        print("nltk.download('stopwords')")
        print("nltk.download('punkt')")
        print("Consulte o README.md para mais instruções de configuração do ambiente.")
        sys.exit(1)
        
    return nlp_spacy, palavras_de_parada

def processar_corpus_super_aprimorado(corpus_textual, nlp_spacy, palavras_de_parada_pt):
    print(f"Corpus Original:\n{corpus_textual}\n" + "-" * 20 + "\n")

    texto_processado = corpus_textual
    
    # 1. Identificar e proteger "Sra. Rosa"
    entidade_sra_rosa_placeholder = "__SRA_ROSA_ENTIDADE__"
    sra_rosa_text_original = ""
    doc_inicial_para_entidades = nlp_spacy(texto_processado)
    for ent in doc_inicial_para_entidades.ents:
        if ent.label_ == "PER" and "Sra." in ent.text and "Rosa" in ent.text:
            sra_rosa_text_original = ent.text
            texto_processado = texto_processado.replace(ent.text, entidade_sra_rosa_placeholder, 1) # Substitui apenas a primeira ocorrência
            break

    # 2. Identificar e proteger expressões comuns (ex: "rosa em flor")
    expressoes_comuns = {
        "rosa em flor": "__EXPRESSAO_ROSA_EM_FLOR__"
    }
    expressao_rosa_em_flor_original = ""

    for expr_texto, expr_placeholder in expressoes_comuns.items():
        if expr_texto.lower() in texto_processado.lower(): # Busca case-insensitive da expressão
            # Encontrar a ocorrência exata para preservar capitalização original da expressão, se necessário, mas o placeholder é fixo
            try:
                match_expr = re.search(re.escape(expr_texto), texto_processado, re.IGNORECASE)
                if match_expr:
                    expressao_rosa_em_flor_original = match_expr.group(0)
                    texto_processado = texto_processado.replace(expressao_rosa_em_flor_original, expr_placeholder, 1)
            except Exception:
                 # Se a expressão não for encontrada com a capitalização original, tentamos uma substituição mais simples
                 # Esta parte pode ser melhorada para lidar com variações de capitalização da expressão
                 texto_processado = texto_processado.lower().replace(expr_texto.lower(), expr_placeholder, 1)
                 expressao_rosa_em_flor_original = expr_texto # Usar a forma padrão da expressão

    # 3. Tokenização e Normalização (conversão para minúsculas)
    # Dividir o texto pelos placeholders para tokenizar as partes separadamente
    # e depois juntar, preservando os placeholders como tokens.
    placeholders = [entidade_sra_rosa_placeholder, expressoes_comuns.get("rosa em flor")]
    placeholders = [p for p in placeholders if p and p in texto_processado] # Apenas placeholders presentes
    
    # Construir um regex para split que inclua todos os placeholders presentes
    split_pattern = "(" + "|".join(map(re.escape, placeholders)) + ")"
    
    tokens_brutos = []
    if placeholders:
        partes_texto = re.split(split_pattern, texto_processado)
    else:
        partes_texto = [texto_processado]

    regex_palavras = r"\b\w+\b"
    for parte in partes_texto:
        if not parte: continue
        if parte in placeholders:
            tokens_brutos.append(parte) # Adiciona o placeholder como está
        else:
            tokens_brutos.extend(re.findall(regex_palavras, parte.lower())) # Tokeniza e minúscula o resto

    print("--- Tokens Normalizados (com placeholders) ---")
    print(tokens_brutos)
    print("-" * 20 + "\n")

    # 4. Remoção de Stop Words (restaurando placeholders para formas textuais intermediárias)
    conjunto_palavras_de_parada = set(palavras_de_parada_pt)
    tokens_filtrados = []
    for token in tokens_brutos:
        if token == entidade_sra_rosa_placeholder:
            tokens_filtrados.append(sra_rosa_text_original if sra_rosa_text_original else "Sra. Rosa")
        elif token == expressoes_comuns.get("rosa em flor"):
            tokens_filtrados.append(expressao_rosa_em_flor_original if expressao_rosa_em_flor_original else "rosa em flor")
        elif token.lower() not in conjunto_palavras_de_parada:
            tokens_filtrados.append(token)
    
    print("--- Tokens Após Remoção de Stop Words (entidades/expressões restauradas) ---")
    print(tokens_filtrados)
    print("-" * 20 + "\n")

    # 5. Geração de N-gramas
    unigramas = tokens_filtrados
    bigramas = list(ngrams(tokens_filtrados, 2))
    trigramas = list(ngrams(tokens_filtrados, 3))
    print("--- Unigramas ---"); print(unigramas); print("-" * 20 + "\n")
    print("--- Bigramas ---"); print(bigramas); print("-" * 20 + "\n")
    print("--- Trigramas ---"); print(trigramas); print("-" * 20 + "\n")

    # 6. Lematização com spaCy e Pós-processamento para Agrupamento Semântico e Minusculização
    texto_para_lematizar = " ".join(tokens_filtrados)
    doc_para_lematizar = nlp_spacy(texto_para_lematizar)
    
    lemas_brutos_spacy = []
    for token_spacy in doc_para_lematizar:
        if token_spacy.text == sra_rosa_text_original:
            lemas_brutos_spacy.append("SRA_ROSA_PESSOA_ID") # Identificador para "Sra. Rosa"
        elif token_spacy.text.lower() == "rosa em flor": # Se a expressão foi mantida como um token
             lemas_brutos_spacy.append("EXPRESSAO_ROSA_EM_FLOR_ID")
        else:
            lemas_brutos_spacy.append(token_spacy.lemma_)

    mapa_semantico_flor = {
        "rosa": "flor_conceito", 
        "rosas": "flor_conceito", 
        "flor": "flor_conceito",
        "roso": "flor_conceito", 
        "rosar": "flor_conceito"
    }

    lematizado_final = []
    for lema_ou_id in lemas_brutos_spacy:
        if lema_ou_id == "SRA_ROSA_PESSOA_ID":
            lematizado_final.append("sra. rosa (pessoa)")
        elif lema_ou_id == "EXPRESSAO_ROSA_EM_FLOR_ID":
            lematizado_final.append("expressao_rosa_em_flor")
        elif lema_ou_id.lower() in mapa_semantico_flor:
            lematizado_final.append(mapa_semantico_flor[lema_ou_id.lower()])
        else:
            lematizado_final.append(lema_ou_id.lower()) # Lematiza e converte para minúsculas
    
    # Garantir que tudo na lista final seja string e minúsculo
    lematizado_final = [str(item).lower() for item in lematizado_final]

    print("--- Texto Lematizado, Agrupado Semanticamente e Minusculizado ---")
    print(lematizado_final)
    print("-" * 20 + "\n")

    print("Pré-processamento super aprimorado concluído.")

if __name__ == "__main__":
    corpus_exemplo = "A Sra. Rosa plantou uma rosa no jardim. O céu estava azul e a brisa era suave. Ela pensou: \"Seria maravilhoso se todos os dias fossem assim, tão tranquilos quanto uma rosa em flor.\""
    
    nlp_spacy_model, stop_words_pt_list = carregar_recursos()
    processar_corpus_super_aprimorado(corpus_exemplo, nlp_spacy_model, stop_words_pt_list)

