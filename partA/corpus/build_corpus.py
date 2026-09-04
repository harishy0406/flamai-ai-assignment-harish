from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "partA" / "corpus" / "raw"
PROCESSED_DIR = ROOT / "partA" / "corpus" / "processed"
MANIFEST_PATH = PROCESSED_DIR / "manifest.json"
IDS_PATH = PROCESSED_DIR / "ids.txt"

DEFAULT_LANGUAGES = {
    "eng": "English",
    "hin": "Hindi",
    "kan": "Kannada",
    "tam": "Tamil",
}

SMOKE_CORPUS = {
    "eng": [
        "Bengaluru International Airport handled record traffic in March.",
        "The quarterly review meeting moved to Thursday.",
        "I bought this book yesterday from a small shop near MG Road.",
        "Children are playing cricket on the ground.",
        "The train arrived exactly on time.",
        "NASA and ISRO announced a joint mission update.",
        "Please keep the books in the cupboard.",
        "We are visiting Mysuru next week.",
        "Do you want tea or coffee?",
        "The GPU cluster ran out of memory during the night job.",
    ],
    "hin": [
        "बेंगलुरु अंतरराष्ट्रीय हवाई अड्डे ने मार्च में रिकॉर्ड यातायात संभाला।",
        "त्रैमासिक समीक्षा बैठक गुरुवार को स्थानांतरित हो गई।",
        "मैंने यह किताब कल एमजी रोड के पास एक छोटी दुकान से खरीदी।",
        "बच्चे मैदान में क्रिकेट खेल रहे हैं।",
        "ट्रेन ठीक समय पर पहुंची।",
        "नासा और इसरो ने संयुक्त मिशन अपडेट की घोषणा की।",
        "कृपया किताबों को अलमारी में रख दें।",
        "हम अगले सप्ताह मैसूर जा रहे हैं।",
        "क्या आप चाय या कॉफी चाहते हैं?",
        "रात के काम के दौरान जीपीयू क्लस्टर की मेमरी खत्म हो गई।",
    ],
    "kan": [
        "ಬೆಂಗಳೂರು ಅಂತರರಾಷ್ಟ್ರೀಯ ವಿಮಾನ ನಿಲ್ದಾಣವು ಮಾರ್ಚಿನಲ್ಲಿ ದಾಖಲೆಯ ಸಂಚಾರವನ್ನು ನಿರ್ವಹಿಸಿತು.",
        "ತ್ರೈಮಾಸಿಕ ಪರಿಶೀಲನಾ ಸಭೆಯನ್ನು ಗುರುವಾರಕ್ಕೆ ಮುಂದೂಡಲಾಯಿತು.",
        "ನಾನು ನಿನ್ನೆ ಎಂ.ಜಿ. ರಸ್ತೆಯ ಬಳಿಯ ಸಣ್ಣ ಅಂಗಡಿಯಿಂದ ಈ ಪುಸ್ತಕವನ್ನು ಖರೀದಿಸಿದೆ.",
        "ಮಕ್ಕಳು ಮೈದಾನದಲ್ಲಿ ಕ್ರಿಕೆಟ್ ಆಡುತ್ತಿದ್ದಾರೆ.",
        "ರೈಲು ಸರಿಯಾದ ಸಮಯಕ್ಕೆ ತಲುಪಿತು.",
        "ನಾಸಾ ಮತ್ತು ಇಸ್ರೋ ಸಂಯುಕ್ತ ಮಿಷನ್ ನವೀಕರಣವನ್ನು ಘೋಷಿಸಿದವು.",
        "ದಯವಿಟ್ಟು ಪುಸ್ತಕಗಳನ್ನು ಅಲಮಾರಿಯಲ್ಲಿ ಇಡಿ.",
        "ನಾವು ಮುಂದಿನ ವಾರ ಮೈಸೂರಿಗೆ ಭೇಟಿ ನೀಡುತ್ತಿದ್ದೇವೆ.",
        "ನಿಮಗೆ ಚಹಾ ಬೇಕೇ ಅಥವಾ ಕಾಫಿ ಬೇಕೇ?",
        "ರಾತ್ರಿ ಕೆಲಸದ ವೇಳೆ ಜಿಪಿಯು ಕ್ಲಸ್ಟರಿನ ಮೆಮರಿ ಮುಗಿದುಹೋಯಿತು.",
    ],
    "tam": [
        "பெங்களூரு சர்வதேச விமான நிலையம் மார்ச் மாதத்தில் சாதனை போக்குவரத்தை கையாள்ந்தது.",
        "காலாண்டு மதிப்பாய்வு கூட்டம் வியாழக்கிழமைக்கு மாற்றப்பட்டது.",
        "நான் நேற்று எம்.ஜி. சாலைக்கு அருகிலுள்ள சிறிய கடையில் இந்த புத்தகத்தை வாங்கினேன்.",
        "குழந்தைகள் மைதானத்தில் கிரிக்கெட் விளையாடுகிறார்கள்.",
        "ரயில் துல்லியமாக நேரத்திற்கு வந்தது.",
        "நாசா மற்றும் இஸ்ரோ இணைந்த மிஷன் புதுப்பிப்பை அறிவித்தன.",
        "தயவுசெய்து புத்தகங்களை அலமாரியில் வையுங்கள்.",
        "நாங்கள் அடுத்த வாரம் மைசூருக்கு செல்கிறோம்.",
        "உங்களுக்கு தேநீரா அல்லது காபியா வேண்டும்?",
        "இரவு பணியின் போது ஜிபியு கிளஸ்டரில் நினைவகம் தீர்ந்தது.",
    ],
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_smoke_corpus(sample_size: int) -> dict[str, Any]:
    entries = {}
    for code, name in DEFAULT_LANGUAGES.items():
        lines = SMOKE_CORPUS[code][:sample_size]
        text = "\n".join(lines) + "\n"
        path = PROCESSED_DIR / f"{code}.txt"
        path.write_text(text, encoding="utf-8", newline="\n")
        entries[code] = {
            "language": name,
            "records": len(lines),
            "sha256": sha256_text(text),
            "path": str(path.relative_to(ROOT)),
            "source": "manual comparable smoke corpus",
            "sample_size_requested": sample_size,
        }
    return {
        "status": "built",
        "reason": (
            "small sentence-aligned smoke corpus for reproducibility; rerun final "
            "metrics on a larger FLORES/FLORES+ sample when network access is available"
        ),
        "languages": entries,
        "seed": 42,
    }


def write_flores_corpus(sample_size: int, dataset_name: str) -> dict[str, Any]:
    from datasets import load_dataset

    try:
        datasets = {
            code: load_dataset(dataset_name, config, split="dev")
            for code, config in {
                "eng": "eng_Latn",
                "hin": "hin_Deva",
                "kan": "kan_Knda",
                "tam": "tam_Taml",
            }.items()
        }
    except Exception as error:
        raise RuntimeError(
            f"Cannot download {dataset_name}. Hugging Face returned an access or "
            "network error. Authenticate with `hf auth login` or use the bundled "
            "offline corpus with `python partA/analysis/corrected_fertility.py "
            "--mode reference`."
        ) from error
    common_ids = set(datasets["eng"]["id"])
    for dataset in datasets.values():
        common_ids &= set(dataset["id"])
    selected_ids = sorted(common_ids)[:sample_size]
    if len(selected_ids) < sample_size:
        raise ValueError(f"FLORES has only {len(selected_ids)} common IDs")

    entries = {}
    for code, dataset in datasets.items():
        sentences = {row["id"]: row["sentence"] for row in dataset}
        text = "\n".join(sentences[item].strip() for item in selected_ids) + "\n"
        path = PROCESSED_DIR / f"{code}.txt"
        path.write_text(text, encoding="utf-8", newline="\n")
        entries[code] = {
            "language": DEFAULT_LANGUAGES[code],
            "records": len(selected_ids),
            "sha256": sha256_text(text),
            "path": str(path.relative_to(ROOT)),
            "source": dataset_name,
            "config": {"eng": "eng_Latn", "hin": "hin_Deva", "kan": "kan_Knda", "tam": "tam_Taml"}[code],
        }
    IDS_PATH.write_text("\n".join(str(item) for item in selected_ids) + "\n", encoding="utf-8")
    return {
        "status": "built",
        "source": dataset_name,
        "split": "dev",
        "selected_ids": str(IDS_PATH.relative_to(ROOT)),
        "languages": entries,
        "seed": 42,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the multilingual evaluation corpus scaffold."
    )
    parser.add_argument("--sample-size", type=int, default=200)
    parser.add_argument("--source", choices=("smoke", "flores", "flores_plus"), default="smoke")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Alias for --source flores; requires datasets download access or a local cache.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    source = "flores" if args.download else args.source
    if source in {"flores", "flores_plus"}:
        dataset_name = "facebook/flores" if source == "flores" else "openlanguagedata/flores_plus"
        manifest = write_flores_corpus(args.sample_size, dataset_name)
    else:
        manifest = write_smoke_corpus(args.sample_size)
    manifest["reason"] = (
        "offline smoke corpus; use --source flores for aligned FLORES evidence"
        if source == "smoke"
        else "aligned FLORES dev split selected by common sentence IDs"
    )

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote corpus manifest to {MANIFEST_PATH}")
    print(f"Status: {manifest['status']}")


if __name__ == "__main__":
    main()
