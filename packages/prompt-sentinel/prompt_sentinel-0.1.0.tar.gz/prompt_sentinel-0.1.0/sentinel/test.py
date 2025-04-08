from sentinel import RegexSecretDetector

detector = RegexSecretDetector()
text = "Contact me at hello@example.com. My password is hunter2."
results = detector.detect(text)

for r in results:
    print(f"{r['type']} → {r['secret']} [{r['start']}–{r['end']}]")