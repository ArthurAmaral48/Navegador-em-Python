import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.util import ngrams
from collections import Counter
import requests
from bs4 import BeautifulSoup
import spacy
from spellchecker import SpellChecker


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    import spacy.cli

    spacy.cli.download("pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")



def carregar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Carregar Arquivo Local",
        filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*"))
    )
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                caixa_entrada.delete("1.0", tk.END)
                caixa_entrada.insert("1.0", conteudo)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")


def buscar_da_web():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira uma URL válida!")
        return
    if not url.startswith("http"):
        url = "https://" + url
    try:
        resposta = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resposta.text, "html.parser")
        texto = soup.get_text()
        caixa_entrada.delete("1.0", tk.END)
        caixa_entrada.insert("1.0", texto)
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível acessar o site.\nErro: {e}")


def limpar_campos():
    caixa_entrada.delete("1.0", tk.END)
    entrada_url.delete(0, tk.END)
    caixa_resultado.delete("1.0", tk.END)



def obter_texto_entrada(nome_funcao):
    texto = caixa_entrada.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", f"Por favor, insira algum texto para {nome_funcao}!")
        return None
    return texto


def exibir_resultado(texto_resultado):
    caixa_resultado.delete("1.0", tk.END)
    caixa_resultado.insert("1.0", texto_resultado)



def executar_tokenizar():
    texto = obter_texto_entrada("tokenizar")
    if texto:
        blob = TextBlob(texto)
        res = f"SENTENÇAS DETECTADAS: {len(blob.sentences)}\n"
        res += f"PALAVRAS DETECTADAS: {len(blob.words)}\n\n"

        res += "LISTA DE PALAVRAS:\n"
        res += "-" * 30 + "\n"

        for palavra in blob.words:
            res += f"- {palavra}\n"

        exibir_resultado(res)


def executar_classes_gramaticais():
    texto = obter_texto_entrada("analisar classes gramaticais")
    if texto:
        blob = TextBlob(texto)
        res = "CLASSES GRAMATICAIS (POS TAGGING):\n"
        res += "-" * 45 + "\n"

        for palavra, classe in blob.tags:
            res += f"{palavra:<20} -> {classe}\n"

        exibir_resultado(res)


def executar_sintagmas():
    texto = obter_texto_entrada("extrair sintagmas")
    if texto:
        blob = TextBlob(texto)
        res = "SINTAGMAS NOMINAIS ENCONTRADOS:\n"
        res += "-" * 45 + "\n"

        for sintagma in blob.noun_phrases:
            res += f"- {sintagma}\n"

        exibir_resultado(res)


def executar_sentimento():
    texto = obter_texto_entrada("analisar sentimento")
    if texto:
        palavras_positivas = [
            "bom", "ótimo", "excelente", "maravilhoso", "gostar", "feliz", "legal",
            "sucesso", "recomendo", "lindo", "positivo", "ganho", "evolução", "vitoria",
            "enriquece", "avanço", "progresso", "inovações", "sublimes", "atemporal",
            "destaca", "relevante", "importante", "qualidade", "perfeito", "incrível",
            "brilhante", "fascinante", "genial", "acerto", "conquista", "benefício",
            "agradável", "interessante", "enriquecedor", "revolucionário", "primoroso",
            "notável"
        ]

        palavras_negativas = [
            "ruim", "péssimo", "erro", "difícil", "problema", "falha", "triste",
            "odiei", "pior", "defeito", "negativo", "perda", "crise", "baixo",
            "sofrimento", "prejuízo", "errado", "conflito", "guerra", "morte",
            "horror", "angústia", "solidão", "traumáticas", "cadáveres", "rejeitada",
            "vingativo", "violências", "exclusões", "ruína", "perigos", "remorso",
            "revolta", "monstruoso", "monstruosidade", "repulsa", "medo", "desespero",
            "trágico", "sombrios", "opressão", "dor", "rejeição", "alienação", "fatalismo",
            "hediondo", "repulsa"
        ]

        texto_lower = texto.lower()
        pos = sum(texto_lower.count(p) for p in palavras_positivas)
        neg = sum(texto_lower.count(p) for p in palavras_negativas)

        if pos > neg:
            interpretacao = "Texto predominantemente POSITIVO \U00002705"
        elif neg > pos:
            interpretacao = "Texto predominantemente NEGATIVO \U0000274C"
        else:
            interpretacao = "Texto NEUTRO \U0001F610"

        res = f"ANÁLISE DE SENTIMENTO EM PORTUGUÊS:\n" + "-" * 35 + "\n"
        res += f"Indicadores Positivos detectados: {pos}\n"
        res += f"Indicadores Negativos detectados: {neg}\n\n"
        res += f"Resultado: {interpretacao}\n"
        res += "-" * 35 + "\n"
        res += "*Nota: Análise baseada na contagem balanceada de palavras-chave emocionais e contextuais."

        exibir_resultado(res)

