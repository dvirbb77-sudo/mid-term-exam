#!/usr/bin/env bash
####################################################
# version: 1.0
# created by: Bibi
# purpose: Setup nginx for the mid-term exam project
# date: 2026-05-11
####################################################
set -euo pipefail

readonly CONF_PATH="/etc/nginx/sites-available/status-dashboard"
readonly ENABLED_PATH="/etc/nginx/sites-enabled/status-dashboard"
readonly DEFAULT_SITE="/etc/nginx/sites-enabled/default"

deploy_nginx_config() {
    echo "Creating Nginx configuration..."
    
    # Using sudo with tee to handle permissions within the script
    sudo tee "$CONF_PATH" > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
}

main() {
    # 1. Remove default site if it exists
    if [[ -L "$DEFAULT_SITE" || -f "$DEFAULT_SITE" ]]; then
        echo "Disabling default Nginx site..."
        sudo rm -f "$DEFAULT_SITE"
    fi

    # 2. Deploy configuration
    deploy_nginx_config

    # 3. Enable site via symlink
    echo "Enabling status-dashboard site..."
    sudo ln -sf "$CONF_PATH" "$ENABLED_PATH"

    # 4. Validate and Restart
    echo "Validating Nginx syntax..."
    if sudo nginx -t; then
        echo "Validation successful. Reloading Nginx..."
        sudo systemctl enable nginx
        sudo systemctl restart nginx
    else
        echo "Error: Nginx configuration is invalid." >&2
        return 1
    fi
}

main "$@"
