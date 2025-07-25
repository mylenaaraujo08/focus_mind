# FocusMind

FocusMind é uma aplicação desktop desenvolvida em Python com Tkinter que oferece recursos de leitura acessível, especialmente voltada para pessoas com dislexia. O aplicativo inclui funcionalidades de texto-para-fala, coloração de sílabas e uma biblioteca de histórias clássicas.

## 🚀 Funcionalidades

- **Leitura Guiada**: Carregue arquivos TXT, PDF e DOCX para leitura com narração
- **Biblioteca de Histórias**: Histórias clássicas pré-carregadas com narração
- **Modo Dislexia**: Fonte e cores otimizadas para pessoas com dislexia
- **Coloração de Sílabas**: Separação visual de sílabas para facilitar a leitura
- **Sistema de Arquivos**: Salve e organize seus textos favoritos
- **Texto-para-Fala**: Narração usando Windows SAPI
- **Interface Intuitiva**: Design amigável e acessível

## 📋 Requisitos do Sistema

- **Sistema Operacional**: Windows (devido ao uso do Windows SAPI para TTS)
- **Python**: 3.8 ou superior
- **Resolução mínima**: 1024x768

## 📦 Bibliotecas Necessárias

### Bibliotecas Principais (obrigatórias)
```bash
pip install tkinter  # Geralmente já vem com Python
pip install pywin32  # Para Windows SAPI (texto-para-fala)
pip install PyMuPDF  # Para leitura de arquivos PDF
```

### Bibliotecas Opcionais (recomendadas)
```bash
pip install python-docx  # Para leitura de arquivos Word (.docx)
pip install pyphen       # Para separação avançada de sílabas
```

## 🛠️ Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd FocusMind
```

2. **Crie um ambiente virtual** (recomendado):
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual**:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instale as dependências**:
```bash
# Instalação completa (recomendada)
pip install pywin32 PyMuPDF python-docx pyphen

# Instalação mínima (apenas funcionalidades básicas)
pip install pywin32 PyMuPDF
```

## ▶️ Como Executar

### Método 1: Arquivo Principal
```bash
python main.py
```

### Método 2: Arquivo Alternativo
```bash
python app.py

## 🎯 Como Usar

### 1. **Primeiro Acesso**
- Execute o aplicativo
- Crie uma conta ou faça login
- Escolha entre "Leitura Guiada" ou "Biblioteca"

### 2. **Leitura Guiada**
- Carregue arquivos TXT, PDF ou DOCX
- Digite texto diretamente na área de texto
- Use os botões de controle para ler o texto
- Salve textos favoritos para acesso rápido

### 3. **Biblioteca de Histórias**
- Escolha uma história da lista
- Use o botão "História Aleatória" para surpresas
- Ative o Modo Dislexia e coloração de sílabas conforme necessário

### 4. **Recursos de Acessibilidade**
- **Modo Dislexia**: Ativa fonte e cores otimizadas
- **Colorir Sílabas**: Facilita a identificação de sílabas
- **Velocidade Otimizada**: TTS configurado para clareza

## ⚙️ Configurações Avançadas

### Velocidade do TTS
A velocidade está otimizada por padrão, mas pode ser ajustada nos arquivos:
- `frames/leitura_frame.py`: linha ~76 (`self.tts_engine.Rate = -1`)
- `frames/biblioteca_frame.py`: linha ~255 (`self.tts_engine.Rate = -2`)

### Limite de Arquivos
Por padrão, o sistema permite até 10 arquivos salvos. Para alterar:
- Edite `frames/leitura_frame.py`, linha ~28: `self.max_files = 10`

## 🔧 Solução de Problemas

### ❌ Erro "Windows SAPI não disponível"
```bash
pip install pywin32
# Depois execute:
python -c "import win32com.client; win32com.client.Dispatch('SAPI.SpVoice')"
```

### ❌ Erro ao carregar PDF
```bash
pip install PyMuPDF
```

### ❌ Erro ao carregar DOCX
```bash
pip install python-docx
```

### ❌ Sílabas não colorindo corretamente
```bash
pip install pyphen
```

## 🌟 Recursos Opcionais

- **OpenDyslexic Font**: Para melhor experiência com dislexia
- **Pyphen**: Para separação avançada de sílabas em português
- **Python-docx**: Para suporte completo a documentos Word

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Faça um pull request
---