def executar_flexao():
    palavra = simpledialog.askstring("Plural/Singular", "Digite uma única palavra em português:")
    if palavra:
        palavra = palavra.strip()
        palavra_lower = palavra.lower()
        plural = palavra + "s"
        singular = palavra

        if palavra_lower.endswith(('r', 's', 'z')):
            plural = palavra + "es"
        elif palavra_lower.endswith('m'):
            plural = palavra[:-1] + "ns"
        elif palavra_lower.endswith(('al', 'el', 'ol', 'ul')):
            plural = palavra[:-1] + "is"
        elif palavra_lower.endswith('ão'):
            plural = palavra[:-2] + "ões"

        if palavra_lower.endswith('ns'):
            singular = palavra[:-2] + "m"
        elif palavra_lower.endswith(('res', 'zes')):
            singular = palavra[:-2]
        elif palavra_lower.endswith('ões'):
            singular = palavra[:-3] + "ão"
        elif palavra_lower.endswith('s') and len(palavra_lower) > 1:
            singular = palavra[:-1]

        res = f"ANÁLISE DE FLEXÃO EM PORTUGUÊS PARA: '{palavra}'\n" + "-" * 50 + "\n\n"
        res += f"Se for SINGULAR, o plural estimado é: {plural}\n"
        res += f"Se for PLURAL, o singular estimado é: {singular}\n"
        exibir_resultado(res)


def verificar_ortografia():
    texto = obter_texto_entrada("corrigir ortografia")
    if texto:
        corretor = SpellChecker(language='pt')
        for char in [".", ",", "!", "?", ";", ":", "(", ")", "\"", "'"]:
            texto = texto.replace(char, " ")
        palavras = texto.split()
        palavras_erradas = corretor.unknown(palavras)

        res = "CORREÇÃO ORTOGRÁFICA (PORTUGUÊS):\n" + "-" * 40 + "\n\n"
        if not palavras_erradas:
            res += "Nenhum erro ortográfico detectado no texto!"
        else:
            res += "Palavras possivelmente incorretas encontradas:\n"
            for p in palavras_erradas:
                res += f"• '{p}' -> Sugestão de Correção: {corretor.correction(p)}\n"
        exibir_resultado(res)


def executar_normalizacao():
    texto = obter_texto_entrada("normalizar (Lematização pt-br)")
    if texto:
        doc = nlp(texto)
        res = f"{'PALAVRA ORIGINAL':<25} | {'LEMA (Forma de Dicionário)':<25}\n"
        res += "-" * 60 + "\n"
        for token in doc:
            if not token.is_space and not token.is_punct:
                res += f"{token.text:<25} | {token.lemma_:<25}\n"
        exibir_resultado(res)


def executar_frequencia():
    texto = obter_texto_entrada("calcular frequência")
    if texto:
        palavras = [t.text.lower() for t in nlp(texto) if not t.is_punct and not t.is_space]
        contagem = Counter(palavras)
        mais_comuns = contagem.most_common(15)
        res = "PALAVRAS MAIS FREQUENTES NO TEXTO:\n" + "-" * 40 + "\n"
        for palavra, freq in mais_comuns:
            res += f"{palavra}: {freq}x\n"
        exibir_resultado(res)


def executar_wordnet():
    palavra = simpledialog.askstring("WordNet Português", "Digite um termo de busca:")
    if palavra:
        synsets = wordnet.synsets(palavra, lang='por')
        if not synsets:
            exibir_resultado(f"Nenhum registro correspondente encontrado na WordNet pt-br para '{palavra}'.")
            return
        res = f"CONSULTA WORDNET (PORTUGUÊS) PARA: '{palavra}'\n" + "=" * 50 + "\n\n"
        for syn in synsets:
            res += f"Definição Conceitual: {syn.definition()}\nSinônimos em pt: "
            sinonimos = [l.name() for l in syn.lemmas(lang='por')]
            res += ", ".join(set(sinonimos)) + "\n\n" + "-" * 45 + "\n"
        exibir_resultado(res)


def executar_stopwords():
    texto = obter_texto_entrada("remover stop words")
    if texto:
        stop_words_pt = set(stopwords.words('portuguese'))
        doc = nlp(texto)
        filtradas = [token.text for token in doc if token.text.lower() not in stop_words_pt and not token.is_space]
        res = "TEXTO FILTRADO (SEM STOP WORDS EM PORTUGUÊS):\n" + "-" * 50 + "\n"
        res += " ".join(filtradas)
        exibir_resultado(res)


def executar_ngramas():
    texto = obter_texto_entrada("gerar n-gramas")
    if texto:
        n = simpledialog.askinteger("N-Gramas", "Digite o valor do agrupamento (N):", initialvalue=2, minvalue=1)
        if n:
            palavras = [t.text for t in nlp(texto) if not t.is_punct and not t.is_space]
            if len(palavras) < n:
                messagebox.showwarning("Aviso", "Texto muito curto para gerar essa quantidade de N-gramas.")
                return
            grams = list(ngrams(palavras, n))
            res = f"{n}-GRAMAS GERADOS:\n" + "-" * 30 + "\n"
            for g in grams:
                res += f"- {' '.join(g)}\n"
            exibir_resultado(res)


