def inject_css(theme):
    # Define colors based on the theme
    if theme == "dark":
        card_background = "#2c2f33"
        ai_response_bg = "#23272a"
        ai_response_border = "#7289da"
        table_header_bg = "#7289da"
        table_row_even_bg = "#23272a"
        button_bg = "#7289da"
        button_hover_bg = "#99aab5"
        text_color = "#ffffff"
    else:
        # Light theme colors
        card_background = "#ffffff"
        ai_response_bg = "#f0f0f0"
        ai_response_border = "#007bff"
        table_header_bg = "#007bff"
        table_row_even_bg = "#f8f9fa"
        button_bg = "#007bff"
        button_hover_bg = "#0056b3"
        text_color = "#000000"

    st.markdown(
        f"""
        <style>
        /* General Card Styling */
        .card {{
            background-color: {card_background};
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
            color: {text_color};
        }}

        /* AI Response Styling */
        .ai-response {{
            background-color: {ai_response_bg};
            border-left: 6px solid {ai_response_border};
            padding: 15px;
            border-radius: 8px;
            font-size: 16px;
            line-height: 1.6;
            color: {text_color};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* Blueprint Table Styling */
        table.blueprint-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        table.blueprint-table th, table.blueprint-table td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
            color: {text_color};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        table.blueprint-table th {{
            background-color: {table_header_bg};
            color: #ffffff;
            font-weight: 600;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        table.blueprint-table tr:nth-child(even) {{
            background-color: {table_row_even_bg};
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        /* Copy Button Styling */
        .copy-button {{
            background-color: {ai_response_border};
            color: #ffffff;
            border: none;
            padding: 8px 12px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin-top: 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        .copy-button:hover {{
            background-color: {button_hover_bg if 'button_hover_bg' in locals() else '#0056b3'};
        }}

        /* Responsive Layout */
        @media (max-width: 768px) {{
            .card {{
                padding: 15px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
