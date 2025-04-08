import os

def load_cover_page(filtered_result):
    """
    Generate the cover page HTML using an f-string.

    :param filtered_result: Dictionary containing cover page data.
    :return: A string containing the dynamically generated cover page HTML.
    """
    try:
        # Extract values from the filtered result
        cover_page_values = filtered_result['final_sales_proposal']['cover_page']

        import tempfile
        import shutil
        from importlib.resources import files

        with files("subatomic_agents.static").joinpath("subatomic_footer.png").open("rb") as src:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                shutil.copyfileobj(src, tmp)
                image_path_str = tmp.name        
        # Generate the cover page HTML using f-strings
        cover_page_html = f"""
        <div class="cover-page">
            <h1 class="client-name">{cover_page_values['company_name']}</h1>
            <h2 class="project-title">{cover_page_values['title']}</h2>
            <h3 class="date">{cover_page_values['dated']}</h3>
            <p class="proposal-subtitle">{cover_page_values['proposal_purpose']}</p>
        </div>

        <!-- Footer Image -->
        <div class="footer-image">
            <img src="file://{image_path_str}" alt="Footer Cover Image">
        </div>

        <div class="page-break"></div> <!-- Page break -->
        """
        return cover_page_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the cover page: {e}")

def load_statement_of_work(filtered_result):
    """
    Generate the Statement of Work (SOW) HTML using an f-string.

    :param filtered_result: Dictionary containing SOW data.
    :return: A string containing the dynamically generated SOW HTML.
    """
    try:
        # Extract values from the filtered result
        sow_values = filtered_result['final_sales_proposal']['statement_of_work']

        # Check if 'service_provider_dba' exists and dynamically include it
        service_provider = (
            f"{sow_values['service_provider']} (DBA: {sow_values['service_provider_dba']})"
            if 'service_provider_dba' in sow_values and sow_values.get('service_provider_dba')
            else sow_values['service_provider']
        )

        # Generate the SOW HTML using f-strings
        sow_html = f"""
        <section class="section">
            <h2 class="section-title">Statement of Work ("SOW")</h2>
            <p>
                This <strong>Statement of Work (“SOW”)</strong>, dated {sow_values['dated']}, comprises an exhibit to the Master Services Agreement between 
                <strong>{service_provider}</strong> (the “Service Provider”) and <strong>{sow_values['customer']}</strong> (the “Customer”) signed on or around 
                {sow_values['msa_date']} (the “MSA”). This SOW is governed by the terms and conditions set out in the MSA.
            </p>
        </section>

        <div class="page-break"></div> <!-- Page break -->
        """
        return sow_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Statement of Work: {e}")

def load_background(filtered_result):
    """
    Generate the Background section HTML using an f-string.

    :param filtered_result: Dictionary containing background data.
    :return: A string containing the dynamically generated Background HTML.
    """
    try:
        # Extract values from the filtered result
        background_values = filtered_result['final_sales_proposal']['background']

        # Generate the Background HTML using f-strings
        background_html = f"""
        <section class="section">
            <h2 class="section-title">Background</h2>
            <p><strong>{background_values['problem_statement']}</strong></p>
            <p>
                {background_values['company_description']}
            </p>
            <p>
                {background_values['problem_details']}
            </p>
        </section> <div class="page-break"></div>
        """
        return background_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Background section: {e}")

def load_scope(filtered_result):
    """
    Generate the Scope section HTML using nested iterations for dynamic content.

    :param filtered_result: Dictionary containing scope data.
    :return: A string containing the dynamically generated Scope HTML.
    """
    try:
        # Extract values from the filtered result
        scope_values = filtered_result['final_sales_proposal']['scope']

        # Build the HTML content for the scope section
        scope_html = f"""
        <section class="section">
            <h2 class="section-title">Scope</h2>
            <p><strong>{scope_values['subtitle'] if scope_values.get('subtitle') else ''}</strong></p>
            <p>{scope_values['description'] if scope_values.get('description') else ''}</p>
            <p>Below, we describe how this solution will address the problem:</p>
            <ol>
        """

        # Iterate over 'solution_listing' for ordered list items
        for val in scope_values['solution_listing']:
            scope_html += f"""
                <li><strong>{val['title']}</strong>
                    <ul>
            """
            # Iterate over 'bullet_points' for nested list items
            for val2 in val['bullet_points']:
                scope_html += f"<li>{val2}</li>"
            scope_html += "</ul>"
            # Add the summary for the current solution
            scope_html += f"<p>{val['summary']}</p></li>"

        scope_html += "</ol>"

        # Iterate over 'sections' for additional sub-sections
        for val in scope_values['sections']:
            scope_html += f"""
                <h3>{val['title']}</h3>
                <p>{val['description'] if val.get('description') else ''}</p>
                <ul>
            """
            # Iterate over 'items' for nested list items
            if val.get('items'):
                for val2 in val['items']:
                    scope_html += f"<li>{val2}</li>"
                scope_html += "</ul>"

        scope_html += """</section> <div class="page-break"></div>"""

        return scope_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Scope section: {e}")

