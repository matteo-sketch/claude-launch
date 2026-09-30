# claude-launch

Pagina ponte per aprire Claude Code (app desktop per Mac) da un link https, per esempio da una proprietà URL di Notion, che non accetta i link `claude://`.

`https://matteo-sketch.github.io/claude-launch/#t=<titolo>&m=<modello>&e=<effort>&z=<prompt compresso>`

La pagina decomprime il prompt (deflate-raw + base64url) e apre `claude://code/new?q=<prompt>&folder=<cartella>`. Tutto sta dopo il `#`, quindi il prompt non arriva mai al server. Il prompt viene solo precompilato: lo invii tu. Il modello non si può impostare da link, quindi la pagina lo mostra e lo scegli nel menu.

I link si generano con `make_link.py`. Parametri opzionali: `f=<cartella>` (predefinita: ClauDB), `q=<prompt in chiaro>` al posto di `z`, `auto=0` per non aprire l'app in automatico.