def executar_spacy_ner():
    texto = obter_texto_entrada("executar NER")
    if texto:
        doc = nlp(texto)
        res = "RECONHECIMENTO DE ENTIDADES NOMEADAS EM PORTUGUÊS (NER):\n" + "-" * 60 + "\n"
        if not doc.ents:
            res += "Nenhuma entidade mapeada no texto (Nomes de pessoas, locais ou organizações)."
        for ent in doc.ents:
            res += f"Entidade: {ent.text:<25} | Tipo/Rótulo: {ent.label_}\n"
        exibir_resultado(res)


def executar_spacy_sim():
    texto1 = simpledialog.askstring("Texto 1", "Digite a primeira sentença em português:")
    texto2 = simpledialog.askstring("Texto 2", "Digite a segunda sentença em português:")
    if texto1 and texto2:
        doc1 = nlp(texto1)
        doc2 = nlp(texto2)
        similaridade = doc1.similarity(doc2)
        res = f"SIMILARIDADE SEMÂNTICA (MODELO PT-BR):\n" + "-" * 50 + "\n\n"
        res += f"Texto 1: \"{texto1}\"\nTexto 2: \"{texto2}\"\n\n"
        res += f"Índice de Proximidade: {similaridade:.4f} ({similaridade * 100:.1f}% de semelhança)"
        exibir_resultado(res)



janela = tk.Tk()
janela.title("Analisador de Texto NLP - Toolbox")
janela.geometry("950x700")
janela.configure(bg="#F3F3F3")

estilo = ttk.Style()
estilo.theme_use('clam')

frame_entrada = tk.Frame(janela, bg="#F3F3F3")
frame_entrada.pack(fill=tk.BOTH, padx=15, pady=5)

lbl_entrada = tk.Label(frame_entrada, text="Texto de entrada:", bg="#F3F3F3", fg="#333333", font=("Arial", 10, "bold"))
lbl_entrada.pack(anchor=tk.W, pady=(5, 2))

caixa_entrada = tk.Text(frame_entrada, height=10, font=("Courier New", 11), bd=1, relief=tk.SOLID)
caixa_entrada.pack(fill=tk.BOTH, expand=True)


frame_url = tk.Frame(janela, bg="#F3F3F3")
frame_url.pack(fill=tk.X, padx=15, pady=10)


lbl_url = tk.Label(frame_url, text="URL:", bg="#F3F3F3", font=("Arial", 10))
lbl_url.pack(side=tk.LEFT, padx=(0, 5))

entrada_url = ttk.Entry(frame_url, font=("Arial", 10))
entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

btn_buscar = ttk.Button(frame_url, text="Buscar da Web", command=buscar_da_web)
btn_buscar.pack(side=tk.LEFT, padx=2)

btn_carregar = ttk.Button(frame_url, text="Carregar Arquivo", command=carregar_arquivo)
btn_carregar.pack(side=tk.LEFT, padx=2)

btn_limpar = ttk.Button(frame_url, text="Limpar", command=limpar_campos)
btn_limpar.pack(side=tk.LEFT, padx=2)

separador = ttk.Separator(janela, orient='horizontal')
separador.pack(fill=tk.X, padx=15, pady=5)

notebook = ttk.Notebook(janela)
notebook.pack(fill=tk.BOTH, padx=15, pady=5)

config_abas = {
    "Tokenização": ("Tokenizar", executar_tokenizar),
    "Classes Gramaticais": ("Analisar Classes", executar_classes_gramaticais),
    "Sintagmas Nominais": ("Extrair Sintagmas", executar_sintagmas),
    "Sentimento": ("Analisar Sentimento", executar_sentimento),
    "Flexão (Plural/Singular)": ("Modificar Palavra", executar_flexao),
    "Ortografia": ("Corrigir Texto", verificar_ortografia),
    "Normalização": ("Gerar Lematização", executar_normalizacao),
    "Frequência": ("Contar Frequência", executar_frequencia),
    "WordNet": ("Consultar Base WordNet", executar_wordnet),
    "Stop Words": ("Remover Stop Words", executar_stopwords),
    "N-gramas": ("Gerar Agrupamentos", executar_ngramas),
    "NER (spaCy)": ("Mapear Entidades (NER)", executar_spacy_ner),
    "Similaridade (spaCy)": ("Medir Proximidade Semântica", executar_spacy_sim)
}

for nome_aba, (texto_botao, funcao) in config_abas.items():
    aba = tk.Frame(notebook, bg="white")
    notebook.add(aba, text=nome_aba)

    btn = ttk.Button(aba, text=texto_botao, command=funcao)
    btn.pack(anchor=tk.W, padx=15, pady=12)

frame_resultado = tk.Frame(janela, bg="#F3F3F3")
frame_resultado.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

lbl_resultado = tk.Label(frame_resultado, text="Resultado do Processamento:", bg="#F3F3F3", fg="#333333",
                         font=("Arial", 10, "bold"))
lbl_resultado.pack(anchor=tk.W, pady=(2, 2))

caixa_resultado = tk.Text(frame_resultado, font=("Courier New", 10), bd=1, relief=tk.SOLID, bg="#FAFAFA")
caixa_resultado.pack(fill=tk.BOTH, expand=True)

janela.mainloop()
