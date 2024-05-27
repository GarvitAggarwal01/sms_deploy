mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableXsrfProtection=true\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
