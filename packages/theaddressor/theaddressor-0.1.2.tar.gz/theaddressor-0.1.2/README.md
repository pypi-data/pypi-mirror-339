# 📬 TheAddressor

Turn messy strings into structured addresses.  
Supports U.S. and Canadian formats with fuzzy parsing, reference extraction, and more.

---

## 🚀 Features

- Parses unstructured address lines into clean components
- Supports:
  - Street addresses
  - Suite/unit numbers
  - U.S. and Canadian cities, states/provinces, ZIP/postal codes
  - Emails, phone numbers, URLs, and reference tags
- Handles noisy, shuffled, or incomplete input
- Easy to plug into shipping, billing, or CRM pipelines

---

## 🛠️ Installation

```bash
pip install theaddressor
```

---

## 🧠 Example

```python
from theaddressor import AddressParser

lines = [
    "DeepMind HQ",
    "48 Innovation Way",
    "Suite B",
    "London ON N6A 3K7",
    "contact@deep.ai",
    "(519) 555-0188"
]

parsed = AddressParser(lines).get()

print(parsed['address1'])  # '48 Innovation Way'
print(parsed['zipcode'])   # 'N6A3K7'
print(parsed['country'])   # 'Canada'
print(parsed['email'][0])  # 'contact@deep.ai'
```

---

## 🧪 Testing

Run unit tests with:

```bash
make test
```

Or manually:

```bash
python3 -m unittest discover tests
```

---

## 📦 Packaging

To build and upload to PyPI:

```bash
make build check upload
```

---

## 📄 License

BSD 3-Clause License © 2025 – Charles Watkins
