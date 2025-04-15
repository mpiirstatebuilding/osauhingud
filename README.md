# Osaühingute Haldusrakendus

See on Flask-põhine veebirakendus osaühingute asutamiseks, otsimiseks ja vaatamiseks.

## Nõuded
- Python 3.9+
- Pip
- Virtuaalkeskkond (soovitatav)

## Paigaldamine

1. **Liikuge projekti kausta:**
```bash
cd osauhingud
```

2. **Looge virtuaalkeskkond ja aktiveerige see:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Installige vajalikud paketid:**
```bash
pip install -r requirements.txt
```

4. **Looge andmebaas ja lisage algandmed:**
```bash
python init_db.py
```

5. **Käivitage rakendus:**
```bash
flask run
```

Vaikimisi asub rakendus aadressil `http://localhost:5000`

## Kataloogistruktuur
```
project/
├── app.py
├── models.py
├── init_db.py
├── templates/
│   ├── avaleht.html
│   ├── asutamine.html
│   └── osauhing_vaade.html
├── static/
│   └── style.css
├── README.md
└── requirements.txt
```

## Funktsionaalsus
- Avaleht koos otsinguga (osaühingu ja osaniku nime/koodi järgi)
- Osaühingu detailvaade koos osanike andmetega
- Uue osaühingu lisamine