def load_project_assumptions(filtered_result):
    """
    Generate the Project Assumptions section HTML using dynamic content.

    :param filtered_result: Dictionary containing project assumptions data.
    :return: A string containing the dynamically generated Project Assumptions HTML.
    """
    try:
        # Extract values from the filtered result
        project_assumptions_values = filtered_result['final_sales_proposal']['project_assumptions']

        # Build the HTML content for the Project Assumptions section
        project_assumptions_html = f"""
        <section class="section">
            <h2 class="section-title">Project Assumptions</h2>
            <h3 class="headline">Headline</h3>
            <ol>
        """

        # Iterate over 'assumptions' to generate list items
        for val in project_assumptions_values['assumptions']:
            project_assumptions_html += f"<li>{val['description']}</li>"

        # Close the ordered list and section
        project_assumptions_html += """
            </ol>
        </section>
        <div class="page-break"></div> <!-- Page break -->
        """

        return project_assumptions_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Project Assumptions section: {e}")

def load_pricing(filtered_result):
    """
    Generate the Pricing section HTML using nested iterations for dynamic content.

    :param filtered_result: Dictionary containing pricing data.
    :return: A string containing the dynamically generated Pricing HTML.
    """
    try:
        # Extract values from the filtered result
        pricing_values = filtered_result['final_sales_proposal']['pricing']

        # Build the HTML content for the pricing section
        pricing_html = f"""
        <section class="section">
            <h2 class="section-title">Pricing</h2>
            <p>{pricing_values['pricing_description']}</p>
            <table class="pricing-table">
                <thead>
                    <tr>
        """

        # Iterate over 'pricing_table' for table headers
        for val in pricing_values['pricing_table']:
            pricing_html += f"<th>{val['category']}</th>"
        pricing_html += "</tr></thead><tbody>"

        # Iterate over 'pricing_table' for table rows
        for val in pricing_values['pricing_table']:
            pricing_html += f"""
                <tr>
                    <td><strong>Annual Fees:</strong> {val['annual_fees']}</td>
                    <td><strong>One-Time Fees:</strong> {val['one_time_fees']}</td>
                </tr>
            """
        pricing_html += "</tbody></table>"

        # Assumptions Subsection
        pricing_html += """
        <h3>Assumptions</h3>
        <ol>
        """
        for val in pricing_values['assumptions']:
            pricing_html += f"<li>{val['description']}</li>"
        pricing_html += "</ol>"

        # Terms of the SOW Subsection
        pricing_html += f"""
        <h3>Terms of the SOW</h3>
        <p>{pricing_values['terms_description']}</p>
        <ul>
        """

        # Iterate over 'payment_terms' for nested lists
        for val in pricing_values['payment_terms']:
            pricing_html += f"""
            <li><strong>{val['description']}</strong>
                <ul>
            """

            if(val.get('subitems')):
                for val2 in val['subitems']:
                    pricing_html += f"""
                        <li>
                            <strong>{val2['subtitle']}: </strong> {val2['description'] if val2['description'] else ''}
                    """
                    # Check if val2 contains further nested 'subitems'
                    if val2.get('subitems'):
                        pricing_html += "<ul>"
                        for val3 in val2['subitems']:
                            pricing_html += f"<li>{val3}</li>"
                        pricing_html += "</ul>"
                    pricing_html += "</li>"
                pricing_html += "</ul></li>"
        pricing_html += "</ul></section><div class='page-break'></div>"

        return pricing_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Pricing section: {e}")

