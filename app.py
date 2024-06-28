import streamlit as st
from product_scraper import estrai_informazioni_prodotto
from quote_generator import generate_quote_html
import base64
from datetime import datetime
import json
import os

# Imposta la modalità wide e il titolo della pagina
st.set_page_config(layout="wide", page_title="Generatore di Preventivi")

# Funzione per salvare i dati in un file JSON
def save_data(data, page_name, file_name):
    directory = f'saved_data/saved_data_{page_name}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'{file_name}.json')
    with open(file_path, 'w') as file:
        json.dump(data, file, default=str)
    st.success(f'Dati salvati in {file_path}')

# Funzione per caricare i dati da un file JSON
def load_data(page_name, file_name):
    file_path = f'saved_data/saved_data_{page_name}/{file_name}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        st.success(f'Dati caricati da {file_path}')
        return data
    else:
        st.error(f'File {file_path} non trovato.')
        return None

# Funzione per ottenere i nomi dei file di salvataggio
def get_saved_files(page_name):
    directory = f'saved_data/saved_data_{page_name}'
    if os.path.exists(directory):
        return [f.split('.')[0] for f in os.listdir(directory) if f.endswith('.json')]
    return []

# Inizializza lo stato della sessione se non già presente
if 'company_info' not in st.session_state:
    st.session_state['company_info'] = {
        'logo_url': 'https://static.wixstatic.com/media/63b1fb_5823409f408844189cd81edc2e3720df~mv2.png',
        'name': 'Gold Solar S.R.L.',
        'address': 'Via del Purgatorio 40, 80147, Napoli, Italia',
        'email': 'info@goldsolarweb.com',
        'pec': 'goldsolar@pec.it',
        'phone': '+39 348 789 4002',
        'vat': '10355251215'
    }

if 'quote_details' not in st.session_state:
    st.session_state['quote_details'] = {
        'number': '2255',
        'date': datetime.now().date(),
        'validity': datetime.now().date(),
        'shipping_cost': '20.00'
    }

if 'client_details' not in st.session_state:
    st.session_state['client_details'] = {
        'name': 'Mario Rossi',
        'address': 'Via Roma 1, 00100, Roma, Italia',
        'tax_code': 'RSSMRA80A01H501Z',
        'vat': '01234567890'
    }

if 'destination_details' not in st.session_state:
    st.session_state['destination_details'] = {
        'address': 'Via Milano 10, 20100, Milano, Italia',
        'contact': 'Mario Rossi',
        'phone': '+39 333 123 4567',
        'email': 'mario.rossi@example.com'
    }

if 'payment_details' not in st.session_state:
    st.session_state['payment_details'] = {
        'payment_mode': 'Bonifico Bancario',
        'iban': 'IT67P0538740070000003971383',
        'payment_terms': '30 giorni dalla data della fattura',
        'discounts': '2% di sconto per pagamento anticipato'
    }

if 'shipping_details' not in st.session_state:
    st.session_state['shipping_details'] = {
        'conditions': 'Spedizione standard entro 7-10 giorni lavorativi',
        'costs': 'Inclusi nel totale'
    }

if 'products' not in st.session_state:
    st.session_state['products'] = {}

if 'product_info_list' not in st.session_state:
    st.session_state['product_info_list'] = []

if 'iva' not in st.session_state:
    st.session_state['iva'] = 22.0

if 'notes_and_terms' not in st.session_state:
    st.session_state['notes_and_terms'] = {
        'note': '',
        'terms_and_conditions': ''
    }


