text= """  """
keywords = ["Einleitung", "Tenor", "Begründung", "Rechtsbehelfsbelehrung", "Unterschrift mit Grußformel"]

def splitTextAndRemoveKeywort(text,keywords):
    
    # Function to split text based on keywords
    def split_text(text, keywords):
        parts = {}
        current_keyword = None
        for line in text.splitlines():
            for keyword in keywords:
                if keyword in line:
                    current_keyword = keyword
                    parts[current_keyword] = []
                    break
            if current_keyword:
                parts[current_keyword].append(line)
        return parts

    # Function to remove keywords from each part
    def remove_keywords(parts):
        for keyword, lines in parts.items():
            for i, line in enumerate(lines):
                lines[i] = line.replace(keyword + ":", "").strip()
        return parts



###----------------------------------Nur für Testen-------------------------------------------#######


# Remove keywords from each part
cleaned_parts = splitTextAndRemoveKeywort(text, keywords)

# Print each part without keywords
for keyword, lines in cleaned_parts.items():
    print(keyword + ":"+"\n"+"-----------------------------------------------------------------------------------")
    print("\n".join(lines))
    print()