def load_timeline(filtered_result):
    """
    Generate the Timeline section HTML using dynamic content.

    :param filtered_result: Dictionary containing timeline data.
    :return: A string containing the dynamically generated Timeline HTML.
    """
    try:
        # Extract values from the filtered result
        timeline_values = filtered_result['final_sales_proposal']['timeline']

        # Build the HTML content for the Timeline section
        timeline_html = f"""
        <section class="section">
            <h2 class="section-title">Timeline</h2>
            <h3 class="timeline-headline">Headline</h3>
            <p>{timeline_values['description']}</p>
            <table class="timeline-table">
                <thead>
                    <tr>
                        <th>Phase</th>
                        <th>Proposed Start Date</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Iterate over 'rows' to generate table rows
        for val in timeline_values['rows']:
            timeline_html += f"""
                <tr>
                    <td>{val['phase']}</td>
                    <td>{val['proposed_start_date']}</td>
                </tr>
            """

        # Close the table and section
        timeline_html += """
                </tbody>
            </table>
        </section>
        <div class="page-break"></div> <!-- Page break -->
        """

        return timeline_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Timeline section: {e}")

def load_signatures(filtered_result):
    """
    Generate the Signatures section HTML dynamically.

    :param filtered_result: Dictionary containing signature data.
    :return: A string containing the dynamically generated Signatures HTML.
    """
    try:
        # Extract values from the filtered result
        signature_values = filtered_result['final_sales_proposal']['signatures']

        # Build the HTML content for the Signatures section
        signatures_html = f"""
        <section class="section signatures">
            <h2 class="section-title">Signatures</h2>
            <p>
                IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.
            </p>
        
            <!-- Service Recipient -->
            <div class="signature-block">
                <h3>Service Recipient:</h3>
                <p><strong>By:</strong> {signature_values['service_recipient']['by']}</p>
                <p><strong>Company:</strong> {signature_values['service_recipient']['company']}</p>
                <p><strong>Title:</strong> {signature_values['service_recipient']['title']}</p>
                <p><strong>Date:</strong> [Insert date here]</p>
                <p><strong>Email:</strong> {signature_values['service_recipient']['email']}</p>
                <p><strong>Signature:</strong> ___________________________</p>
            </div>

            <!-- Separation -->
            <hr style="margin: 30px 0; border: 1px solid #ccc;">
        
            <!-- Service Provider -->
            <div class="signature-block">
                <h3>Service Provider:</h3>
                <p><strong>By:</strong> {signature_values['service_provider']['by']}</p>
                <p><strong>Name:</strong> {signature_values['service_provider']['company']}</p>
                <p><strong>Title:</strong> {signature_values['service_provider']['title']}</p>
                <p><strong>Date:</strong> [Insert date here]</p>
                <p><strong>Email:</strong> {signature_values['service_provider']['email']}</p>
                <p><strong>Signature:</strong> ___________________________</p>
            </div>
        </section>
        """

        return signatures_html
    except KeyError as e:
        raise KeyError(f"Missing required key in filtered_result: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while generating the Signatures section: {e}")

def load_html_css_string(html_content, css_path):
    """
    Load CSS from a file and inject it into an existing HTML string.

    :param html_content: The base HTML content (string).
    :param css_path: Path to the CSS file.
    :return: A complete HTML string with embedded CSS.
    """
    try:
        with open(css_path, "r", encoding="utf-8") as css_file:
            css_content = f"<style>{css_file.read()}</style>"

        # Inject the CSS into the <head> section of the HTML
        full_html = html_content.replace("</head>", f"{css_content}</head>")

        return full_html
    except FileNotFoundError:
        raise FileNotFoundError(f"CSS file not found at {css_path}")
    except Exception as e:
        raise Exception(f"An error occurred while loading the CSS file: {e}")

def generate_full_sales_proposal_with_css(filtered_result, css_path):
    """
    Generate the full sales proposal HTML document by integrating all dynamically generated sections,
    while dynamically injecting the CSS file.

    :param filtered_result: Dictionary containing sales proposal data.
    :param css_path: Path to the CSS file for styling.
    :return: A complete HTML string with embedded CSS.
    """
    try:
        # Generate individual sections
        cover_page_html = load_cover_page(filtered_result)
        sow_html = load_statement_of_work(filtered_result)
        background_html = load_background(filtered_result)
        scope_html = load_scope(filtered_result)
        project_assumptions_html = load_project_assumptions(filtered_result)
        pricing_html = load_pricing(filtered_result)
        timeline_html = load_timeline(filtered_result)
        signatures_html = load_signatures(filtered_result)

        # Combine all sections into a complete HTML document
        base_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sales Proposal</title>
        </head>
        <body>
            {cover_page_html}
            {sow_html}
            {background_html}
            {scope_html}
            {project_assumptions_html}
            {pricing_html}
            {timeline_html}
            {signatures_html}
        </body>
        </html>
        """

        # Inject the CSS into the HTML document
        full_html = load_html_css_string(base_html, css_path)

        return full_html
    except Exception as e:
        raise Exception(f"An error occurred while generating the full sales proposal: {e}")
