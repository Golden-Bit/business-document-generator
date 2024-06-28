# quote_generator.py

def generate_quote_html(template_path, output_path, company_info, quote_details, client_details, destination_details, payment_details, shipping_details, products, iva, notes_and_terms):
    with open(template_path, 'r', encoding='utf-8') as file:
        html_template = file.read()

    product_row_template = """
<tr>
    <td><img src="{product_image}" alt="Prodotto"></td>
    <td>{product_name}</td>
    <td>{product_code}</td>
    <td>{product_quantity}</td>
    <td>{product_unit_price:.2f} €</td>
    <td>{product_total_price:.2f} €</td>
</tr>
"""

    product_rows = ""
    total_before_tax = 0.0
    for product in products.values():
        product_info = product
        quantity = product.get('quantity')
        unit_price = product_info.get('Prezzo del prodotto', product.get('unit_price'))
        total_price = quantity * unit_price
        total_before_tax += total_price

        product_rows += product_row_template.format(
            product_image=product_info.get('URL dell\'immagine principale', product.get('image')),
            product_name=product_info.get('Nome del prodotto', product.get('name')),
            product_code=product_info.get('Codice del prodotto', product.get('code')),
            product_quantity=quantity,
            product_unit_price=unit_price,
            product_total_price=total_price
        )

    # tax = (total_before_tax + float(quote_details['shipping_cost'])) * (iva / 100)
    tax = total_before_tax * (iva / 100) + float(quote_details['shipping_cost']) * 0.22
    total_cost = total_before_tax + float(quote_details['shipping_cost']) + tax

    # Funzione per rimuovere paragrafi vuoti
    def remove_empty_paragraphs(text, **kwargs):
        for key, value in kwargs.items():
            if not value:
                text = text.replace(f'<p><strong>{key.capitalize()}:</strong> {{{{{key}}}}}</p>', '')
        return text

    html_output = html_template.format(
        logo_url=company_info['logo_url'],
        company_name=company_info['name'],
        company_address=company_info['address'],
        company_email=company_info['email'],
        company_pec=company_info['pec'],
        company_phone=company_info['phone'],
        company_vat=company_info['vat'],
        quote_number=quote_details['number'],
        quote_date=quote_details['date'],
        quote_validity=quote_details['validity'],
        client_name=client_details['name'],
        client_address=client_details['address'],
        client_tax_code=client_details['tax_code'],
        client_vat=client_details['vat'],
        destination_address=destination_details['address'],
        destination_contact=destination_details['contact'],
        destination_phone=destination_details['phone'],
        destination_email=destination_details['email'],
        iban=payment_details['iban'],
        payment_terms=payment_details['payment_terms'],
        discounts=payment_details['discounts'],
        payment_mode=payment_details['payment_mode'],
        shipping_conditions=shipping_details['conditions'],
        shipping_costs=shipping_details['costs'],
        product_rows=product_rows,
        total_before_tax=f"{total_before_tax:.2f}",
        shipping_cost=quote_details['shipping_cost'],
        tax=f"{tax:.2f}",
        total_cost=f"{total_cost:.2f}",
        iva=iva,
        note=notes_and_terms['note'],
        terms_and_conditions=notes_and_terms['terms_and_conditions']
    )

    # Rimuovi paragrafi vuoti
    html_output = remove_empty_paragraphs(
        html_output,
        company_name=company_info['name'],
        company_address=company_info['address'],
        company_email=company_info['email'],
        company_pec=company_info['pec'],
        company_phone=company_info['phone'],
        company_vat=company_info['vat'],
        quote_number=quote_details['number'],
        quote_date=quote_details['date'],
        quote_validity=quote_details['validity'],
        client_name=client_details['name'],
        client_address=client_details['address'],
        client_tax_code=client_details['tax_code'],
        client_vat=client_details['vat'],
        destination_address=destination_details['address'],
        destination_contact=destination_details['contact'],
        destination_phone=destination_details['phone'],
        destination_email=destination_details['email'],
        iban=payment_details['iban'],
        payment_terms=payment_details['payment_terms'],
        discounts=payment_details['discounts'],
        payment_mode=payment_details['payment_mode'],
        shipping_conditions=shipping_details['conditions'],
        shipping_costs=shipping_details['costs'],
        note=notes_and_terms['note'],
        terms_and_conditions=notes_and_terms['terms_and_conditions']
    )

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_output)