def company_info_page():
    st.header("Informazioni Azienda")

    saved_files = get_saved_files('company_info')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Informazioni Azienda"):
        data = load_data('company_info', selected_file)
        if data:
            st.session_state['company_info'] = data

    with st.form(key='company_info_form'):
        company_info = {
            'logo_url': st.text_input("Logo URL", st.session_state['company_info']['logo_url']),
            'name': st.text_input("Nome Azienda", st.session_state['company_info']['name']),
            'address': st.text_input("Indirizzo Azienda", st.session_state['company_info']['address']),
            'email': st.text_input("Email Azienda", st.session_state['company_info']['email']),
            'pec': st.text_input("PEC Azienda", st.session_state['company_info']['pec']),
            'phone': st.text_input("Telefono Azienda", st.session_state['company_info']['phone']),
            'vat': st.text_input("P.IVA Azienda", st.session_state['company_info']['vat'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Informazioni Azienda", use_container_width=True):
            st.session_state['company_info'] = company_info
            save_data(company_info, 'company_info', file_name)


def quote_details_page():
    st.header("Dettagli Preventivo")

    saved_files = get_saved_files('quote_details')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Dettagli Preventivo"):
        data = load_data('quote_details', selected_file)
        if data:
            # Convert date strings to datetime.date objects
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
            data['validity'] = datetime.strptime(data['validity'], '%Y-%m-%d').date()
            st.session_state['quote_details'] = data

    with st.form(key='quote_details_form'):
        quote_details = {
            'number': st.text_input("Numero Preventivo", st.session_state['quote_details']['number']),
            'date': st.date_input("Data Preventivo", st.session_state['quote_details']['date']),
            'validity': st.date_input("Validità Preventivo", st.session_state['quote_details']['validity']),
            'shipping_cost': st.text_input("Costi di Spedizione", st.session_state['quote_details']['shipping_cost'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Dettagli Preventivo", use_container_width=True):
            st.session_state['quote_details'] = quote_details
            save_data(quote_details, 'quote_details', file_name)


def client_details_page():
    st.header("Dettagli Cliente")

    saved_files = get_saved_files('client_details')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Dettagli Cliente"):
        data = load_data('client_details', selected_file)
        if data:
            st.session_state['client_details'] = data

    with st.form(key='client_details_form'):
        client_details = {
            'name': st.text_input("Nome Cliente", st.session_state['client_details']['name']),
            'address': st.text_input("Indirizzo Cliente", st.session_state['client_details']['address']),
            'tax_code': st.text_input("Codice Fiscale Cliente", st.session_state['client_details']['tax_code']),
            'vat': st.text_input("P.IVA Cliente", st.session_state['client_details']['vat'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Dettagli Cliente", use_container_width=True):
            st.session_state['client_details'] = client_details
            save_data(client_details, 'client_details', file_name)


def destination_details_page():
    st.header("Dettagli Destinazione")

    saved_files = get_saved_files('destination_details')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Dettagli Destinazione"):
        data = load_data('destination_details', selected_file)
        if data:
            st.session_state['destination_details'] = data

    with st.form(key='destination_details_form'):
        destination_details = {
            'address': st.text_input("Indirizzo di Spedizione", st.session_state['destination_details']['address']),
            'contact': st.text_input("Contatto", st.session_state['destination_details']['contact']),
            'phone': st.text_input("Telefono", st.session_state['destination_details']['phone']),
            'email': st.text_input("Email", st.session_state['destination_details']['email'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Dettagli Destinazione", use_container_width=True):
            st.session_state['destination_details'] = destination_details
            save_data(destination_details, 'destination_details', file_name)


def payment_details_page():
    st.header("Informazioni di Pagamento")

    saved_files = get_saved_files('payment_details')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Informazioni di Pagamento"):
        data = load_data('payment_details', selected_file)
        if data:
            st.session_state['payment_details'] = data

    with st.form(key='payment_details_form'):
        payment_details = {
            'payment_mode': st.text_input("Modalità di Pagamento", st.session_state['payment_details']['payment_mode']),
            'iban': st.text_input("IBAN Azienda", st.session_state['payment_details']['iban']),
            'payment_terms': st.text_input("Termini di Pagamento", st.session_state['payment_details']['payment_terms']),
            'discounts': st.text_input("Sconti Disponibili", st.session_state['payment_details']['discounts'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Informazioni di Pagamento", use_container_width=True):
            st.session_state['payment_details'] = payment_details
            save_data(payment_details, 'payment_details', file_name)


def shipping_details_page():
    st.header("Informazioni di Spedizione")

    saved_files = get_saved_files('shipping_details')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Informazioni di Spedizione"):
        data = load_data('shipping_details', selected_file)
        if data:
            st.session_state['shipping_details'] = data

    with st.form(key='shipping_details_form'):
        shipping_details = {
            'conditions': st.text_input("Condizioni di Spedizione", st.session_state['shipping_details']['conditions']),
            'costs': st.text_input("Costi di Spedizione", st.session_state['shipping_details']['costs'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Informazioni di Spedizione", use_container_width=True):
            st.session_state['shipping_details'] = shipping_details
            save_data(shipping_details, 'shipping_details', file_name)


def notes_and_terms_page():
    st.header("Note e Termini e Condizioni")

    saved_files = get_saved_files('notes_and_terms')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Note e Termini e Condizioni"):
        data = load_data('notes_and_terms', selected_file)
        if data:
            st.session_state['notes_and_terms'] = data

    with st.form(key='notes_and_terms_form'):
        notes_and_terms = {
            'note': st.text_area("Note", st.session_state['notes_and_terms']['note']),
            'terms_and_conditions': st.text_area("Termini e Condizioni", st.session_state['notes_and_terms']['terms_and_conditions'])
        }
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Note e Termini e Condizioni", use_container_width=True):
            st.session_state['notes_and_terms'] = notes_and_terms
            save_data(notes_and_terms, 'notes_and_terms', file_name)


def products_page():
    st.header("Aggiungi Prodotti")
    num_products = st.number_input("Numero di Prodotti", min_value=1, step=1)

    for i in range(int(num_products)):
        st.subheader(f"Prodotto {i + 1}")

        with st.form(key=f'product_form_{i}'):
            url = st.text_input(f"URL Prodotto {i + 1} (opzionale)", key=f'url_{i}')
            if st.form_submit_button(f"Carica Prodotto {i + 1} da URL", use_container_width=True) and url:
                product_info = estrai_informazioni_prodotto(url)
                if product_info:
                    st.success(f"Prodotto {i + 1} Caricato!")
                    st.session_state[f'product_info_{i}'] = product_info
                else:
                    st.error(f"Errore nel caricamento del prodotto {i + 1}")

            saved_files = get_saved_files('products')
            selected_file = st.selectbox(f"Seleziona file di salvataggio per Prodotto {i + 1}", saved_files, key=f'select_{i}')
            if st.form_submit_button(f"Carica Prodotto {i + 1} da File", use_container_width=True):
                product_info = load_data('products', selected_file)
                if product_info:
                    st.success(f"Prodotto {i + 1} Caricato da File!")
                    st.session_state[f'product_info_{i}'] = product_info

            product_info = st.session_state.get(f'product_info_{i}', {})
            name = st.text_input(f"Nome del prodotto {i + 1}", product_info.get("name", ''), key=f'name_{i}')
            code = st.text_input(f"Codice del prodotto {i + 1}", product_info.get("code", ''), key=f'code_{i}')
            price = st.number_input(f"Prezzo del prodotto {i + 1}", value=product_info.get("unit_price", 0.0), key=f'price_{i}')
            image_url = st.text_input(f"URL dell'immagine principale {i + 1}", product_info.get("image", ''), key=f'image_{i}')
            quantity = st.number_input(f"Quantità Prodotto {i + 1}", min_value=1, step=1, value=product_info.get("quantity", 1), key=f'quantity_{i}')
            if st.form_submit_button(f"Salva Prodotto {i + 1}", use_container_width=True):
                product = {
                    'name': name,
                    'code': code,
                    'unit_price': price,
                    'quantity': quantity,
                    'image': image_url,
                    'total_price': price * quantity
                }
                st.session_state.products[i] = product
                st.success(f"Prodotto {i + 1} Salvato!")


def create_product_page():
    st.header("Crea Prodotto")

    with st.form(key='create_product_form'):
        url = st.text_input("URL Prodotto (opzionale)")
        if st.form_submit_button("Carica Prodotto da URL", use_container_width=True) and url:
            product_info = estrai_informazioni_prodotto(url)
            if product_info:
                st.success("Prodotto Caricato!")
                st.session_state['product_info'] = product_info
            else:
                st.error("Errore nel caricamento del prodotto")

        saved_files = get_saved_files('products')
        selected_file = st.selectbox("Seleziona file di salvataggio per Prodotto", saved_files, key='select')
        if st.form_submit_button("Carica Prodotto da File", use_container_width=True):
            product_info = load_data('products', selected_file)
            if product_info:
                st.success("Prodotto Caricato da File!")
                st.session_state['product_info'] = product_info

        product_info = st.session_state.get('product_info', {})
        name = st.text_input("Nome del prodotto", product_info.get("name", ''), key='name')
        code = st.text_input("Codice del prodotto", product_info.get("code", ''), key='code')
        price = st.number_input("Prezzo del prodotto", value=product_info.get("unit_price", 0.0), key='price')
        image_url = st.text_input("URL dell'immagine principale", product_info.get("image", ''), key='image')
        quantity = st.number_input("Quantità Prodotto", min_value=1, step=1, value=product_info.get("quantity", 1), key='quantity')
        file_name = st.text_input("Nome file di salvataggio", key='file_name')

        if st.form_submit_button("Salva Prodotto", use_container_width=True):
            product = {
                'name': name,
                'code': code,
                'unit_price': price,
                'quantity': quantity,
                'image': image_url,
                'total_price': price * quantity
            }
            save_data(product, 'products', file_name)
            st.success("Prodotto Salvato!")


def iva_details_page():
    st.header("Dettagli IVA")

    saved_files = get_saved_files('iva')
    selected_file = st.selectbox("Seleziona file di salvataggio", saved_files)
    if st.button("Carica Dettagli IVA"):
        data = load_data('iva', selected_file)
        if data:
            st.session_state['iva'] = data['iva']

    with st.form(key='iva_details_form'):
        iva = st.number_input("IVA (%)", min_value=0.0, max_value=100.0, step=0.01, value=st.session_state['iva'])
        file_name = st.text_input("Nome file di salvataggio")
        if st.form_submit_button("Salva Dettagli IVA", use_container_width=True):
            st.session_state['iva'] = iva
            save_data({'iva': iva}, 'iva', file_name)


def generate_quote_page():
    st.header("Generazione Documento")

    # Ottieni tutti i file template disponibili nella directory 'document_templates'
    template_directory = 'document_templates'
    if not os.path.exists(template_directory):
        os.makedirs(template_directory)
    templates = [f for f in os.listdir(template_directory) if f.endswith('.html')]

    selected_template = st.selectbox("Seleziona Template HTML", templates)
    template_path = os.path.join(template_directory, selected_template)

    with st.form(key='generate_quote_form'):
        output_path = st.text_input("Percorso Output HTML", 'quote.html')
        generate_button = st.form_submit_button("Genera Documento", use_container_width=True)

        if generate_button:
            company_info = st.session_state['company_info']
            quote_details = st.session_state['quote_details']
            client_details = st.session_state['client_details']
            destination_details = st.session_state['destination_details']
            payment_details = st.session_state['payment_details']
            shipping_details = st.session_state['shipping_details']
            products = st.session_state['products']
            iva = st.session_state['iva']
            notes_and_terms = st.session_state['notes_and_terms']

            generate_quote_html(template_path, output_path, company_info, quote_details, client_details,
                                destination_details, payment_details, shipping_details, products, iva, notes_and_terms)
            st.success(f"Documento generato con successo! Salvato in {output_path}")

            # Leggi il file HTML generato
            with open(output_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Codifica il file HTML in base64 per il download
            b64 = base64.b64encode(html_content.encode()).decode()

            st.session_state['download_ready'] = b64

            # Mostra l'anteprima del file senza il controllo di zoom
            st.markdown(f"""
                <div style="text-align: center;">
                    <iframe src="data:text/html;base64,{b64}" width="100%" height="600" style="border: none;"></iframe>
                </div>
            """, unsafe_allow_html=True)

    if 'download_ready' in st.session_state:
        st.markdown(
            f"""
            <a href="data:text/html;base64,{st.session_state['download_ready']}" download="documento.html" class="download-button">
                Scarica Documento
            </a>
            """,
            unsafe_allow_html=True
        )


def main():
    st.sidebar.title("Navigazione")
    page = st.sidebar.radio("Vai a",
                            ["Informazioni Azienda", "Dettagli Preventivo", "Dettagli Cliente", "Dettagli Destinazione",
                             "Informazioni di Pagamento", "Informazioni di Spedizione", "Crea Prodotto", "Aggiungi Prodotti",
                             "Dettagli IVA", "Note e Termini e Condizioni", "Generazione Documento"])

    if page == "Informazioni Azienda":
        company_info_page()
    elif page == "Dettagli Preventivo":
        quote_details_page()
    elif page == "Dettagli Cliente":
        client_details_page()
    elif page == "Dettagli Destinazione":
        destination_details_page()
    elif page == "Informazioni di Pagamento":
        payment_details_page()
    elif page == "Informazioni di Spedizione":
        shipping_details_page()
    elif page == "Note e Termini e Condizioni":
        notes_and_terms_page()
    elif page == "Aggiungi Prodotti":
        products_page()
    elif page == "Crea Prodotto":
        create_product_page()
    elif page == "Dettagli IVA":
        iva_details_page()
    elif page == "Generazione Documento":
        generate_quote_page()

    st.markdown("""
        <style>
        .stButton button {
            width: 100%;
            background-color: white;
            color: #006400;
            border: 2px solid #006400;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #006400;
            color: white;
            border: 2px solid #006400;
        }
        .download-button {
            width: 100%;
            background-color: white;
            color: #006400;
            border: 2px solid #006400;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            transition: background-color 0.3s ease, color 0.3s ease;
            text-align: center;
            display: block;
            text-decoration: none.
        }
        .download-button:hover {
            background-color: #006400;
            color: white.
            border: 2px solid #006400.
        }
        .download-button a {
            color: #006400.
            text-decoration: none.
        }
        .download-button a:hover {
            color: white.
            text-decoration: none.
        }
        .download-button a:link {
            color: #006400.
            text-decoration: none.
        }
        .download-button a:visited {
            color: #006400.
            text-decoration: none.
        }
        .download-button a:hover {
            color: white.
            text-decoration: none.
        }
        .download-button a:active {
            color: #006400.
            text-decoration: none.
        }
        </style>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
