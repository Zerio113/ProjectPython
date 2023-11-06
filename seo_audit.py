import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Fonction pour obtenir les occurrences des mots dans un texte
def get_word_occurrences(text):
    words = text.lower().split()
    word_occurrences = {}
    for word in words:
        word_occurrences[word] = word_occurrences.get(word, 0) + 1
    sorted_occurrences = sorted(word_occurrences.items(), key=lambda item: item[1], reverse=True)
    return sorted_occurrences

# Fonction pour supprimer les mots parasites
def remove_parasite_words(word_occurrences, parasite_words):
    cleaned_word_occurrences = [item for item in word_occurrences if item[0] not in parasite_words]
    return cleaned_word_occurrences

# Fonction pour récupérer les mots parasites à partir du fichier CSV
def get_parasite_words(file_path='parasite.csv'):
    with open(file_path, 'r') as file:
        parasite_words = file.read().split(',')
    return [word.strip() for word in parasite_words]

# Fonction pour effectuer l'audit SEO complet
def perform_seo_audit(text, url):
    # Utiliser la fonction pour enlever les balises HTML
    text_without_html = remove_html_tags(text)

    # Récupération des mots clés importants
    occurrences = get_word_occurrences(text_without_html)
    parasite_list = get_parasite_words()
    cleaned_occurrences = remove_parasite_words(occurrences, parasite_list)

    # Extraction des liens entrants et sortants ainsi que des balises alt
    soup = BeautifulSoup(text, 'html.parser')
    all_links = get_tag_attribute_values(text, 'a', 'href')
    num_incoming_links, num_outgoing_links = len(all_links), len(all_links)
    alt_values = get_alt_tags_details(soup)
    SHOW_MORE_BUTTON_TEXT = "Afficher Plus"
    DOWNLOAD_CSV_BUTTON_TEXT = "Télécharger CSV"
    # Génération du rapport d'audit au format HTML
    report = f'''
    <html>
    <head>
        <title>Rapport d'Audit SEO</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                padding: 20px;
                background-color: #f2f2f2;
            }}
            h1, h2, p, ul, li, table {{
                margin: 0;
                padding: 0;
            }}
            h1 {{
                font-size: 36px;
                text-align: center;
                margin-bottom: 20px;
                color: #333;
            }}
            h2 {{
                font-size: 24px;
                margin-top: 40px;
                margin-bottom: 10px;
                color: #333;
            }}
            p, li {{
                font-size: 16px;
                color: #555;
            }}
            ul {{
                margin-top: 10px;
                list-style-type: none;
            }}
            table {{
                width: 80%;
                border-collapse: collapse;
                margin: 20px auto;
                background-color: #fff;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            img {{
                display: block;
                margin: 20px auto;
                max-width: 150px;
                height: auto;
            }}
            .content-table {{
                display: table;
            }}
            .visible-table {{
                display: table;
            }}
            .hidden-row {{
                display: none;
            }}
            .toggle-button {{
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: block;
                margin: 20px 10px;
                cursor: pointer;
            }}
        </style>
        <script>
            var showMoreButtonText = "{SHOW_MORE_BUTTON_TEXT}";
            var downloadCSVButtonText = "{DOWNLOAD_CSV_BUTTON_TEXT}";
            function toggleTable(tableId) {{
                var table = document.getElementById(tableId);
                var toggleButton = table.previousElementSibling;
                var rows = table.getElementsByTagName('tr');
                for (var i = 10; i < rows.length; i++) {{
                    if (rows[i].classList.contains('hidden-row')) {{
                        rows[i].classList.remove('hidden-row');
                    }} else {{
                        rows[i].classList.add('hidden-row');
                    }}
                }}
                if (table.classList.contains('content-table')) {{
                    table.classList.remove('content-table');
                    table.classList.add('visible-table');
                    toggleButton.innerText = 'Afficher Moins';
                }} else {{
                    table.classList.remove('visible-table');
                    table.classList.add('content-table');
                    toggleButton.innerText = 'Afficher Plus';
                }}
            }}
            function sortTable(tableId, col, asc) {{
                var table, rows, switching, i, x, y, shouldSwitch;
                table = document.getElementById(tableId);
                switching = true;
                while (switching) {{
                    switching = false;
                    rows = table.rows;
                    for (i = 1; i < (rows.length - 1); i++) {{
                        shouldSwitch = false;
                        x = rows[i].getElementsByTagName("td")[col];
                        y = rows[i + 1].getElementsByTagName("td")[col];
                        if (asc) {{
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }} else {{
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }}
                    }}
                    if (shouldSwitch) {{
                        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                        switching = true;
                    }}
                }}
            }}
            function downloadTableAsCSV(tableId, filename) {{
                var csv = [];
                var rows = document.querySelectorAll("#" + tableId + " tr");
                for (var i = 0; i < rows.length; i++) {{
                    var row = [], cols = rows[i].querySelectorAll("td, th");
                    for (var j = 0; j < cols.length; j++)
                        row.push(cols[j].innerText);
                    csv.push(row.join(","));
                }}
                // Download CSV file
                downloadCSV(csv.join("\\n"), filename);
            }}

            function downloadCSV(csv, filename) {{
                var csvFile;
                var downloadLink;

                // CSV file
                csvFile = new Blob([csv], {{type: "text/csv"}});

                // Download link
                downloadLink = document.createElement("a");

                // File name
                downloadLink.download = filename;

                // Create a link to the file
                downloadLink.href = window.URL.createObjectURL(csvFile);

                // Hide download link
                downloadLink.style.display = "none";

                // Add the link to DOM
                document.body.appendChild(downloadLink);

                // Click download link
                downloadLink.click();
            }}
        </script>
    </head>
    <body>
        <h1>Rapport d'Audit SEO</h1>
        <img src="https://www.esiee-it.fr/themes/custom/generic/medias/logo-esiee-it.png" alt="ESIEE-IT Logo">
        <p>Date d'audit : {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</p>
        <h2>URL analysée :</h2>
        <p>{url}</p>
        <h2>Mots clés importants :</h2>
        <button class="toggle-button" onclick="toggleTable('keywords-table')">Afficher Plus</button>
        <button class="toggle-button" onclick="downloadTableAsCSV('keywords-table', 'keywords.csv')">Télécharger CSV</button>
        <table id="keywords-table" class="content-table">
            <tr>
                <th>Mot clé</th>
                <th>Occurrences</th>
            </tr>
            {''.join(f"<tr><td>{keyword}</td><td>{occurrence}</td></tr>" for keyword, occurrence in cleaned_occurrences[:10])}
            {''.join(f"<tr class='hidden-row'><td>{keyword}</td><td>{occurrence}</td></tr>" for keyword, occurrence in cleaned_occurrences[10:])}
        </table>
        <h2>Liens entrants :</h2>
        <button class="toggle-button" onclick="toggleTable('incoming-links-table')">Afficher Plus</button>
        <button class="toggle-button" onclick="downloadTableAsCSV('incoming-links-table', 'incoming_links.csv')">Télécharger CSV</button>
        <table id="incoming-links-table" class="content-table">
            <tr>
                <th>URL</th>
                <th>Occurrences</th>
            </tr>
            {''.join(f"<tr><td>{link}</td><td>{all_links.count(link)}</td></tr>" for link in all_links[:10])}
            {''.join(f"<tr class='hidden-row'><td>{link}</td><td>{all_links.count(link)}</td></tr>" for link in all_links[10:])}
        </table>
        <h2>Liens sortants :</h2>
        <button class="toggle-button" onclick="toggleTable('outgoing-links-table')">Afficher Plus</button>
        <button class="toggle-button" onclick="downloadTableAsCSV('outgoing-links-table', 'outgoing_links.csv')">Télécharger CSV</button>
        <table id="outgoing-links-table" class="content-table">
            <tr>
                <th>URL</th>
                <th>Occurrences</th>
            </tr>
            {''.join(f"<tr><td>{link}</td><td>{all_links.count(link)}</td></tr>" for link in all_links[:10])}
            {''.join(f"<tr class='hidden-row'><td>{link}</td><td>{all_links.count(link)}</td></tr>" for link in all_links[10:])}
        </table>
        <h2>Balises alt :</h2>
        <button class="toggle-button" onclick="toggleTable('alt-table')">Afficher Plus</button>
        <button class="toggle-button" onclick="downloadTableAsCSV('alt-table', 'alt_tags.csv')">Télécharger CSV</button>
        <table id="alt-table" class="content-table">
            <tr>
                <th>Balise Alt</th>
                <th>Nombre d'Occurrences</th>
                <th>URL Liée</th>
            </tr>
            {''.join(f"<tr><td>{alt['alt_text']}</td><td>{alt['occurrences']}</td><td>{alt['link_url']}</td></tr>" for alt in alt_values)}
        </table>
    </body>
    </html>
    '''

    with open('audit_report.html', 'w', encoding='utf-8') as file:
        file.write(report)

# Fonction pour supprimer les balises HTML d'un texte
def remove_html_tags(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

# Fonction pour obtenir les valeurs des attributs d'une balise
def get_tag_attribute_values(html_text, tag_name, attribute_name):
    soup = BeautifulSoup(html_text, 'html.parser')
    values = [tag.get(attribute_name) for tag in soup.find_all(tag_name)]
    return values

# Fonction pour extraire les détails des balises alt
def get_alt_tags_details(soup):
    alt_values = []
    all_img_tags = soup.find_all('img')
    for img in all_img_tags:
        alt = img.get('alt')
        link_url = img.parent.get('href') if img.parent.name == 'a' else 'N/A'
        alt_values.append({
            'alt_text': alt,
            'occurrences': sum(1 for t in alt_values if t == alt),
            'link_url': link_url
        })
    return alt_values

# Programme principal pour l'audit de la première page
def main():
    url = input("Veuillez saisir l'URL de la page à analyser : ")
    response = requests.get(url)
    html_text = response.text
    perform_seo_audit(html_text, url)
    print("Le rapport d'audit a été généré avec succès.")

if __name__ == "__main__":
    main()
