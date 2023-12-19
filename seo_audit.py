import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

class SEOAnalyzer:
    def __init__(self, url, keywords):
        self.url = url
        self.keywords = keywords
        self.text = self.get_html_text()
        self.soup = BeautifulSoup(self.text, 'html.parser')

    def get_html_text(self):
        response = requests.get(self.url)
        return response.text

    def get_word_occurrences(self, text):
        words = text.lower().split()
        word_occurrences = {}
        for word in words:
            word_occurrences[word] = word_occurrences.get(word, 0) + 1
        sorted_occurrences = sorted(word_occurrences.items(), key=lambda item: item[1], reverse=True)
        return sorted_occurrences

    def remove_parasite_words(self, word_occurrences, parasite_words):
        cleaned_word_occurrences = [item for item in word_occurrences if item[0] not in parasite_words]
        return cleaned_word_occurrences

    def get_parasite_words(self, file_path='parasite.csv'):
        with open(file_path, 'r') as file:
            parasite_words = file.read().split(',')
        return [word.strip() for word in parasite_words]

    def remove_html_tags(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()

    def get_tag_attribute_values(self, tag_name, attribute_name):
        values = [tag.get(attribute_name) for tag in self.soup.find_all(tag_name)]
        return values

    def get_alt_tags_details(self):
        alt_values = []
        all_img_tags = self.soup.find_all('img')
        for img in all_img_tags:
            alt = img.get('alt')
            link_url = img.parent.get('href') if img.parent.name == 'a' else 'N/A'
            alt_values.append({
                'alt_text': alt,
                'occurrences': sum(1 for t in alt_values if t == alt),
                'link_url': link_url
            })
        return alt_values

    def perform_seo_audit(self):
        text_without_html = self.remove_html_tags(self.text)
        occurrences = self.get_word_occurrences(text_without_html)
        parasite_list = self.get_parasite_words()
        cleaned_occurrences = self.remove_parasite_words(occurrences, parasite_list)
        all_links = self.get_tag_attribute_values('a', 'href')
        num_incoming_links, num_outgoing_links = len(all_links), len(all_links)
        alt_values = self.get_alt_tags_details()
        return cleaned_occurrences, all_links, num_incoming_links, num_outgoing_links, alt_values

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("SEO Analyzer")
        self.geometry("500x300")

        # Add a title label
        title_label = tk.Label(self, text="SEO Analyzer", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # URL Entry
        self.url_label = tk.Label(self, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)

        # Keywords Entry
        self.keywords_label = tk.Label(self, text="Enter Keywords (comma-separated):")
        self.keywords_label.pack()
        self.keywords_entry = tk.Entry(self, width=40)
        self.keywords_entry.pack(pady=5)

        # Analyze Button
        self.analyze_button = tk.Button(self, text="Analyze", command=self.analyze, bg="green", fg="white")
        self.analyze_button.pack(pady=10)

    def analyze(self):
        url = self.url_entry.get()
        keywords = self.keywords_entry.get().split(',')
        self.seo_analyzer = SEOAnalyzer(url, keywords)
        self.destroy()
        self.results_window = ResultsWindow(self.seo_analyzer)

class ResultsWindow(tk.Tk):
    def __init__(self, seo_analyzer):
        tk.Tk.__init__(self)
        self.title("SEO Results")
        self.geometry("800x600")
        self.seo_analyzer = seo_analyzer
        self.create_widgets()

    def create_widgets(self):
        cleaned_occurrences, all_links, num_incoming_links, num_outgoing_links, alt_values = self.seo_analyzer.perform_seo_audit()

        # Results Text
        self.results_text = tk.Text(self, wrap=tk.WORD)
        self.results_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Insert Results
        self.results_text.insert(tk.END, f"Number of incoming links: {num_incoming_links}\n", "big")
        self.results_text.insert(tk.END, f"Number of outgoing links: {num_outgoing_links}\n", "big")

        self.results_text.insert(tk.END, "\nAlt tags details:\n", "big")
        for alt in alt_values:
            self.results_text.insert(tk.END, f"{alt}\n")

        self.results_text.insert(tk.END, "\nKeywords occurrences:\n", "big")
        for word, count in cleaned_occurrences:
            self.results_text.insert(tk.END, f"{word}: {count}\n")

        # Save Button
        self.save_button = tk.Button(self, text="Save Report", command=self.save_report, bg="blue", fg="white")
        self.save_button.pack(pady=10)

        # Tag Configurations
        self.results_text.tag_configure("big", font=("Helvetica", 12, "bold"))

    def save_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(file_path, 'w') as file:
            file.write(self.results_text.get(1.0, tk.END))

if __name__ == "__main__":
    app = Application()
    app.mainloop()