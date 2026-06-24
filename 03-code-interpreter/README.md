# 03 - Generative AI Tools

## Doel

Demonstreren hoe Azure OpenAI gebruik kan maken van verschillende tools binnen de Responses API.

In deze module worden de belangrijkste tool-categorieën behandeld:

* Basic Responses
* Code Interpreter
* Web Search
* File Search
* Function Calling
* Retrieval-Augmented Generation (RAG) met eigen documenten

Meer info: https://learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps/

---

## Labs

### Lab 001 - Basic Response

**Bestand:** `lab001-basic-response.py`

Controleert de basisverbinding met Azure OpenAI en voert een eenvoudige prompt uit via de Responses API.

Onderwerpen:

* Azure OpenAI configuratie
* Responses API
* Deployment gebruik
* Eerste AI response

---

### Lab 002 - Code Interpreter

**Bestand:** `lab002-code-interpreter.py`

Toont hoe de Code Interpreter tool kan worden toegevoegd aan een Responses API request zodat het model Python-code kan uitvoeren.

Onderwerpen:

* Tool gebruik binnen Responses API
* Code Interpreter
* Rekenkundige berekeningen
* Container execution

---

### Lab 003 - Web Search

**Bestand:** `lab003-web-search.py`

Demonstreert hoe actuele informatie van internet kan worden opgehaald met behulp van de Web Search tool.

Onderwerpen:

* Web Search tool
* Realtime informatie ophalen
* Responses API tools

---

### Lab 004 - File Search

**Bestand:** `lab004-file-search.py`

Gebruikt een eigen kennisbank met retro DOS games die wordt opgeslagen in een Vector Store.

Onderwerpen:

* Vector Stores
* Document indexing
* Semantic Search
* File Search tool

Gebruikte kennisbank:

Bestand : `retro-dos-race-games.md`

* Stunts
* Test Drive II
* Street Rod
* Grand Prix Circuit

---

### Lab 005 - Function Calling

**Bestand:** `lab005-function-calling.py`

Demonstreert hoe een AI-model functies kan aanroepen die in Python beschikbaar zijn.

Voorbeeldfunctie:

* `get_time()`

Onderwerpen:

* Function Calling
* Tool orchestration
* Tool output verwerken
* Conversatiecontext behouden

---

### Lab 006 - Exercise: Use Your Own Data

**Bestand:** `lab006-exercise-use-own-data.py`

Volledige oefening gebaseerd op Microsoft Learn waarbij PDF-brochures worden geïndexeerd in een Vector Store.

De applicatie combineert:

* File Search
* Web Search
* Conversatiecontext
* Eigen documenten

Onderwerpen:

* PDF document indexing
* Vector Stores
* Retrieval-Augmented Generation (RAG)
* Conversational AI
* Hybrid search

Voorbeeldvragen:

* What hotels does Margie's Travel offer?
* What's happening in San Francisco next month?
* Which destinations are available in the brochures?

---

## Gedeelde componenten

### shared/config.py

Laadt configuratie uit het `.env` bestand.

### shared/openai_client.py

Centrale Azure OpenAI client die door meerdere labs wordt gebruikt.

---

## Vereisten

Python packages:

```bash
pip install -r requirements.txt
```

Benodigde omgevingsvariabelen:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_KEY=
```

---

## Learn Module

https://learn.microsoft.com/en-us/training/modules/use-generative-ai-tools/

Microsoft Learn:

* Use Code Interpreter
* Use File Search
* Use Function Calling
* Use Web Search
* Use Your Own Data
