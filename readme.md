The prime structure can be generated using primestructure.py and it is a kind of Universal structure.

It was invented a year from now.

A clear preview of the structure is in this post



https://lnkd.in/p/dFX9s5vC





The fundamental structure is discussed in this book before



https://books.google.cz/books/about/Fundamental\_Structure\_of\_The\_Universe.html?id=3n41EQAAQBAJ\&redir\_esc=y



And there is more on the new Pie Function for Prime Density in this book, again the book launched an year before

https://www.google.cz/books/edition/The\_Golden\_Distribution\_Before\_Universe/yTiREQAAQBAJ?hl=en\&gbpv=1\&dq=inauthor:%22Wasiful+Alam%22\&printsec=frontcover





And the Prime Base System is discussed in this paper, it serves a broader reason, required to be in another book.

https://www.researchgate.net/publication/401370203\_The\_Prime\_Algorithm\_encodes\_data\_using\_a\_function\_that\_depends\_on\_Prime\_base



This is an ongoing development for five years on this topic and still in progress for understanding the imaginary plane.


About 3000 page lean code made readable
Lean Code extraction from the Clude Alpoge Proof of Riemann Hypothesis was done using a vectorized data base RAG search to find the closest matches for these


"theorem lemma def Riemann zeta function Dirichlet series Euler product critical strip critical line Re s",

"theorem lemma analytic continuation meromorphic pole functional equation completed zeta xi trivial zeros",

"theorem lemma bound growth estimate logarithmic derivative zeta prime over zeta strip convexity",

"theorem lemma zeros critical line nontrivial zeros argument principle Jensen Hadamard explicit formula",

"theorem main theorem Riemann hypothesis zeros real part half prime counting error bound"



The whole pipeline turns a Lean formalization repository into a searchable index, a dependency graph, and stage-ordered slices of theorems and lemmas. It combines vector similarity search with dependency graph traversal so you do not have to read thousands of .lean files by hand or guess which helper lemmas a theorem relies on.



Creating the Databases (lean\_vector\_db and proof\_graph.sqlite)



Source scanning and declaration parsing happen first. The indexer walks the .lean source files in the repository (F:\\Codes\\remanhypothesis\\riemann-hypothesis) and splits them into individual declarations such as theorem, lemma, def, abbrev, or axiom, recording each declaration's ID, file path, symbol name, declaration kind, source snippet, and dependency references.



Dependency graph storage uses proof\_graph.sqlite. Declaration records and their dependency lists (deps\_json) are stored in SQLite, built with streaming parsing via ijson to avoid loading huge JSON structures into RAM all at once. Storing the graph in SQLite lets you walk prerequisite and dependency edges from any starting declaration without holding the whole repository graph in memory.



Vector embedding and indexing use lean\_vector\_db. Each declaration's text or code is sent to a local Ollama instance running nomic-embed-text to produce dense embedding vectors. ChromaDB persists those float32 vectors alongside the Lean document text, metadata, and HNSW index structures on disk. Because every declaration gets an embedding vector, full Lean code, metadata, and HNSW index links across a large mathematical codebase, the directory grows to roughly 30 GB.



Technologies Used and What Each One Does



Python 3.11 and uv orchestrate file parsing, graph traversal, topological sorting, batching, checkpointing, and CLI execution.



ChromaDB (lean\_vector\_db) acts as a local persistent vector database that finds declarations semantically similar to a stage query.



Ollama with nomic-embed-text, plus optional generation models, generates query and document embeddings locally so semantic search runs offline against the exact same embedding space used when indexing.



SQLite (proof\_graph.sqlite) and ijson store declaration metadata, code, and dependency links (deps\_json) on disk with low memory overhead.



Python graphlib.TopologicalSorter orders the retrieved dependency subgraph so prerequisite lemmas and definitions appear before theorems that depend on them, with a fallback order if cycles occur.



Extracting Data for Different Queries (The 5-Stage Pass)



Rather than dumping an entire database at once, multi-stage extraction uses each stage query as a semantic entry point and expands outward through the dependency graph.



Query embedding embeds each stage's natural-language or keyword query using nomic-embed-text, covering setup and definitions, analytic continuation and functional equation, bounds and logarithmic derivative, zeros and explicit formula, or main theorem and consequences.



Seed lookup queries ChromaDB and returns the top-k (top\_k\_seeds, typically 6 or 8) closest declarations to that query.



Graph expansion and topological sort start from those seeds, walk proof\_graph.sqlite recursively up to max\_depth (4 to 6) along deps\_json, and order the nodes topologically.



Cross-stage deduplication (seen\_ids) skips any declaration ID already collected in an earlier stage so later stages only pull new unique nodes not already seen.



Filtering and output filter declarations to theorem and lemma (plus optional definitions if requested) and write them out either directly into a fast retrieval file like 5stages.txt with no LLM pass or into batches for summarization and translation.



Why the Extracted Lean Codes Are Relevant



Preserving exact formal assumptions and types keeps explicit binders, typeclasses, algebraic structures, and hypotheses intact that plain English summaries can easily blur or oversimplify.



Capturing supporting steps via graph dependencies ensures a headline theorem is not treated in isolation, since walking deps\_json pulls in the intermediate lemmas and helper facts that actually bridge definitions to conclusions.



